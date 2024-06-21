import os
from PyPDF2 import PdfReader


def read_file(file):
    _, file_extension = os.path.splitext(file.name)

    if file_extension == '.pdf':
        return read_pdf(file)
    elif file_extension == '.txt':
        return read_text(file)
    else:
        raise ValueError('File type not supported. Only PDF and TXT files are allowed.')


def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


def read_text(file):
    text = file.read().decode('utf-8')
    return text
