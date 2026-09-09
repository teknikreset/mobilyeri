# -*- coding: utf-8 -*-
import re
import random

TR = {"ç": "c", "ğ": "g", "ı": "i", "i": "i", "ö": "o", "ş": "s", "ü": "u", "â": "a"}


def nstr(s):
    s = str(s or "")
    for a, b in (("İ", "i"), ("I", "ı"), ("Ş", "ş"), ("Ğ", "ğ"),
                 ("Ü", "ü"), ("Ö", "ö"), ("Ç", "ç")):
        s = s.replace(a, b)
    s = s.lower()
    s = "".join(TR.get(c, c) for c in s)
    return re.sub(r"[^a-z0-9 ]", " ", s)


def _e(**kw):
    base = dict(cinsiyet=None, turk=None, hayatta=True, insan=True, aktor=False, sarkici=False,
                politikaci=False, sporcu=False, bilim=False, yazar=False, ressam=False,
                komedyen=False, model=False, dansci=False, asker=False, kraliyet=False,
                buyucu=False, hayali=False, hayvan=False, tarihsel=False, evli=None, cocuk=None,
                ulke=[], sehir=[], spor=[], turler=[], kulup=[], gorunum=[], yas=None,
                hayvan_turu=[], meslek=[])
    base.update(kw)
    return base


