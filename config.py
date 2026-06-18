# Mapping of user-friendly language names to their respective ISO codes required by deep-translator
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
    "Arabic": "ar",
    "German": "de",
    "Chinese": "zh-CN",
    "Hindi": "hi"
}

def get_language_list():
    """Returns a simple list of language names for our frontend dropdowns."""
    return list(SUPPORTED_LANGUAGES.keys())