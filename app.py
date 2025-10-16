"""
VocalizeAI - Your Voice, Any Language
Main Streamlit Application Entry Point
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import numpy as np
import soundfile as sf
import time

# Import core modules
from core.audio_recorder import AudioRecorder
from core.voice_cloner import VoiceCloner
from core.speech_to_text import SpeechToText
from core.translator import Translator
from core.text_to_speech import TextToSpeech
from utils.config import Config
from utils.audio_utils import AudioUtils

# Load environment variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="VocalizeAI - Your Voice, Any Language",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main Theme */
    .main {
        background-color: #0E1117;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #00B4DB 0%, #0083B0 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 150, 200, 0.2);
    }
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
    }
    .main-header p {
        font-size: 1.1rem;
        color: #E0E0E0;
    }
    
    /* Tool Cards */
    .tool-card {
        background-color: #1E1E1E;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #2A2A2A;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        height: 100%;
    }
    .tool-card h3 {
        color: #00B4DB;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #0083B0;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00B4DB;
        color: white;
    }
    .stButton>button[kind="secondary"] {
        background-color: #444;
    }
    .stButton>button[kind="secondary"]:hover {
        background-color: #666;
    }

    /* Results section */
    .results-container {
        background-color: #1E1E1E;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #2A2A2A;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    defaults = {
        'cloned_voice_id': None,
        'cloned_voice_name': None,
        'source_text': None, # To hold original text from either speech or text input
        'source_text_label': "Orijinal Metin",
        'translated_text': None,
        'output_audio_path': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main():
    """Main application function."""
    
    initialize_session_state()
    
    # --- HEADER ---
    st.markdown("""
        <div class="main-header">
            <h1>🗣️ VocalizeAI</h1>
            <p>Konuş, Çevir, Seslendir - Your Voice, Any Language</p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- API KEY CHECK ---
    api_key = os.getenv("ELEVENLABS_API_KEY")
    use_mock = False
    if not api_key:
        st.warning("⚠️ ElevenLabs API anahtarı bulunamadı! Uygulama 'mock' modunda çalışıyor. `.env` dosyanızı kontrol edin.")
        use_mock = True
    
    # --- INITIALIZE CORE COMPONENTS (with mock fallbacks if API key missing) ---
    try:
        config = Config()
        audio_recorder = AudioRecorder(config)
        translator = Translator()

        if not use_mock:
            voice_cloner = VoiceCloner(api_key)
            speech_to_text = SpeechToText(api_key)
            text_to_speech = TextToSpeech(api_key)
        else:
            class MockVoiceCloner:
                def clone_voice(self, audio_path, voice_name): time.sleep(2); return f"mock_{int(time.time())}_{voice_name}"
            class MockSpeechToText:
                def transcribe(self, audio_path): time.sleep(1); return "(Mock) Bu bir örnek transkripsiyondur."
            class MockTextToSpeech:
                def synthesize(self, text, voice_id, stability, similarity):
                    time.sleep(2)
                    out_dir = Path(config.OUTPUT_DIR) if hasattr(config, 'OUTPUT_DIR') else Path('assets/outputs')
                    out_dir.mkdir(parents=True, exist_ok=True)
                    out_path = out_dir / f"vocalizeai_mock_{int(time.time())}.wav"
                    sf.write(str(out_path), np.zeros(22050 * 2), 22050); return str(out_path)
            voice_cloner = MockVoiceCloner(); speech_to_text = MockSpeechToText(); text_to_speech = MockTextToSpeech()
    except Exception as e:
        st.error(f"Uygulama bileşenleri başlatılırken bir hata oluştu: {e}"); return

    # --- SIDEBAR SETTINGS ---
    with st.sidebar:
        st.header("⚙️ Ayarlar")
        st.subheader("🌍 Dil Seçimi")
        target_language = st.selectbox("Hedef Dil", options=list(config.SUPPORTED_LANGUAGES.keys()),
                                     format_func=lambda x: f"{config.SUPPORTED_LANGUAGES[x]['flag']} {config.SUPPORTED_LANGUAGES[x]['name']}")
        st.subheader("🎚️ Ses Üretim Ayarları")
        st.info("Bu ayarlar tüm seslendirme işlemleri için geçerlidir.")
        stability = st.slider("Stability (Kararlılık)", 0.0, 1.0, 0.5, 0.05)
        similarity = st.slider("Similarity Boost (Benzerlik)", 0.0, 1.0, 0.75, 0.05)
        st.subheader("⏱️ Kayıt Süresi")
        max_duration = st.number_input("Maksimum Kayıt Süresi (saniye)", 5, 60, 20)

    # --- VOICE SELECTION LOGIC ---
    def get_voice_id_and_show_info():
        if st.session_state.cloned_voice_id:
            st.info(f"Klonlanmış sesiniz **'{st.session_state.cloned_voice_name}'** kullanılıyor.")
            return st.session_state.cloned_voice_id
        else:
            st.warning("Henüz bir ses klonlanmadığı için varsayılan ses (Rachel) kullanılacaktır.")
            return "Rachel" # A default, high-quality voice from ElevenLabs

    # --- MAIN CONTENT LAYOUT ---
    col1, col2 = st.columns(2)

    # === COLUMN 1: VOICE CLONING TOOL ===
    with col1:
        with st.container(): # HATA DÜZELTİLDİ: border=True kaldırıldı
            st.markdown("<h3>🎙️ Ses Klonlama Aracı</h3>", unsafe_allow_html=True)
            if st.session_state.cloned_voice_id:
                st.success(f"✅ Aktif Klon: **{st.session_state.cloned_voice_name}**")
                if st.button("Yeni Bir Ses Klonla", type="secondary"):
                    st.session_state.cloned_voice_id = None; st.session_state.cloned_voice_name = None; st.rerun()
            else:
                voice_name = st.text_input("Klonlanacak Sese Bir İsim Verin", "MyVoice")
                audio_path_clone = audio_recorder.record_audio_button(max_duration)
                if audio_path_clone:
                    st.audio(audio_path_clone)
                    if st.button("🧬 Sesi Klonla"):
                        with st.spinner("Ses klonlanıyor..."):
                            voice_id = voice_cloner.clone_voice(audio_path_clone, voice_name)
                            if voice_id:
                                st.session_state.cloned_voice_id = voice_id; st.session_state.cloned_voice_name = voice_name
                                st.balloons(); st.rerun()
                            else: st.error("Klonlama başarısız oldu.")

    # === COLUMN 2: SPEECH-TO-SPEECH TRANSLATION TOOL ===
    with col2:
        with st.container(): # HATA DÜZELTİLDİ: border=True kaldırıldı
            st.markdown("<h3>🌍 Konuşarak Anlık Çeviri</h3>", unsafe_allow_html=True)
            
            audio_path_translate = audio_recorder.record_audio_button(max_duration, "🎤 Çeviri İçin Konuşmaya Başla")
            
            if audio_path_translate:
                st.audio(audio_path_translate)
                progress_bar = st.progress(0, "Başlatılıyor...")
                try:
                    voice_to_use = get_voice_id_and_show_info()
                    
                    progress_bar.progress(25, "1/3: Ses metne dönüştürülüyor...")
                    transcribed_text = speech_to_text.transcribe(audio_path_translate)
                    st.session_state.source_text = transcribed_text
                    st.session_state.source_text_label = "Deşifre Edilen Metin"
                    if not transcribed_text: raise ValueError("Ses metne dönüştürülemedi.")

                    progress_bar.progress(50, "2/3: Metin çevriliyor...")
                    translated_text = translator.translate(transcribed_text, target_language)
                    st.session_state.translated_text = translated_text
                    if not translated_text: raise ValueError("Metin çevrilemedi.")
                    
                    progress_bar.progress(75, "3/3: Konuşma oluşturuluyor...")
                    output_path = text_to_speech.synthesize(translated_text, voice_to_use, stability, similarity)
                    st.session_state.output_audio_path = output_path
                    progress_bar.progress(100, "Tamamlandı!")
                except Exception as e: st.error(f"Bir hata oluştu: {e}")
                finally: progress_bar.empty()

    st.markdown("<br>", unsafe_allow_html=True)

    # === NEW: TEXT-TO-SPEECH TOOL ===
    with st.container(): # HATA DÜZELTİLDİ: border=True kaldırıldı
        st.markdown("<h3>📝 Metinden Sese Dönüştürme</h3>", unsafe_allow_html=True)
        tts_text = st.text_area("Seslendirilecek metni buraya girin veya yapıştırın.", height=150)
        
        if st.button("🔊 Metni Seslendir"):
            if tts_text:
                with st.spinner("Ses oluşturuluyor..."):
                    try:
                        voice_to_use = get_voice_id_and_show_info()
                        st.session_state.source_text = tts_text
                        st.session_state.source_text_label = "Girilen Metin"
                        st.session_state.translated_text = None # No translation in this tool
                        
                        output_path = text_to_speech.synthesize(tts_text, voice_to_use, stability, similarity)
                        st.session_state.output_audio_path = output_path
                    except Exception as e: st.error(f"Ses oluşturulurken bir hata oluştu: {e}")
            else:
                st.warning("Lütfen seslendirilecek bir metin girin.")

    # === DYNAMIC RESULTS SECTION ===
    if st.session_state.output_audio_path:
        st.markdown("---")
        with st.container(): # HATA DÜZELTİLDİ: border=True kaldırıldı
            st.subheader("🎉 Sonuç")
            st.audio(st.session_state.output_audio_path)
            with open(st.session_state.output_audio_path, "rb") as f:
                st.download_button("💾 Ses Dosyasını İndir", f, f"vocalizeai_output.mp3", "audio/mpeg")

            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.info(f"**{st.session_state.source_text_label}:**\n\n{st.session_state.source_text}")
            if st.session_state.translated_text:
                with res_col2:
                    st.success(f"**Çevrilmiş Metin ({target_language}):**\n\n{st.session_state.translated_text}")

    # --- FOOTER ---
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666;'><p>Powered by ElevenLabs AI | VocalizeAI v1.2</p></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    if 'record_audio_button' not in dir(AudioRecorder):
        def record_audio_button(self, duration, label="🔴 Kayda Başla"):
            if st.button(label):
                with st.spinner("Kaydediliyor..."):
                    return self.record_audio(duration=duration)
            return None
        AudioRecorder.record_audio_button = record_audio_button
    main()