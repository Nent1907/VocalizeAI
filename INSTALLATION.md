# 🎙️ EchoMinds - Kurulum Tamamlandı!

## ✅ Projeniz Başarıyla Oluşturuldu!

### 📁 Proje Yapısı
```
echominds/
├── app.py                    # Ana Streamlit uygulaması ✨
├── requirements.txt          # Python bağımlılıkları ✅
├── .env                      # Ortam değişkenleri (API KEY buraya)
├── .env.example             # Örnek ortam değişkenleri
├── README.md                # Detaylı dokümantasyon 📖
├── QUICKSTART.md           # Hızlı başlangıç kılavuzu 🚀
├── LICENSE                  # MIT Lisansı
│
├── core/                    # Ana modüller
│   ├── audio_recorder.py   # Ses kayıt modülü 🎤
│   ├── voice_cloner.py     # Ses klonlama 🧬
│   ├── speech_to_text.py   # Ses-metin dönüşümü 📝
│   ├── translator.py       # Çeviri motoru 🌍
│   └── text_to_speech.py   # Metin-ses sentezi 🔊
│
├── utils/                   # Yardımcı araçlar
│   ├── config.py           # Yapılandırma ayarları
│   ├── audio_utils.py      # Ses işleme araçları
│   └── validators.py       # Doğrulama fonksiyonları
│
├── assets/                  # Varlık dosyaları
│   ├── temp/               # Geçici dosyalar
│   ├── cloned_voices/      # Klonlanmış sesler
│   └── outputs/            # Çıktı dosyaları
│
└── tests/                   # Test dosyaları
    ├── test_audio.py
    ├── test_cloning.py
    └── test_translation.py
```

## 🚀 Hemen Başlayın!

### 1️⃣ API Key Ayarlayın
`.env` dosyasını bir metin editörü ile açın ve ElevenLabs API key'inizi ekleyin:

```env
ELEVENLABS_API_KEY=your_actual_api_key_here
```

**API Key Nasıl Alınır?**
1. 🌐 https://elevenlabs.io adresine gidin
2. 📝 Üye olun veya giriş yapın
3. ⚙️ Settings > API Keys bölümüne gidin
4. ➕ "Generate New Key" ile yeni key oluşturun
5. 📋 Key'i kopyalayın ve `.env` dosyasına yapıştırın

### 2️⃣ Uygulamayı Çalıştırın
```powershell
# Virtual environment aktifleştirin (eğer aktif değilse)
venv\Scripts\activate

# Uygulamayı başlatın
streamlit run app.py
```

🎉 Tarayıcıda otomatik olarak `http://localhost:8501` açılacak!

## 🎯 Nasıl Kullanılır?

### Adım 1: Sesinizi Klonlayın 🧬
1. Sol panelde **"🔴 Kayda Başla"** butonuna tıklayın
2. Mikrofonunuza **10-30 saniye** kadar konuşun
3. **"🧬 Sesi Klonla"** butonuna tıklayın
4. ~10 saniye bekleyin ⏱️

💡 **İpucu**: Sessiz ortamda, doğal bir tonla konuşun!

### Adım 2: Konuşun ve Çevirin 🌍
1. Sağ panelde **hedef dili** seçin (örn: İngilizce 🇺🇸)
2. **"🎤 Konuşmaya Başla"** butonuna tıklayın
3. Çevrilmesini istediğiniz metni söyleyin
4. **"🚀 Çevir ve Konuştur"** butonuna tıklayın
5. Çıktıyı dinleyin ve indirin 💾

## ✨ Özellikler

✅ **Ses Klonlama**: 10 saniyede sesinizi klonlayın
✅ **29+ Dil**: Türkçe, İngilizce, İspanyolca, Fransızca ve daha fazlası
✅ **Yüksek Kalite**: ElevenLabs AI ile profesyonel ses
✅ **Kolay Kullanım**: Modern web arayüzü
✅ **Dosya İndirme**: MP3 formatında kaydetme

## 📊 Desteklenen Diller

🇹🇷 Türkçe | 🇺🇸 İngilizce | 🇪🇸 İspanyolca | 🇫🇷 Fransızca
🇩🇪 Almanca | 🇮🇹 İtalyanca | 🇵🇹 Portekizce | 🇷🇺 Rusça
🇯🇵 Japonca | 🇰🇷 Korece | 🇨🇳 Çince | 🇦🇪 Arapça
...ve 17 dil daha!

## 🔧 Gereksinimler

- ✅ Python 3.10+
- ✅ ElevenLabs API Key
- ✅ İnternet bağlantısı
- ✅ Mikrofon

## 📝 Detaylı Bilgi

- 📖 **Tam Dokümantasyon**: `README.md` dosyasına bakın
- 🚀 **Hızlı Başlangıç**: `QUICKSTART.md` dosyasına bakın
- 🐛 **Sorun mu var?**: QUICKSTART.md'deki "Sorun Giderme" bölümüne bakın

## 🎨 Teknolojiler

- **Framework**: Streamlit (Python)
- **AI Platform**: ElevenLabs
- **Çeviri**: Google Translate API
- **Ses İşleme**: sounddevice, soundfile, pydub
- **UI**: Modern web arayüzü

## 📞 Destek

- 📧 GitHub Issues
- 📚 ElevenLabs Docs: https://docs.elevenlabs.io
- 💬 Topluluk Desteği

## 📜 Lisans

MIT License - Ticari kullanım için uygun

---

## ⚡ Hızlı Komutlar

```powershell
# Uygulamayı çalıştır
streamlit run app.py

# Testleri çalıştır
pytest tests/

# Kodu formatla
black .

# Kod kalitesi kontrolü
flake8 .
```

---

**🎉 Hazırsınız! Artık kendi sesinizle 29 dilde konuşabilirsiniz!**

Made with ❤️ by EchoMinds Team | Powered by ElevenLabs AI
