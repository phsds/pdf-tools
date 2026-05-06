import os
import re
from shutil import move
from pypdf import PdfReader, PdfWriter
from time import sleep

# hi, my friend

path = 'pdfs/'
results = 'results/'
output_merger = 'merged.pdf'
output_split = 'splited_combined.pdf'
done = "All'"
writer = PdfWriter()
# PdfMerger is removed in pypdf 4.0+. We use PdfWriter instead.

# HINT: The directory where PDF files are placed is "pdfs".
# Create the `path` and `results` directories where saved PDFs will go.
def mkdir_pdfs():
    if not os.path.exists(path):
        os.mkdir(path)

def mkdir_results():
    if not os.path.exists(results):
        os.mkdir(results)
        
#Check if the directory "path" have something in it, this function will substitute the bug of pypdf where no FileNotFoundError errors are showed.
def check_paths():
    if not os.path.exists(path) or not os.path.exists(results):
        print('Folders /pdfs or /results not found, creating one of each.')
        mkdir_pdfs()
        mkdir_results()
        sleep(1)
        print('Folders created!')
    else:
        print("Folders already created.")

def check_pdfs():
    # Checks if the directory is empty
    if len(os.listdir(path)) < 1:
        return False  # Returns False if there are no files in the directory
    return True  # Returns True if there are files in the directory


    # Extract text from PDF files in the "pdfs" directory
def extract_text():
    for archive in os.listdir(path):
        pdf = os.path.join(path, archive)
        reader = PdfReader(pdf, 'rb')
        for page in reader.pages:
            text = page.extract_text()
            with open(f'{results}{archive}.txt', 'a', encoding='utf-8') as out:
                out.write(text)
        print(f'\n{pdf.replace("pdfs/", "").replace(".pdf", "")} extracted!')

#Extract images from pdf files in "pdfs" directory
def extract_images():
    try:
        for archive in os.listdir(path):
            pdf = os.path.join(path, archive)
            with open(pdf, 'rb') as file:
                reader = PdfReader(file)
                for page_num in range(0, len(reader.pages)):
                    selected_page = reader.pages[page_num]
                    for img_file_obj in selected_page.images:
                        with open(img_file_obj.name, 'wb') as out:
                            out.write(img_file_obj.data)
                        try:
                            move(f'{img_file_obj.name}', './results/')
                        except Exception:
                            os.remove(img_file_obj.name)
    except Exception as err:
        print("There was an error with the PDF formatting, and it was not possible to extract all images.")
        print(f"\n {err}")
    print(f'\n{done}')

#Natural sorting function to sort the pdf files in the directory
def natural_key(text):
    # Split the text into numeric and non-numeric parts for natural sorting
    return [int(s) if s.isdigit() else s.lower() for s in re.split(r'(\d+)', text)]

#Merge pdf files in "pdfs" directory
def merge_pdfs():
    # List and sort PDF files by name using natural sorting
    pdf_files = sorted(
        [f for f in os.listdir(path) if f.lower().endswith('.pdf')],
        key=natural_key
    )
    merger = PdfWriter()  # Ensure a fresh merger on each call
    for archive in pdf_files:
        pdf = os.path.join(path, archive)
        merger.append(pdf)
    merger.write(f'{results}{output_merger}')
    merger.close()
    print('\nAll done!')

#Especify a range of pdfs pages that will be splitted and merged into a singlefile.
def _get_pages_per_file():
    # Ask the user how many pages per file they want
    while True:
        try:
            pages_per_file = int(input("How many pages per file? "))
            if pages_per_file <= 0:
                raise ValueError()
            return pages_per_file
        except ValueError:
            print("Please enter an integer greater than 0.")

def _process_single_pdf(archive, pages_per_file):
    pdf_path = os.path.join(path, archive)
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    base_name = os.path.splitext(archive)[0]

    start = 0
    while start < total_pages:
        end = start + pages_per_file
        # If end exceeds total_pages, adjust to the remainder
        if end >= total_pages:
            end = total_pages

        writer = PdfWriter()
        for p in range(start, end):
            writer.add_page(reader.pages[p])

        # Mount the name as requested: "pdf name (page or pages)"
        if start + 1 == end:
            page_label = f"{start+1}"
        else:
            page_label = f"{start+1}-{end}"

        output_name = f"{base_name} ({page_label}).pdf"
        output_path = os.path.join(results, output_name)

        with open(output_path, 'wb') as out_f:
            writer.write(out_f)

        print(f"Saved: {output_path}")

        start = end

    print(f"{archive} processed ({total_pages} pages).")

#Especify a range of pdfs pages that will be splitted and merged into a singlefile.
def split_combine():
    pages_per_file = _get_pages_per_file()

    # Ensure that the results folder exists
    if not os.path.exists(results):
        os.makedirs(results, exist_ok=True)

    # Lists and sorts the PDF files in the `path` directory
    pdf_files = sorted([f for f in os.listdir(path) if f.lower().endswith('.pdf')], key=natural_key)

    for archive in pdf_files:
        _process_single_pdf(archive, pages_per_file)

    print('\nAll done!')

