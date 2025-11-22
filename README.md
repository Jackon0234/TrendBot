# 🚀 TrendBot v1.0 - Google Trends Telegram Analizörü

**TrendBot**, Telegram üzerinden gönderdiğiniz anahtar kelimeleri (Örn: "Yapay Zeka", "Dolar") Google Trends API'si ile analiz eden, detaylı **PDF raporu** oluşturan ve modern bir **Web Yönetim Paneli** üzerinden yönetilen açık kaynaklı bir araçtır.

![TrendBot Web Panel](https://i.imgur.com/n5xEwOh.png)

## 🌟 Özellikler

* **Web Yönetim Paneli:** Botu terminale girmeden "Başlat/Durdur" yapın ve canlı logları izleyin. (Bootstrap 5 & Dark Mode).
* **PDF Raporlama:** Türkçe karakter destekli, şık tasarımlı analiz raporları üretir.
* **Anlık Trend Analizi:** Kelimenin zaman içindeki popülaritesini ve "Rising" (Yükselen) ilgili aramaları çeker.
* **Threading (Çoklu İş Parçacığı):** Bot arka planda çalışırken web arayüzü donmaz.

## 📸 Ekran Görüntüleri

| Web Yönetim Paneli | Oluşturulan PDF Raporu |
| :---: | :---: |
| ![](https://i.imgur.com/n5xEwOh.png) | ![](https://i.imgur.com/Sf8Vdvm.png) |

## 🛠️ Kurulum ve Kullanım

Projeyi bilgisayarınıza indirin (veya `git clone` yapın) ve proje klasörüne gidin.

### 1. Gerekli Kütüphaneleri Yükleyin
Terminal veya CMD'yi açıp şu komutu çalıştırın:
pip install flask pyTelegramBotAPI pytrends fpdf pandas

###2. Bot Token Ayarı
app.py dosyasını açın. Telegram @BotFather üzerinden aldığınız tokeni şu satıra yapıştırın:
API_TOKEN = 'BURAYA_TOKEN_GELECEK'

###3. Çalıştırın
Terminalden uygulamayı başlatın:
python app.py
