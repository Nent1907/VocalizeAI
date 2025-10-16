"""
Speech to Text Module
Handles speech recognition using ElevenLabs API
"""

from elevenlabs import ElevenLabs
from pathlib import Path


class SpeechToText:
    """
    Speech to text conversion using ElevenLabs API
    """
    
    def __init__(self, api_key):
        """
        Initialize SpeechToText
        
        Args:
            api_key: ElevenLabs API key
        """
        self.api_key = api_key
        self.client = ElevenLabs(api_key=api_key)
    
    def transcribe(self, audio_path, language=None):
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            language: Language code (optional, auto-detect if None)
        
        Returns:
            str: Transcribed text, or None if failed
        """
        try:
            print(f"🎯 Transcribing audio: {audio_path}")
            
            # Read audio file
            with open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Use ElevenLabs Speech-to-Text
            # Note: This is a simplified version. Check ElevenLabs SDK docs for exact method
            try:
                # Try using the speech-to-text endpoint
                result = self.client.speech_to_text.convert(
                    audio=audio_data
                )
                text = result.text if hasattr(result, 'text') else str(result)
                
            except AttributeError:
                # Alternative method if SDK structure is different
                # Some versions might use different method names
                print("⚠️ Using alternative transcription method...")
                # This is a fallback - you might need to adjust based on SDK version
                import requests
                
                url = "https://api.elevenlabs.io/v1/speech-to-text"
                headers = {
                    "xi-api-key": self.api_key
                }
                
                files = {
                    'audio': audio_data
                }
                
                response = requests.post(url, headers=headers, files=files)
                
                if response.status_code == 200:
                    text = response.json().get('text', '')
                else:
                    print(f"❌ API Error: {response.status_code}")
                    return None
            
            print(f"✅ Transcription successful!")
            print(f"📝 Text: {text}")
            
            return text
            
        except Exception as e:
            print(f"❌ Transcription failed: {str(e)}")
            print("💡 Tip: Check if your ElevenLabs plan supports Speech-to-Text")
            return None
    
    def transcribe_with_timestamps(self, audio_path):
        """
        Transcribe audio with word-level timestamps
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            dict: Transcription with timestamps
        """
        try:
            with open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # This would return transcription with timestamps
            # Format: {"text": "...", "words": [{"word": "...", "start": 0.0, "end": 1.0}, ...]}
            # Implementation depends on ElevenLabs API capabilities
            
            print("⏱️ Timestamped transcription not yet implemented")
            return None
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def detect_language(self, audio_path):
        """
        Detect language from audio
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            str: Detected language code
        """
        try:
            # Transcribe first, then detect language from text
            text = self.transcribe(audio_path)
            
            if text:
                # Use langdetect for language detection
                from langdetect import detect
                lang = detect(text)
                print(f"🌍 Detected language: {lang}")
                return lang
            
            return None
            
        except Exception as e:
            print(f"❌ Language detection failed: {str(e)}")
            return None
    
    def batch_transcribe(self, audio_files):
        """
        Transcribe multiple audio files
        
        Args:
            audio_files: List of audio file paths
        
        Returns:
            dict: Dictionary mapping file paths to transcriptions
        """
        results = {}
        
        for audio_path in audio_files:
            print(f"\n📁 Processing: {audio_path}")
            text = self.transcribe(audio_path)
            results[audio_path] = text
        
        return results
    
    def validate_audio(self, audio_path):
        """
        Validate if audio file is suitable for transcription
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            tuple: (is_valid, message)
        """
        try:
            import soundfile as sf
            
            # Check if file exists
            if not Path(audio_path).exists():
                return False, "File does not exist"
            
            # Read audio info
            info = sf.info(audio_path)
            
            # Check duration
            if info.duration < 0.5:
                return False, f"Audio too short ({info.duration:.1f}s)"
            
            if info.duration > 300:  # 5 minutes
                return False, f"Audio too long ({info.duration:.1f}s). Maximum: 300s"
            
            # Check sample rate
            if info.samplerate < 8000:
                return False, f"Sample rate too low ({info.samplerate} Hz)"
            
            return True, f"Audio valid: {info.duration:.1f}s, {info.samplerate} Hz"
            
        except Exception as e:
            return False, f"Error validating audio: {str(e)}"
    
    def get_audio_info(self, audio_path):
        """
        Get detailed audio file information
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            dict: Audio information
        """
        try:
            import soundfile as sf
            
            info = sf.info(audio_path)
            
            return {
                'duration': info.duration,
                'sample_rate': info.samplerate,
                'channels': info.channels,
                'format': info.format,
                'subtype': info.subtype,
                'frames': info.frames
            }
            
        except Exception as e:
            print(f"❌ Error getting audio info: {str(e)}")
            return None
