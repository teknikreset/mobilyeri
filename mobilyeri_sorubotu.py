# -*- coding: utf-8 -*-
import socket, ssl, struct, base64, os, time, json, re, sys, random, queue
import http.client
import urllib.request, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sorular import normal_pool, erotik_pool
from kimimben import (random_entity, full_name, answer_question, guess_hit, false_guess,
                      question_like, UNKNOWN_RESPONSES)
from tabu import kart_pool
from futbol import FutbolTakip
from burc import gunluk_yorum


# Sunucu ayarları. GitHub'a yüklerken gizli/kişisel değerleri kodun içine yazmayın.
# Ortam değişkenleri ile değiştirilebilir.
HOST = os.getenv("BOT_HOST", "sohbet.mobilyeri.com")
PORT = int(os.getenv("BOT_PORT", "4267"))
ORIGIN = os.getenv("BOT_ORIGIN", "https://sohbet.mobilyeri.com")
WS_PATH = os.getenv("BOT_WS_PATH", "/socket.io/?EIO=4&transport=websocket")

NICK = os.getenv("BOT_NICK", "SoruBotu")
CINSIYET = os.getenv("BOT_GENDER", "e")
FINGERPRINT = os.getenv("BOT_FINGERPRINT", "2718281828459045")
BOT_SCREEN = os.getenv("BOT_SCREEN", "1920x1080")
BOT_LOCATION = os.getenv("BOT_LOCATION", "38.4_27.1")
ROUND_LEN = 30
TIME_PER_Q = 25
HINT_AFTER = 15
PACK_SIZE = 50
KIB_LEN = 10
KIB_Q_TIME = 40
TABU_LEN = 10
TABU_TIME = 45
WORK_TURN = 15   # sıradaki oyuncunun doğru kelime için süresi (sn)
WORK_MIN = 2     # oyunun başlayabilmesi için en az katılımcı
WORK_TUR = 5     # toplam üretilecek kelime (tur) sayısı
WORK_KATILIM = 25  # /kelimeoyunu sonrası katılım için beklenen süre (sn)
INSAN_ISIMLERI = set("""ahmet mehmet mustafa ali veli hasan huseyin recep murat mehmetcan yusuf emre osman omer ismail mustafa hakan emrah burak mert berkay umut baran onur kerem arda ege deniz efe emir kaan cagri serkan volkan kemal faruk cengiz selim mahmut necati enes samet talha fatih ertugrul sultan beyza zeynep elif elifsu fatma ayse hatice emine merve esra gulsah elifnaz zehra tugba sevgi seda dilek sibel nurgul melike betul kubra sude nazli ebru gulcan aylin demet yasemin figen perihan gamze hande irem berrak selma sanem sila cemre asli ecrin buse elifsu damla ilayda seyma sultan dilara ozge ayca inci ece melis cisem gozde pelin sebnem didem ahu nezih serap sukran rabia meryem eslem gulben nurbanu asuman fadime kerime suzan zeliha zeynepesra melda hamiyet saadet ilknur aysegul fatmanur haticekubra elifemine rabia nur sena mihriban vildan abdurrahman abdullah ramazan adem ibrahim musa harun isa yakup yusuf eyup sami ali emirhan emiraslan kagan alparslan ugur gokhan tolga cengizhan basaran yilmaz gurkan onuralp koray umutcan oguzhan saltuk polat emirzat bugra yatagan bahadir inanc hayrullah seyyid mustafa kemal muhammet izzet erkan kayra yavuz nuh balaban oguz selcuk turker burakcan emrecan efehan ali kerem beyzanur zekiye muzeyyen gullu sukriye nagehan siranur helin hiranur sudeynur necibe sehriban gulizar nazan pervin nebahat zerrin nihat gaye gonul canan sevcan aybike iller kutbettin erman yaman cetin taner cihat cigdem selen meltem ilker kaan burakhan emiralp galip teoman metin sezai oral guven cenk bahadir ediz penbe ibrahim walter jessica michael david james jennifer linda elizabeth sarah kevin thomas jason john smith william joseph daniel anthony mark paul steven andrew karen nancy patricia maria sandra donna carol ruth sharon michelle laura amy kimberly deborah davidson jordan scott taylor ashley adam justin brandon christian sofia ana mia emma lucas leo mateo daniela camila valentina santiago alejandro diego carmen rosario isabella sofie emil lars oskar noah liam oliver elijah mason""".split())
TAUNT = [
    "Yarışmacılar nerede? Cevap gelmedi, hepiniz nal topladınız :D",
    "Bu soru çok kolaydı ama meydan boş, uyuyakalmışsınız :)",
    "Vay be, kimse bilemedi. İnternetiniz mi kesildi hepinizin?",
    "Cevap bekliyorum ben, siz tavana bakıyorsunuz :)",
    "Bu soruyla sabaha kadar uğraşılmaz, yazın cevabı yahu :D",
    "Skor tablosu boş kalacak bu gidişle, cevap yazmaktan kim korkuyor :D",
    "Bu saatte kimse seyretmiyor galiba, cevabı söylüyorum :D",
    "Cevap yok mu? Klavye başında futbol oynayanlar baksın buraya :)",
    "Eyvah, yarış macılar derin uykuda, ben yine anlatacağım :)",
    "Hadi ama! Bu soruyu bilmeyen yarışa hiç girmesin :D",
    "Meydan okumam boşa gitti, cevap bekliyorum hala...",
    "Bakalım kimin parmağı havaya kalkacak, cevap bekliyorum :)",
]

