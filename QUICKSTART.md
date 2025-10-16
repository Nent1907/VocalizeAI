# EchoMinds - Hızlı Başlangıç Kılavuzu

## 🚀 Kurulum Adımları

### 1. Python Sanal Ortam Oluştur
```powershell
cd c:\Users\djosm\Desktop\echominds
python -m venv venv
venv\Scripts\activate
```

### 2. Bağımlılıkları Yükle
```powershell
pip install -r requirements.txt
```

### 3. API Key Ayarla
```powershell
# .env dosyası oluştur
copy .env.example .env

# .env dosyasını bir metin editörü ile aç ve API key'ini ekle:
# ELEVENLABS_API_KEY=your_actual_api_key_here
```

**API Key Nasıl Alınır?**
1. https://elevenlabs.io adresine git
2. Üye ol / Giriş yap
3. Settings > API Keys bölümüne git
4. "Generate New Key" ile yeni key oluştur
5. Key'i kopyala ve .env dosyasına yapıştır

### 4. Uygulamayı Çalıştır
```powershell
streamlit run app.py
```

Tarayıcıda otomatik olarak `http://localhost:8501` açılacaktır.

---

## 📖 Kullanım Rehberi

### Adım 1: Ses Klonlama
1. Sol panelde "🔴 Kayda Başla" butonuna tıkla
2. 10-30 saniye arası temiz bir şekilde konuş
3. "🧬 Sesi Klonla" butonuna tıkla
4. Klonlama işleminin tamamlanmasını bekle (~10 saniye)

**💡 İpuçları:**
- Sessiz bir ortamda kayıt yap
- Mikrofona çok yakın olma
- Doğal bir tonla konuş
- En az 10 saniye kayıt önerilir

### Adım 2: Çeviri ve Konuşma
1. Sağ panelde hedef dili seç (örn: İngilizce 🇺🇸)
2. "🎤 Konuşmaya Başla" butonuna tıkla
3. Çevrilmesini istediğin metni söyle
4. "🚀 Çevir ve Konuştur" butonuna tıkla
5. Çıktıyı dinle ve indir

---

## 🎯 Özellikler

✅ **Gerçek Zamanlı Ses Klonlama**: 10 saniyede sesinizi klonlayın
✅ **Çoklu Dil Desteği**: 29+ dil arası çeviri
✅ **Yüksek Kalite**: ElevenLabs AI ile profesyonel ses kalitesi
✅ **Kolay Kullanım**: Web tabanlı modern arayüz
✅ **Ses İndirme**: MP3 formatında dosya indirme

---

## 🔧 Sorun Giderme

### Mikrofon Çalışmıyor
**Problem**: Mikrofona erişilemiyor
**Çözüm**:
1. Tarayıcıda mikrofon izni ver
2. Windows ayarlarından mikrofon izinlerini kontrol et
3. Farklı tarayıcı dene (Chrome önerilir)

### API Hatası
**Problem**: "Invalid API Key" hatası
**Çözüm**:
1. `.env` dosyasındaki API key'i kontrol et
2. Key'de boşluk veya fazladan karakter olmadığından emin ol
3. ElevenLabs hesabınızın aktif olduğunu doğrula

### Bağımlılık Hatası
**Problem**: Modül bulunamıyor hatası
**Çözüm**:
```powershell
pip install --upgrade -r requirements.txt
```

### Ses Kalitesi Düşük
**Problem**: Klonlanan ses gerçekçi değil
**Çözüm**:
- Daha uzun kayıt yap (20-30 saniye)
- Sessiz ortamda kayıt yap
- Stability ve Similarity ayarlarını değiştir

---

## 📊 Limitler (Free Tier)

- ✅ Aylık 10,000 karakter TTS
- ✅ 10 instant voice clone
- ⚠️ Her klonlama yaklaşık ~100 karakter tüketir

**İpucu**: Klonlanan sesi sakla, her seferinde yeniden klonlama

---

## 🎨 Gelişmiş Ayarlar

### Ses Ayarları
- **Stability (0-1)**: Yüksek = Daha kararlı, Düşük = Daha ifadeli
- **Similarity (0-1)**: Yüksek = Orijinale daha yakın

### Önerilen Ayarlar
- **Dengelenmiş**: Stability 0.5, Similarity 0.75
- **Kararlı**: Stability 0.75, Similarity 0.75
- **İfadeli**: Stability 0.3, Similarity 0.8

---

## 📞 Destek

**Dokümantasyon**: README.md dosyasına bakın
**GitHub Issues**: Hata bildirimi için
**ElevenLabs Docs**: https://docs.elevenlabs.io

---

## 🎓 Notlar

1. **İlk Kullanım**: İlk klonlama biraz daha uzun sürebilir
2. **İnternet**: Sürekli internet bağlantısı gereklidir
3. **Gizlilik**: Sesler ElevenLabs sunucularında işlenir
4. **Lisans**: MIT License - ticari kullanım için uygun

---

**🎉 Başarılar! Artık kendi sesinizle 29 dilde konuşabilirsiniz!**
