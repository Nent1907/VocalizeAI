"""
Translation Tests
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.translator import Translator
from utils.config import Config


class TestTranslation(unittest.TestCase):
    """Test translation functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.translator = Translator()
        self.config = Config()
    
    def test_detect_language(self):
        """Test language detection"""
        # English text
        lang = self.translator.detect_language("Hello, how are you?")
        self.assertEqual(lang, 'en')
        
        # Turkish text
        lang = self.translator.detect_language("Merhaba, nasılsın?")
        self.assertEqual(lang, 'tr')
    
    def test_get_language_name(self):
        """Test language name retrieval"""
        name = self.translator.get_language_name('en')
        self.assertEqual(name, 'English')
        
        name = self.translator.get_language_name('tr')
        self.assertEqual(name, 'Turkish')
    
    def test_is_language_supported(self):
        """Test language support check"""
        self.assertTrue(self.translator.is_language_supported('en'))
        self.assertTrue(self.translator.is_language_supported('tr'))
        self.assertFalse(self.translator.is_language_supported('xyz'))
    
    def test_validate_text(self):
        """Test text validation"""
        valid, msg = self.translator.validate_text("Hello")
        self.assertTrue(valid)
        
        valid, msg = self.translator.validate_text("")
        self.assertFalse(valid)
    
    def test_split_long_text(self):
        """Test long text splitting"""
        long_text = " ".join(["sentence"] * 100)
        chunks = self.translator.split_long_text(long_text, max_chunk_size=100)
        
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 150)  # Some margin for sentence boundaries


if __name__ == '__main__':
    unittest.main()
