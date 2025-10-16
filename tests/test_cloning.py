"""
Voice Cloning Tests
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.validators import Validators


class TestVoiceCloning(unittest.TestCase):
    """Test voice cloning functionality"""
    
    def test_validate_voice_name(self):
        """Test voice name validation"""
        # Valid names
        valid_names = ["MyVoice", "Voice_1", "Test-Voice", "Voice 123"]
        for name in valid_names:
            valid, msg = Validators.validate_voice_name(name)
            self.assertTrue(valid, f"Name '{name}' should be valid")
        
        # Invalid names
        invalid_names = ["ab", "", "a" * 100, "Voice@123"]
        for name in invalid_names:
            valid, msg = Validators.validate_voice_name(name)
            self.assertFalse(valid, f"Name '{name}' should be invalid")
    
    def test_validate_stability(self):
        """Test stability value validation"""
        valid, msg = Validators.validate_stability_value(0.5)
        self.assertTrue(valid)
        
        valid, msg = Validators.validate_stability_value(1.5)
        self.assertFalse(valid)
        
        valid, msg = Validators.validate_stability_value(-0.1)
        self.assertFalse(valid)
    
    def test_validate_similarity(self):
        """Test similarity value validation"""
        valid, msg = Validators.validate_similarity_value(0.75)
        self.assertTrue(valid)
        
        valid, msg = Validators.validate_similarity_value(2.0)
        self.assertFalse(valid)


if __name__ == '__main__':
    unittest.main()
