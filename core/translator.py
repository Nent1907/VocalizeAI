"""
Translator Module
Handles text translation between languages
"""

from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException


class Translator:
    """
    Text translation class using Google Translate
    """
    
    def __init__(self):
        """Initialize Translator"""
        self.translator = None
        self.supported_languages = self._get_supported_languages()
    
    def translate(self, text, target_lang, source_lang='auto'):
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code (e.g., 'en', 'tr', 'es')
            source_lang: Source language code (default: 'auto' for auto-detection)
        
        Returns:
            str: Translated text, or None if failed
        """
        try:
            if not text or text.strip() == "":
                print("⚠️ Empty text provided")
                return None
            
            print(f"🌍 Translating to: {target_lang}")
            
            # Auto-detect source language if not specified
            if source_lang == 'auto':
                try:
                    source_lang = detect(text)
                    print(f"🔍 Detected source language: {source_lang}")
                except LangDetectException:
                    print("⚠️ Could not detect source language, using 'en' as default")
                    source_lang = 'en'
            
            # Check if translation is needed
            if source_lang == target_lang:
                print("✅ Source and target languages are the same, no translation needed")
                return text
            
            # Initialize translator
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            
            # Translate
            translated_text = translator.translate(text)
            
            print(f"✅ Translation successful!")
            print(f"📝 Original: {text}")
            print(f"🗣️ Translated: {translated_text}")
            
            return translated_text
            
        except Exception as e:
            print(f"❌ Translation failed: {str(e)}")
            return None
    
    def translate_batch(self, texts, target_lang, source_lang='auto'):
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            target_lang: Target language code
            source_lang: Source language code (default: 'auto')
        
        Returns:
            list: List of translated texts
        """
        translated_texts = []
        
        for text in texts:
            translated = self.translate(text, target_lang, source_lang)
            translated_texts.append(translated)
        
        return translated_texts
    
    def detect_language(self, text):
        """
        Detect language of text
        
        Args:
            text: Text to analyze
        
        Returns:
            str: Detected language code, or None if failed
        """
        try:
            lang = detect(text)
            return lang
        except Exception as e:
            print(f"❌ Language detection failed: {str(e)}")
            return None
    
    def get_language_name(self, lang_code):
        """
        Get language name from code
        
        Args:
            lang_code: Language code (e.g., 'en', 'tr')
        
        Returns:
            str: Language name
        """
        language_names = {
            'en': 'English',
            'tr': 'Turkish',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'nl': 'Dutch',
            'pl': 'Polish',
            'sv': 'Swedish',
            'hi': 'Hindi',
            'cs': 'Czech',
            'da': 'Danish',
            'fi': 'Finnish',
            'el': 'Greek',
            'hu': 'Hungarian',
            'id': 'Indonesian',
            'no': 'Norwegian',
            'ro': 'Romanian',
            'sk': 'Slovak',
            'uk': 'Ukrainian',
            'vi': 'Vietnamese',
            'th': 'Thai',
            'bg': 'Bulgarian'
        }
        
        return language_names.get(lang_code, lang_code.upper())
    
    def _get_supported_languages(self):
        """
        Get list of supported language codes
        
        Returns:
            list: List of supported language codes
        """
        return [
            'en', 'tr', 'es', 'fr', 'de', 'it', 'pt', 'ru',
            'ja', 'ko', 'zh', 'ar', 'nl', 'pl', 'sv', 'hi',
            'cs', 'da', 'fi', 'el', 'hu', 'id', 'no', 'ro',
            'sk', 'uk', 'vi', 'th', 'bg'
        ]
    
    def is_language_supported(self, lang_code):
        """
        Check if language is supported
        
        Args:
            lang_code: Language code to check
        
        Returns:
            bool: True if supported, False otherwise
        """
        return lang_code in self.supported_languages
    
    def translate_with_alternatives(self, text, target_lang, source_lang='auto'):
        """
        Translate text and provide alternative translations
        
        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code (default: 'auto')
        
        Returns:
            dict: Dictionary with main translation and alternatives
        """
        try:
            # Main translation
            main_translation = self.translate(text, target_lang, source_lang)
            
            # For now, return just the main translation
            # In future, could add multiple translation engines for alternatives
            return {
                'main': main_translation,
                'alternatives': []
            }
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def validate_text(self, text, max_length=5000):
        """
        Validate if text is suitable for translation
        
        Args:
            text: Text to validate
            max_length: Maximum allowed length (default: 5000)
        
        Returns:
            tuple: (is_valid, message)
        """
        if not text or text.strip() == "":
            return False, "Text is empty"
        
        if len(text) > max_length:
            return False, f"Text too long ({len(text)} chars). Maximum: {max_length}"
        
        return True, "Text valid"
    
    def split_long_text(self, text, max_chunk_size=1000):
        """
        Split long text into chunks for translation
        
        Args:
            text: Text to split
            max_chunk_size: Maximum size of each chunk (default: 1000)
        
        Returns:
            list: List of text chunks
        """
        # Split by sentences
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def translate_long_text(self, text, target_lang, source_lang='auto', max_chunk_size=1000):
        """
        Translate long text by splitting into chunks
        
        Args:
            text: Long text to translate
            target_lang: Target language code
            source_lang: Source language code (default: 'auto')
            max_chunk_size: Maximum size of each chunk (default: 1000)
        
        Returns:
            str: Translated text
        """
        try:
            # Split text
            chunks = self.split_long_text(text, max_chunk_size)
            
            # Translate each chunk
            translated_chunks = []
            for i, chunk in enumerate(chunks):
                print(f"📄 Translating chunk {i+1}/{len(chunks)}...")
                translated = self.translate(chunk, target_lang, source_lang)
                if translated:
                    translated_chunks.append(translated)
            
            # Combine translated chunks
            full_translation = " ".join(translated_chunks)
            
            return full_translation
            
        except Exception as e:
            print(f"❌ Long text translation failed: {str(e)}")
            return None
