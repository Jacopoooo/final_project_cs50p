import speech_recognition as sr
from speech_recognition import Recognizer
import time
import sys

terminate_recording = False
content = []


class SpeechRecognitionUtils(Recognizer):
    def __init__(self, microphone: sr.Microphone, duration):
        self._duration = duration

        assert isinstance(
            microphone, sr.Microphone), 'Il microfono deve essere di tipo [sr.Microphone]'

        self._microphone = microphone

        super().__init__()

    def background_listening(self, text_content: list()):
        text_data = ''

        with self._microphone as source:
            print("Adattando il microfono per i rumori nell'ambiente...")
            self.adjust_for_ambient_noise(source)

        stop_recognition = self.listen_in_background(source, callback)

        for _ in range(self._duration):
            if terminate_recording:
                text_content.clear()
                sys.exit('Registrazione terminata')
            time.sleep(1)

        stop_recognition()

        for sentence in text_content:
            text_data += sentence + ' '

        if len(text_content) != 0:
            text_content.clear()

        return text_data

    def get_pdf_type(self, text_content):
        print('Che tipo di pdf vuoi creare? ')

        text = self.background_listening(text_content)

        if 'note' in text:
            return 'notes'
        elif 'gpt' in text:
            return 'gpt'
        else:
            raise ValueError(
                'Puoi creare solo file di note o che sfruttano chatgpt')


def callback(recognizer: sr.Recognizer, audio_data: sr.AudioData):
    global content
    global terminate_recording

    try:
        text = recognizer.recognize_google(audio_data, language='it-IT')
        # print('Google ha sentito:', text)
    except sr.UnknownValueError:
        print('Google non comprende quello che stai dicendo')
    except sr.RequestError as e:
        print('Errore nella richiesta del servizio di Google', e)
    else:
        if 'termina la registrazione' in text:
            terminate_recording = True
        content.append(text)


def main():
    global content

    duration = 10
    m = sr.Microphone()

    utils = SpeechRecognitionUtils(m, duration)
    print(utils.get_pdf_type(content))


main()