PRAISE = [
    "%s örümcek adam gibi davrandı, herkesten hızlı doğruyu buldu :) (+1 puan)",
    "Aferin %s, cevabı duşta değil burda mi buldun :) (+1 puan)",
    "%s bu akşamın yıldızı, herkes şapka çıkarsın :D (+1 puan)",
    "%s yıldırım hızıyla vurdu, bu cevap tam profesyonel! (+1 puan)",
    "Gece gece hangi beyin bu kadar çalışır %s? Aferin :) (+1 puan)",
    "Aferin %s! Doğru cevap, kıskananlar çatlaksın :D (+1 puan)",
    "%s skor tabelasının yeni lideri oldu, bravo :) (+1 puan)",
    "Eline sağlık %s, beynin kadar elin de hızlıymış :) (+1 puan)",
    "%s sinirli bir detektif gibi yakaladı cevabı :D (+1 puan)",
    "Şampiyon adayı belli oldu, %s keleş gibi :) (+1 puan)",
    "Bravo %s, bu performansla herkesi mahçup ettin :D (+1 puan)",
    "%s cevabı fısıldar gibi söyledi ama tam isabet! (+1 puan)",
]

IDLE = [
    "Canınız sıkıldıysa /sorusor yazarak 30 soruluk yarışmayı başlatabilirsiniz :)",
    "10 turluk KimimBen'de gizli kimlikleri bulun: /kimimben yazın :)",
    "Bilgiye doymak isteyen /sorusor yazsın, sorular 25 saniyede bir :)",
    "Meraklısına: /sorusor'da her 3 soruda 1 yetişkin soru var :D",
    "Yarışma için /sorusor, 10 turluk KimimBen için /kimimben yazmanız yeterli :)",
    "Bu lobide bilgi yarışması ister misiniz? /sorusor yeterli :)",
    "Boş boş beklemek yerine /sorusor yazın, beyinler jimnastik yapsın :D",
    "Ben 2146 genel + 932 yetişkin soruyla buradayım. /sorusor ile başlat :)",
    "30 soruluk turda her 3 soruda 1 yetişkin soru sorarım, /puan ile skoru gör :)",
    "İpucu 15 saniyede gelir, matematik sorularına ipucu verilmez :)",
    "Doğru cevaba +1 puan veririm, kim kazanır? /sorusor ile başlasın :)",
    "Rekorları görmek için /puan, bilgi yarışması için /sorusor yazın :)",
    "KimimBen'de bana soru sorun siz bulun, 10 turda 10 kimlik: /kimimben :)",
    "İpucuna dikkat: harfler kurnazca gizlenir, cevabı sen çöz :D",
    "/sorusor yazan olursa 25 saniyelik sorularla 30 soruluk tur başlıyor :)",
    "Soru dağılımı: genel + yetişkin karışık, her 3 soruda 1 yetişkin :)",
    "Bilgi yarışması anlatırım, Kimler milyoner olur? Sen olabilirsin :D",
    "KimimBen'de bana 'Evet/Hayır' soruları sorun, 10 turda 10 kimliği bulun: /kimimben :)",
    "Hepiniz cevap yazın, puanlar biriksin, sonuçta sıralama çıksın :)",
    "Ortam 18+ ya, yetişkin soruları da sormakta sakınca yok :D",
    "Bilenlere şeref: /sorusor, 30 soru, +1 puan, sonunda sıralama :)",
    "Soru bankam 2500'e yakın, tekrar bekleme derdi yok :)",
    "Nasıl oynanır? /sorusor başlat, doğru cevabı yaz, puan topla :)",
    "KimimBen'de ipucudan 40 saniye sonra cevabı söyler, sonraki tura geçerim :)",
    "Tabu'da gizli kelimeyi yazın, yasaklı kelime yazana patlar :D /tabu ile başla :)",
    "10 kartlık Tabu turu için /tabu yazın, +1 puan sizi bekliyor :)",
    "Skor sıralaması /puan ile, kimlerin aklı keskin görün :)",
    "Boştayım, yine /sorusor ya da /kimimben ya da /tabu bekliyorum. Ne dersiniz? :)",
    "Elinde kalemle dolaşan varsa /sorusor yazsın, soru yağsın :)",
    "Yarışma havası gelsin diye buradayım: /sorusor yeterli :)",
]


def norm(s):
    s = s.lower()
    tr = {"ç": "c", "ğ": "g", "ı": "i", "i": "i", "ö": "o", "ş": "s", "ü": "u", "â": "a"}
    s = "".join(tr.get(c, c) for c in s)
    return re.sub(r"[^a-z0-9]", "", s)


def hint_text(word):
    word = re.sub(r"[^a-zA-ZçğıöşüÇĞİÖŞÜ0-9 ]", "", word)
    parts = word.split(" ")
    out = []
    for w in parts:
        if not w:
            continue
        low = w.lower()
        chars = list(low)
        if len(chars) <= 2:
            out.append(low)
            continue
        for i in range(1, len(chars) - 1):
            if (i % 3 != 2) and i != len(chars) - 1:
                chars[i] = "_"
        out.append("".join(chars))
    return " ".join(out)


