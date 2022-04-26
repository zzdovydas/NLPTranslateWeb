import googletrans
import deepl

# Initializing Google trans and DeepL libraries
google_translator = googletrans.Translator()
deepl_translator = deepl.Translator("79a65e69-3772-0564-8f46-a5139c56d515:fx")

# This function is used to translate from lt language to specified language
def translate(language, text):
    translate_deepl = True
    if language[:3] == 'gt:':
        translate_deepl = False
        language = language[3:]
    google_translation = google_translator.translate(text, src='lt', dest=language)
    if translate_deepl:
        if language == 'en': language = 'en-us'
        try: # deepl has a 500000 character a month limit
            deepl_translation = deepl_translator.translate_text(text, source_lang="LT", target_lang=language.upper())
            return (google_translation.text, deepl_translation.text)
        except deepl.exceptions.QuotaExceededException:
            return (google_translation.text, '[Quota exceeded]')
    else: return (google_translation.text, '[Not supported]')

# This function is used to get API supported languages in HTML <select> format
def getSupportedLanguagesForSelect():
    google_languages = googletrans.LANGUAGES
    deepl_languages = deepl_translator.get_target_languages()
    forSelect = ''

    parsed_deepl = []
    for lang in deepl_languages:
        # english is one of the exceptions with different codes
        if lang.code == 'EN-US':
            parsed_deepl.append('en')
        else: parsed_deepl.append(lang.code.lower())

    for language in google_languages.keys():
        if language in parsed_deepl:
            forSelect += f"<option value='{language}'>{google_languages[language]}</option>"
        else: forSelect += f"<option value='gt:{language}'>{google_languages[language]} (Google Translate only)</option>"
    return forSelect