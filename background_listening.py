import speech_recognition as sr
from openai_api_key import OPENAI_API_KEY
from openai import OpenAI
from pdf_creation import PdfCreation


# Funzione chiamata dal thread in background
def callback(recognizer: sr.Recognizer, audio_data: sr.AudioData):
    google_heard_something = [False]

    try:
        text = recognizer.recognize_google(audio_data, language='it-IT')
        print('Google ha sentito:', text)
    except sr.UnknownValueError:
        if not google_heard_something[0]:
            print('Google non comprende quello che stai dicendo')
    except sr.RequestError as e:
        print('Errore nella richiesta del servizio di Google', e)
        calls._stop = True
    except KeyboardInterrupt:
        pass
    else:
        google_heard_something[0] = True
        if 'termina la registrazione' in text.lower():
            calls._stop = True
        calls._data.append(text)


m = sr.Microphone()
client = OpenAI(api_key=OPENAI_API_KEY)
calls = PdfCreation(callback, client)


def main():
    print(calls.get_pdf_name())
    print(calls.get_notes_title())
    print(calls.get_pdf_type())


main()
