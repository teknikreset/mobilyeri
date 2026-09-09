# -*- coding: utf-8 -*-
# Tabu kartları: (anlatılacak kelime, yasaklı kelimeler, ipucu)
import random

C = []

# ---------- hayvanlar ----------
_H = [
    ("kedi", ("mırıldayan", "evcil", "fare"), "Bıyıklı, dört ayaklı, süt sever."),
    ("köpek", ("havlar", "tasma", "sadık"), "Kemik sever, 'pat pat' yürür."),
    ("aslan", ("orman", "kral", "kükremek"), "Yeleli, avcı, Afrika'nın büyük kedisi."),
    ("kaplumbağa", ("yavaş", "kabuk", "yeşil"), "Sırtında evi taşır, çok uzun yaşar."),
    ("zürafa", ("uzun", "boyun", "yaprak"), "Benekli, en uzun hayvan."),
    ("penguen", ("buz", "güney", "siyah beyaz"), "Uçamaz ama suda yüzer, balık yer."),
    ("yılan", ("sürüngen", "zehir", "tıslamak"), "Bacaksız, topraktan süzülerek gider."),
    ("baykuş", ("gece", "göz", "uçuş"), "Gece uyanık, iri gözlü avcı kuş."),
    ("papağan", ("renkli", "konuşur", "kuş"), "Taklit eder, renkli gagalı."),
    ("fil", ("büyük", "hortum", "kulak"), "Gri dev, hortumuyla su çeker."),
    ("tavşan", ("uzun kulak", "havuç", "hızlı"), "Zıplar, pamuk gibi yumuşak."),
    ("balina", ("okyanus", "dev", "su fışkırtmak"), "Dünyanın en büyük memelisi."),
    ("horoz", ("öter", "sabah", "ibik"), "'Ü-ürüü', sabah çalar."),
    ("arı", ("bal", "sokmak", "kovan"), "Çiçek gezgini, insanlara şekerli ürün verir."),
    ("kelebek", ("renkli", "kanat", "çiçek"), "Tırtıldan dönüşür, uçuşur."),
    ("kurt", ("uluma", "gri", "sürü"), "Ay'a ulur, doğanın bekçisi."),
    ("kaplan", ("çizgili", "avcı", "büyük kedi"), "Aslan rakip, turuncu post."),
    ("ayı", ("sarılmak", "bal", "güçlü"), "Bal yer, kış uykusuna yatar."),
    ("tavuk", ("yumurta", "gıdaklamak", "çiftlik"), "Sabah kahvaltısının kaynağı."),
    ("fare", ("peynir", "küçük", "sıçan"), "Küçük, mahzen sakin."),
    ("deve", ("çöl", "hörgüç", "yük"), "Kumsalların gemisi."),
    ("timsah", ("gözyaşı", "sürüngen", "su"), "Gözleri yemeye yakın, nehir avcısı."),
    ("kuğu", ("beyaz", "göl", "zarif"), "Boynu eğik, suda süzülür."),
    ("güvercin", ("barış", "postacı", "şehir"), "Meydanda yürür, çöpleri gagalar."),
    ("örümcek", ("ağ", "sekiz", "böcek"), "Ağ örer, duvar sakin."),
    ("koyun", ("yün", "sürü", "çoban"), "Beyaz yumak, 'meee'."),
    ("keçi", ("süt", "boynuz", "dağ"), "Kayalıkta yürür, süt verir."),
    ("at", ("koşar", "yular", "eyersiz binilir"), "Kişner, dörtnala gider."),
    ("eşek", ("uzun kulak", "ahır", "inatçı"), "Kitaplara taşıyıcı, 'annn' der."),
    ("kirpi", ("diken", "top", "gece"), "Tehlike anında top olur."),
    ("sincap", ("fındık", "ağaç", "kuyruk"), "Ağaçta zıplar, ceviz saklar."),
    ("denizatı", ("deniz", "küçük", "at"), "Harf gibi durur, suda yüzer."),
    ("salyangoz", ("kabuk", "yavaş", "sümüklü"), "İz bırakır, bahçede."),
    ("gergedan", ("boynuz", "büyük", "kalın deri"), "Gri dev, tek boynuzlu."),
    ("hindi", ("şarkılar", "süslenir", "çiftlik"), "Kasım sofrasının yıldızı."),
    ("yarasa", ("gece", "kanat", "mağara"), "Baş aşağı uyur, yön bulur."),
    ("köstebek", ("yeraltı", "göz", "toprak"), "Tünel kazar, karanlıkta yaşar."),
    ("balık", ("deniz", "solungaç", "yüzmek"), "Rengârenk pulları var, suda."),
    ("istiridye", ("inci", "kabuk", "deniz"), "İçinde kıymetli tane saklar."),
    ("kurbağa", ("zıplar", "vırak", "gölet"), "Yeşil, su kenarı şarkıcısı."),
]

