import speech_recognition as sr
from speech_recognition import Recognizer
import time
import sys
from pathvalidate import validate_filename, ValidationError
from pdf_types import GptPDF, NotesPDF
from openai import OpenAI


class PdfCreation(Recognizer):
    _data = []
    _stop = False

    def __init__(self, callback, open_ai_client: OpenAI):

        assert isinstance(
            open_ai_client, OpenAI), 'Il parametro [open_ai_client] deve essere di tipo [OpenAI]'

        self._callback = callback
        self._client = open_ai_client
        self._mic = sr.Microphone()

        super().__init__()

    def background_listening(self, duration, message: str):
        text_data = ''

        with self._mic as source:
            print("Adattando il microfono per i rumori nell'ambiente...")
            self.adjust_for_ambient_noise(source)
            print('Microfono pronto')

        print(message)

        stop_recognition = self.listen_in_background(source, self._callback)

        for _ in range(duration):
            if self._stop:
                self._data.clear()
                sys.exit('Registrazione terminata')
            time.sleep(1)

        stop_recognition()

        for sentence in self._data:
            text_data += sentence + ' '

        if len(self._data) != 0:
            self._data.clear()

        return text_data

    # Inizio funzionalità di personalizzazione del pdf

    def get_pdf_type(self, duration=10, message='Che tipo di pdf vuoi creare? '):
        text = self.background_listening(
            duration, message).lower()

        if 'note' in text:
            return 'notes'
        elif 'gpt' in text or 'chatgpt' in text:
            return 'gpt'
        else:
            raise ValueError(
                'Puoi creare solo file di note o che sfruttano chatgpt')

    def get_pdf_name(self, duration=12, message='Come vuoi chiamare il tuo pdf?'):
        is_valid = True

        while True:
            try:
                if is_valid:
                    pdf_name = self.background_listening(
                        duration, message).strip()
                else:
                    pdf_name = self.background_listening(
                        duration, message='Detta un nuovo nome valido per il tuo pdf.').strip()

                if not pdf_name:
                    raise ValueError

                pdf_name += '.pdf'

                validate_filename(pdf_name)

            except (ValidationError, ValueError) as e:
                is_valid = False
                print('Nome invalido', e)

            else:
                return pdf_name

    def synthesize_notes(self, notes: str):
        prompt = {'role': 'user',
                  'data': f'Can you to summarize my notes. Here are my notes: {notes}'}

        response = self._client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'data': 'You are an Italian teacher. You are specialized on summarizing, schematizing and highlighting the most important parts of the text. You are designed to output a JSON object.'},
                prompt
            ]
        )

        return response['choices'][0]['message']['data']

    def get_response(self, prompt: str):
        prompt = {'role': 'user', 'data': prompt}

        response = self._client.chat.completions.create(
            messages=[
                {'role': 'system', 'data': 'You are a helpful assistant.'},
                prompt
            ]
        )

        return response['choices'][0]['message']['data']

    def get_notes_title(self, duration=15, message='Che titolo vuoi dare alle tue note?'):
        return self.background_listening(
            duration, message).strip()

    def get_notes_body(self, duration=30, message='Detta la tue note'):
        return self.background_listening(duration, message).strip()

    def get_prompt(self, duration=15, message='Detta il tuo prompt'):
        return self.background_listening(
            duration, message).strip()

    def create_pdf(self):
        type = self.get_pdf_type()
        name = self.get_pdf_name()
        if type == 'gpt':
            prompt = self.get_prompt()
            print('Creating your pdf...')
            pdf = GptPDF(prompt=prompt, text=self.get_response(prompt))
            pdf.print_chapter()
            pdf.output(name)
            print('Pdf created successfully')
        else:
            title = self.get_notes_title()
            body = self.get_notes_body()
            pdf = NotesPDF(text=self.synthesize_notes(body), name=title)
            pdf.print_chapter()
            pdf.output(name)