ENTITIES = [
    _e(isim="Atatürk", tam="Mustafa Kemal Atatürk", cinsiyet="e", turk=True, hayatta=False,
       politikaci=True, asker=True, tarihsel=True, ulke=["türkiye"], sehir=["istanbul", "ankara"],
       gorunum=["sarışın", "mavi gözlü", "bıyıklı"], yas="orta", evli=True, cocuk=False,
       hint="Cumhuriyet'i kuran lider, asker, sarışın ve mavi gözlü"),
    _e(isim="Recep Tayyip Erdoğan", tam="Recep Tayyip Erdoğan", cinsiyet="e", turk=True,
       politikaci=True, ulke=["türkiye"], sehir=["istanbul"], yas="yaşlı", evli=True, cocuk=True,
       hint="Türkiye'nin Cumhurbaşkanı"),
    _e(isim="Tarkan", tam="Tarkan Tevetoğlu", cinsiyet="e", turk=True, sarkici=True,
       turler=["pop"], ulke=["türkiye"], sehir=["istanbul"], gorunum=["sarışın", "bıyıklı"],
       yas="orta", evli=True, cocuk=True, hint="Pop müziğin 'Mikrop'u, sarışın"),
    _e(isim="Hadise", tam="Hadise Açıkgöz", cinsiyet="k", turk=True, sarkici=True,
       turler=["pop"], ulke=["belçika", "türkiye"], sehir=["bruksel"], yas="genç", evli=False,
       cocuk=False, hint="Belçika'da büyüyen genç Türk şarkıcı"),
    _e(isim="Kenan İmirzalıoğlu", tam="Kenan İmirzalıoğlu", cinsiyet="e", turk=True, aktor=True,
       ulke=["türkiye"], sehir=["ankara"], yas="orta", evli=True, cocuk=True,
       hint="Ezel dizisinin yıldızı"),
    _e(isim="Kemal Sunal", tam="Kemal Sunal", cinsiyet="e", turk=True, hayatta=False,
       aktor=True, komedyen=True, ulke=["türkiye"], sehir=["istanbul"], yas="orta", evli=True,
       cocuk=True, hint="Şaban karakterinin ustası komedyen"),
    _e(isim="Barış Manço", tam="Barış Manço", cinsiyet="e", turk=True, hayatta=False,
       sarkici=True, turler=["rock", "anadolu rock"], ulke=["türkiye"], gorunum=["bıyıklı"],
       yas="orta", evli=True, cocuk=True, hint="Adam Olacak Çocuk'un sunucusu"),
    _e(isim="Müslüm Gürses", tam="Müslüm Gürses", cinsiyet="e", turk=True, hayatta=False,
       sarkici=True, turler=["arabesk"], ulke=["türkiye"], gorunum=["bıyıklı", "esmer"],
       yas="yaşlı", evli=True, cocuk=True, hint="Arabesk'in efsanesi"),
    _e(isim="Şener Şen", tam="Şener Şen", cinsiyet="e", turk=True, aktor=True,
       ulke=["türkiye"], gorunum=["bıyıklı"], yas="yaşlı", evli=True, cocuk=True,
       hint="Kara mizah ustası oyuncu"),
    _e(isim="Şebnem Ferah", tam="Şebnem Ferah", cinsiyet="k", turk=True, sarkici=True,
       turler=["rock"], ulke=["türkiye"], gorunum=["esmer"], yas="genç", evli=False, cocuk=False,
       hint="Rock müziğin güçlü sesi"),
    _e(isim="Cem Yılmaz", tam="Cem Yılmaz", cinsiyet="e", turk=True, aktor=True, komedyen=True,
       ulke=["türkiye"], sehir=["istanbul"], yas="orta", evli=False, cocuk=True,
       hint="Stand-up komedyen, vizyon devam ediyor"),
    _e(isim="Sezen Aksu", tam="Sezen Aksu", cinsiyet="k", turk=True, sarkici=True,
       turler=["pop"], ulke=["türkiye"], gorunum=["esmer"], yas="yaşlı", evli=False, cocuk=True,
       hint="Minik Serçe"),
    _e(isim="Aziz Sancar", tam="Aziz Sancar", cinsiyet="e", turk=True, bilim=True,
       ulke=["türkiye"], sehir=["mardin"], gorunum=["bıyıklı"], yas="yaşlı", evli=True,
       cocuk=None, hint="Nobel Ödüllü bilim insanı"),
    _e(isim="Selçuk Bayraktar", tam="Selçuk Bayraktar", cinsiyet="e", turk=True, bilim=True,
       ulke=["türkiye"], sehir=["istanbul"], yas="orta", evli=True, cocuk=True,
       hint="SİHA'ların mimarı, Bayraktar"),
    _e(isim="İlber Ortaylı", tam="İlber Ortaylı", cinsiyet="e", turk=True, yazar=True,
       tarihsel=True, ulke=["türkiye"], gorunum=["gözlüklü", "sakallı"], yas="yaşlı", evli=False, cocuk=True,
       hint="Ünlü tarihçi, gözlüklü ve sakallı"),
    _e(isim="Naim Süleymanoğlu", tam="Naim Süleymanoğlu", cinsiyet="e", turk=True, hayatta=False,
       sporcu=True, spor=["halter"], ulke=["bulgaristan", "türkiye"], gorunum=["kısa"],
       yas="yaşlı", evli=True, cocuk=True, hint="Cep Herkülü halterci"),
    _e(isim="Arda Güler", tam="Arda Güler", cinsiyet="e", turk=True, sporcu=True,
       spor=["futbol"], kulup=["real madrid"], ulke=["türkiye"], sehir=["ankara"], yas="genç",
       evli=False, cocuk=False, hint="Real Madrid'de oynayan genç"),
    _e(isim="Sabiha Gökçen", tam="Sabiha Gökçen", cinsiyet="k", turk=True, hayatta=False,
       asker=True, ulke=["türkiye"], yas="yaşlı", evli=True, cocuk=True,
       hint="İlk kadın savaş pilotu"),
    _e(isim="Nasreddin Hoca", tam="Nasreddin Hoca", cinsiyet="e", turk=True, hayatta=False,
       komedyen=True, tarihsel=True, ulke=["türkiye"], sehir=["akşehir"],
       gorunum=["sakallı", "uzun"], yas="orta", evli=True, cocuk=None,
       hint="Eşeğe ters binen mizahçı, ak sakallı"),
    _e(isim="Keloğlan", tam="Keloğlan", cinsiyet="e", turk=True, hayali=True, insan=True,
       ulke=["türkiye"], gorunum=["kel", "dazlak"], yas="genç", evli=False, cocuk=False,
       hint="Tepesi kel masal kahramanı"),
    _e(isim="Albert Einstein", tam="Albert Einstein", cinsiyet="e", turk=False, hayatta=False,
       bilim=True, ulke=["almanya", "amerika"], gorunum=["sakallı", "bıyıklı", "dağınık"],
       yas="yaşlı", evli=True, cocuk=True, hint="Görecelilik kuramının babası"),
    _e(isim="Pablo Picasso", tam="Pablo Picasso", cinsiyet="e", turk=False, hayatta=False,
       ressam=True, ulke=["ispanya"], gorunum=["kel"], yas="yaşlı", evli=True, cocuk=True,
       hint="Küpizm akımının ressamı"),
    _e(isim="Frida Kahlo", tam="Frida Kahlo", cinsiyet="k", turk=False, hayatta=False,
       ressam=True, ulke=["meksika"], gorunum=["esmer", "bıyıklı"], yas="orta", evli=True,
       cocuk=False, hint="Kaşlı Meksikalı ressam"),
    _e(isim="Elvis Presley", tam="Elvis Presley", cinsiyet="e", turk=False, hayatta=False,
       sarkici=True, turler=["rock", "rock and roll"], ulke=["amerika"], gorunum=["esmer"],
       yas="orta", evli=True, cocuk=True, hint="Rock'n roll'un kralı"),
    _e(isim="Marilyn Monroe", tam="Marilyn Monroe", cinsiyet="k", turk=False, hayatta=False,
       aktor=True, ulke=["amerika"], gorunum=["sarışın"], yas="genç", evli=True, cocuk=False,
       hint="Sarışın sinema efsanesi"),
    _e(isim="Cristiano Ronaldo", tam="Cristiano Ronaldo", cinsiyet="e", turk=False, sporcu=True,
       spor=["futbol"], kulup=["al nasr", "real madrid"], ulke=["portekiz"], yas="orta",
       evli=True, cocuk=True, hint="Portekizli golcü, CR7"),
    _e(isim="Lionel Messi", tam="Lionel Messi", cinsiyet="e", turk=False, sporcu=True,
       spor=["futbol"], kulup=["barça", "ilecci", "psg"], ulke=["arjantin"],
       gorunum=["sakallı", "kısa"], yas="orta", evli=True, cocuk=True,
       hint="Arjantinli ceviz, 8 Altın Top"),
    _e(isim="Sherlock Holmes", tam="Sherlock Holmes", cinsiyet="e", turk=False, hayali=True,
       ulke=["ingiltere"], sehir=["londra"], yas="orta", evli=False, cocuk=False,
       hint="Londralı, boru ve kelebekli dedektif"),
    _e(isim="Mickey Mouse", tam="Mickey Mouse", cinsiyet="e", turk=False, insan=False,
       hayali=True, hayvan=True, hayvan_turu=["fare"], ulke=["amerika"], yas="orta", evli=False,
       cocuk=False, hint="Disney'in siyah kulaklı faresi"),
    _e(isim="Garfield", tam="Garfield", cinsiyet="e", turk=False, insan=False, hayali=True,
       hayvan=True, hayvan_turu=["kedi"], ulke=["amerika"], yas="orta", evli=False, cocuk=False,
       hint="Lazanya sevdalısı turuncu kedi"),
    _e(isim="Dumbledore", tam="Albus Dumbledore", cinsiyet="e", turk=False, hayali=True,
       buyucu=True, ulke=["ingiltere"], gorunum=["uzun", "sakallı"], yas="yaşlı", evli=False,
       cocuk=False, hint="Hogwarts'ın beyaz sakallı büyücüsü"),
    _e(isim="Harry Potter", tam="Harry Potter", cinsiyet="e", turk=False, hayali=True,
       buyucu=True, ulke=["ingiltere"], gorunum=["gözlüklü"], yas="genç", evli=True, cocuk=True,
       hint="Yara izli, gözlüklü genç büyücü"),
    _e(isim="Charlie Chaplin", tam="Charlie Chaplin", cinsiyet="e", turk=False, hayatta=False,
       aktor=True, komedyen=True, tarihsel=True, ulke=["ingiltere", "amerika"],
       gorunum=["bıyıklı"], yas="yaşlı", evli=True, cocuk=True,
       hint="Şarlo, melon şapkalı sessiz film ustası"),
    _e(isim="Osman Gazi", tam="Osman Gazi", cinsiyet="e", turk=True, hayatta=False,
       politikaci=True, asker=True, tarihsel=True, ulke=["türkiye"], yas="yaşlı", evli=True,
       cocuk=True, hint="Osmanlı Devleti'nin kurucusu"),
    _e(isim="Kanuni Sultan Süleyman", tam="Kanuni Sultan Süleyman", cinsiyet="e", turk=True,
       hayatta=False, politikaci=True, asker=True, tarihsel=True, yazar=True,
       ulke=["türkiye"], yas="yaşlı", evli=True, cocuk=True,
       hint="Devletin en uzun tahta kalan padişahı"),
    _e(isim="Yunus Emre", tam="Yunus Emre", cinsiyet="e", turk=True, hayatta=False, yazar=True,
       tarihsel=True, ulke=["türkiye"], yas="yaşlı", evli=None, cocuk=None,
       hint="'Sevelim sevilelim' diyen halk şairi"),
    _e(isim="İbrahim Tatlıses", tam="İbrahim Tatlıses", cinsiyet="e", turk=True, sarkici=True,
       turler=["arabesk", "halk"], ulke=["türkiye"], gorunum=["bıyıklı"], yas="yaşlı", evli=True, cocuk=True,
       hint="Arabesk'in ve halk türküsünün kralı"),
    _e(isim="Ajda Pekkan", tam="Ajda Pekkan", cinsiyet="k", turk=True, sarkici=True,
       turler=["pop"], ulke=["türkiye"], yas="yaşlı", evli=False, cocuk=False,
       hint="Süperstar"),
    _e(isim="Mahmut Tuncer", tam="Mahmut Tuncer", cinsiyet="e", turk=True, sarkici=True,
       turler=["halk"], ulke=["türkiye"], gorunum=["bıyıklı"], yas="orta", evli=True, cocuk=True,
       hint="Türkücü, 'Gafiye' sistemin babası"),
    _e(isim="Merih Demiral", tam="Merih Demiral", cinsiyet="e", turk=True, sporcu=True,
       spor=["futbol"], kulup=["al nasr"], ulke=["türkiye"], yas="genç", evli=False,
       cocuk=False, hint="Bozkurt stoper, milli futbolcu"),
    _e(isim="Pikachu", tam="Pikachu", cinsiyet="e", turk=False, insan=False, hayali=True,
       hayvan=True, hayvan_turu=["fare"], ulke=["japonya"], yas="genç", evli=False, cocuk=False,
       hint="Sarı, şimşek saçan Pokemon"),
    _e(isim="Bülent Ecevit", tam="Bülent Ecevit", cinsiyet="e", turk=True, hayatta=False,
       politikaci=True, yazar=True, ulke=["türkiye"], yas="yaşlı", evli=True, cocuk=True,
       hint="Karaoğlan, eski başbakan"),
    _e(isim="Cem Karaca", tam="Cem Karaca", cinsiyet="e", turk=True, hayatta=False,
       sarkici=True, turler=["rock", "anadolu rock"], ulke=["türkiye"], gorunum=["uzun saç"],
       yas="orta", evli=True, cocuk=True, hint="Anadolu rock'un unutulmaz sesi"),
    _e(isim="Süpermen", tam="Superman", cinsiyet="e", turk=False, hayali=True,
       ulke=["amerika"], gorunum=["esmer", "uzun"], yas="orta", evli=False, cocuk=False,
       hint="Kriptolu, pelerinli çizgi roman süper kahramanı"),
    _e(isim="Batman", tam="Batman", cinsiyet="e", turk=False, hayali=True,
       ulke=["amerika"], gorunum=["esmer"], yas="orta", evli=False, cocuk=False,
       hint="Yarasa kostümlü karanlık şövalye, çizgi roman kahramanı"),
    _e(isim="Walter White", tam="Walter White", cinsiyet="e", turk=False, hayali=True,
       aktor=True, ulke=["amerika"], gorunum=["kel", "sakallı"], yas="yaşlı", evli=True,
       cocuk=True, hint="Breaking Bad dizisinin kel kimyager öğretmeni"),
    _e(isim="Aziz Nesin", tam="Aziz Nesin", cinsiyet="e", turk=True, hayatta=False,
       yazar=True, komedyen=True, ulke=["türkiye"], gorunum=["bıyıklı"], yas="yaşlı",
       evli=True, cocuk=True, hint="Zübük romanının usta mizah yazarı"),
    _e(isim="Sıla", tam="Sıla Gençoğlu", cinsiyet="k", turk=True, sarkici=True,
       turler=["pop"], ulke=["türkiye"], sehir=["denizli"], gorunum=["esmer"], yas="genç",
       evli=False, cocuk=False, hint="Türk popunun güçlü sesi, Denizlili"),
    _e(isim="Süleyman Soylu", tam="Süleyman Soylu", cinsiyet="e", turk=True,
       politikaci=True, ulke=["türkiye"], sehir=["istanbul"], yas="orta", evli=True,
       cocuk=True, hint="Eski İçişleri Bakanı"),
    _e(isim="Neymar", tam="Neymar da Silva Santos Júnior", cinsiyet="e", turk=False,
       sporcu=True, spor=["futbol"], kulup=["psg", "al hilal"], ulke=["brezilya"],
       gorunum=["kısa"], yas="genç", evli=False, cocuk=True, hint="Brezilyalı bohem futbolcu"),
]


