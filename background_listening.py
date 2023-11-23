import speech_recognition as sr
from speech_recognition import Recognizer
import time
import sys

terminate_recording = False
m = sr.Microphone()


class BackgroundCalls(Recognizer):
    def __init__(self, microphone: sr.Microphone):

        assert isinstance(
            microphone, sr.Microphone), 'Il microfono deve essere di tipo [sr.Microphone]'

        self._microphone = microphone
        self._content = []

        super().__init__()

    def background_listening(self, duration, message: str):
        text_data = ''

        with self._microphone as source:
            print("Adattando il microfono per i rumori nell'ambiente...")
            self.adjust_for_ambient_noise(source)
            print('Microfono pronto')

        print(message)

        stop_recognition = self.listen_in_background(source, callback)

        for _ in range(duration):
            if terminate_recording:
                self._content.clear()
                sys.exit('Registrazione terminata')
            time.sleep(1)

        stop_recognition()

        for sentence in self._content:
            text_data += sentence + ' '

        if len(self._content) != 0:
            self._content.clear()

        return text_data

    # Inizio funzionalità di personalizzazione del pdf

    def get_notes_title(self, duration=15, message='Che titolo vuoi dare alle tue note?'):
        notes_title = self.background_listening(
            duration, message).lower()

        return notes_title.strip()

    def get_prompt(self, duration=15, message='Che prompt vuoi dare a ChatGPT?'):
        prompt = self.background_listening(
            duration, message).lower()

        return prompt.strip()

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
        counter = 0

        while True:
            try:
                pdf_name = self.background_listening(
                    duration, message).lower()

                if counter != 0:
                    print('Inserisci un nuovo nome valido')

                if not pdf_name:
                    raise OSError

                with open(pdf_name + '.pdf', 'w'):
                    pass

            except OSError:
                counter += 1
                print('Nome invalido')
            else:
                return pdf_name.strip()


# Funzione chiamata dal thread in background
def callback(recognizer: sr.Recognizer, audio_data: sr.AudioData):
    global terminate_recording

    try:
        text = recognizer.recognize_google(audio_data, language='it-IT')
        print('Google ha sentito:', text)
    except sr.UnknownValueError:
        print('Google non comprende quello che stai dicendo')
    except sr.RequestError as e:
        print('Errore nella richiesta del servizio di Google', e)
    except KeyboardInterrupt:
        pass
    else:
        if 'termina la registrazione' in text:
            terminate_recording = True
        calls.__dict__['_content'].append(text)


calls = BackgroundCalls(m)


def main():
    print(calls.get_pdf_type())
    print(calls.get_pdf_name())


main()
