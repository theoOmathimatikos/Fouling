import subprocess
from io import StringIO
import pdfminer
from pdfminer.high_level import extract_text_to_fp
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral, PSKeyword
from pdfminer.utils import decode_text


def print_version():
    print(pdfminer.__version__)


def extract(file_path):

    text = extract_text(file_path)
    print(text)


def extract_with_command(file_path):

    path, name = file_path.rsplit("/", 1)
    name = name.rsplit(".")[0]

    command = f"pdf2txt.py {file_path} > {path}/{name}.txt"
    _ = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def extract_and_print(file_path, to_html=False):

    output_string = StringIO()

    if to_html:
        with open(file_path, 'rb') as fin:
            extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='html', codec=None)
    else:
        with open(file_path, 'rb') as fin:
            extract_text_to_fp(fin, output_string)

    print(output_string.getvalue().strip())


def extract_components(file_path):

    output_string = StringIO()
    with open(file_path, 'rb') as in_file:

        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    print(output_string.getvalue())


def extract_images(file_path, output_path="pdf_images"):

    command = f"pdf2txt.py {file_path} --output-dir {output_path}"
    _ = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def decode_value(value):

    if isinstance(value, (PSLiteral, PSKeyword)):
        return value.name
    elif isinstance(value, bytes):
        return decode_text(value)
    else:
        return None
    
def extract_interactive_forms(file_path):

    data = {}
    with open(file_path, 'rb') as fp:

        parser = PDFParser(fp)
        doc = PDFDocument(parser)

        res = resolve1(doc.catalog)
        if 'AcroForm' not in res:
            raise ValueError("No AcroForm Found")   

        fields = resolve1(doc.catalog['AcroForm'])['Fields']
        for f in fields:

            field = resolve1(f)
            name, values = field.get('T'), field.get('V')

            name = decode_text(name)
            values = resolve1(values)

            if isinstance(values, list):
                values = [decode_value(v) for v in values]
            else:
                values = decode_value(values)

            data.update({name: values})
            print(name, values)


if __name__=="__main__":

    file_path = "pdf_files/Inspection_2.pdf"
    # extract(file_path)
    # extract_and_print(file_path)
    # extract_to_html(file_path)
    # extract_components(file_path)
    extract_interactive_forms(file_path=file_path)