_KAT_SON = []  # son turda seçilen ana kategorilerin geçmişi (çeşitlilik için)


def _ana_kategori(e):
    if e["hayvan"]:
        return "hayvan"
    if e["buyucu"]:
        return "buyucu"
    if e["sarkici"]:
        return "sarkici"
    if e["sporcu"]:
        return "sporcu"
    if e["aktor"] or e["komedyen"]:
        return "komedyen" if e["komedyen"] else "aktor"
    if e["politikaci"]:
        return "politikaci"
    if e["bilim"]:
        return "bilim"
    if e["ressam"]:
        return "ressam"
    if e["yazar"]:
        return "yazar"
    if e["asker"]:
        return "asker"
    return "diger"


def random_entity():
    global _KAT_SON
    kategoriler = ["hayvan", "buyucu", "sarkici", "sporcu", "komedyen", "aktor",
                   "politikaci", "bilim", "ressam", "yazar", "asker", "diger"]
    # Son 2 turda gelen kategorileri mümkün olduğunca bu turda engelle,
    # böylece art arda benzer (aynı tür) kimlikler tekrar etmez.
    yasak = set(_KAT_SON[-2:])
    adaylar = [e for e in ENTITIES if _ana_kategori(e) not in yasak] or ENTITIES
    e = random.choice(adaylar)
    _KAT_SON.append(_ana_kategori(e))
    _KAT_SON = _KAT_SON[-10:]
    return e


