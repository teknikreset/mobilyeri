# SoruBotu

Python ile yazılmış SoruBotu. Bot; soru yarışması, KimimBen, Tabu, kelime oyunu,
futbol ve günlük burç özelliklerini içerir.

## Gereksinimler

- Python 3.10 veya üzeri
- İnternet bağlantısı
- Botun bağlanacağı sunucuya erişim

Proje yalnızca Python standart kütüphanelerini kullandığı için harici `pip`
paketi gerektirmez.

## Windows'ta çalıştırma

```bash
python mobilyeri_sorubotu.py
```

## Linux/VPS'te çalıştırma

```bash
python3 mobilyeri_sorubotu.py
```

Uzun süre çalıştırmak için VPS üzerinde `systemd`, Docker veya benzeri bir
süreç yöneticisi kullanılması önerilir.

## Ortam değişkenleri

Varsayılan değerler kodda çalışır durumdadır. İsterseniz bunları ortam
değişkenleriyle değiştirebilirsiniz:

- `BOT_HOST`
- `BOT_PORT`
- `BOT_ORIGIN`
- `BOT_WS_PATH`
- `BOT_NICK`
- `BOT_GENDER`
- `BOT_FINGERPRINT`
- `BOT_SCREEN`
- `BOT_LOCATION`

Örnek:

```bash
BOT_NICK=SoruBotu python3 mobilyeri_sorubotu.py
```

## GitHub'a yükleme

```bash
git init
git add .
git commit -m "SoruBotu ilk sürüm"
git branch -M main
git remote add origin <GITHUB_REPO_URL>
git push -u origin main
```

> GitHub bir kod deposudur; tek başına sürekli çalışan Python bot sunucusu
> değildir. Botun 7/24 çalışması için GitHub'daki bu projeyi bir VPS veya
> sürekli çalışan bir worker servisine deploy etmeniz gerekir.

## Dosyalar

- `mobilyeri_sorubotu.py` — ana bot
- `sorular.py` — soru havuzu
- `kimimben.py` — KimimBen veri ve oyun mantığı
- `tabu.py` — Tabu kartları
- `futbol.py` — futbol takip özellikleri
- `burc.py` — günlük burç verisi

## GitHub Actions ile çalıştırma

Projede `.github/workflows/run-bot.yml` hazırdır. GitHub Actions, botu Ubuntu üzerinde
çalıştırır ve yaklaşık 5 saat 50 dakika sonra iş bittiğinde bir sonraki zamanlanmış
çalıştırmada yeniden başlatır.

### Kurulum

1. Projeyi GitHub'da **public repository** olarak oluşturun.
2. Bu klasördeki tüm dosyaları repository'ye yükleyin.
3. GitHub'da **Settings → Secrets and variables → Actions → New repository secret**
   bölümünden isterseniz aşağıdaki değerleri ekleyin:

   - `BOT_HOST`
   - `BOT_PORT`
   - `BOT_ORIGIN`
   - `BOT_WS_PATH`
   - `BOT_NICK`
   - `BOT_GENDER`
   - `BOT_FINGERPRINT`
   - `BOT_SCREEN`
   - `BOT_LOCATION`

   Değer eklemezseniz workflow dosyasında tanımlı varsayılanlar kullanılır.

4. **Actions → SoruBotu → Run workflow** ile elle başlatabilirsiniz.
5. Botun loglarını aynı Actions sayfasındaki çalışmadan görebilirsiniz.

> Not: GitHub Actions bir VPS değildir. Bu yöntem botu GitHub'ın Actions runner'ında
> çalıştırır; sürekli 7/24 sunucu garantisi vermez. GitHub'ın Actions kullanım ve
> otomatik çalıştırma kuralları değişebileceğinden, uzun süreli üretim kullanımı için
> VPS/worker servisi daha uygundur.
