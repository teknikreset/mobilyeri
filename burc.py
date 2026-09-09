# -*- coding: utf-8 -*-
# Günlük burç yorumu çekici (gunlukburc.net kaynak).
# Her burç için sabit URL: https://www.gunlukburc.net/gunluk-burc-yorumlari/{burc}.html
# Sayfa her gün güncellenir; içerik <div id="articleBody"> içindeki
# <h2> başlıklı bölümlerden (Genel Durum, Aşk Hayatınız, ...) oluşur.
import re
import ssl
import urllib.request

BASE = "https://www.gunlukburc.net/gunluk-burc-yorumlari/%s.html"

# Türkçe burç adı -> gunlukburc.net slug
BURC_SLUG = {
    "koc": "koc",
    "boga": "boga",
    "ikizler": "ikizler",
    "yengec": "yengec",
    "aslan": "aslan",
    "basak": "basak",
    "terazi": "terazi",
    "akrep": "akrep",
    "yay": "yay",
    "oglak": "oglak",
    "kova": "kova",
    "balik": "balik",
}

# Güzel görünen burç adları (mesaj başında kullanılır)
BURC_ADI = {
    "koc": "Koç", "boga": "Boğa", "ikizler": "İkizler", "yengec": "Yengeç",
    "aslan": "Aslan", "basak": "Başak", "terazi": "Terazi", "akrep": "Akrep",
    "yay": "Yay", "oglak": "Oğlak", "kova": "Kova", "balik": "Balık",
}


def norm(s):
    s = s.lower()
    tr = {"ç": "c", "ğ": "g", "ı": "i", "i": "i", "ö": "o", "ş": "s", "ü": "u", "â": "a"}
    s = "".join(tr.get(c, c) for c in s)
    return re.sub(r"[^a-z0-9]", "", s)


def eslestir(kelime):
    n = norm(kelime)
    if not n:
        return None
    for ad, slug in BURC_SLUG.items():
        if n == ad or n in ad or ad in n:
            return slug
    return None


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
                 "Accept": "text/html"})
    raw = urllib.request.urlopen(req, timeout=timeout, context=ctx).read()
    return _decode(raw)


def _strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&").replace("<br>", " ")
    return re.sub(r"\s+", " ", s).strip()


def _bolumler(html):
    """articleBody div içeriğini (baslik -> paragraf listesi) sözlüğe çevirir."""
    m = re.search(r'id="articleBody"[^>]*>(.*?)</div>\s*</div>\s*<!--\s*/.haber-ana',
                  html, re.DOTALL)
    if not m:
        return {}
    body = m.group(1)
    parts = re.split(r'<h2[^>]*>(.*?)</h2>', body)
    bolumler = {}
    for i in range(1, len(parts) - 1, 2):
        baslik = _strip_tags(parts[i])
        metin = " ".join(_strip_tags(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', parts[i + 1], re.DOTALL))
        if baslik and metin:
            bolumler[baslik] = metin
    return bolumler


def _kisalt(metin, sinir=280):
    if len(metin) <= sinir:
        return metin
    uc = metin[:sinir]
    idx = max(uc.rfind(". "), uc.rfind(".  "), uc.rfind("..."))
    if idx > sinir * 0.5:
        return uc[:idx + 1]
    return uc.rsplit(" ", 1)[0] + "..."


def gunluk_yorum(kelime):
    slug = eslestir(kelime)
    if not slug:
        return None, "Geçersiz burç adı :("
    url = BASE % slug
    try:
        html = _get(url)
    except Exception:
        return None, "Burç servisine ulaşılamadı :("
    bolumler = _bolumler(html)
    if not bolumler:
        return None, "Bugünün yorumu henüz yayınlanmamış :("
    genel = _bolum_bul(bolumler, ["Genel Durum", "Genel"])
    ask = _bolum_bul(bolumler, ["Aşk Hayatınız", "Aşk", "Aşk hayatı"])
    ad = BURC_ADI.get(slug, slug.capitalize())
    satirlar = []
    if genel:
        satirlar.append("⭐ %s burcu bugün: %s" % (ad, _kisalt(genel)))
    if ask:
        satirlar.append("💕 Aşk: %s" % _kisalt(ask))
    if not satirlar:
        return None, "Bugünün yorumu alınamadı :("
    return "\n".join(satirlar), None


def _bolum_bul(bolumler, adaylar):
    for ad_aday in adaylar:
        n_aday = norm(ad_aday)
        if not n_aday:
            continue
        for baslik, metin in bolumler.items():
            if n_aday in norm(baslik):
                return metin
    return None
