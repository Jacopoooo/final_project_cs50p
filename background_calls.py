import speech_recognition as sr
import time
import sys


class BackgroundCalls(sr.Recognizer):
    _data = []
    _stop = False
    _mic = sr.Microphone()
    _language = 'en'

    """
    The default language is english
    """

    def __init__(self, callback, translate_text):
        self._callback = callback
        self._translate_text = translate_text

        super().__init__()

    def background_listening(self, duration, message: str):
        text_data = ''

        with self._mic as source:
            print(self._translate_text(
                'Adapting the microphone for noises in the environment...', self._language))
            self.adjust_for_ambient_noise(source)
            print(self._translate_text(
                'Microphone ready.', self._language))

        print(message)

        stop_recognition = self.listen_in_background(source, self._callback)

        for _ in range(duration):
            if self._stop:
                self._data.clear()
                sys.exit(self._translate_text(
                    'Registration finished.', self._language))
            time.sleep(1)

        stop_recognition()

        for sentence in self._data:
            text_data += sentence + ' '

        if len(self._data) != 0:
            self._data.clear()

        return text_data
