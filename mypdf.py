from fpdf import FPDF, FPDFException


file_path = './text.txt'


class GptPDF(FPDF):
    def __init__(self, text: str, prompt: str):
        self._prompt = prompt
        self._text = text
        self.set_title('GPT')
        super().__init__()

    def header(self):
        self.set_font('Helvetica', size=12)
        # Pdf title color
        self.set_text_color(87, 84, 77)
        title_width = self.get_string_width(self.title) + 6
        self.set_x(((210 - title_width) / 2))
        self.cell(title_width, 20, self.title, new_x='LMARGIN',
                  new_y='NEXT', align='C')
        self.ln(8)

    def print_title(self):
        self.set_font('helvetica', 'I', 20)
        # chapter title color
        self.set_text_color(155, 154, 151)
        self.cell(0, 10, f'Prompt: {self._prompt}',
                  new_x='LMARGIN', new_y='NEXT')
        self.ln(8)

    def print_body(self):
        self.set_font('Times', size=12)
        # body text color
        self.set_text_color(55, 68, 51)
        self.multi_cell(0, 5, self._text)
        self.ln(30)
        self.set_font(style='I')
        self.cell(0, 5, 'End of pdf', align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def print_chapter(self):
        self.add_page()
        self.print_title()
        self.print_body()


class NotesPDF(FPDF):
    def __init__(self, text: str, name: str):
        self._name = name
        self._text = text
        self.set_title('Notes')
        super().__init__()

    def header(self):
        self.set_font('Helvetica', size=12)
        # Pdf title color
        self.set_text_color(87, 84, 77)
        title_width = self.get_string_width(self.title) + 6
        self.set_x(((210 - title_width) / 2))
        self.cell(title_width, 20, self.title, new_x='LMARGIN',
                  new_y='NEXT', align='C')
        self.ln(8)

    def print_title(self):
        self.set_font('helvetica', 'I', 20)
        # chapter title color
        self.set_text_color(155, 154, 151)
        self.cell(0, 10, self._name,
                  new_x='LMARGIN', new_y='NEXT')
        self.ln(8)

    def print_body(self):
        self.set_font('Times', size=12)
        # body text color
        self.set_text_color(55, 68, 51)
        self.multi_cell(0, 5, self._text)
        self.ln(30)
        self.set_font(style='I')
        self.cell(0, 5, 'End of pdf', align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def print_chapter(self):
        self.add_page()
        self.print_title()
        self.print_body()


def main():
    with open(file_path, 'rb') as f:
        text = f.read().decode('latin-1')
    pdf = NotesPDF(text=text,
                   name='Note Personali 1')
    pdf.print_chapter()
    pdf.output('test.pdf')


if __name__ == '__main__':
    main()
