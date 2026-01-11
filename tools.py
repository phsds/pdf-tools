import os
import re
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

#Natural sorting function to sort the pdf files in the directory
def natural_key(text):
    # Divide o texto em partes numéricas e não numéricas para ordenação natural
    return [int(s) if s.isdigit() else s.lower() for s in re.split(r'(\d+)', text)]

#Merge pdf files in "pdfs" directory
def merge_pdfs():
    # Lista e ordena os arquivos PDF pelo nome usando ordenação natural
    pdf_files = sorted(
        [f for f in os.listdir(path) if f.lower().endswith('.pdf')],
        key=natural_key
    )
    merger = PdfMerger()  # Garante que o merger está limpo a cada chamada
    for archive in pdf_files:
        pdf = os.path.join(path, archive)
        merger.append(pdf)
    merger.write(f'{results}{output_merger}')
    merger.close()
    print('\nAll done!')

#Especify a range of pdfs pages that will be splitted and merged into a singlefile.
def split_combine():
    # Pergunta ao usuário quantas páginas por arquivo deseja
    while True:
        try:
            pages_per_file = int(input("Quantas páginas por arquivo? "))
            if pages_per_file <= 0:
                raise ValueError()
            break
        except ValueError:
            print("Por favor, insira um número inteiro maior que 0.")

    # Garante que a pasta de resultados exista
    if not os.path.exists(results):
        os.makedirs(results, exist_ok=True)

    # Lista e ordena os arquivos PDF no diretório `path`
    pdf_files = sorted([f for f in os.listdir(path) if f.lower().endswith('.pdf')], key=natural_key)

    for archive in pdf_files:
        pdf_path = os.path.join(path, archive)
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        base_name = os.path.splitext(archive)[0]

        start = 0
        while start < total_pages:
            end = start + pages_per_file
            # Se end ultrapassar total_pages, ajusta para o restante
            if end >= total_pages:
                end = total_pages

            writer = PdfWriter()
            for p in range(start, end):
                writer.add_page(reader.pages[p])

            # Monta o nome conforme pedido: "nome do pdf (página ou páginas)"
            if start + 1 == end:
                page_label = f"{start+1}"
            else:
                page_label = f"{start+1}-{end}"

            output_name = f"{base_name} ({page_label}).pdf"
            output_path = os.path.join(results, output_name)

            with open(output_path, 'wb') as out_f:
                writer.write(out_f)

            print(f"Salvo: {output_path}")

            start = end

        print(f"{archive} processado ({total_pages} páginas).")

    print('\nAll done!')

#For debugging porpouses. Just remove the hash downside if you want execute this file without main.

if __name__ == "__main__":
    pass