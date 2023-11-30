import speech_recognition as sr
import time
import sys


class BackgroundCalls(sr.Recognizer):
    _data = []
    _stop = False
    _mic = sr.Microphone()

    def __init__(self, callback: function, translate_text: function):
        self._callback = callback
        self._translate_text = translate_text

        super().__init__()

    def background_listening(self, duration, message: str):
        text_data = ''

        with self._mic as source:
            print(self._translate_text(
                'Adapting the microphone for noises in the environment...'))
            self.adjust_for_ambient_noise(source)
            print(self._translate_text(
                'Microphone ready.'))

        print(message)

        stop_recognition = self.listen_in_background(source, self._callback)

        for _ in range(duration):
            if self._stop:
                self._data.clear()
                sys.exit(self._translate_text(
                    'Registration finished.'))
            time.sleep(1)

        stop_recognition()

        for sentence in self._data:
            text_data += sentence + ' '

        if len(self._data) != 0:
            self._data.clear()

        return text_data
