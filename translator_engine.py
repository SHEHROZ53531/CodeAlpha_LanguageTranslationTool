from deep_translator import GoogleTranslator
from config import SUPPORTED_LANGUAGES

def translate_text(text, source_lang_name, target_lang_name):
    """
    Takes input text and language names, maps them to their ISO codes,
    and returns the translated string.
    """
    # Defensive checks for empty inputs
    if not text.strip():
        return "Error: Please enter some text to translate."
    
    try:
        # Get the strict language codes from our config dictionary
        src_code = SUPPORTED_LANGUAGES.get(source_lang_name)
        tgt_code = SUPPORTED_LANGUAGES.get(target_lang_name)
        
        # Double check if valid mapping exists
        if not src_code or not tgt_code:
            return "Error: Invalid language selection."
            
        # Initialize the translator and process the translation
        translator = GoogleTranslator(source=src_code, target=tgt_code)
        translated_result = translator.translate(text)
        
        return translated_result
        
    except Exception as error:
        # Catch connection timeouts or API issues cleanly
        return f"Translation failed. Please check your internet connection. (Details: {error})"