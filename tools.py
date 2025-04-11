import os
from shutil import move
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from time import sleep

#hi, my friend

path = 'pdfs/'
results = 'results/'
output_merger = 'merged.pdf'
output_split = 'splited_combined.pdf'
writer = PdfWriter()
merger = PdfMerger()

#HINT : The directory where pdf(s) file(s) are putted is "pdfs".
#Create "path" and results" directory where saved pdfs will go.
def mkdir_pdfs():
    if not os.path.exists(path):
        os.mkdir(path)

def mkdir_results():
    if not os.path.exists(results):
        os.mkdir(results)
        
#Check if the directory "path" have something in it, this function will substitute the bug of PyPDF2 where no FileNotFoundError errors are showed.
def check_paths():
    if not os.path.exists(path) or not os.path.exists(results):
        print('Folders /pdfs or /results not found, creating one of each.')
        mkdir_pdfs()
        mkdir_results()
        sleep(1)
        print('Folders created!')
    else:
        print("Folders already created.")
        pass

def check_pdfs():
    # Verifica se o diretório está vazio
    if len(os.listdir(path)) < 1:
        return False  # Retorna False se não houver arquivos no diretório
    return True  # Retorna True se houver arquivos no diretório
    
    #Extract text from pdf files in "pdfs" directory
def extractText():
    for archive in os.listdir(path):
        pdf = os.path.join(path, archive)
        reader = PdfReader(pdf, 'rb')
        for page in reader.pages:
            text = page.extract_text()
            with open(f'{results}{archive}.txt', 'a', encoding='utf-8') as out:
                out.write(text)
        print(f'\n{pdf.replace("pdfs/", "").replace(".pdf", "")} extracted!')

#Extract images from pdf files in "pdfs" directory
def extractImage():
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
                        except:
                            os.remove(img_file_obj.name)
    except Exception as err:
        print("There was an error with the PDF formatting, and it was not possible to extract all images.")
        print(f"\n {err}")
    print('\nAll done!')

#Merge pdf files in "pdfs" directory
def merge_pdfs():
    for archive in os.listdir(path):
        pdf = os.path.join(path, archive)
        merger.append(pdf)
    merger.write(f'{results}{output_merger}')
    print('\nAll done!')

#Especify a range of pdfs pages that will be splitted and merged into a singlefile.
def split_combine():
    for archive in os.listdir(path):
        pdf = os.path.join(path, archive)
        reader = PdfReader(pdf ,'rb')
        writer.add_page(reader.pages[0])
        writer.write(f'{results}{output_split}')
    print('\nAll done!')

#For debugging porpouses. Just remove the hash downside if you want execute this file without main.

if __name__ == "__main__":
    pass