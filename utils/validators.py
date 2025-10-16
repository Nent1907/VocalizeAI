"""
Validators Module
Input validation functions
"""

import re
from pathlib import Path


class Validators:
    """
    Validation utility class
    """
    
    @staticmethod
    def validate_api_key(api_key):
        """
        Validate ElevenLabs API key format
        
        Args:
            api_key: API key string
        
        Returns:
            tuple: (is_valid, message)
        """
        if not api_key:
            return False, "API key is empty"
        
        if len(api_key) < 20:
            return False, "API key too short"
        
        # Basic format check
        if not re.match(r'^[a-zA-Z0-9]+$', api_key):
            return False, "API key contains invalid characters"
        
        return True, "API key valid"
    
    @staticmethod
    def validate_audio_file(file_path):
        """
        Validate audio file existence and format
        
        Args:
            file_path: Path to audio file
        
        Returns:
            tuple: (is_valid, message)
        """
        path = Path(file_path)
        
        if not path.exists():
            return False, "File does not exist"
        
        if not path.is_file():
            return False, "Path is not a file"
        
        valid_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a']
        if path.suffix.lower() not in valid_extensions:
            return False, f"Invalid file format. Supported: {', '.join(valid_extensions)}"
        
        # Check file size (max 50MB)
        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > 50:
            return False, f"File too large ({file_size_mb:.1f}MB). Maximum: 50MB"
        
        return True, "Audio file valid"
    
    @staticmethod
    def validate_text_length(text, max_length=5000):
        """
        Validate text length
        
        Args:
            text: Text string
            max_length: Maximum allowed length
        
        Returns:
            tuple: (is_valid, message)
        """
        if not text or text.strip() == "":
            return False, "Text is empty"
        
        if len(text) > max_length:
            return False, f"Text too long ({len(text)} chars). Maximum: {max_length}"
        
        return True, f"Text valid ({len(text)} chars)"
    
    @staticmethod
    def validate_language_code(lang_code, supported_languages):
        """
        Validate language code
        
        Args:
            lang_code: Language code (e.g., 'en', 'tr')
            supported_languages: Dictionary of supported languages
        
        Returns:
            tuple: (is_valid, message)
        """
        if not lang_code:
            return False, "Language code is empty"
        
        if lang_code not in supported_languages:
            return False, f"Language '{lang_code}' not supported"
        
        return True, f"Language '{lang_code}' is supported"
    
    @staticmethod
    def validate_voice_name(name):
        """
        Validate voice name
        
        Args:
            name: Voice name string
        
        Returns:
            tuple: (is_valid, message)
        """
        if not name or name.strip() == "":
            return False, "Voice name is empty"
        
        if len(name) < 3:
            return False, "Voice name too short (minimum 3 characters)"
        
        if len(name) > 50:
            return False, "Voice name too long (maximum 50 characters)"
        
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9_\-\s]+$', name):
            return False, "Voice name contains invalid characters"
        
        return True, "Voice name valid"
    
    @staticmethod
    def validate_recording_duration(duration, min_duration=3, max_duration=600):
        """
        Validate recording duration
        
        Args:
            duration: Duration in seconds
            min_duration: Minimum allowed duration
            max_duration: Maximum allowed duration
        
        Returns:
            tuple: (is_valid, message)
        """
        try:
            duration = float(duration)
        except (ValueError, TypeError):
            return False, "Invalid duration value"
        
        if duration < min_duration:
            return False, f"Duration too short ({duration}s). Minimum: {min_duration}s"
        
        if duration > max_duration:
            return False, f"Duration too long ({duration}s). Maximum: {max_duration}s"
        
        return True, f"Duration valid ({duration}s)"
    
    @staticmethod
    def validate_stability_value(stability):
        """
        Validate voice stability value
        
        Args:
            stability: Stability value (0.0 to 1.0)
        
        Returns:
            tuple: (is_valid, message)
        """
        try:
            stability = float(stability)
        except (ValueError, TypeError):
            return False, "Invalid stability value"
        
        if stability < 0.0 or stability > 1.0:
            return False, f"Stability must be between 0.0 and 1.0 (got {stability})"
        
        return True, f"Stability valid ({stability})"
    
    @staticmethod
    def validate_similarity_value(similarity):
        """
        Validate voice similarity value
        
        Args:
            similarity: Similarity value (0.0 to 1.0)
        
        Returns:
            tuple: (is_valid, message)
        """
        try:
            similarity = float(similarity)
        except (ValueError, TypeError):
            return False, "Invalid similarity value"
        
        if similarity < 0.0 or similarity > 1.0:
            return False, f"Similarity must be between 0.0 and 1.0 (got {similarity})"
        
        return True, f"Similarity valid ({similarity})"
    
    @staticmethod
    def validate_email(email):
        """
        Validate email address
        
        Args:
            email: Email address string
        
        Returns:
            tuple: (is_valid, message)
        """
        if not email:
            return False, "Email is empty"
        
        # Basic email regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        return True, "Email valid"
    
    @staticmethod
    def validate_url(url):
        """
        Validate URL
        
        Args:
            url: URL string
        
        Returns:
            tuple: (is_valid, message)
        """
        if not url:
            return False, "URL is empty"
        
        # Basic URL regex
        url_pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        
        if not re.match(url_pattern, url):
            return False, "Invalid URL format"
        
        return True, "URL valid"
    
    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize filename by removing invalid characters
        
        Args:
            filename: Original filename
        
        Returns:
            str: Sanitized filename
        """
        # Remove invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
        
        # Replace spaces with underscores
        sanitized = sanitized.replace(' ', '_')
        
        # Limit length
        if len(sanitized) > 100:
            name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
            sanitized = name[:95] + ('.' + ext if ext else '')
        
        return sanitized
    
    @staticmethod
    def validate_file_path(file_path, must_exist=True):
        """
        Validate file path
        
        Args:
            file_path: Path to validate
            must_exist: Whether file must exist (default: True)
        
        Returns:
            tuple: (is_valid, message)
        """
        try:
            path = Path(file_path)
            
            if must_exist and not path.exists():
                return False, "Path does not exist"
            
            if must_exist and not path.is_file():
                return False, "Path is not a file"
            
            # Check if path is valid
            if not path.parent.exists():
                return False, "Parent directory does not exist"
            
            return True, "Path valid"
            
        except Exception as e:
            return False, f"Invalid path: {str(e)}"
    
    @staticmethod
    def validate_directory(directory, create_if_missing=False):
        """
        Validate directory path
        
        Args:
            directory: Directory path
            create_if_missing: Create directory if it doesn't exist
        
        Returns:
            tuple: (is_valid, message)
        """
        try:
            path = Path(directory)
            
            if not path.exists():
                if create_if_missing:
                    path.mkdir(parents=True, exist_ok=True)
                    return True, "Directory created"
                else:
                    return False, "Directory does not exist"
            
            if not path.is_dir():
                return False, "Path is not a directory"
            
            return True, "Directory valid"
            
        except Exception as e:
            return False, f"Invalid directory: {str(e)}"
    
    @staticmethod
    def validate_sample_rate(sample_rate):
        """
        Validate audio sample rate
        
        Args:
            sample_rate: Sample rate in Hz
        
        Returns:
            tuple: (is_valid, message)
        """
        try:
            sample_rate = int(sample_rate)
        except (ValueError, TypeError):
            return False, "Invalid sample rate value"
        
        valid_rates = [8000, 16000, 22050, 44100, 48000]
        
        if sample_rate not in valid_rates:
            return False, f"Sample rate must be one of: {valid_rates}"
        
        return True, f"Sample rate valid ({sample_rate} Hz)"
    
    @staticmethod
    def validate_channels(channels):
        """
        Validate audio channels
        
        Args:
            channels: Number of channels
        
        Returns:
            tuple: (is_valid, message)
        """
        try:
            channels = int(channels)
        except (ValueError, TypeError):
            return False, "Invalid channels value"
        
        if channels not in [1, 2]:
            return False, "Channels must be 1 (mono) or 2 (stereo)"
        
        return True, f"Channels valid ({channels})"
