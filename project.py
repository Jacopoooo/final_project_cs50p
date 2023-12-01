from speech_recognition import UnknownValueError, RequestError
from openai_api_key import OPENAI_API_KEY
from openai import OpenAI
from pdf_creation import PdfCreation
from deep_translator import GoogleTranslator as gt
from pdf_types import GptPDF, NotesPDF


# Funzione chiamata dal thread in background
def callback(recognizer, audio_data):
    language = pdf_create.language

    try:
        text = recognizer.recognize_google(
            audio_data, language=language)
        print(translate_text('Google heard:', language), text)
    except UnknownValueError:
        print(translate_text(
            "Google doesn't understand what you're saying", language))
    except RequestError as e:
        print(translate_text('Error requesting Google service', language), e)
        pdf_create.stop = True
    except KeyboardInterrupt:
        pass
    else:
        if translate_text('finish recording', language) in text.lower():
            pdf_create.stop = True
        pdf_create.data.append(text)


def translate_text(text, language) -> str:
    return gt(target=language).translate(
        text).lower()


def synthesize_notes(notes: str):
    prompt = {'role': 'user',
              'data': f'Can you to summarize my notes. Here are my notes: {notes}'}

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'data': 'You are an Italian teacher. You are specialized on summarizing, schematizing and highlighting the most important parts of the text. You are designed to output a JSON object.'},
            prompt
        ]
    )

    return response['choices'][0]['message']['data']


def get_response(prompt: str):
    prompt = {'role': 'user', 'data': prompt}

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'data': 'You are a helpful assistant.'},
            prompt
        ]
    )
    
    return response['choices'][0]['message']['data']


client = OpenAI(api_key=OPENAI_API_KEY)
pdf_create = PdfCreation(callback, translate_text)


def main():
    language = pdf_create.select_language()
    type = pdf_create.get_pdf_type()
    name = pdf_create.get_pdf_name()
    if type == 'gpt':
        prompt = pdf_create.get_prompt()
        print(translate_text('Creating your pdf...', language))
        pdf = GptPDF(get_response(prompt), prompt)
        pdf.print_chapter()
        pdf.output(name)
        print(translate_text('Pdf created successfully!', language))
    else:
        title = pdf_create.get_notes_title()
        body = pdf_create.get_notes_body()
        print(translate_text('Creating your pdf...', language))
        pdf = NotesPDF(synthesize_notes(body), title)
        pdf.print_chapter()
        pdf.output(name)
        print(translate_text('Pdf created successfully!', language))


if __name__ == '__main__':
    main()
