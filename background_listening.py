from speech_recognition import UnknownValueError, RequestError
from openai_api_key import OPENAI_API_KEY
from openai import OpenAI
from pdf_creation import PdfCreation
from utils import translate_text
from pdf_types import GptPDF, NotesPDF


# Funzione chiamata dal thread in background
def callback(recognizer, audio_data):
    google_heard_something = [False]
    language = pdf_create._language

    try:
        text = recognizer.recognize_google(
            audio_data, language=language)
        print(translate_text('Google heard:', language), text)
    except UnknownValueError:
        if not google_heard_something[0]:
            print(translate_text(
                "Google doesn't understand what you're saying", language))
    except RequestError as e:
        print(translate_text('Error requesting Google service', language), e)
        pdf_create._stop = True
    except KeyboardInterrupt:
        pass
    else:
        google_heard_something[0] = True
        if translate_text('finish recording', language) in text.lower():
            pdf_create._stop = True
        pdf_create._data.append(text)


def synthesize_notes(openai_client: OpenAI, notes: str):
    prompt = {'role': 'user',
              'data': f'Can you to summarize my notes. Here are my notes: {notes}'}

    response = openai_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'data': 'You are an Italian teacher. You are specialized on summarizing, schematizing and highlighting the most important parts of the text. You are designed to output a JSON object.'},
            prompt
        ]
    )

    return response['choices'][0]['message']['data']


def get_response(openai_client: OpenAI, prompt: str):
    prompt = {'role': 'user', 'data': prompt}

    response = openai_client.chat.completions.create(
        messages=[
            {'role': 'system', 'data': 'You are a helpful assistant.'},
            prompt
        ]
    )

    return response['choices'][0]['message']['data']


client = OpenAI(api_key=OPENAI_API_KEY)
pdf_create = PdfCreation(callback, translate_text)


def main():
    language = pdf_create._language
    pdf_create.select_language()
    type = pdf_create.get_pdf_type()
    name = pdf_create.get_pdf_name()
    if type == 'gpt':
        prompt = pdf_create.get_prompt()
        print(translate_text('Creating your pdf...', language))
        pdf = GptPDF(get_response(client, prompt), prompt)
        pdf.print_chapter()
        pdf.output(name)
        print(translate_text('Pdf created successfully!', language))
    else:
        title = pdf_create.get_notes_title()
        body = pdf_create.get_notes_body()
        print(translate_text('Creating your pdf...', language))
        pdf = NotesPDF(body, title)
        pdf.print_chapter()
        pdf.output(name)
        print(translate_text('Pdf created successfully!', language))


main()