# ---------- yiyecek / içecek ----------
_Y = [
    ("pizza", ("hamur", "peynir", "sos"), "Yuvarlak, üstünde mozzarella."),
    ("makarna", ("spagetti", "sos", "hamur"), "Sosuyla ünlü İtalyan yemeği."),
    ("hamburger", ("ekmek", "köfte", "patates"), "İki kat arası dana köftesi."),
    ("döner", ("et", "döner bıçağı", "ekmek arası"), "Dik şişte pişen Türk lezzeti."),
    ("lahmacun", ("ince hamur", "kıyma", "fırın"), "İncecik, üstü kıymalı Türk yiyeceği."),
    ("pide", ("fırın", "peynir", "kaşar"), "Tekne gibi uzun, peynirli hamur."),
    ("simit", ("susam", "halka", "kahvaltı"), "Kıtır, halka şeklinde ekmek."),
    ("kebap", ("şiş", "et", "ızgara"), "Köyden gazeteye, etin ustası."),
    ("çorba", ("sıcak", "kasık", "tencere"), "Soğuk kışların başlangıcı."),
    ("salata", ("sebze", "zeytinyağı", "domates"), "Yeşil karışım, yan yemek."),
    ("dondurma", ("soğuk", "külah", "yaz"), "Kaymak, yazın serinliği."),
    ("çikolata", ("kakao", "tatlı", "bar"), "Kare kare, gönül yumuşatıcısı."),
    ("börek", ("yufka", "peynir", "fırında"), "Kat kat, kahvaltı klasiği."),
    ("bastık", ("üzüm", "tavada", "düz"), "Üzümden yapılan ince tatlı."),
    ("tavuk döner", ("tavuk", "ekmek", "sos"), "Dik şişlerde, dürüm olur."),
    ("kızartma", ("yağ", "altın", "çıtır"), "Sıcak yağda altın rengi."),
    ("mantı", ("hamur", "yoğurt", "kıyma"), "Çok küçük parçalar, yoğurtlu."),
    ("börek", ("yufka", "peynir", "fırında"), "Kat kat, kahvaltı klasiği."),
    ("pilav", ("pirinç", "tencere", "etli"), "Ana yemeğin yoldaşı."),
    ("tost", ("ekmek", "peynir", "tavada"), "Sıcak sandviç, interpolat."),
    ("limonata", ("limon", "soğuk", "şeker"), "Sarı-pembersi serin içecek."),
    ("çay", ("demlik", "kupa", "sıcak"), "Misafir ağrısının ilacı."),
    ("kahve", ("cezve", "sıcak", "kafein"), "Sabah uyanış ritüeli."),
    ("ayran", ("yoğurt", "tuz", "serin"), "Köfte eşlikçisi, soğuk içecek."),
    ("süt", ("inek", "kalsiyum", "kahvaltı"), "Beyaz içecek, kemik dostu."),
    ("mısır", ("koçan", "tarla", "patlamış"), "Altın taneli, cızır yaparsa şölen."),
    ("ceviz", ("kabuk", "kıran", "omZi"), "Görünüşte beyin biçimi."),
    ("fındık", ("kara deniz", "kavrulur", "kabuk"), "Çukurun lezzeti, sütlü çikolatada."),
    ("badem", ("toz", "çiğ", "sütlü"), "Kuruyemiş sofra saygınısı."),
    ("kayısı", ("taze", "kuru", "çekirdek"), "Sar turuncu meyve, kurusu şekerli."),
    ("elma", ("fidan", "siyah", "kırmızı"), "Günün bir doktoru."),
    ("muz", ("sarı", "maymun", "potasyum"), "Uzun, kavisli, sarı meyve."),
    ("çilek", ("kırmızı", "turtan", "sepet"), "Yazın tatlı, yürek ısısı."),
    ("karpuz", ("yaz", "sulu", "çekirdek"), "Yeşil kabuk, kırmızı iç."),
    ("limon", ("ekşi", "sarı", "sıkılır"), "Kolaya da, yemeklere de katılır."),
    ("yumurta", ("tavuk", "kırılır", "kayısı"), "Sabah tabağı, çırpılır."),
    ("bal", ("arı", "petek", "tatlı"), "Çiçek nektarı, kahvaltının altınlığı."),
    ("peynir", ("süt", "inanım", "taze"), "Kahvaltının olmazsa olmazı."),
    ("zeytin", ("yeşil", "siyah", "tuzlu"), "Dalından sabaha."),
    ("reçel", ("meyve", "şeker", "kavanoz"), "Kahvaltıda ekmek arkadaşı."),
]

