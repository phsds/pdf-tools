from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from docx import Document
from time import sleep
import fitz
import os

images_path = 'output-images/'

def check_path_images():
    if not os.path.exists(images_path):
        print('output-images directory not found, creating one putting the images in it.')
        convert_pdf_pages_to_images("teste-pdfs", "output-images")
    else:
        print("Directory already created.")
        pass

def convert_pdf_pages_to_images(input_folder, output_folder="output-images", zoom=4.0, image_format="png"):
    """
    Converte páginas de PDFs em imagens com alta qualidade e verifica dimensões para dividir imagens largas.
    
    Args:
        input_folder (str): Pasta contendo os PDFs de entrada.
        output_folder (str): Pasta onde as imagens serão salvas.
        zoom (float): Fator de zoom para aumentar a qualidade (padrão: 4.0).
        image_format (str): Formato da imagem de saída (padrão: "png").
    """
    # Cria a pasta de saída
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

        for page_number in range(total_pages):
            output_image_path = os.path.join(pdf_output_folder, f"{str(page_number).zfill(3)}.{image_format}")
            try:
                # Renderiza a página como uma imagem com alta qualidade
                page = pdf_document[page_number]
                pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
                pix.save(output_image_path)
                print(f"Página {page_number} salva como {output_image_path}")
            except Exception as e:
                print(f"Erro ao renderizar a página {page_number}: {e}")
                print(f"Tentando reextrair a página {page_number} do PDF...")
                try:
                    # Tenta reextrair a página e salva sem aplicar separação
                    page = pdf_document[page_number]
                    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
                    pix.save(output_image_path)
                    print(f"Página {page_number} reextraída e salva como {output_image_path} (sem separação)")
                except Exception as re_extraction_error:
                    print(f"Erro ao reextrair a página {page_number}: {re_extraction_error}")
                    continue

        pdf_document.close()

        # Verifica e divide imagens largas na subpasta
        print(f"Verificando imagens na subpasta '{pdf_output_folder}'...")
        image_files = [os.path.join(pdf_output_folder, f) for f in os.listdir(pdf_output_folder) if f.endswith(f".{image_format}")]
        for image_file in image_files:
            try:
                # Verifica se o arquivo existe e não está vazio
                if not os.path.exists(image_file) or os.path.getsize(image_file) == 0:
                    print(f"Erro: Arquivo '{image_file}' está vazio ou não existe. Tentando reextrair...")
                    page_number = int(os.path.basename(image_file).split('.')[0])  # Obtém o número da página
                    page = pdf_document[page_number]
                    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
                    pix.save(image_file)
                    print(f"Página {page_number} reextraída e salva como {image_file} (sem separação)")
                    continue

                with Image.open(image_file) as img:
                    width, height = img.size
                    if width > height:
                        print(f"Imagem '{image_file}' é larga. Dividindo...")

                        # Divide a imagem em duas partes (esquerda e direita)
                        left_image = img.crop((0, 0, width // 2, height))  # Parte esquerda
                        right_image = img.crop((width // 2, 0, width, height))  # Parte direita

                        # Salva as partes divididas
                        left_image_path = image_file.replace(f".{image_format}", f"_left.{image_format}")
                        right_image_path = image_file.replace(f".{image_format}", f"_right.{image_format}")
                        left_image.save(left_image_path)
                        right_image.save(right_image_path)
                        print(f"Imagem dividida salva como '{left_image_path}' e '{right_image_path}'")

                        # Remove a imagem original
                        os.remove(image_file)
                    else:
                        print(f"Imagem '{image_file}' não precisa ser dividida.")
            except Exception as e:
                print(f"Erro ao processar a imagem '{image_file}': {e}")

    print("Processamento concluído.")
        
def activation():
    check_path_images()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def Pen_to_Print(browser):
    # Realiza o login no site
    print("Iniciando login no site...")
    browser.get("https://www.pen-to-print.com/App/notes/")  # Abre a página inicial
    sleep(3)  # Aguarda o carregamento da página

    # Clica no botão "Accept cookies" antes de continuar
    try:
        accept_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "rcc-confirm-button"))
        )
        browser.execute_script("arguments[0].click();", accept_button)
        print("Botão 'Accept cookies' clicado com sucesso.")
    except Exception as e:
        print(f"Erro ao clicar no botão 'Accept cookies': {e}")

    # Passo 1: Localiza e clica no botão "Log in"
    wait = WebDriverWait(browser, 10)  # Aguarda até 10 segundos
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Log in']")))
    login_button.click()
    print("Botão de login clicado e popup aberto.")

    # Passo 2: Aguarda o popup de login e preenche os campos
    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_input.send_keys("pdfferramenta@outlook.com")

    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys("Gmo2Ha5z2!rio@by@Vb22hE68yj^eQKyWR%P9BB8C!58vNmjV899oTDA8CXZ82^&")

    # Clica no botão "Login" dentro do popup
    popup_login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-button button[type='submit']")))
    popup_login_button.click()
    print("Login realizado com sucesso!")
    sleep(5)  # Aguarda o login ser processado

    # Caminho para a pasta "output-images"
    folder_path = os.path.abspath("output-images")

    # Verifica se a pasta "output-images" existe, caso contrário, cria-a
    if not os.path.exists(folder_path):
        print(f"A pasta '{folder_path}' não existe. Criando...")
        os.makedirs(folder_path)

    # Lista todas as subpastas dentro de "output-images"
    subfolders = [os.path.join(folder_path, d) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

    for subfolder in subfolders:
        print(f"Processando subpasta: {subfolder}")
        # Lista todos os arquivos PNG na subpasta atual
        png_files = [os.path.join(subfolder, f) for f in sorted(os.listdir(subfolder)) if f.endswith(".png")]

        total_files = len(png_files)

        # Cria o arquivo Word para salvar o texto extraído
        output_file = os.path.join("results", f"{os.path.basename(subfolder)}.docx")
        os.makedirs("results", exist_ok=True)
        doc = Document()

        batch_size = 50
        current_index = 0

        while current_index < total_files:
            batch_files = png_files[current_index:current_index + batch_size]

            # Envia os arquivos do lote
            for png_file in batch_files:
                print(f"Enviando arquivo: {png_file}")
                try:
                    upload_input = browser.find_element(By.CSS_SELECTOR, "input[type='file']")
                    browser.execute_script("arguments[0].value = '';", upload_input)
                    upload_input.send_keys(png_file)
                    sleep(1)
                except Exception as e:
                    print(f"Erro ao enviar o arquivo {png_file}: {e}")
                    continue

            # Clica no botão "converter" após enviar o lote
            try:
                button = WebDriverWait(browser, 30).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "convert-button"))
                )
                browser.execute_script("arguments[0].scrollIntoView(true);", button)
                sleep(1)
                button.click()
                print("Botão de conversão clicado. Aguardando processamento...")
                WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "scanline-cell-content"))
                )
            except Exception as e:
                print(f"Erro ao clicar no botão de conversão: {e}")
                continue

            # Extrai o texto das páginas e salva no arquivo Word
            try:
                page_counter = browser.find_element(By.CLASS_NAME, "page-counter").text
                current_page, total_pages = map(int, page_counter.split(" ")[1].split("/"))

                while current_page <= total_pages:
                    textarea = browser.find_element(By.CLASS_NAME, "scanline-cell-content")
                    text_content = textarea.get_attribute("value")
                    if text_content.strip():
                        doc.add_paragraph(text_content)
                        doc.add_paragraph("")  # Adiciona um parágrafo vazio para separar as páginas

                    if current_page < total_pages:
                        next_button = browser.find_element(By.XPATH, "//div[@class='scanline-arrow']/img[@alt='next page']")
                        browser.execute_script("arguments[0].click();", next_button)
                        sleep(2)
                        page_counter = browser.find_element(By.CLASS_NAME, "page-counter").text
                        current_page, total_pages = map(int, page_counter.split(" ")[1].split("/"))
                    else:
                        break

                doc.save(output_file)
                print(f"Texto extraído e salvo em '{output_file}'.")
            except Exception as e:
                print(f"Erro ao navegar ou salvar o texto: {e}")
                continue

            # Clica no botão "closeWindowButton" após o processamento do lote
            try:
                close_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "closeWindowButton"))
                )
                browser.execute_script("arguments[0].click();", close_button)
                print("Botão 'closeWindowButton' clicado com sucesso.")
                sleep(2)  # Aguarda o fechamento da janela
            except Exception as e:
                print(f"Erro ao clicar no botão 'closeWindowButton': {e}")

            # Atualiza o índice para o próximo lote
            current_index += batch_size

            # Reinicia o processo para as imagens restantes
            if current_index < total_files:
                print("Reiniciando o processo para as imagens restantes...")
                browser.get("https://www.pen-to-print.com/App/notes/")
                sleep(5)  # Aguarda o carregamento da página inicial

        # Após finalizar a subpasta, retorna à URL inicial para processar a próxima subpasta
        print(f"Subpasta '{subfolder}' processada com sucesso. Retornando à página inicial...")
        browser.get("https://www.pen-to-print.com/App/notes/")
        sleep(5)  # Aguarda o carregamento da página inicial

    print("Processamento concluído para todas as subpastas.")
    browser.quit()
    
#Executa a função
Pen_to_Print(activation())
