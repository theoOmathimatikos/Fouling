import subprocess

def extract_text_from_pdf(pdf_path):
    command = ['pdftotext', pdf_path, '-']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

if __name__ == "__main__":

    pdf_path = "pdf_files/Inspection_2.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    print(extracted_text)
