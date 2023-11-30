from background_calls import BackgroundCalls
from pathvalidate import ValidationError, validate_filename


class PdfCreation(BackgroundCalls):
    def __init__(self, callback, translate_text):
        super().__init__(callback=callback, translate_text=translate_text)

    def select_language(self, duration=10, message='Dictate in english the language you want to select.'):
        language = self.background_listening(
            duration, self._translate_text(message, self._language)).lower()

        if 'english' in language:
            self._language = 'en'
        elif 'italian' in language:
            self._language = 'it'

        """
        Supported languages:
        1) English [en]
        2) Italian [it]
        """

    def get_pdf_type(self, duration=10, message='What type of pdf you want to create? '):
        text = self.background_listening(
            duration, self._translate_text(message, self._language)).lower()

        if self._translate_text('notes', self._language) in text:
            return 'notes'
        elif 'gpt' in text or 'chatgpt' in text:
            return 'gpt'
        else:
            raise ValueError(
                self._translate_text('You can create note-only files or files that take advantage of chatgpt', self._language))

    def get_pdf_name(self, duration=12, message='What do you want to call your pdf?'):
        is_valid = True

        while True:
            try:
                if is_valid:
                    pdf_name = self.background_listening(
                        duration, self._translate_text(message, self._language)).strip()
                else:
                    pdf_name = self.background_listening(
                        duration, message=self._translate_text('Dictate a new and correct name for your pdf.', self._language)).strip()

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
            duration, self._translate_text(message, self._language)).strip()

    def get_notes_body(self, duration=30, message='Dictate your notes'):
        return self.background_listening(duration, self._translate_text(message, self._language)).strip()

    def get_prompt(self, duration=15, message='Dictate your prompt'):
        return self.background_listening(
            duration, self._translate_text(message, self._language)).strip()
    