class Conn:
    def __init__(self, ss, buf):
        self.ss = ss
        self.buf = buf

    def send(self, text):
        payload = text.encode("utf-8")
        ln = len(payload)
        if ln < 126:
            hdr = bytes([0x81, 0x80 | ln])
        elif ln < 65536:
            hdr = bytes([0x81, 0x80 | 126]) + struct.pack(">H", ln)
        else:
            hdr = bytes([0x81, 0x80 | 127]) + struct.pack(">Q", ln)
        mask = os.urandom(4)
        self.ss.sendall(hdr + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))

    def recv(self, timeout=2):
        self.ss.settimeout(timeout)
        if not self.buf:
            h = self._r(2)
        else:
            h, self.buf = self.buf[:2], self.buf[2:]
        ln = h[1] & 0x7F
        if ln == 126:
            ln = struct.unpack(">H", self._r(2))[0]
        elif ln == 127:
            ln = struct.unpack(">Q", self._r(8))[0]
        return self._r(ln).decode("utf-8", "replace")

    def _r(self, n):
        if self.buf:
            take = min(n, len(self.buf))
            out, self.buf = self.buf[:take], self.buf[take:]
        else:
            out = b""
        while len(out) < n:
            c = self.ss.recv(n - len(out))
            if not c:
                raise IOError("kapandi")
            out += c
        return out


