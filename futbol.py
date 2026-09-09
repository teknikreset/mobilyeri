# -*- coding: utf-8 -*-
# Canlı Türkiye ligi takibi (GS - BJK - FB - TS).
# Kaynak: livescore.com halka açık API (anahtar gerektirmez, güncel skor).
#   - gunluk liste : /v1/api/app/date/soccer/{yyyymmdd}/0  -> mac + durum (NS/HT/FT/dakika), skor, devre skoru
#   - mac olaylari : /v1/api/app/incidents/soccer/{eid}    -> gol (IT 36/37/39/40) + anlik skor, asist, kartlar (43 sari, 44/45 kirmizi)
import json
import re
import ssl
import threading
import datetime
import urllib.request

TRACK = {"galatasaray", "fenerbahce", "besiktas", "trabzonspor"}
POLL_SEC = 30

DATE_API = "https://prod-public-api.livescore.com/v1/api/app/date/soccer/%s/0"
INC_API = "https://prod-public-api.livescore.com/v1/api/app/incidents/soccer/%s"

TR_COMP = {"Süper Lig", "S\u00c3\u00bcper Lig"}
GOAL_IT = {36, 37, 39, 40}
RED_IT = {44, 45}
# durumlar (Esid): 1=baslamadi(NS), 3=devam(Y'n'), 6=bitti(FT)


def _norm(s):
    TR = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return "".join(ch for ch in (s or "").translate(TR).lower() if ch.isalnum())


def _decode(raw):
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="replace")


def _get(url, timeout=20):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                 "Accept": "application/json"})
    raw = urllib.request.urlopen(req, timeout=timeout, context=ctx).read()
    return json.loads(_decode(raw))


def minute_of(eps):
    s = (eps or "").replace("'", "").strip().lower()
    if s in ("ns", "", "ht"):
        return 0 if s != "ht" else 45
    if s == "ft":
        return 90
    if s == "pen":
        return 120
    m = re.match(r"(\d+)(?:\+(\d+))?", s)
    if not m:
        return 0
    base = int(m.group(1))
    return base + int(m.group(2) or 0)


def fetch_real_date():
    try:
        data = _get(DATE_API % "20000101")
        ts = data.get("Ts")
        if ts:
            return datetime.datetime.utcfromtimestamp(ts).date()
    except Exception:
        pass
    return None


def fetch_date(date=None):
    date = date or datetime.date.today().strftime("%Y%m%d")
    try:
        data = _get(DATE_API % date)
    except Exception:
        return None
    out = []
    comp_hits = 0
    for st in data.get("Stages") or []:
        compn = st.get("CompN") or st.get("Cnm") or ""
        is_tr = str(st.get("CompId")) == "32" or compn in TR_COMP
        for ev in st.get("Events") or []:
            t1 = ((ev.get("T1") or [{}])[0].get("Nm") or "")
            t2 = ((ev.get("T2") or [{}])[0].get("Nm") or "")
            if is_tr or _norm(t1) in TRACK or _norm(t2) in TRACK:
                comp_hits += is_tr or 0
                out.append({
                    "eid": ev.get("Eid"),
                    "home": t1,
                    "away": t2,
                    "eps": ev.get("Eps"),
                    "esid": ev.get("Esid"),
                    "esd": ev.get("Esd"),
                    "sc": [ev.get("Tr1"), ev.get("Tr2")],
                    "ht": [ev.get("Trh1"), ev.get("Trh2")],
                    "is_tr": bool(is_tr),
                })
    return out


def _from_ts(ts):
    s = str(ts or "")
    if len(s) < 10:
        return None
    try:
        return datetime.datetime.strptime(s[:12], "%Y%m%d%H%M")
    except ValueError:
        return None


