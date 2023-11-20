import speech_recognition as sr
import time
import sys
from fpdf import FPDF
from pdf_types import GptPDF, NotesPDF

DURATION = 20
content = []
terminate_recording = False


def callback(recognizer: sr.Recognizer, audio_data: sr.AudioData):
    global terminate_recording

    try:
        text = recognizer.recognize_google(audio_data, language='it-IT')
        print('Google ha sentito:', text)
    except sr.UnknownValueError:
        print('Google non comprende quello che stai dicendo')
    except sr.RequestError as e:
        print('Errore nella richiesta del servizio di Google', e)
    else:
        if 'termina la registrazione' in text:
            terminate_recording = True
        content.append(text)


def get_pdf_type():
    pdf_type = input('Che tipo di file vuoi creare? ')
    if pdf_type == 'notes':
        return pdf_type
    else:
        raise ValueError(
            'Puoi creare solo file di note o che sfruttano chatgpt')


def get_pdf_name():
    return input('Che nome vuoi dare al tuo pdf? ')


def background_listening(mic: sr.Microphone, rec: sr.Recognizer):
    with mic as source:
        rec.adjust_for_ambient_noise(source)

    stop_recognition = rec.listen_in_background(mic, callback)

    for _ in range(DURATION):
        if terminate_recording:
            sys.exit('Registrazione terminata')
        time.sleep(1)

    stop_recognition()


def create_pdf(pdf_type, pdf_name):
    print(content)
    print('Costruendo il tuo pdf...')
    text = ''
    for sentence in content:
        text += sentence + ' '
    if pdf_type == 'notes':
        print(text)
        print(pdf_name)
        pdf = NotesPDF(text=text, name=pdf_name)
        pdf.print_chapter()
        pdf.output('example.pdf')
        print('Pdf costruito con successo!')


def main():
    r = sr.Recognizer()
    m = sr.Microphone()

    pdf_type = get_pdf_type()
    pdf_name = get_pdf_name()
    background_listening(m, r)
    create_pdf(pdf_name=pdf_name, pdf_type=pdf_type)


main()
