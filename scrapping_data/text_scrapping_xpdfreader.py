import subprocess

def extract_text_from_pdf(pdf_path, out_path, args):

    cmd = ["pdftotext"]
    for k, v in args.items():
        if v in [None, "None"]: 
            continue
        if isinstance(v, str) == False:
            try:
                v = str(v)
            except:
                return 
        cmd.extend([k, v])
    cmd.extend([pdf_path, out_path])
    print(cmd)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

if __name__ == "__main__":

    pdf_path = "pdf_files/pdfs/Inspection_2.pdf"
    out_path = "pdf_files/txt_from_pdf/Insp_2.txt"
    f = 2
    l = 2
    args = {"-f":f, "-l":l, "-layout": "None", "-table": "None"}
    extracted_text = extract_text_from_pdf(pdf_path, out_path, args)
    print(extracted_text)
