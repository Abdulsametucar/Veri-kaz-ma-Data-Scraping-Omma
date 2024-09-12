# OMMA Dispanser Veri Kazıma Projesi

Bu proje, Python ve Selenium kullanarak [OMMA web sitesi](https://omma.us.thentiacloud.net/webs/omma/register/#/business/search/all/Dispensary) üzerindeki dispanser işletme verilerini kazıyarak, elde edilen verileri Excel dosyasına aktarmaktadır.

## Proje Özeti

Bu betik, OMMA kaydındaki dispanser verilerini otomatik olarak toplar; işletme adları, lisanslar, şehirler ve iletişim bilgileri gibi verileri içerir. Kazınan veriler daha sonra analiz veya kayıt amacıyla bir Excel dosyasına kaydedilir.

### Özellikler
- Web sitesinden birden fazla sayfayı kazır.
- İlgili veri alanlarını toplar (örneğin, işletme adı, lisans türü, şehir, iletişim bilgileri).
- Verileri bir Excel dosyasına aktarır.

## Gereksinimler

Aşağıdaki paketlerin kurulu olduğundan emin olun:

- Python 3.x
- Selenium
- Pandas
- Chrome için WebDriver Manager

Gerekli paketleri aşağıdaki komut ile kurabilirsiniz:

```bash
pip install selenium pandas webdriver-manager

