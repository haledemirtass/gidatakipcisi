Gelişmiş Mutfak Takip Uygulaması
Gelişmiş Mutfak Takip, mutfağınızdaki ürünleri etkin bir şekilde yönetmenizi sağlayan bir masaüstü uygulamasıdır. Uygulama, ürünlerin son kullanma tarihlerini takip etmenize, stok durumunu görüntülemenize ve alışveriş listesi oluşturmanıza olanak tanır.
Özellikler

Ürün Yönetimi

Yeni ürün ekleme
Ürün kategorilendirme
Miktar takibi
Son kullanma tarihi kontrolü
Otomatik stok güncellemesi


Kategori Sistemi

Meyve/Sebze
Et Ürünleri
Süt Ürünleri
Kuru Gıda
Diğer


Raporlama

Son kullanma tarihi yaklaşan ürünler raporu
Kategori bazlı stok raporu


Alışveriş Listesi

Alınacak ürünleri listeleme
Miktar ve birim belirtme
Liste temizleme


Görsel Özellikler

Açık/Koyu tema desteği
Kullanıcı dostu arayüz
Sekmeli navigasyon sistemi



Gereksinimler

Python 3.x
tkinter
json
datetime
threading
os

## Kurulum

1. Python 3.8 veya daha üstü bir sürümü bilgisayarınıza yükleyin.
2. Gerekli kütüphaneleri kurun:

   ```bash
   pip install tk
   ```

3. Proje dosyasını klonlayın veya indirin:

   GitHub linki: https://github.com/haledemirtass/mutfak-takip
   Komutlarla klonlamak için:
   ```bash
   git clone https://github.com/kullaniciadi/mutfak-takip.git
   cd mutfak-takip
   ```

4. Uygulamayı başlatın:

   ```bash
   python mutfak_takip.py
   ```


Kullanım
Ürün Ekleme

"Ürün Ekle" sekmesine gidin
Kategori seçin
Ürün adı, miktar ve birim bilgilerini girin
Son kullanma süresini gün cinsinden belirtin
İsteğe bağlı not ekleyin
"Ürün Ekle" butonuna tıklayın

Ürün Listesi

Tüm ürünleri görüntüleme
Kategoriye göre filtreleme
Ürün silme
Miktar artırma/azaltma

Raporlar

Son kullanma tarihi yaklaşan ürünleri görüntüleme
Kategori bazlı stok durumu raporlama

Alışveriş Listesi

"Alışveriş Listesi" sekmesine gidin
Alınacak ürün adı ve miktarını girin
"Listeye Ekle" butonuyla ürünü ekleyin
Gerektiğinde listeyi temizleyin

Özellikler
Otomatik Silme

Uygulama, son kullanma tarihi geçen ürünleri otomatik olarak sistemden kaldırır
Kontrol günlük olarak yapılır

Tema Değiştirme

Sağ üst köşedeki tema değiştirme butonu ile açık/koyu tema arasında geçiş yapılabilir

Veri Saklama
Uygulama verileri mutfak.json dosyasında saklanır.

