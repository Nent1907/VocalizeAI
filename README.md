# 🎙️ EchoMinds - Voice Clone & Translate

## 📋 Proje Özeti

EchoMinds, kullanıcının sesini klonlayarak farklı dillerde konuşmasını sağlayan yapay zeka destekli bir uygulamadır.

## 🎯 Temel Özellikler

### 1. Ses Kaydı ve İşleme
- 🎤 Gerçek zamanlı mikrofon kaydı
- 📊 Ses seviyesi göstergesi
- ⏱️ Kayıt süresi limitleri (3-10 saniye minimum)
- 🔊 Kayıt öncesi test ve önizleme

### 2. Voice Cloning
- 🧬 ElevenLabs Voice Cloning API entegrasyonu
- 👤 Instant voice cloning (hızlı klonlama)
- 🎭 Professional voice cloning (detaylı klonlama - opsiyonel)
- 💾 Klonlanmış seslerin kaydedilmesi

### 3. Speech-to-Text (STT)
- 🎯 ElevenLabs STT ile yüksek doğruluk
- 🌍 Çoklu dil desteği
- 📝 Noktalama işaretleri ile metinleştirme
- ⚡ Hızlı işlem süresi

### 4. Çeviri Sistemi
- 🗣️ 29+ dil desteği
- 🔄 Otomatik kaynak dil tespiti
- 📚 Profesyonel çeviri kalitesi
- 🌐 Google Translate API entegrasyonu

### 5. Text-to-Speech (TTS)
- 🎵 Klonlanmış ses ile sentezleme
- 🎚️ Ayarlanabilir konuşma hızı
- 💎 Yüksek kaliteli ses çıktısı
- 📱 Çoklu format desteği (MP3, WAV)

### 6. Kullanıcı Arayüzü
- 🖥️ Modern Streamlit web arayüzü
- 📱 Responsive tasarım
- 🎨 Kullanıcı dostu görsel tasarım
- 📊 Gerçek zamanlı ilerleme göstergeleri
- 🔄 Kolay dil seçimi dropdown menüleri

## 🏗️ Mimari Yapı

```
echominds/
├── app.py                      # Ana Streamlit uygulaması
├── requirements.txt            # Python bağımlılıkları
├── .env.example               # Ortam değişkenleri şablonu
├── .gitignore                 # Git ignore dosyası
├── README.md                  # Proje dokümantasyonu
│
├── core/
│   ├── __init__.py
│   ├── audio_recorder.py      # Ses kayıt modülü
│   ├── voice_cloner.py        # Voice cloning işlemleri
│   ├── speech_to_text.py      # STT işlemleri
│   ├── translator.py          # Çeviri işlemleri
│   └── text_to_speech.py      # TTS işlemleri
│
├── utils/
│   ├── __init__.py
│   ├── audio_utils.py         # Ses dosyası işlemleri
│   ├── config.py              # Yapılandırma ayarları
│   └── validators.py          # Giriş validasyonları
│
├── assets/
│   ├── temp/                  # Geçici ses dosyaları
│   ├── cloned_voices/         # Klonlanmış sesler
│   └── outputs/               # Çıktı ses dosyaları
│
└── tests/
    ├── __init__.py
    ├── test_audio.py
    ├── test_cloning.py
    └── test_translation.py
```

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler

#### Ana Framework
- **Python 3.10+**: Ana programlama dili
- **Streamlit 1.28+**: Web arayüzü framework'ü

#### ElevenLabs Entegrasyonu
- **elevenlabs**: Official Python SDK
- **API Version**: v1 (stable)
- **Endpoints**:
  - `/v1/speech-to-text`: Ses-metin dönüşümü
  - `/v1/text-to-speech`: Metin-ses dönüşümü
  - `/v1/voices/add`: Ses klonlama
  - `/v1/voices/{voice_id}`: Klonlanmış ses yönetimi

#### Ses İşleme
- **sounddevice**: Mikrofon kaydı
- **soundfile**: Ses dosyası okuma/yazma
- **pydub**: Ses format dönüşümleri
- **numpy**: Ses verisi işleme

#### Çeviri
- **deep-translator**: Çoklu çeviri motoru desteği
- **langdetect**: Dil tespiti

#### Yardımcı Kütüphaneler
- **python-dotenv**: Ortam değişkenleri
- **requests**: HTTP istekleri
- **pathlib**: Dosya yolu yönetimi

### API Limitleri ve Öneriler

#### ElevenLabs Free Tier
- ✅ 10,000 karakter/ay TTS
- ✅ 10 instant voice clone
- ⚠️ 3 professional voice clone
- 🎯 Önerilen: Instant cloning kullanımı

#### Ses Kayıt Özellikleri
- **Sample Rate**: 44100 Hz (professional)
- **Channels**: Mono (1 kanal)
- **Format**: WAV (16-bit PCM)
- **Min Duration**: 3 saniye (instant clone için)
- **Max Duration**: 10 dakika
- **Optimal Duration**: 30-60 saniye (kaliteli klonlama için)

### Desteklenen Diller