def fact_questions(e):
    qs = []
    qs.append(("Ben erkek miyim?", e["cinsiyet"] == "e"))
    qs.append(("Ben kadın mıyım?", e["cinsiyet"] == "k"))
    qs.append(("Ben Türk müyüm?", e["turk"] == True))
    qs.append(("Ben yabancı mıyım?", e["turk"] == False))
    qs.append(("Ben yaşıyor muyum?", e["hayatta"] == True))
    qs.append(("Ben oyuncu muyum?", e["aktor"] == True))
    qs.append(("Ben şarkıcı mıyım?", e["sarkici"] == True))
    qs.append(("Ben politikacı mıyım?", e["politikaci"] == True))
    qs.append(("Ben bilim insanı mıyım?", e["bilim"] == True))
    qs.append(("Ben yazar mıyım?", e["yazar"] == True))
    qs.append(("Ben ressam mıyım?", e["ressam"] == True))
    qs.append(("Ben komedyen miyim?", e["komedyen"] == True))
    qs.append(("Ben manken miyim?", e["model"] == True))
    qs.append(("Ben dansçı mıyım?", e["dansci"] == True))
    qs.append(("Ben asker miyim?", e["asker"] == True))
    qs.append(("Ben büyücü müyüm?", e["buyucu"] == True))
    qs.append(("Ben kraliyetten miyim?", e["kraliyet"] == True))
    qs.append(("Ben hayali bir karakter miyim?", e["hayali"] == True))
    qs.append(("Ben hayvan mıyım?", e["hayvan"] == True))
    qs.append(("Ben insan mıyım?", e["insan"] == True))
    qs.append(("Ben genç miyim?", e["yas"] == "genç"))
    qs.append(("Ben yaşlı mıyım?", e["yas"] == "yaşlı"))
    if e["evli"] is not None:
        qs.append(("Ben evli miyim?", e["evli"] is True))
        qs.append(("Ben bekar mıyım?", e["evli"] is False))
    if e["cocuk"] is not None:
        qs.append(("Benim çocuğum var mı?", e["cocuk"] is True))
    qs.append(("Ben gözlüklü müyüm?", "gözlüklü" in e["gorunum"]))
    qs.append(("Ben sarışın mıyım?", "sarışın" in e["gorunum"]))
    qs.append(("Ben esmer miyim?", "esmer" in e["gorunum"]))
    qs.append(("Ben bıyıklı mıyım?", "bıyıklı" in e["gorunum"]))
    qs.append(("Ben sakallı mıyım?", "sakallı" in e["gorunum"]))
    qs.append(("Ben kel miyim?", "kel" in e["gorunum"]))
    qs.append(("Ben uzun boylu muyum?", "uzun" in e["gorunum"]))
    qs.append(("Ben kısa boylu muyum?", "kısa" in e["gorunum"]))
    qs.append(("Ben futbolcu muyum?", "futbol" in e["spor"]))
    qs.append(("Ben basketbolcu muyum?", "basketbol" in e["spor"]))
    qs.append(("Ben halterci miyim?", "halter" in e["spor"]))
    for c in ("türkiye", "amerika", "ingiltere", "almanya", "meksika", "arjantin",
              "portekiz", "belçika", "italya", "ispanya", "japonya", "bulgaristan"):
        qs.append(("Ben %s'lı mıyım?" % c, c in e["ulke"]))
    trues = [q for q in qs if q[1] is True]
    falses = [q for q in qs if q[1] is False]
    random.shuffle(trues)
    random.shuffle(falses)
    return (trues[:10] + falses[:10])


