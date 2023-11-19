import speech_recognition as sr
import time
import sys
from fpdf import FPDF

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
        if isinstance(text, str) and 'termina la registrazione' in text:
            terminate_recording = True
        content.append(text)


def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(family='Helvetica', size=30)
    return pdf


r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source)

stop_recognition = r.listen_in_background(m, callback)


for _ in range(DURATION):
    if terminate_recording:
        sys.exit('Registrazione terminata')
    time.sleep(1)



if len(content) != 0:
    print('Building your pdf...')
    pdf = create_pdf()
    for sentence in content:
        pdf.cell(text=sentence)
    pdf.output('output.pdf')
    print('Pdf created successfully')
else:
    print('Google non ha sentito nulla')
