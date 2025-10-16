"""
Voice Cloner Module
Handles voice cloning using ElevenLabs API
"""

from elevenlabs import ElevenLabs, Voice, VoiceSettings
from pathlib import Path
import time


class VoiceCloner:
    """
    Voice cloning class using ElevenLabs API
    """
    
    def __init__(self, api_key):
        """
        Initialize VoiceCloner
        
        Args:
            api_key: ElevenLabs API key
        """
        self.api_key = api_key
        self.client = ElevenLabs(api_key=api_key)
        
        # Ensure cloned voices directory exists
        self.cloned_voices_dir = Path("assets/cloned_voices")
        self.cloned_voices_dir.mkdir(parents=True, exist_ok=True)
    
    def clone_voice(self, audio_path, voice_name, description="Cloned voice"):
        """
        Clone a voice from audio file
        
        Args:
            audio_path: Path to audio file for cloning
            voice_name: Name for the cloned voice
            description: Description of the voice (optional)
        
        Returns:
            str: Voice ID of cloned voice, or None if failed
        """
        try:
            print(f"🧬 Cloning voice from: {audio_path}")
            print(f"📝 Voice name: {voice_name}")
            
            # Read audio file
            with open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clone voice using ElevenLabs API
            # Note: Using the instant voice cloning approach
            voice = self.client.clone(
                name=voice_name,
                description=description,
                files=[audio_path]
            )
            
            voice_id = voice.voice_id
            
            print(f"✅ Voice cloned successfully!")
            print(f"🆔 Voice ID: {voice_id}")
            
            # Save voice info locally
            self._save_voice_info(voice_id, voice_name, audio_path)
            
            return voice_id
            
        except Exception as e:
            print(f"❌ Voice cloning failed: {str(e)}")
            return None
    
    def clone_voice_professional(self, audio_files, voice_name, labels=None):
        """
        Clone voice with professional quality (requires multiple audio files)
        
        Args:
            audio_files: List of audio file paths
            voice_name: Name for the cloned voice
            labels: Dictionary mapping audio files to labels (optional)
        
        Returns:
            str: Voice ID of cloned voice, or None if failed
        """
        try:
            print(f"🎭 Professional voice cloning started...")
            print(f"📁 Audio files: {len(audio_files)}")
            
            # This would use ElevenLabs professional voice cloning
            # Requires multiple audio samples and better quality
            # Implementation depends on ElevenLabs SDK version
            
            voice = self.client.clone(
                name=voice_name,
                files=audio_files,
                description="Professional cloned voice"
            )
            
            voice_id = voice.voice_id
            
            print(f"✅ Professional voice cloned!")
            print(f"🆔 Voice ID: {voice_id}")
            
            return voice_id
            
        except Exception as e:
            print(f"❌ Professional cloning failed: {str(e)}")
            return None
    
    def get_voice_info(self, voice_id):
        """
        Get information about a cloned voice
        
        Args:
            voice_id: ID of the voice
        
        Returns:
            dict: Voice information
        """
        try:
            voices = self.client.voices.get_all()
            
            for voice in voices.voices:
                if voice.voice_id == voice_id:
                    return {
                        'voice_id': voice.voice_id,
                        'name': voice.name,
                        'category': voice.category,
                        'description': voice.description if hasattr(voice, 'description') else None,
                        'labels': voice.labels if hasattr(voice, 'labels') else None
                    }
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting voice info: {str(e)}")
            return None
    
    def list_cloned_voices(self):
        """
        List all cloned voices in the account
        
        Returns:
            list: List of voice dictionaries
        """
        try:
            voices = self.client.voices.get_all()
            cloned_voices = []
            
            for voice in voices.voices:
                # Filter for cloned voices (category would be 'cloned')
                if hasattr(voice, 'category') and 'clone' in voice.category.lower():
                    cloned_voices.append({
                        'voice_id': voice.voice_id,
                        'name': voice.name,
                        'category': voice.category
                    })
            
            return cloned_voices
            
        except Exception as e:
            print(f"❌ Error listing voices: {str(e)}")
            return []
    
    def delete_voice(self, voice_id):
        """
        Delete a cloned voice
        
        Args:
            voice_id: ID of the voice to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.client.voices.delete(voice_id)
            print(f"✅ Voice {voice_id} deleted successfully!")
            
            # Remove local info file
            info_file = self.cloned_voices_dir / f"{voice_id}.txt"
            if info_file.exists():
                info_file.unlink()
            
            return True
            
        except Exception as e:
            print(f"❌ Error deleting voice: {str(e)}")
            return False
    
    def _save_voice_info(self, voice_id, voice_name, audio_path):
        """
        Save voice information locally
        
        Args:
            voice_id: Voice ID
            voice_name: Voice name
            audio_path: Path to source audio file
        """
        try:
            info_file = self.cloned_voices_dir / f"{voice_id}.txt"
            
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write(f"Voice ID: {voice_id}\n")
                f.write(f"Voice Name: {voice_name}\n")
                f.write(f"Source Audio: {audio_path}\n")
                f.write(f"Created: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f"💾 Voice info saved to: {info_file}")
            
        except Exception as e:
            print(f"⚠️ Could not save voice info: {str(e)}")
    
    def validate_audio_for_cloning(self, audio_path, min_duration=3, max_duration=600):
        """
        Validate if audio file is suitable for voice cloning
        
        Args:
            audio_path: Path to audio file
            min_duration: Minimum duration in seconds (default: 3)
            max_duration: Maximum duration in seconds (default: 600)
        
        Returns:
            tuple: (is_valid, message)
        """
        try:
            import soundfile as sf
            
            # Read audio file info
            info = sf.info(audio_path)
            duration = info.duration
            sample_rate = info.samplerate
            channels = info.channels
            
            # Check duration
            if duration < min_duration:
                return False, f"Audio too short ({duration:.1f}s). Minimum: {min_duration}s"
            
            if duration > max_duration:
                return False, f"Audio too long ({duration:.1f}s). Maximum: {max_duration}s"
            
            # Check sample rate (prefer 44100 Hz or higher)
            if sample_rate < 16000:
                return False, f"Sample rate too low ({sample_rate} Hz). Recommended: 44100 Hz"
            
            # Check if mono or stereo
            if channels > 2:
                return False, f"Too many channels ({channels}). Use mono or stereo."
            
            return True, f"Audio valid: {duration:.1f}s, {sample_rate} Hz, {channels} channel(s)"
            
        except Exception as e:
            return False, f"Error validating audio: {str(e)}"
    
    def get_voice_settings(self, stability=0.5, similarity=0.75):
        """
        Get voice settings for TTS
        
        Args:
            stability: Voice stability (0.0 to 1.0)
            similarity: Voice similarity boost (0.0 to 1.0)
        
        Returns:
            VoiceSettings: Voice settings object
        """
        return VoiceSettings(
            stability=stability,
            similarity_boost=similarity
        )