def full_name(e):
    return e.get("tam") or e["isim"]


BOOLQ = [
    (("erkek", "bayan değil"), "cinsiyet", "e"),
    (("kadın", "bayan", "hanım", "kız mısın"), "cinsiyet", "k"),
    (("yaşıyor", "hayatta", "canlı", "yaşayan", "hayattasın"), "hayatta", True),
    (("ölü", "öldü", "vefat", "rahmetli", "hayatı sonlandı"), "hayatta", False),
    (("türk", "türkiye'den", "anadolu'dan"), "turk", True),
    (("yabancı", "başka ülkeden"), "turk", False),
    (("oyuncu", "aktör", "aktris", "film yıldızı", "dizi oyuncusu"), "aktor", True),
    (("şarkıcı", "vokal", "popçu", "sanatçı", "şarkı söylüyormus", "müzisyen", "bestekar", "söz yazarı"), "sarkici", True),
    (("politikacı", "siyasetçi", "başbakan", "cumhurbaşkanı", "milletvekili", "siyaset", "bürokrat", "bakan"), "politikaci", True),
    (("bilim insanı", "bilim adamı", "profesör", "nobel", "araştırmacı", "mucit", "fizikçi", "kimyager", "icat"), "bilim", True),
    (("bilge",), "bilim", True),
    (("yazar", "şair", "kitap yazıyormus", "roman", "edebiyatçı", "denemeci", "oyun yazarı"), "yazar", True),
    (("ressam", "resim yapıyormus", "tablo", "tuval"), "ressam", True),
    (("komedyen", "komedi", "espri yapıyormus", "stand up", "güldürü"), "komedyen", True),
    (("manken", "model", "podyum", "modellik"), "model", True),
    (("dansçı", "dans ediyormus", "balet"), "dansci", True),
    (("asker", "komutan", "mareşal", "general", "subay", "ordusun"), "asker", True),
    (("kral", "kraliçe", "prens", "prenses", "taht", "kraliyet"), "kraliyet", True),
    (("büyücü", "sihirbaz", "sihir", "asap", "büyülü"), "buyucu", True),
    (("çizgi", "animasyon", "hayali", "masal", "kurgusal", "karakter", "kurgu", "hikaye kahramanı", "çizgi roman"), "hayali", True),
    (("hayvan", "hayvansın"), "hayvan", True),
    (("tarihsel", "tarihi", "geçmişten", "eski çağlardan", "tarih kitabında"), "tarihsel", True),
    (("insan", "gerçek biri", "gerçek insan"), "insan", True),
    (("evli", "eşin var"), "evli", True),
    (("bekar", "evli değil"), "evli", False),
    (("çocuğ", "evladın var", "çocuğun mu"), "cocuk", True),
]


