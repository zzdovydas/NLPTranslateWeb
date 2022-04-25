import googletrans
import deepl

# Initializing Google trans and DeepL libraries
google_translator = googletrans.Translator()
deepl_translator = deepl.Translator("79a65e69-3772-0564-8f46-a5139c56d515:fx")

# This function is used to translate from lt language to specified language
def translate(language, text):
    google_translation = google_translator.translate(text, src='lt', dest=language)
    if language == 'en': language = 'en-us'
    try: # deepl has a 500000 character a month limit
        deepl_translation = deepl_translator.translate_text(text, source_lang="LT", target_lang=language.upper())
    except deepl.exceptions.QuotaExceededException:
        return (google_translation.text, '')
    return (google_translation.text, deepl_translation.text)

# This function is used to get API supported languages in HTML <select> format
def getSupportedLanguagesForSelect():
    google_languages = googletrans.LANGUAGES
    deepl_languages = deepl_translator.get_target_languages()
    langSelect = ''
    for language in deepl_languages:
        lang_code = language.code.lower()
        # english is one of the exceptions with different codes
        if lang_code == 'en-us':
            langSelect += f"<option value='en'>english</option>"
        if lang_code in google_languages.keys():
            langSelect += f"<option value='{lang_code}'>{google_languages[lang_code]}</option>"
    return langSelect
