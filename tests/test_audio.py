"""
Audio Module Tests
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import Config
from utils.audio_utils import AudioUtils
from utils.validators import Validators


class TestAudioUtils(unittest.TestCase):
    """Test audio utility functions"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = Config()
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        original = "my test file<>:.wav"
        sanitized = Validators.sanitize_filename(original)
        
        self.assertNotIn('<', sanitized)
        self.assertNotIn('>', sanitized)
        self.assertNotIn(':', sanitized)
    
    def test_validate_sample_rate(self):
        """Test sample rate validation"""
        valid, msg = Validators.validate_sample_rate(44100)
        self.assertTrue(valid)
        
        valid, msg = Validators.validate_sample_rate(1000)
        self.assertFalse(valid)
    
    def test_validate_channels(self):
        """Test channel validation"""
        valid, msg = Validators.validate_channels(1)
        self.assertTrue(valid)
        
        valid, msg = Validators.validate_channels(3)
        self.assertFalse(valid)


class TestValidators(unittest.TestCase):
    """Test validator functions"""
    
    def test_validate_text_length(self):
        """Test text length validation"""
        short_text = "Hello"
        valid, msg = Validators.validate_text_length(short_text)
        self.assertTrue(valid)
        
        long_text = "a" * 10000
        valid, msg = Validators.validate_text_length(long_text, max_length=5000)
        self.assertFalse(valid)
    
    def test_validate_voice_name(self):
        """Test voice name validation"""
        valid, msg = Validators.validate_voice_name("MyVoice")
        self.assertTrue(valid)
        
        valid, msg = Validators.validate_voice_name("ab")
        self.assertFalse(valid)
    
    def test_validate_email(self):
        """Test email validation"""
        valid, msg = Validators.validate_email("test@example.com")
        self.assertTrue(valid)
        
        valid, msg = Validators.validate_email("invalid-email")
        self.assertFalse(valid)


if __name__ == '__main__':
    unittest.main()