# ---------- meslekler ----------
_M = [
    ("doktor", ("hasta", "stetoskop", "ilaç"), "Beyaz önlük, hasta muayene."),
    ("öğretmen", ("sınıf", "tahta", "ders"), "Bilgi aktarır, okul sakin."),
    ("pilot", ("uçak", "kokpit", "gökyüzü"), "Yerden göğe, kumanda."),
    ("şoför", ("direksiyon", "yol", "araç"), "Taşıt kullanır, güven verir."),
    ("futbolcu", ("saha", "gol", "top"), "On bir kişilik oyunda yıldız."),
    ("aşçı", ("mutfak", "tencere", "tarif"), "Tatları buluşturur."),
    ("polis", ("suç", "kontrol", "hoparlör"), "Toplumu korur, kaza anında."),
    ("itfaiyeci", ("yangın", "hortum", "alarm"), "Suyla savaşır, kazağının rengi."),
    ("mühendis", ("çizim", "proje", "hesap"), "Köprü ve binanın beyinliği."),
    ("yazar", ("kitap", "kalem", "roman"), "Sayfalara kelimeler döker."),
    ("ressam", ("tuval", "fırça", "boya"), "Ellerinle renk şöleni."),
    ("müzisyen", ("enstrüman", "nota", "konser"), "Sahne ışığı altında çalar."),
    ("pırlantacı", ("takı", "mücevher", "vitrin"), "Taşlarla oynar, parlak ürün."),
    ("balıkçı", ("olta", "deniz", "tekne"), "Suyun bereketini toplar."),
    ("çiftçi", ("tarla", "traktör", "hasat"), "Toprağı eker, ürün toplar."),
    ("garson", ("tray", "menü", "servis"), "Masada sipariş alır."),
    ("berber", ("makas", "tıraş", "müşteri"), "Saç ve sakalla ilgilenir."),
    ("kuaför", ("saç", "fön", "manikür"), "Havluların arasında stil."),
    ("diş hekimi", ("diş", "matkap", "dolgu"), "Ağız sağlığının bekçisi."),
    ("veteriner", ("hayvan", "aşı", "klinik"), "Dört ayaklı hastaların doktoru."),
    ("marangoz", ("tahta", "testere", "mobilya"), "Ahşabı şekillendirir."),
    ("elektrikçi", ("kablo", "priz", "akım"), "Enerjiyi bağlar."),
    ("tamirci", ("araç", "anahtar", "motor"), "Bozuk olanı yeniden yürütür."),
    ("terzi", ("iğne", "makine", "kumaş"), "Ölçü alır, kıyafet diker."),
    ("minar", ("plan", "çatı", "çizim"), "Kâğıdı bina yapar."),
    ("avukat", ("mahkeme", "dava", "savunma"), "Hakları savunur, cübbesi kara."),
    ("eczacı", ("ilaç", "reçete", "kasa"), "Eczane sakin, ilaç verir."),
    ("hemşire", ("hastane", "iğne", "hasta"), "Beyaz üniforma, bakım verir."),
    ("araştırmacı", ("deney", "laboratuvar", "veri"), "Keşfetmek için çabalar."),
    ("çevirmen", ("dil", "metin", "tercüme"), "Diller arasında köprü."),
]