class SoruBotu:
    def __init__(self):
        self.pool = normal_pool()
        self.erotik = erotik_pool()
        self.pack_norm = []
        self.pack_er = []
        self.score = {}
        self.display = {}
        self.players = set()
        self.round = False
        self.qno = 0
        self.question = None
        self.q_start = 0
        self.hint_sent = False
        self.answers = ()
        self.round_questions = []
        self.kripto = ""
        self.godaid = 1
        self.conn = None
        self.nick = NICK
        self.next_send = 0
        self.last_idle = time.time()
        self.idle_next = 900
        self.kib = None
        self.kib_last = 0
        self.kib_q = 0
        self.kib_tur = 1
        self.tabu = None
        self.tabu_pool = []
        self.tabu_q = 0
        self.tabu_last = 0
        self.work = None
        self.work_last = 0
        self.fb_queue = queue.Queue()
        self.futbol = FutbolTakip(say_cb=self._fb_push)

    def _fb_push(self, msg):
        self.fb_queue.put(msg)

    def _drain_fb(self):
        while True:
            try:
                msg = self.fb_queue.get_nowait()
            except queue.Empty:
                break
            self.say(msg)

    # ---------- baglanti ----------
    def http_login(self, nick):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        h = http.client.HTTPSConnection(HOST, PORT, timeout=15, context=ctx)
        hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Origin": ORIGIN,
                "Content-Type": "application/json", "Accept": "application/json"}
        h.request("GET", "/init", headers=hdrs)
        r = h.getresponse()
        r.read()
        h.close()
        body = json.dumps({"nick": nick, "gender": CINSIYET, "fromId": FINGERPRINT,
                           "ekran": BOT_SCREEN, "EnlemBoylam": BOT_LOCATION}).encode()
        h = http.client.HTTPSConnection(HOST, PORT, timeout=15, context=ctx)
        hdrs["Content-Length"] = str(len(body))
        h.request("POST", "/login", body=body, headers=hdrs)
        r = h.getresponse()
        resp = r.read().decode("utf-8", "replace")
        cookies = []
        for c in (r.headers.get_all("Set-Cookie") or []):
            m = re.match(r"([^=]+)=([^;]*);", c)
            if m:
                cookies.append(m.group(1) + "=" + m.group(2))
        h.close()
        sid = [c for c in cookies if c.startswith("sid=")]
        return sid[-1] if sid else None, resp

    def connect_ws(self, cookie):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = socket.create_connection((HOST, PORT), timeout=15)
        ss = ctx.wrap_socket(s, server_hostname=HOST)
        key = base64.b64encode(os.urandom(16)).decode()
        req = ("GET %s HTTP/1.1\r\nHost: %s:%d\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
               "Origin: %s\r\nSec-WebSocket-Key: %s\r\nSec-WebSocket-Version: 13\r\n"
               "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\nCookie: %s\r\n\r\n") % (
            WS_PATH, HOST, PORT, ORIGIN, key, cookie)
        ss.sendall(req.encode())
        data = b""
        ss.settimeout(6)
        while b"\r\n\r\n" not in data:
            d = ss.recv(4096)
            if not d:
                raise IOError("handshake kapandi")
            data += d
        head, rest = data.split(b"\r\n\r\n", 1)
        if b" 101 " not in head:
            raise IOError("101 degil: " + head.decode("utf-8", "replace"))
        conn = Conn(ss, rest)
        for _ in range(10):
            t = conn.recv(4)
            if t.startswith("0"):
                conn.send("40")
                break
        for _ in range(10):
            t = conn.recv(4)
            if t.startswith("40"):
                break
        return conn

    def login_and_connect(self, nick=None):
        nick = nick or self.nick
        cookie, resp = self.http_login(nick)
        if not cookie:
            raise IOError("login basarisiz: " + resp[:200])
        conn = self.connect_ws(cookie)
        time.sleep(1.0)
        conn.send('42["userClop","%s","%s",0,"e","e","e","e","e"]' % (nick, CINSIYET))
        self.conn = conn
        self.next_send = time.time()
        return conn

    def reconnect(self, attempt=0):
        if attempt > 6:
            raise SystemExit("Baglanti kurulamadi")
        print("Yeniden baglaniliyor (%d)..." % attempt, flush=True)
        time.sleep(3 + attempt * 3)
        try:
            self.login_and_connect()
            self.say("Bağlantı yenilendi, yarışma kaldığı yerden devam edebilir :)")
        except Exception as e:
            self.nick = NICK + str(random.randint(10, 99))
            print("nick degisti:", self.nick, e, flush=True)
            self.reconnect(attempt + 1)

    # ---------- mesaj ----------
    def say(self, text, force=False):
        if time.time() < self.next_send and not force:
            wait = self.next_send - time.time()
            time.sleep(min(wait, 3))
        self.conn.send('42["mesajYolla","%s","000000"]' % text.replace('"', "'").replace("\n", " "))
        self.next_send = time.time() + 2.5
        print("[TX]", text, flush=True)

    # ---------- oyun ----------
    def _ensure(self, name, factory):
        if not getattr(self, name):
            setattr(self, name, factory())

    def make_pack(self):
        self._ensure("pool", normal_pool)
        self._ensure("erotik", erotik_pool)
        er = max(1, PACK_SIZE // 3)
        self.pack_norm = [self.pool.pop() for _ in range(PACK_SIZE - er)]
        self.pack_er = [self.erotik.pop() for _ in range(er)]
        random.shuffle(self.pack_norm)
        random.shuffle(self.pack_er)

    def pop_normal(self):
        if not self.pack_norm:
            self.make_pack()
        return self.pack_norm.pop()

    def pop_erotik(self):
        if not self.pack_er:
            self.make_pack()
        return self.pack_er.pop()

    def next_question(self):
        if self.qno >= ROUND_LEN:
            self.finish_round()
            return
        self.question = self.round_questions[self.qno]
        self.qno += 1
        self.answers = self.question[1]
        self.q_start = time.time()
        self.hint_sent = False
        self.say("Soru %d/%d: %s" % (self.qno, ROUND_LEN, self.question[0]))

    def start_round(self):
        if self.round:
            self.say("Yarışma zaten devam ediyor :)")
            return
        self.score = {}
        self.players = set()
        self.display = {}
        self.round = True
        self.qno = 0
        er_n = ROUND_LEN // 3
        self.round_questions = ([self.pop_erotik() for _ in range(er_n)]
                                + [self.pop_normal() for _ in range(ROUND_LEN - er_n)])
        random.shuffle(self.round_questions)
        self.say("Merhaba herkese! 30 soruluk mini bilgi yarışması başlıyor :)")
        self.say("Her 3 soruda 1 yetişkin soru var, matematikte ipucu verilmez :)")
        time.sleep(1.5)
        self.next_question()

    def finish_round(self):
        self.round = False
        self.say("Yarışma bitti! Sonuçlar:")
        if self.score:
            sirala = sorted(self.score.items(), key=lambda x: (-x[1], x[0]))
            for i, (key, p) in enumerate(sirala, 1):
                goster = self.display.get(key, key).capitalize()
                self.say("%d) %s - %d puan" % (i, goster, p))
        else:
            self.say("Kimse puan alamadı :(")
        self.say("Yeni yarışma için /sorusor, 10 turluk KimimBen için /kimimben yazın :)")
        self.last_idle = time.time()
        self.idle_next = 900

    def tick(self, now):
        if not self.round or not self.question:
            return
        elapsed = now - self.q_start
        if not self.hint_sent and elapsed >= HINT_AFTER:
            self.hint_sent = True
            cvn = norm(self.question[1][0])
            if cvn.isdigit():
                return
            cv = self.question[1][0]
            if len(cv) > 1:
                self.say("İpucu: %s" % hint_text(cv))
        if elapsed >= TIME_PER_Q:
            cv = self.question[1][0]
            self.say("Süre doldu! " + random.choice(TAUNT))
            self.say("Cevap: %s" % cv)
            self.next_question()

    def idle_tick(self, now):
        if not self.round and now - self.last_idle > self.idle_next:
            self.last_idle = now
            self.idle_next = 900
            self.say(random.choice(IDLE))

    def show_football_scores(self, filtre=""):
        from futbol import fetch_date, fetch_real_date, _norm, TRACK
        import datetime
        gercek = fetch_real_date() or datetime.date.today()
        fxt = []
        hata = False
        for gun in range(0, 10):
            tarih = (gercek - datetime.timedelta(days=gun)).strftime("%Y%m%d")
            g = fetch_date(tarih)
            if g is None:
                hata = True
                continue
            fxt.extend(g)
        if hata and not fxt:
            self.say("Skor servisine ulaşılamadı :(")
            return
        if not fxt:
            self.say("Son günlerde takip edilen takımların maçı yok (GS-FB-BJK-TS). /skor beşiktaş gibi bir takım adı da deneyebilirsiniz :)")
            return
        bulunan = []
        for f in fxt:
            hn = f.get("home", "")
            an = f.get("away", "")
            if filtre:
                fn = _norm(filtre)
                if fn not in _norm(hn) and fn not in _norm(an):
                    continue
            elif _norm(hn) not in TRACK and _norm(an) not in TRACK:
                continue
            eps = (f.get("eps") or "").strip() or "NS"
            sc = f.get("sc") or ["?", "?"]
            ht = f.get("ht") or ["-", "-"]
            if eps in ("NS", ""):
                durum = "Henüz başlamadı"
            elif eps == "HT":
                durum = "Devre arası"
            elif eps == "FT":
                durum = "Bitti"
            else:
                durum = "Canlı (%s')" % eps
            bulunan.append("%s %s-%s %s (%s | ilk yarı: %s-%s)" %
                           (hn, sc[0], sc[1], an, durum, ht[0], ht[1]))
        if bulunan:
            for satir in bulunan:
                self.say(satir)
        else:
            if filtre:
                self.say("'%s' maçı bulunamadı :(" % filtre.title())
            else:
                self.say("Bugün takip edilen maç yok :)")

    def on_message(self, rumuz, mtext, gcript):
        gt = mtext.strip()
        if not gt:
            return
        low = gt.lower()
        if low == "/bitir":
            self.round = False
            self.qno = 0
            self.question = None
            self.q_start = 0
            self.hint_sent = False
            self.answers = ()
            self.round_questions = []
            self.kib = None
            self.kib_tur = 1
            self.tabu = None
            self.tabu_pool = []
            self.tabu_q = 0
            self.work = None
            self.say("Oyun durduruldu :)")
            return
        if low in ("/sorusor", "/botbasla"):
            if self.round:
                self.say("Yarışma zaten devam ediyor :)")
            elif self.kib:
                self.say("KimimBen devam ediyor, önce /cevap ile bitirin :)")
            elif self.tabu:
                self.say("Tabu devam ediyor, önce /bitir yazın :)")
            else:
                self.start_round()
            return
        if low == "/kimimben" or low == "/kim":
            if self.kib:
                self.say("KimimBen zaten devam ediyor :)")
            elif self.round:
                self.say("Önce 30 soruluk yarışma bitsin :)")
            elif self.tabu:
                self.say("Tabu devam ediyor, önce /bitir yazın :)")
            else:
                self.start_kib()
            return
        if low == "/tabu":
            if self.tabu:
                self.say("Tabu zaten devam ediyor :)")
            elif self.round:
                self.say("Önce 30 soruluk yarışma bitsin :)")
            elif self.kib:
                self.say("KimimBen devam ediyor, önce /cevap ile bitirin :)")
            else:
                self.start_tabu()
            return
        if low == "/kelimeoyunu" or low == "/worksor" or low == "/work":
            if self.work:
                self.say("Kelime Oyunu zaten devam ediyor :)")
            elif self.round:
                self.say("Önce 30 soruluk yarışma bitsin :)")
            elif self.kib:
                self.say("KimimBen devam ediyor, önce /cevap ile bitirin :)")
            elif self.tabu:
                self.say("Tabu devam ediyor, önce /bitir yazın :)")
            else:
                self.start_work()
            return
        if low in ("/cevap", "/gizli", "/vazgec"):
            if self.kib:
                self.say("İpucu yok, kimlik %s idi :D" % full_name(self.kib))
                self.end_kib_tur(bulundu=True)
            else:
                self.say("Aktif bir KimimBen oyunu yok :)")
            return
        if low == "/katıl" or low == "/katil":
            if self.work:
                self.work_katil(rumuz)
            elif self.round:
                self.say("/sorusor'da /katıl gerekmez, doğru cevap veren herkes otomatik katılır :)")
            else:
                self.say("Yarışma başlamadı, başlatmak için /sorusor yazın :)")
            return
        if low == "/skor" or low.startswith("/skor "):
            takim = low.replace("/skor", "").strip()
            self.show_football_scores(takim)
            return
        if low in ("/puan", "/skor2"):
            if self.score:
                sirala = sorted(self.score.items(), key=lambda x: (-x[1], x[0]))
                self.say("Skor: " + ", ".join("%s: %d" % (self.display.get(k, k), v) for k, v in sirala))
            else:
                self.say("Henüz puan yok :)")
            return
        if low == "/fbtest":
            self.fb_queue.put("⚽ GOOL! Test Oyuncu (Galatasaray) 50'. dakikada attı! Skor: 2-1")
            return
        if "fried help" in low or low == "/help":
            self.say("Komutlar: /sorusor (30 soruluk yarışma), /kimimben (10 turluk gizli kimlik), /tabu (10 kart), /kelimeoyunu (kelime zinciri), /katıl, /puan, /cevap, /bitir, /ikizler gibi burç adları (günlük burç yorumu)")
            return
        if low.startswith("/") and len(norm(low)) in range(3, 9):
            yorum, hata = gunluk_yorum(low[1:])
            if hata is None:
                self.say(yorum)
                return
        if self.kib and gcript != self.kripto and rumuz != self.nick:
            self.handle_kib(rumuz, gt)
            return
        if self.work and gcript != self.kripto and rumuz != self.nick:
            self.handle_work(rumuz, gt)
            return
        if self.tabu and gcript != self.kripto and rumuz != self.nick:
            self.handle_tabu(rumuz, gt)
            return
        if self.round and self.question and gcript != self.kripto and rumuz != self.nick:
            if self.answer_hit(gt):
                self.award(rumuz, gt)

    def answer_hit(self, gt):
        n = norm(gt)
        for a in self.answers:
            if n == norm(a):
                return True
        return False

    def add_point(self, rumuz):
        key = norm(rumuz)
        if not key:
            return
        self.score[key] = self.score.get(key, 0) + 1
        self.players.add(rumuz)
        self.display[key] = rumuz
        self.say(random.choice(PRAISE) % rumuz)

    def award(self, rumuz, gt):
        self.add_point(rumuz)
        self.next_question()

    # ---------- kimimben ----------
    def start_kib(self):
        self.kib_tur = 1
        self.say("KimimBen yarışması başladı! 10 tur, 10 gizli kimlik :)")
        self.say("Soru sormak sizden! Bana 'Evet/Hayır' soruları sorun, bildiğinizde adımı yazın (+1 puan).")
        self.say("İpucu verildikten 40 saniye sonra cevap gelmezse kimliği söyler, sonraki tura geçerim :)")
        self.start_kib_tur()

    def start_kib_tur(self):
        self.kib = random_entity()
        self.kib_last = time.time()
        if self.kib.get("hint"):
            self.say("Tur %d/%d -> İpucu: %s" % (self.kib_tur, KIB_LEN, self.kib["hint"]))
        else:
            self.say("Tur %d/%d başladı, hadi sorun :)" % (self.kib_tur, KIB_LEN))

    def end_kib_tur(self, bulundu=False):
        if not bulundu:
            self.say("40 saniye doldu! Kimlik %s idi :)" % full_name(self.kib))
        self.kib = None
        self.kib_tur += 1
        if self.kib_tur > KIB_LEN:
            self.finish_kib()
        else:
            time.sleep(1.2)
            self.start_kib_tur()

    def finish_kib(self):
        self.say("KimimBen yarışması bitti! 10 tur tamamlandı :D")
        if self.score:
            sirala = sorted(self.score.items(), key=lambda x: (-x[1], x[0]))
            self.say("Skor: " + ", ".join("%s: %d" % (self.display.get(k, k), v) for k, v in sirala))
        self.kib = None

    def handle_kib(self, rumuz, gt):
        if not self.kib:
            return
        if guess_hit(self.kib, gt):
            self.say("Bildin! Ben %s'ydim :D" % full_name(self.kib))
            self.add_point(rumuz)
            self.end_kib_tur(bulundu=True)
            return
        if question_like(gt):
            v = answer_question(self.kib, gt)
            if v is None:
                self.say(random.choice(UNKNOWN_RESPONSES))
            else:
                self.say("Evet" if v else "Hayır")
            return
        if false_guess(self.kib, gt):
            self.say("Hayır, o değilim :)")
            return

    def kib_tick(self, now):
        if self.kib and now - self.kib_last > KIB_Q_TIME:
            self.end_kib_tur()

    # ---------- tabu ----------
    def start_tabu(self):
        self.tabu_pool = kart_pool()
        self.tabu_q = 0
        self.say("Tabu başladı! %d kart oynuyoruz :) Anlatacağım kelimeyi bulun." % TABU_LEN)
        self.say("İpucuna göre gizli kelimeyi yazın (+1 puan). Yasaklı kelimeleri yazarsanız Tabu patlar :D")
        self.next_tabu()

    def next_tabu(self):
        if self.tabu_q >= TABU_LEN or not self.tabu_pool:
            self.finish_tabu()
            return
        kelime, yasak, ipucu = self.tabu_pool.pop()
        self.tabu = {"kelime": kelime, "yasak": [y.lower() for y in yasak], "ipucu": ipucu}
        self.tabu_q += 1
        self.tabu_last = time.time()
        self.say("Kart %d/%d -> İpucu: %s" % (self.tabu_q, TABU_LEN, ipucu))
        self.say("Yasaklı kelimeler: %s" % ", ".join(yasak))

    def handle_tabu(self, rumuz, gt):
        if not self.tabu:
            return
        n = norm(gt)
        if n and n == norm(self.tabu["kelime"]):
            kelime = self.tabu["kelime"]
            self.say("Bildin! Gizli kelime %s'di :D" % kelime)
            self.add_point(rumuz)
            self.tabu = None
            self.tabu_last = time.time()
            self.next_tabu()
            return
        for y in self.tabu["yasak"]:
            if y and norm(y) and norm(y) in n:
                self.say("Tabu patladı! '%s' yasaklıydı, patlama sesini duydunuz mu :D" % y)
                return
        if len(n) <= 2:
            return

    def tabu_tick(self, now):
        if self.tabu and now - self.tabu_last > TABU_TIME:
            self.say("Süre doldu! Gizli kelime: %s" % self.tabu["kelime"])
            self.tabu = None
            self.tabu_last = now
            self.next_tabu()

    def finish_tabu(self):
        self.say("Tabu bitti! %d kart tamamlandı :D" % TABU_LEN)
        if self.score:
            sirala = sorted(self.score.items(), key=lambda x: (-x[1], x[0]))
            self.say("Skor: " + ", ".join("%s: %d" % (self.display.get(k, k), v) for k, v in sirala))
        self.tabu = None
        self.tabu_pool = []
        self.tabu_q = 0

    # ---------- work (kelime zinciri) ----------
    def start_work(self):
        work = random.choice(["ka", "de", "gi", "ko", "me", "ba", "se", "ta", "ya",
                              "su", "an", "ha", "is", "ki", "le", "or", "sa", "ku",
                              "mo", "pi", "re", "ne", "ge", "ça", "cı", "be", "do"])
        self.work = {
            "katilimcilar": [],
            "sira": 0,
            "tur": 1,
            "aranan": norm(work),
            "baslangic": None,
            "son_kelime": None,
            "kullanilan": set(),
            "adim": "bekleniyor",
            "tstart": time.time(),
        }
        self.say("Kelime Oyunu başladı! Oyun başlatmak için /katıl komutunu yazmanız gerekiyor :)")
        self.say("Oyun en az %d kişi ile oynanır. Oyunun başlaması için %d saniye bekliyorum :)"
                 % (WORK_MIN, WORK_KATILIM))
        self.say("Nasıl oynanır? Bot bir kelimenin başlangıcını verir, sıradaki oyuncu o harflerle başlayan bir kelime üretir. Sonraki her oyuncu bir önceki kelimenin SON 2 harfiyle yeni kelime üretir :)")
        self.work_last = time.time()

    def work_view(self):
        k = self.work
        return [r for r, elen in k["katilimcilar"] if not elen]

    def work_baslat(self):
        katilan = self.work_view()
        if len(katilan) < WORK_MIN:
            self.say("Yeterli katılımcı olmadı, oyun başlamadı :(")
            return
        self.work["adim"] = "sira"
        self.work["sira"] = 0
        self.say("Oyuncular (katılım sırası): %s" % ", ".join(katilan))
        self.work_duyur()

    def work_duyur(self):
        k = self.work
        aktif = self.work_view()
        if not aktif or len(aktif) == 1:
            self.finish_work()
            return
        k["sira"] = k["sira"] % len(aktif)
        oyuncu = aktif[k["sira"]]
        k["oyuncu"] = oyuncu
        k["adim"] = "sira"
        k["tstart"] = time.time()
        self.say("Sıra -> @%s, '%s' ile başlayan bir kelime üret (%d sn) :)"
                 % (oyuncu, self.work_harf(), WORK_TURN))

    def work_harf(self):
        k = self.work
        return k["baslangic"] if k["baslangic"] else k["aranan"]

    def work_harfler(self):
        return ["ka", "de", "gi", "ko", "me", "ba", "se", "ta", "ya", "su", "an",
                "ha", "is", "ki", "le", "or", "sa", "ku", "mo", "pi", "re", "ne",
                "ge", "ça", "cı", "be", "do"]

    def work_soklu_get(self, url):
        """Sertifika doğrulaması kapalı HTTPS isteği (ortam sertifika sorunları için)."""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            return r.read().decode("utf-8", "replace")

    def work_gecerli_kelime(self, kelime_norm):
        """Kelimenin geçerli olup olmadığını kontrol eder: insan ismi veya Türkçe (TDK) sözlük."""
        if kelime_norm in INSAN_ISIMLERI:
            return True
        try:
            q = urllib.parse.quote(kelime_norm)
            d = json.loads(self.work_soklu_get("https://sozluk.gov.tr/gts?ara=" + q))
            if d and isinstance(d, list):
                return True
        except Exception:
            pass
        return False

    def work_katil(self, rumuz):
        k = self.work
        if not k:
            return
        if k["adim"] != "bekleniyor":
            self.say("Kelime Oyunu başladı, artık katılım kapalı :)")
            return
        if any(r == rumuz for r, _ in k["katilimcilar"]):
            self.say("%s zaten katıldı :) Tekrar katılamazsın :D" % rumuz)
            return
        k["katilimcilar"].append((rumuz, False))
        self.say("%s Kelime Oyununa katıldı :) Katılanlar: %d (%d sn kaldı)"
                 % (rumuz, len(k["katilimcilar"]), max(0, int(WORK_KATILIM - (time.time() - k["tstart"])))))
        self.work_last = time.time()

    def handle_work(self, rumuz, gt):
        k = self.work
        if not k or k["adim"] != "sira":
            return
        if rumuz != k["oyuncu"]:
            # Sırası gelmeyenin / elenenin mesajı kabul edilmez
            return
        kelime = gt.strip()
        on = norm(kelime)
        if len(on) < 3:
            self.say("@%s, en az 3 harfli bir kelime yaz :)" % rumuz)
            return
        if on in k["kullanilan"]:
            self.say("@%s, '%s' zaten kullanıldı :) Farklı bir kelime üret (%d sn)"
                     % (rumuz, kelime, WORK_TURN))
            return
        hedef = norm(k["baslangic"] if k["baslangic"] else k["aranan"])
        if not on.startswith(hedef):
            self.say("@%s, '%s' doğru değil. '%s' ile başlamalıydı :) Tekrar dene (%d sn)"
                     % (rumuz, kelime, hedef, WORK_TURN))
            return
        if not self.work_gecerli_kelime(on):
            self.say("@%s, '%s' anlamlı/geçerli bir kelime değil :) Farklı bir kelime üret (%d sn)"
                     % (rumuz, kelime, WORK_TURN))
            return
        k["kullanilan"].add(on)
        k["son_kelime"] = kelime
        k["tur"] += 1
        w = norm(kelime)
        k["baslangic"] = w[-2:] if len(w) >= 2 else hedef
        self.say("Bildin @%s! '%s' doğru :) Yeni başlangıç: '%s'" % (rumuz, kelime, self.work_harf()))
        aktif = self.work_view()
        if rumuz in aktif:
            k["sira"] = (aktif.index(rumuz) + 1) % len(aktif)
        time.sleep(1.2)
        self.work_duyur()

    def work_yeni_harf(self):
        """Elenen biri olduğunda sıradaki oyuncu için rastgele yeni bir 2 harf verir."""
        k = self.work
        k["baslangic"] = random.choice(self.work_harfler())
        while norm(k["baslangic"]) == norm(k["aranan"]) or (k["son_kelime"] and norm(k["baslangic"]) == norm(k["son_kelime"])[-2:]):
            k["baslangic"] = random.choice(self.work_harfler())

    def work_ele(self, oyuncu):
        for i, (r, elen) in enumerate(self.work["katilimcilar"]):
            if r == oyuncu:
                self.work["katilimcilar"][i] = (r, True)
                break
        self.say("@%s süresi doldu, elendi! Artık mesajları kabul edilmiyor :(" % oyuncu)

    def work_tick(self, now):
        k = self.work
        if not k:
            return
        if k["adim"] == "bekleniyor":
            if now - k["tstart"] > WORK_KATILIM:
                if len(self.work_view()) >= WORK_MIN:
                    self.work_baslat()
                else:
                    self.say("%d saniye doldu, yeterli katılımcı olmadı (en az %d gerekli). Oyun başlamadı :("
                             % (WORK_KATILIM, WORK_MIN))
                    self.work = None
                    self.work_last = 0
            return
        if k["adim"] != "sira":
            return
        if now - k["tstart"] > WORK_TURN:
            oyuncu = k["oyuncu"]
            self.work_ele(oyuncu)
            aktif = self.work_view()
            if len(aktif) <= 1:
                self.finish_work()
                return
            self.say("Sıradaki oyuncuya yeni kelime başlangıcı veriliyor...")
            self.work_yeni_harf()
            k["sira"] = k["sira"] % len(aktif)
            self.work_duyur()
            return

    def finish_work(self):
        k = self.work
        if k:
            sirali = [r for r, e in k["katilimcilar"] if not e]
            elenen = [r for r, e in k["katilimcilar"] if e]
            if sirali and len(sirali) == 1:
                self.say("Kelime Oyunu bitti! Kazanan: @%s :D" % sirali[0])
            else:
                self.say("Kelime Oyunu bitti :D")
            if elenen:
                self.say("Sıralama: " + ", ".join(sirali + elenen))
        self.work = None
        self.work_last = 0

    # ---------- dongu ----------
    def run(self):
        self.login_and_connect()
        self.say("Merhaba, ben SoruBotu! /sorusor ile 30 soruluk yarışma, /kimimben ile 10 turluk Gizli Kimlik, /tabu ile yasaklı kelime :)", force=True)
        self.futbol.start()
        self.last_idle = time.time()
        self.idle_next = 900
        while True:
            now = time.time()
            try:
                t = self.conn.recv(2)
            except socket.timeout:
                self._drain_fb()
                self.tick(now)
                self.idle_tick(now)
                self.kib_tick(now)
                self.tabu_tick(now)
                self.work_tick(now)
                continue
            except (IOError, OSError, ssl.SSLError) as e:
                print("kopma:", e, flush=True)
                self.reconnect()
                continue
            if t == "2":
                self.conn.send("3")
                continue
            if t.startswith("42["):
                try:
                    ev, payload = json.loads(t[2:])
                except Exception:
                    continue
                if ev == "OdaSendMesaj":
                    self.handle_o(now, payload)
                elif ev == "girisData":
                    self.kripto = payload.get("kripto", "")
                elif ev in ("fullDisconnect", "SocketLogout"):
                    print("sunucu koptur:", ev, flush=True)
                    self.reconnect()
                    continue
            self.tick(time.time())
            self._drain_fb()
            self.idle_tick(time.time())
            self.kib_tick(time.time())
            self.work_tick(time.time())

    def handle_o(self, now, p):
        if not isinstance(p, dict):
            return
        if p.get("tip") not in (0, "", None):
            return
        rumuz = p.get("grumuz", "")
        gcript = p.get("gcript", "")
        mtext = p.get("gmesaj", "")
        if not rumuz or rumuz == self.nick:
            return
        self.tick(now)
        self.on_message(rumuz, mtext, gcript)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    bot = SoruBotu()
    bot.run()