from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from docx import Document
from time import sleep
import fitz
import os

def convert_pdf_pages_to_images(input_folder, output_folder="output-images", zoom=4.0, image_format="png"):
    """
    Converte páginas de PDFs em imagens com alta qualidade.
    
    Args:
        input_folder (str): Pasta contendo os PDFs de entrada.
        output_folder (str): Pasta onde as imagens serão salvas (fora de "teste-pdfs").
        zoom (float): Fator de zoom para aumentar a qualidade (padrão: 4.0).
        image_format (str): Formato da imagem de saída (padrão: "png").
    """
    # Cria a pasta de saída fora de "teste-pdfs"
    os.makedirs(output_folder, exist_ok=True)

    # Lista todos os arquivos PDF na pasta de entrada
    pdf_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        # Nome do PDF sem extensão
        pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
        # Cria uma pasta para o PDF atual dentro de "output-images"
        pdf_output_folder = os.path.join(output_folder, pdf_name)
        os.makedirs(pdf_output_folder, exist_ok=True)

        # Abre o PDF
        pdf_document = fitz.open(pdf_file)
        total_pages = len(pdf_document)  # Número total de páginas no PDF
        padding = len(str(total_pages - 1))  # Calcula o número de dígitos necessários para zero-padding

        for page_number in range(total_pages):
            # Renderiza a página como uma imagem com alta qualidade
            page = pdf_document[page_number]
            matrix = fitz.Matrix(zoom, zoom)  # Aumenta a resolução da imagem
            pix = page.get_pixmap(matrix=matrix)

            # Salva a imagem com zero-padding no nome
            output_image_path = os.path.join(pdf_output_folder, f"{str(page_number).zfill(padding)}.{image_format}")
            pix.save(output_image_path)

        pdf_document.close()
        print(f"PDF '{pdf_file}' convertido e salvo em '{pdf_output_folder}'.")

def activation():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def pdf24 (browser):

    browser.get("https://tools.pdf24.org/pt/pdf-para-imagens")

    #browser.maximize_window()

    button = browser.find_element("class name", "btn")
    button.click()
    sleep(10)
    conversion = browser.find_element(By.XPATH, "//a[@class='btn action']")
    conversion.click()
    #download = browser.find_element(By.XPATH, "//a[@id='downloadTool']")
    #sleep(10)
    #download.click()
    
    #Consertar a última parte


def Pen_to_Print(browser):
    folder_path = os.path.abspath("output-images")  # Caminho para a pasta "output-images"
    
    # Lista todas as subpastas dentro de "output-images"
    subfolders = [os.path.join(folder_path, d) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

    for subfolder in subfolders:
        # Lista todos os arquivos PNG na subpasta atual
        png_files = [os.path.join(subfolder, f) for f in sorted(os.listdir(subfolder)) if f.endswith(".png")]

        # Processa os arquivos em lotes de 50
        batch_size = 50
        total_files = len(png_files)
        current_index = 0

        while current_index < total_files:
            # Abre o site para cada lote
            browser.get("https://www.pen-to-print.com/App/notes/")
            sleep(3)  # Aguarda o carregamento do site

            # Seleciona o lote atual de arquivos
            batch_files = png_files[current_index:current_index + batch_size]

            for png_file in batch_files:
                # Recarrega o elemento de upload para cada arquivo
                upload_input = browser.find_element(By.CSS_SELECTOR, "input[type='file']")
                
                # Limpa o campo de upload antes de enviar o próximo arquivo
                browser.execute_script("arguments[0].value = '';", upload_input)
                
                # Envia o arquivo atual
                upload_input.send_keys(png_file)
                sleep(1)  # Aguarda um momento para o upload

            # Clica no botão "convert-button"
            button = browser.find_element(By.CLASS_NAME, "convert-button")
            button.click()
            sleep(6)

            # Seleciona o botão "word"
            button = browser.find_element(By.ID, "word")
            browser.execute_script("arguments[0].click();", button)
            sleep(5)  # Aguarda o processamento

            # Localiza o elemento <textarea> e extrai o texto
            textarea = browser.find_element(By.CLASS_NAME, "scanline-cell-content")
            text_content = textarea.get_attribute("value")  # Usa "value" para capturar o conteúdo do <textarea>

            # Salva o texto extraído em um arquivo Word
            doc = Document()  # Cria um novo documento Word
            doc.add_paragraph(text_content)  # Adiciona o texto extraído como um parágrafo
            output_file = f".\\results\\{os.path.basename(subfolder)}_lote_{current_index // batch_size + 1}.docx"
            doc.save(output_file)  # Salva o documento no formato .docx

            print(f"Texto extraído e salvo em '{output_file}'.")

            # Atualiza o índice para o próximo lote
            current_index += batch_size
    

# Executa a função
Pen_to_Print(activation())
# Exemplo de uso
#convert_pdf_pages_to_images("teste-pdfs", "output-images")