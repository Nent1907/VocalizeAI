"""
Configuration Module
Application settings and constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """
    Application configuration class
    """
    
    # Application Info
    APP_NAME = os.getenv("APP_NAME", "EchoMinds")
    VERSION = "1.0.0"
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # API Keys
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    
    # Audio Settings
    SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", 44100))
    CHANNELS = int(os.getenv("CHANNELS", 1))
    AUDIO_FORMAT = os.getenv("AUDIO_FORMAT", "wav")
    
    # Directory Paths
    BASE_DIR = Path(__file__).parent.parent
    ASSETS_DIR = BASE_DIR / "assets"
    TEMP_DIR = os.getenv("TEMP_DIR", str(ASSETS_DIR / "temp"))
    CLONED_VOICES_DIR = os.getenv("CLONED_VOICES_DIR", str(ASSETS_DIR / "cloned_voices"))
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", str(ASSETS_DIR / "outputs"))
    
    # Recording Limits
    MIN_RECORDING_DURATION = int(os.getenv("MIN_RECORDING_DURATION", 3))
    MAX_RECORDING_DURATION = int(os.getenv("MAX_RECORDING_DURATION", 600))
    DEFAULT_RECORDING_DURATION = int(os.getenv("DEFAULT_RECORDING_DURATION", 30))
    
    # API Settings
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    
    # Voice Cloning Settings
    VOICE_CLONE_TYPE = os.getenv("VOICE_CLONE_TYPE", "instant")
    
    # TTS Settings
    DEFAULT_VOICE_STABILITY = float(os.getenv("DEFAULT_VOICE_STABILITY", 0.5))
    DEFAULT_VOICE_SIMILARITY = float(os.getenv("DEFAULT_VOICE_SIMILARITY", 0.75))
    DEFAULT_SPEECH_RATE = float(os.getenv("DEFAULT_SPEECH_RATE", 1.0))
    
    # Translation Settings
    DEFAULT_SOURCE_LANG = os.getenv("DEFAULT_SOURCE_LANG", "auto")
    DEFAULT_TARGET_LANG = os.getenv("DEFAULT_TARGET_LANG", "en")
    
    # UI Settings
    THEME = os.getenv("THEME", "light")
    
    # Cache Settings
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "True").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))
    
    # Supported Languages with flags and names
    SUPPORTED_LANGUAGES = {
        'en': {'name': 'English', 'flag': '🇺🇸'},
        'tr': {'name': 'Turkish', 'flag': '🇹🇷'},
        'es': {'name': 'Spanish', 'flag': '🇪🇸'},
        'fr': {'name': 'French', 'flag': '🇫🇷'},
        'de': {'name': 'German', 'flag': '🇩🇪'},
        'it': {'name': 'Italian', 'flag': '🇮🇹'},
        'pt': {'name': 'Portuguese', 'flag': '🇵🇹'},
        'ru': {'name': 'Russian', 'flag': '🇷🇺'},
        'ja': {'name': 'Japanese', 'flag': '🇯🇵'},
        'ko': {'name': 'Korean', 'flag': '🇰🇷'},
        'zh': {'name': 'Chinese', 'flag': '🇨🇳'},
        'ar': {'name': 'Arabic', 'flag': '🇦🇪'},
        'nl': {'name': 'Dutch', 'flag': '🇳🇱'},
        'pl': {'name': 'Polish', 'flag': '🇵🇱'},
        'sv': {'name': 'Swedish', 'flag': '🇸🇪'},
        'hi': {'name': 'Hindi', 'flag': '🇮🇳'},
        'cs': {'name': 'Czech', 'flag': '🇨🇿'},
        'da': {'name': 'Danish', 'flag': '🇩🇰'},
        'fi': {'name': 'Finnish', 'flag': '🇫🇮'},
        'el': {'name': 'Greek', 'flag': '🇬🇷'},
        'hu': {'name': 'Hungarian', 'flag': '🇭🇺'},
        'id': {'name': 'Indonesian', 'flag': '🇮🇩'},
        'no': {'name': 'Norwegian', 'flag': '🇳🇴'},
        'ro': {'name': 'Romanian', 'flag': '🇷🇴'},
        'sk': {'name': 'Slovak', 'flag': '🇸🇰'},
        'uk': {'name': 'Ukrainian', 'flag': '🇺🇦'},
        'vi': {'name': 'Vietnamese', 'flag': '🇻🇳'},
        'th': {'name': 'Thai', 'flag': '🇹🇭'},
        'bg': {'name': 'Bulgarian', 'flag': '🇧🇬'}
    }
    
    # ElevenLabs Models
    TTS_MODELS = {
        'monolingual': 'eleven_monolingual_v1',
        'multilingual': 'eleven_multilingual_v2',
        'turbo': 'eleven_turbo_v2'
    }
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.TEMP_DIR,
            cls.CLONED_VOICES_DIR,
            cls.OUTPUT_DIR
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
            # Create .gitkeep file
            gitkeep = Path(directory) / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
    
    @classmethod
    def validate_config(cls):
        """
        Validate configuration settings
        
        Returns:
            tuple: (is_valid, errors_list)
        """
        errors = []
        
        # Check API key
        if not cls.ELEVENLABS_API_KEY:
            errors.append("ELEVENLABS_API_KEY is not set")
        
        # Check sample rate
        if cls.SAMPLE_RATE < 8000 or cls.SAMPLE_RATE > 48000:
            errors.append(f"Invalid SAMPLE_RATE: {cls.SAMPLE_RATE}")
        
        # Check channels
        if cls.CHANNELS not in [1, 2]:
            errors.append(f"Invalid CHANNELS: {cls.CHANNELS}")
        
        # Check recording durations
        if cls.MIN_RECORDING_DURATION < 1:
            errors.append(f"MIN_RECORDING_DURATION too small: {cls.MIN_RECORDING_DURATION}")
        
        if cls.MAX_RECORDING_DURATION < cls.MIN_RECORDING_DURATION:
            errors.append("MAX_RECORDING_DURATION must be >= MIN_RECORDING_DURATION")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    @classmethod
    def get_config_summary(cls):
        """
        Get configuration summary as dictionary
        
        Returns:
            dict: Configuration summary
        """
        return {
            'app_name': cls.APP_NAME,
            'version': cls.VERSION,
            'debug_mode': cls.DEBUG_MODE,
            'sample_rate': cls.SAMPLE_RATE,
            'channels': cls.CHANNELS,
            'min_recording': cls.MIN_RECORDING_DURATION,
            'max_recording': cls.MAX_RECORDING_DURATION,
            'voice_clone_type': cls.VOICE_CLONE_TYPE,
            'supported_languages': len(cls.SUPPORTED_LANGUAGES)
        }
    
    @classmethod
    def print_config(cls):
        """Print configuration to console"""
        print("=" * 60)
        print(f"🎙️ {cls.APP_NAME} v{cls.VERSION}")
        print("=" * 60)
        print(f"Debug Mode: {cls.DEBUG_MODE}")
        print(f"Sample Rate: {cls.SAMPLE_RATE} Hz")
        print(f"Channels: {cls.CHANNELS}")
        print(f"Recording: {cls.MIN_RECORDING_DURATION}-{cls.MAX_RECORDING_DURATION}s")
        print(f"Voice Clone Type: {cls.VOICE_CLONE_TYPE}")
        print(f"Supported Languages: {len(cls.SUPPORTED_LANGUAGES)}")
        print("=" * 60)


# Initialize directories on import
Config.ensure_directories()
