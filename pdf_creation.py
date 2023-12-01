from call_creation import CreateCall
from pathvalidate import ValidationError, validate_filename


class PdfCreation(CreateCall):

    LANGUAGES = {
        'english': 'en',
        'italian': 'it',
        'albanian': 'sq',
        'chinese': 'zw-TW',
        'french': 'fr',
        'latin': 'la',
        'greek': 'el',
        'arabic': 'ar',
        'spanish': 'es',
        'german': 'de'
    }

    def __init__(self, callback, translate_text):
        super().__init__(callback=callback, translate_text=translate_text)

    def select_language(self, duration=10, message='Dictate in english the language you want to select.'):
        selected_language = self.background_listening(
            duration, self._translate_text(message, self.language)).lower()

        for key in self.LANGUAGES:
            if key in selected_language:
                self.language = self.LANGUAGES[key]
                return self.LANGUAGES[key]

        """
        Supported languages:

        1) english: 'en'
        2) albanian: 'sq'
        3) chinese (traditional): 'zh-TW'
        4) italian: 'it'
        5) french: 'fr'
        6) latin: 'la'
        7) greek: 'el'
        8) arabic: 'ar'
        9) spanish: 'es'
        10) german: 'de'
        """

    def get_pdf_type(self, duration=12, message='What type of pdf you want to create? '):
        text = self.background_listening(
            duration, self._translate_text(message, self.language)).lower()

        if self._translate_text('notes', self.language) in text:
            return 'notes'
        elif 'gpt' in text or 'chatgpt' in text:
            return 'gpt'
        else:
            raise ValueError(
                self._translate_text('You can create note-only files or files that take advantage of chatgpt', self.language))

    def get_pdf_name(self, duration=12, message='What do you want to call your pdf?'):
        is_valid = True

        while True:
            try:
                if is_valid:
                    pdf_name = self.background_listening(
                        duration, self._translate_text(message, self.language)).strip()
                else:
                    pdf_name = self.background_listening(
                        duration, message=self._translate_text('Dictate a new and correct name for your pdf.', self.language)).strip()

                if not pdf_name:
                    raise ValueError

                pdf_name += '.pdf'

                validate_filename(pdf_name)

            except (ValidationError, ValueError) as e:
                is_valid = False
                print('Invalid name.', e)

            else:
                return pdf_name

    def get_notes_title(self, duration=15, message='What title do you want to give your notes?'):
        return self.background_listening(
            duration, self._translate_text(message, self.language)).strip()

    def get_notes_body(self, duration=30, message='Dictate your notes'):
        return self.background_listening(duration, self._translate_text(message, self.language)).strip()

    def get_prompt(self, duration=15, message='Dictate your prompt'):
        return self.background_listening(
            duration, self._translate_text(message, self.language)).strip()