CATS = [
    dict(attr="ulke", map={
        "türk": "türkiye", "türkiye'den": "türkiye", "türkiyeli": "türkiye",
        "amerikalı": "amerika", "amerika": "amerika",
        "ingiliz": "ingiltere", "ingiltere": "ingiltere",
        "alman": "almanya", "alemanyalı": "almanya", "almanya": "almanya",
        "meksikalı": "meksika", "meksika": "meksika",
        "arjantinli": "arjantin", "arjantin": "arjantin",
        "portekizli": "portekiz", "portekiz": "portekiz",
        "belçikalı": "belçika", "belçika": "belçika",
        "isviçreli": "isviçre", "isviçre": "isviçre",
        "fransız": "fransa", "fransa": "fransa",
        "italyan": "italya", "italya": "italya",
        "ispan": "ispanya", "ispanya": "ispanya",
        "japon": "japonya", "japonya": "japonya",
        "rus": "rusya", "rusya": "rusya",
        "hollandalı": "hollanda", "hollanda": "hollanda",
        "bulgar": "bulgaristan", "bulgaristan": "bulgaristan",
        "çinli": "çin", "çin": "çin",
        "brezilyalı": "brezilya", "brezilya": "brezilya",
        "mısır": "mısır",
        "hindistan": "hindistan",
        "yunan": "yunanistan", "yunanistan": "yunanistan",
    }),
    dict(attr="sehir", map={
        "istanbul": "istanbul", "istanbullu": "istanbul",
        "ankara": "ankara", "ankaralı": "ankara",
        "izmir": "izmir", "izmirli": "izmir",
        "bursa": "bursa", "bursalı": "bursa",
        "adana": "adana", "adanalı": "adana",
        "trabzon": "trabzon", "trabzonlu": "trabzon",
        "samsun": "samsun", "samsunlu": "samsun",
        "konya": "konya", "konyalı": "konya",
        "mardin": "mardin", "mardinli": "mardin",
        "londra": "londra", "londralı": "londra",
        "paris": "paris",
        "akşehir": "akşehir", "akşehirli": "akşehir",
        "bruksel": "bruksel", "brüksel": "bruksel",
    }),
    dict(attr="spor", map={
        "futbolcu": "futbol", "futbol": "futbol",
        "basketbolcu": "basketbol", "basketbol": "basketbol",
        "halterci": "halter", "halter": "halter",
        "güreşçi": "güreş", "güreş": "güreş",
        "boksör": "boks", "boks": "boks",
        "tenisçi": "tenis", "tenis": "tenis",
        "voleybolcu": "voleybol", "voleybol": "voleybol",
        "atlet": "atletizm", "atletizm": "atletizm",
        "yüzücü": "yüzme", "yüzme": "yüzme",
        "koşucu": "koşu", "koşu": "koşu",
        "sprinter": "koşu",
        "maratoncu": "koşu",
    }),
    dict(attr="turler", map={
        "pop": "pop", "popçu": "pop",
        "rock": "rock", "rock and roll": "rock",
        "arabesk": "arabesk",
        "halk müziği": "halk", "türkü": "halk", "türkücü": "halk",
        "tasavvuf": "tasavvuf",
        "klasik": "klasik",
        "rap": "rap",
        "caz": "caz",
        "folk": "folk",
        "anadolu rock": "anadolu rock",
        "metal": "metal",
        "elektronik": "elektronik",
    }),
    dict(attr="kulup", map={
        "real madrid": "real madrid", "madrid": "real madrid",
        "barça": "barça", "barcelona": "barça",
        "ilecci": "ilecci", "ilk ligdiki": "ilecci",
        "psg": "psg", "paris saint germain": "psg",
        "al nasr": "al nasr", "nasr": "al nasr",
        "fenerbahçe": "fenerbahçe", "fener": "fenerbahçe",
        "galatasaray": "galatasaray", "gs": "galatasaray",
        "beşiktaş": "beşiktaş", "bjk": "beşiktaş",
        "trabzonspor": "trabzonspor",
        "liverpool": "liverpool",
        "manchester": "manchester",
        "bayern": "bayern",
    }),
    dict(attr="gorunum", map={
        "sarışın": "sarışın", "sarı saçlı": "sarışın",
        "esmer": "esmer", "esmerim": "esmer",
        "bıyıklı": "bıyıklı", "bıyık": "bıyıklı",
        "sakallı": "sakallı", "sakal": "sakallı",
        "gözlüklü": "gözlüklü", "gözlük": "gözlüklü",
        "kel": "kel", "dazlak": "kel", "saçsız": "kel",
        "uzun boy": "uzun", "uzun boylu": "uzun", "uzunum": "uzun",
        "kısa boylu": "kısa", "kısa boy": "kısa", "kısayım": "kısa",
        "şişman": "şişman", "zayıf": "zayıf",
        "kambur": "kambur",
        "mavi gözlü": "mavi gözlü", "mavi göz": "mavi gözlü",
        "yeşil gözlü": "yeşil gözlü", "kahverengi gözlü": "kahverengi gözlü",
        "uzun saç": "uzun saç", "dağınık saç": "dağınık",
    }),
    dict(attr="hayvan_turu", map={
        "fare": "fare", "fare mısın": "fare",
        "kedi": "kedi", "kedi misin": "kedi",
        "köpek": "köpek", "köpeksin": "köpek",
        "kuş": "kuş",
        "at": "at",
        "panda": "panda",
        "tilki": "tilki",
        "ayı": "ayı",
        "kaplan": "kaplan",
        "domuz": "domuz",
        "maymun": "maymun",
        "yılan": "yılan",
    }),
    dict(attr="yas", map={
        "genç": "genç", "gençsin": "genç", "küçüksün": "genç", "yaşın genç": "genç",
        "yaşlı": "yaşlı", "yaşlısın": "yaşlı", "ihtiyar": "yaşlı",
        "orta yaşlı": "orta", "ortalarda": "orta",
    }),
]