**Çeviri için 29 Dil:**
```
🇺🇸 English (en)    🇹🇷 Turkish (tr)     🇪🇸 Spanish (es)    🇫🇷 French (fr)
🇩🇪 German (de)     🇮🇹 Italian (it)     🇵🇹 Portuguese (pt) 🇷🇺 Russian (ru)
🇯🇵 Japanese (ja)   🇰🇷 Korean (ko)      🇨🇳 Chinese (zh)    🇦🇷 Arabic (ar)
🇳🇱 Dutch (nl)      🇵🇱 Polish (pl)      🇸🇪 Swedish (sv)    🇮🇳 Hindi (hi)
🇨🇿 Czech (cs)      🇩🇰 Danish (da)      🇫🇮 Finnish (fi)    🇬🇷 Greek (el)
🇭🇺 Hungarian (hu)  🇮🇩 Indonesian (id)  🇳🇴 Norwegian (no)  🇷🇴 Romanian (ro)
🇸🇰 Slovak (sk)     🇺🇦 Ukrainian (uk)   🇻🇳 Vietnamese (vi) 🇹🇭 Thai (th)
🇧🇬 Bulgarian (bg)
```

## 📦 Kurulum

### 1. Gereksinimler
```bash
Python 3.10 veya üzeri
ElevenLabs API Key
İnternet bağlantısı
Mikrofon erişimi
```

### 2. Proje Kurulumu
```bash
# Proje dizinine git
cd echominds

# Virtual environment oluştur
python -m venv venv

# Virtual environment'ı aktifleştir
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 3. Yapılandırma
```bash
# .env dosyası oluştur
copy .env.example .env

# .env dosyasını düzenle ve API key ekle
ELEVENLABS_API_KEY=your_api_key_here
```

### 4. Çalıştırma
```bash
streamlit run app.py
```

Tarayıcıda otomatik olarak `http://localhost:8501` açılacaktır.

## 🎮 Kullanım

### Adım 1: Ses Kaydı
1. 🎤 "Start Recording" butonuna tıklayın
2. 🗣️ Mikrofonunuza konuşun (en az 3 saniye)
3. ⏹️ "Stop Recording" ile kaydı durdurun
4. ▶️ Önizleme ile sesi kontrol edin

### Adım 2: Voice Cloning
1. 🧬 "Clone Voice" butonuna tıklayın
2. ⏳ İşlemin tamamlanmasını bekleyin (~5-10 saniye)
3. ✅ Klonlama başarılı mesajını görün

### Adım 3: Konuşma ve Çeviri
1. 🎤 Yeni bir ses kaydı yapın (çevrilecek metin)
2. 🌍 Hedef dili seçin
3. 🚀 "Translate & Speak" butonuna tıklayın
4. 🔊 Çıktıyı dinleyin

### Adım 4: Kaydetme
1. 💾 "Save Output" ile çıktıyı kaydedin
2. 📁 Dosyalar `assets/outputs/` klasörüne kaydedilir

## 🔐 Güvenlik ve Gizlilik

### API Key Güvenliği
- ✅ API anahtarları `.env` dosyasında saklanır
- ✅ `.env` dosyası `.gitignore`'a eklenmiştir
- ⚠️ API anahtarlarınızı asla paylaşmayın

### Ses Dosyaları
- 🗑️ Geçici dosyalar otomatik temizlenir
- 💾 Klonlanmış sesler yerel olarak saklanır
- 🔒 Sadece kullanıcı erişimi vardır

### GDPR Uyumluluğu
- 📝 Kullanıcı onayı alınır
- 🗑️ Veri silme hakkı tanınır
- 🔐 Veriler şifrelenmeden saklanmaz

## 🚀 İleri Seviye Özellikler (Gelecek Versiyonlar)

### v2.0 Planları
- [ ] 👥 Çoklu ses profili desteği
- [ ] 💬 Gerçek zamanlı canlı çeviri
- [ ] 🎛️ Ses efektleri (pitch, speed, emotion)
- [ ] 📊 Kullanıcı istatistikleri ve geçmiş
- [ ] 🌐 Web API endpoint'leri
- [ ] 📱 Mobil uygulama entegrasyonu

### v3.0 Vizyonu
- [ ] 🤖 Yapay zeka asistanı entegrasyonu
- [ ] 🎭 Duygu (emotion) kontrolü
- [ ] 🎬 Video dubbing desteği
- [ ] ☁️ Cloud storage entegrasyonu
- [ ] 🔄 Batch işlem desteği

## 🐛 Sorun Giderme

### Mikrofon Erişimi
```
Hata: Mikrofona erişilemiyor
Çözüm: Tarayıcı izinlerini kontrol edin
```

### API Limiti
```
Hata: Quota exceeded
Çözüm: ElevenLabs dashboard'dan kullanım kontrolü yapın
```

### Ses Kalitesi
```
Problem: Düşük kalite klonlama
Çözüm: Daha uzun ve temiz ses kaydı yapın (30+ saniye)
```

## 📊 Performans Metrikleri

- ⚡ **Ses Kaydı**: ~0.1 saniye gecikme
- 🧬 **Voice Cloning**: 5-15 saniye (instant)
- 📝 **Speech-to-Text**: 2-5 saniye
- 🌍 **Çeviri**: 0.5-2 saniye
- 🔊 **Text-to-Speech**: 3-8 saniye

**Toplam İşlem Süresi**: ~10-30 saniye (ortalama)

## 📄 Lisans

MIT License - Detaylar için `LICENSE` dosyasına bakın.

## 🤝 Katkıda Bulunma

Pull request'ler kabul edilir. Büyük değişiklikler için lütfen önce bir issue açın.

## 📧 İletişim

Sorularınız için issue açabilir veya iletişime geçebilirsiniz.

## 🙏 Teşekkürler

- ElevenLabs - Ses teknolojisi için
- Streamlit - Harika UI framework için
- Open Source topluluğu - Tüm kütüphaneler için

---

**Made with ❤️ by EchoMinds Team**