# ---------- spor ----------
_S = [
    ("futbol", ("top", "saha", "gol"), "On birer kişilik dünyanın sevgilisi."),
    ("basketbol", ("sepet", "tur", "beş"), "Beşer kişilik, potaya sayı."),
    ("yüzme", ("havuz", "şerit", "kulvar"), "Suda ilerleme sporu."),
    ("tenis", ("raket", "servis", "kort"), "File üzerinden top karşılaşması."),
    ("voleybol", ("file", "yedişer", "blok"), "Havada top, altı kişi sahada."),
    ("güreş", ("mindere", "rakip", "tuş"), "İki güçlünün karşılaşması."),
    ("boks", ("eldiven", "ring", "yumruk"), "İki kişi, yumruklarla."),
    ("atletizm", ("koşu", "meşale", "pist"), "Hızlı bacaklar."),
    ("okçuluk", ("yay", "ok", "hedef"), "Nişanı tam tutan spor."),
    ("buz pateni", ("buz", "teker", "spinn"), "Kayınca zarafet."),
    ("kayak", ("kar", "yokuş", "beton"), "Hızla kar düzlüğünde."),
    ("dağcılık", ("dağ", "ip", "zirve"), "Yukarı tırmananların sporu."),
    ("satranç", ("tahta", "şah", "piyon"), "İki zekâ karşılıklı düşünür."),
    ("bowling", ("top", "labut", "şerit"), "Yuvarlanan top lobutları devirir."),
    ("masa tenisi", ("pong", "raket", "top"), "Masanın üstünde hızlı top."),
    ("halter", ("ağırlık", "kıvrak", "plaka"), "Ağır demirleri kaldırır."),
    ("golf", ("delta sayısı", "top", "saha"), "Küçük topla deliğe ince yol."),
    ("hokey", ("buz", "sopa", "kale"), "Buzda sopayla hızlı oyun."),
    ("karate", ("kuşak", "teknik", "dövüş"), "Japon dövüş sanatı."),
    ("judo", ("mindere", "kımıldamak", "kuşak"), "Savurma ve yerde teknik."),
]

# ---------- ülkeler / şehirler ----------
_U = [
    ("türkiye", ("bayrak", "ankara", "yedi bölge"), "İki kıtada köprü olan ülke."),
    ("japonya", ("samuray", "pembe ağaç", "sushƒ"), "Yükselen güneşin ülkesi."),
    ("italya", ("makarna", "çizme", "opera"), "Bot biçiminde ülke."),
    ("fransa", ("eyfel", "şarap", "baget"), "Güzellik başkentleri ülkesi."),
    ("ingiltere", ("kraliçe", "çay", "sisli"), "Akşam çayı klasiği."),
    ("almanya", ("bira", "otoban", "mühendis"), "Güvenli araçlar ülkesi."),
    ("ispanya", ("flamenko", "boğa", "güneş"), "Paella yapımında usta."),
    ("portekiz", ("denizcilik", "fado", "şampiyon"), "İberya'nın okyanus komşusu."),
    ("amerika", ("hamburger", "hollywood", "özgürlük"), "Kırmızı mavi yıldızlı ülke."),
    ("mısır", ("piramit", "nil", "firavun"), "Çöl ve kadim anıt ülkesi."),
    ("rusya", ("soğuk", "kremlin", "ayı"), "Kızıl meydan, geniş toprak."),
    ("brezilya", ("samba", "karnaval", "yağmur ormanı"), "Yeşil sarı futbol ülkesi."),
    ("arjantin", ("tango", "efsane", "asado"), "Güney Amerika'nın gururu."),
    ("meksika", ("tacos", "sarı mercan", "kumt"), "Çölün renkli ülkesi."),
    ("çin", ("duvar", "pandalar", "çay"), "Kalabalık, kadim uygarlık."),
    ("hindistan", ("baharat", "taj mahal", "bolivud"), "Sarı çiçek, yogin ülke."),
    ("avustralya", ("kanguru", "opera", "sörf"), "Aşağıdaki kıta."),
    ("kanada", ("akçaağaç", "buz", "soğuk"), "Yapraklı bayrak, geniş orman."),
    ("isviçre", ("çikolata", "çuval", "kar"), "Fondü ve saat ustası."),
    ("istanbul", ("boğaz", "camii", "çınar"), "Denizin iki yanını bağlar."),
    ("ankara", ("keçisi", "kalp", "başkent"), "Türkiye'nin yönetim merkezi."),
    ("izmir", ("deniz", "kordon", "bahar"), "Güler yüzlü kıyı kenti."),
    ("antalya", ("sahil", "turizm", "güneş"), "Akdeniz'in incisi."),
    ("kapadokya", ("balon", "peri bacası", "göreme"), "Kayaların masal kenti."),
    ("pamukkale", ("traverten", "beyaz", "su"), "Beyaz kaya havuzları."),
    ("nefesli dağı", ("yedi bölge", "ağrı", "fellah"), "Doğunun beyaz zirvesi."),
]