UNKNOWN_RESPONSES = [
    "Hmm, o bilgim yok :) Ama 'Türk müsün?', 'Şarkıcı mısın?', 'Sporcu musun?' diye sorablirsin",
    "Kafamı karıştırdın :D Daha net sor: 'Erkek misin?', 'Gözlüklü müsün?', 'Evli misin?'",
    "Bilmiyorum :( Ama ülkesini, şehrini, saç rengini sorabilirsin mesela",
    "O kadar derine inmeyelim :) 'Ünlü müsün?', 'Futbolcu musun?', 'Genç misin?' der misin?",
    "Öyle bir bilgi saklı :) Yine de dene: 'Sarışın mısın?', 'Arjantinli misin?', 'Kedi misin?'",
]


def _val(e, attr, expected):
    v = e.get(attr)
    if isinstance(expected, tuple):
        for x in expected:
            r = _val(e, attr, x)
            if r is not None:
                return r
        return None
    if v is None:
        return None
    if isinstance(v, list):
        return expected in v
    return v == expected


def answer_question(e, q):
    qn = nstr(q)
    neg = ("değil" in qn) or ("degis" in qn and "değil" in qn)
    results = []
    for kws, attr, want in BOOLQ:
        if any(nstr(k) in qn for k in kws):
            r = _val(e, attr, want)
            if r is None:
                return None
            results.append(r)
    for cat in CATS:
        hit = None
        for kw, canon in cat["map"].items():
            if nstr(kw) in qn:
                hit = canon
                break
        if hit is not None:
            r = _val(e, cat["attr"], hit)
            if r is None:
                return None
            results.append(r)
    if any(w in qn for w in (nstr("ünlü"), nstr("meşhur"), nstr("tanınmış"))):
        results.append(True)
    if not results:
        return None
    ans = all(results)
    if neg:
        ans = not ans
    return ans


def guess_hit(e, q):
    toks = set(nstr(q).split())
    for a in (e["isim"], e["tam"]):
        for t in nstr(a).split():
            if t in toks:
                return True
    return False


def false_guess(e, q):
    toks = set(nstr(q).split())
    for other in ENTITIES:
        if other is e:
            continue
        if guess_hit(other, q):
            return other["isim"]
    return None


def question_like(q):
    qn = nstr(q)
    surekli = ("misin", "mısın", "musun", "müsün", "misiniz", "mısınız", "musunuz", "müsünüz")
    return qn.endswith(("mi", "mı", "mu", "mü")) or any(s in qn for s in surekli)