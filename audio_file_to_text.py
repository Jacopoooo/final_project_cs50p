import speech_recognition as sr
import sys
from os import path

file_name = 'audio1_english.wav'
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), file_name)

r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)

try:
    print('Google is listening to your audio file...')
    text = r.recognize_google(audio)
except sr.UnknownValueError as e:
    print('Error:', e)
except sr.RequestError as e:
    print('Error:', e)
else:
    if text:
        with open('output.txt', 'w') as f:
            f.write(text)
    else:
        print("Google heard nothing")