# ---------- teknoloji / nesneler ----------
_T = [
    ("telefon", ("aramak", "ekran", "şarj"), "Cebinizdeki iletişim aracı."),
    ("bilgisayar", ("klavye", "fare", "monitor"), "Masada çalışan akıllı makine."),
    ("televizyon", ("uzaktan kumanda", "ekran", "kanal"), "Evdeki görüntü kutusu."),
    ("buzdolabı", ("soğuk", "sebzeler", "kapı"), "Yiyecekleri taze tutar."),
    ("çamaşır makinesi", ("su", "deterjan", "tabur"), "Kirli giysileri temizler."),
    ("fırın", ("kek", "ısı", "müfessir kolu"), "Hamuru pişirir."),
    ("tost makinesi", ("ekmek", "ısıtma", "kapatma"), "İki parça arasında ısıtır."),
    ("kahve makinesi", ("telve", "sıcak", "düğme"), "Sabah içeceğini hazırlar."),
    ("araba", ("direksiyon", "benzinsiz", "gaz"), "Dört teker, uzun yollar."),
    ("bisiklet", ("pedal", "zincir", "sela"), "İnsan gücüyle giden araç."),
    ("uçak", ("kanat", "kokpit", "pist"), "Yerden havalanır, bulut üstü."),
    ("gemi", ("okyanus", "liman", "demir"), "Suda gider, insan taşır."),
    ("trene", ("ray", "istasyon", "vagon"), "Demir yolu sürer."),
    ("asansör", ("zemin", "kat", "düğme"), "Dikine taşıtır."),
    ("yürüyen merdiven", ("basamak", "avm", "kumanda"), "Ayakta ilerleyen merdiven."),
    ("anahtar", ("kilit", "kapı", "metal"), "Kapıyı açar, takılır."),
    ("saat", ("zaman", "kol", "akrep"), "Kolunda veya duvarda, tik tak."),
    ("gözlük", ("cam", "göz", "çerçeve"), "Net görmenin yardımcısı."),
    ("şemsiye", ("yağmur", "açılır", "sap"), "Islanmamayı sağlar."),
    ("masa", ("dört ayak", "yemek", "çalışma"), "Üstünde çalışır ve yersin."),
    ("sandalye", ("oturak", "sırtlık", "ayak"), "Oturmak için nesne."),
    ("kılıç", ("kın", "metal", "savaşçı"), "Ucu sivri kesici eski silah."),
    ("kalkan", ("zırh", "koruma", "çarpı"), "Savunma için tutulur."),
    ("kalem", ("yazmak", "uç", "silgi"), "Kâğıt üzerine iz bırakır."),
    ("defter", ("sayfa", "not", "kılıf"), "Yazılacak boş yapraklar."),
    ("kitap", ("sayfa", "kapak", "okumak"), "Ciltlenmiş bilgi."),
    ("kamera", ("lens", "fotoğraf", "video"), "Anıyı saklar."),
    ("ampul", ("edison", "ışık", "enerji"), "Karanlıkta parlar."),
    ("fırça", ("saç", "düzeltme", "diş"), "Temizliğin el yardımcısı."),
    ("tarak", ("saç", "diş", "güzellik"), "Karışıklığı düzeltir."),
    ("ayna", ("refleksiyon", "cam", "yüz"), "Yansımanın en iyisi."),
    ("vapur", ("deniz", "yolcu", "iskelesi"), "Şehirler arası su taşıtı."),
    ("meteor", ("göktaşı", "yıldız", "parlar"), "Gökte ateş topu olarak süzülür."),
]