class FutbolTakip:
    def __init__(self, say_cb, poll=POLL_SEC):
        self.say_cb = say_cb
        self.poll = poll
        self.stop = threading.Event()
        self.tracked = {}

    def start(self):
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()

    def _say(self, msg):
        if not self.say_cb:
            return
        try:
            self.say_cb(msg)
        except Exception as e:
            print("futbol say hatasi:", e, flush=True)

    def _loop(self):
        while not self.stop.is_set():
            try:
                self._poll()
            except Exception as e:
                print("futbol sorgu hatasi:", type(e).__name__, e, flush=True)
            self.stop.wait(self.poll)

    def _team_of(self, rec, n):
        return rec["home"] if str(n) == "1" else rec["away"]

    def _poll(self):
        fxt = fetch_date()
        if fxt is None:
            return
        fxt = fxt or []
        now = datetime.datetime.now()
        for f in fxt:
            if not f.get("eid"):
                continue
            eid = str(f["eid"])
            rec = self.tracked.get(eid)
            if rec is None:
                rec = {"home": f["home"], "away": f["away"], "esd": f.get("esd"),
                       "started": False, "halftime": False, "resumed": False,
                       "done": False, "announced": set(), "lastsc": list(f.get("sc") or [])}
                self.tracked[eid] = rec
            self._date_step(rec, f)
        fxt_ids = {str(f["eid"]) for f in fxt}
        for eid, rec in list(self.tracked.items()):
            if rec["done"] or not rec["started"]:
                continue
            if eid in fxt_ids:
                continue
            dt = _from_ts(rec.get("esd"))
            if dt and now - dt > datetime.timedelta(hours=3):
                rec["done"] = True
                lsc = rec.get("lastsc") or ["?", "?"]
                self._say("🏁 Maç bitti! %s %s-%s %s" % (rec["home"], lsc[0], lsc[1], rec["away"]))
        # baslamasi gereken ama gunluk listeden dusen maclar: yine de olaylari izle
        now_ts = now.strftime("%Y%m%d%H%M")
        for eid, rec in list(self.tracked.items()):
            if rec["done"] or rec["started"]:
                continue
            if rec.get("esd") and str(rec["esd"]) <= now_ts:
                self._incident_step(rec, eid)

    def _date_step(self, rec, f):
        eid = str(f["eid"])
        eps = (f.get("eps") or "").strip() or "NS"
        esid = f.get("esid")
        hn, an = rec["home"], rec["away"]
        sc = f.get("sc") or ["?", "?"]
        live = esid == 3 or (
            esid is None and eps not in ("NS", "FT", "HT", "CAN", "ABD", ""))
        if live and not rec["started"]:
            rec["started"] = True
            self._say("⚽ Canlı maç takibi başladı: %s - %s (dakika %s, skor %s-%s)" %
                      (hn, an, eps, sc[0], sc[1]))
        if live:
            last = rec.get("lastsc") or ["?", "?"]
            if last[0] not in ("?", None) and sc[0] not in ("?", None):
                if int(last[0]) < int(sc[0]) or int(last[1]) < int(sc[1]):
                    kim = hn if int(sc[0]) > int(last[0]) else an
                    self._say("⚽ GOOL! %s (%s) skoru değiştirdi! Skor: %s-%s (%s')" %
                              (kim, eps, sc[0], sc[1], eps))
            rec["lastsc"] = list(sc)
        if eps == "HT" and not rec["halftime"]:
            rec["halftime"] = True
            self._say("⏸ İlk yarı bitti! %s %s-%s %s (devre arası)" % (hn, sc[0], sc[1], an))
        elif rec["halftime"] and not rec["resumed"] and live:
            rec["resumed"] = True
            self._say("▶ İkinci yarı başladı! %s %s-%s %s (kaldığı yerden devam)" % (hn, sc[0], sc[1], an))
        if esid == 6 or eps == "FT":
            if not rec["done"]:
                rec["done"] = True
                self._say("🏁 Maç bitti! %s %s-%s %s" % (hn, sc[0], sc[1], an))

    def _incident_step(self, rec, eid):
        try:
            data = _get(INC_API % eid)
        except Exception:
            return
        if not isinstance(data, dict):
            return
        incs = data.get("Incs") or {}
        for groups in incs.values():
            for g in groups:
                sub = g.get("Incs") or [g]
                for inc in sub:
                    it = inc.get("IT")
                    pn = inc.get("Pn")
                    if not pn or pn == "?":
                        continue
                    mn = inc.get("Min")
                    tm = self._team_of(rec, inc.get("Nm"))
                    if it in GOAL_IT:
                        key = ("g", mn, pn)
                        if key not in rec["announced"]:
                            rec["announced"].add(key)
                            sc = inc.get("Sc") or rec.get("lastsc") or ["?", "?"]
                            tag = " (penaltı)" if it == 37 else ""
                            self._say("⚽ GOOL! %s (%s) %s'. dakikada attı%s! Skor: %s-%s" %
                                      (pn, tm, mn, tag, sc[0], sc[1]))
                    elif it in RED_IT:
                        key = ("c", mn, pn)
                        if key not in rec["announced"]:
                            rec["announced"].add(key)
                            self._say("🟥 Kırmızı kart! %s (%s) - %s'. dakika" % (pn, tm, mn))

    def _poll_now(self):
        self._poll()


if __name__ == "__main__":
    def print_say(m):
        print("[LIVE]", m, flush=True)
    t = FutbolTakip(print_say, poll=10)
    t._poll_now()
    while not t.stop.is_set():
        t.stop.wait(10)
        try:
            t._poll_now()
        except Exception as e:
            print("hata:", e, flush=True)