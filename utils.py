from deep_translator import GoogleTranslator as gt


def translate_text(text, language):
    return gt(target=language).translate(
        text)