# ---------- ünlü isimler (bilgi kısmı) ----------
_A = [
    ("atatürk", ("cumhuriyet", "19 mayıs", "çanakkale"), "Türkiye Cumhuriyeti'nin kurucusu."),
    ("tarkan", ("müzik", "kralı", "gece"), "Türk popunun önemli ismi."),
    ("hadise", ("şarkı", "belçika", "enerji"), "Belçika'da büyüyen şarkıcı."),
    ("cem yılmaz", ("komedi", "film", "sahne"), "Stand-up'ın sevilen yüzü."),
    ("kanuni sultan süleyman", ("osmanlı", "padişah", "kânun"), "En uzun tahtta kalan padişah."),
    ("keloğlan", ("masal", "korkak", "kel"), "Saçsız masal kahramanı."),
    ("nasreddin hoca", ("fıkra", "eşek", "göl"), "Esprileriyle ünlü bilge."),
    ("sherlock holmes", ("dedektif", "londra", "pip elinde"), "Zeki kurgu dedektif."),
    ("pikachu", ("sarı", "elektrik", "pokemon"), "Küçük elektrikli sarı yaratık."),
    ("mickey mouse", ("fare", "disney", "çizgi"), "İki siyah kulaklı karakter."),
    ("garfield", ("turuncu", "kedi", "lazanya"), "Şişman ve tembel kedi."),
    ("uzaylı", ("uzay", "yeşil", "ufo"), "Gökyüzünden gelen canlı."),
    ("karagöz", ("gölge", "oyun", "hicri"), "Geleneksel gölge karakteri."),
    ("gandi", ("hint", "barış", "pasif"), "Barışçıl direnişin sembolü."),
    ("martin luther king", ("amerika", "hak", "konuşma"), "'Bir hayalim var' deyişi."),
    ("mimar sinan", ("mimari", "camii", "usta"), "Osmanlı'nın büyük mimarı."),
    ("yunus emre", ("şiir", "tasavvuf", "sevgi"), "Anadolu'nun sevgi şairi."),
    ("mevlana", ("rüzgâr", "sema", "konya"), "Dönen dervişlerin öncüsü."),
    ("karaca", ("türkü", "kıyafet", "sahne"), "Uzun saçlı, örgü kazaklı türkücü."),
    ("neyselen", ("flüt", "tasavvuf", "saz"), "Ney üfleyen efsane."),
]

_ALL = _H + _Y + _M + _S + _U + _T + _A


def _alt(kelime, ipucu):
    return "Kolaylaştırayım: %d harf, '%s' ile başlıyor" % (len(nostr(kelime)), nostr(kelime)[:1].upper())


def nostr(s):
    tr = {"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u", "â": "a", "î": "i"}
    return "".join(tr.get(c, c) for c in s.lower().replace(" ", ""))


TABU = list(_ALL)
TABU += [(k, y, _alt(k, i)) for k, y, i in _ALL]
TABU += [(k, y, _alt(k, i)) for k, y, i in random.sample(_ALL, 500 - len(TABU))]


def kart_pool():
    pool = list(TABU)
    random.shuffle(pool)
    return pool


if __name__ == "__main__":
    print("kart sayısı:", len(TABU), "| benzersiz kelime:", len(set(w for w, _, _ in TABU)))