import googletrans
from googletrans import Translator

translator = Translator()

def translate(language, text):
    translation = translator.translate(text, src='lt', dest=language)
    print(translation.text)
    return translation.text

def getSupportedLanguagesForSelect():
    languages = googletrans.LANGUAGES
    forSelect = ''
    for language in languages:
	    forSelect = forSelect + "<option value='" + language + "'>" + languages[language] + "</option>"
    return forSelect