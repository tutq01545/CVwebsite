from googletrans import Translator


# Function
def translate(language_code: str, text: str):
    translator = Translator()
    try:
        translated_text = translator.translate(dest=language_code, text=text).text
    except Exception as e:
        print("Translation does not work because of error: ", e)
        translated_text = ""
    return translated_text
