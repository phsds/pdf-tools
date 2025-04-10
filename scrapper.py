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
        print('output-images directory not found, creating one and putting the images in it.')
        convert_pdf_pages_to_images("teste-pdfs", "output-images")
    else:
        print("Directory already created.")
        pass

def convert_pdf_pages_to_images(input_folder, output_folder="output-images", zoom=4.0, image_format="png"):
    """
    Converts PDF pages into high-quality images and checks dimensions to split wide images.
    
    Args:
        input_folder (str): Folder containing the input PDFs.
        output_folder (str): Folder where the images will be saved.
        zoom (float): Zoom factor to increase quality (default: 4.0).
        image_format (str): Output image format (default: "png").
    """
    # Creates the output folder
    os.makedirs(output_folder, exist_ok=True)

    # Lists all PDF files in the input folder
    pdf_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        # PDF name without extension
        pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
        # Creates a folder for the current PDF inside "output-images"
        pdf_output_folder = os.path.join(output_folder, pdf_name)
        os.makedirs(pdf_output_folder, exist_ok=True)

        # Opens the PDF
        pdf_document = fitz.open(pdf_file)
        total_pages = len(pdf_document)  # Total number of pages in the PDF

        for page_number in range(total_pages):
            output_image_path = os.path.join(pdf_output_folder, f"{str(page_number).zfill(3)}.{image_format}")
            try:
                # Renders the page as a high-quality image
                page = pdf_document[page_number]
                pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
                pix.save(output_image_path)
                print(f"Page {page_number} saved as {output_image_path}")
            except Exception as e:
                print(f"Error rendering page {page_number}: {e}")
                print(f"Trying to re-extract page {page_number} from the PDF...")
                try:
                    # Attempts to re-extract the page and save without splitting
                    page = pdf_document[page_number]
                    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
                    pix.save(output_image_path)
                    print(f"Page {page_number} re-extracted and saved as {output_image_path} (without splitting)")
                except Exception as re_extraction_error:
                    print(f"Error re-extracting page {page_number}: {re_extraction_error}")
                    continue

        pdf_document.close()

        # Checks and splits wide images in the subfolder
        print(f"Checking images in the subfolder '{pdf_output_folder}'...")
        image_files = [os.path.join(pdf_output_folder, f) for f in os.listdir(pdf_output_folder) if f.endswith(f".{image_format}")]
        for image_file in image_files:
            try:
                # Checks if the file exists and is not empty
                if not os.path.exists(image_file) or os.path.getsize(image_file) == 0:
                    print(f"Error: File '{image_file}' is empty or does not exist. Trying to re-extract...")
                    page_number = int(os.path.basename(image_file).split('.')[0])  # Gets the page number
                    page = pdf_document[page_number]
                    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
                    pix.save(image_file)
                    print(f"Page {page_number} re-extracted and saved as {image_file} (without splitting)")
                    continue

                with Image.open(image_file) as img:
                    width, height = img.size
                    if width > height:
                        print(f"Image '{image_file}' is wide. Splitting...")

                        # Splits the image into two parts (left and right)
                        left_image = img.crop((0, 0, width // 2, height))  # Left part
                        right_image = img.crop((width // 2, 0, width, height))  # Right part

                        # Saves the split parts
                        left_image_path = image_file.replace(f".{image_format}", f"_left.{image_format}")
                        right_image_path = image_file.replace(f".{image_format}", f"_right.{image_format}")
                        left_image.save(left_image_path)
                        right_image.save(right_image_path)
                        print(f"Split image saved as '{left_image_path}' and '{right_image_path}'")

                        # Removes the original image
                        os.remove(image_file)
                    else:
                        print(f"Image '{image_file}' does not need to be split.")
            except Exception as e:
                print(f"Error processing image '{image_file}': {e}")

    print("Processing completed.")
        
def activation():
    check_path_images()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def Pen_to_Print(browser):
    # Logs into the website
    print("Starting login on the website...")
    browser.get("https://www.pen-to-print.com/App/notes/")  # Opens the homepage
    sleep(3)  # Waits for the page to load

    # Clicks the "Accept cookies" button before continuing
    try:
        accept_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "rcc-confirm-button"))
        )
        browser.execute_script("arguments[0].click();", accept_button)
        print("'Accept cookies' button clicked successfully.")
    except Exception as e:
        print(f"Error clicking the 'Accept cookies' button: {e}")

    # Step 1: Locates and clicks the "Log in" button
    wait = WebDriverWait(browser, 10)  # Waits up to 10 seconds
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Log in']")))
    login_button.click()
    print("Login button clicked and popup opened.")

    # Step 2: Waits for the login popup and fills in the fields
    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_input.send_keys("pdfferramenta@outlook.com")

    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys("Gmo2Ha5z2!rio@by@Vb22hE68yj^eQKyWR%P9BB8C!58vNmjV899oTDA8CXZ82^&")

    # Clicks the "Login" button inside the popup
    popup_login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-button button[type='submit']")))
    popup_login_button.click()
    print("Login successful!")
    sleep(5)  # Waits for the login to be processed

    # Path to the "output-images" folder
    folder_path = os.path.abspath("output-images")

    # Checks if the "output-images" folder exists, otherwise creates it
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist. Creating...")
        os.makedirs(folder_path)

    # Lists all subfolders inside "output-images"
    subfolders = [os.path.join(folder_path, d) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

    for subfolder in subfolders:
        print(f"Processing subfolder: {subfolder}")
        # Lists all PNG files in the current subfolder
        png_files = [os.path.join(subfolder, f) for f in sorted(os.listdir(subfolder)) if f.endswith(".png")]

        total_files = len(png_files)

        # Creates the Word file to save the extracted text
        output_file = os.path.join("results", f"{os.path.basename(subfolder)}.docx")
        os.makedirs("results", exist_ok=True)
        doc = Document()

        batch_size = 50
        current_index = 0

        while current_index < total_files:
            batch_files = png_files[current_index:current_index + batch_size]

            # Uploads the batch files
            for png_file in batch_files:
                print(f"Uploading file: {png_file}")
                try:
                    upload_input = browser.find_element(By.CSS_SELECTOR, "input[type='file']")
                    browser.execute_script("arguments[0].value = '';", upload_input)
                    upload_input.send_keys(png_file)
                    sleep(1)
                except Exception as e:
                    print(f"Error uploading the file {png_file}: {e}")
                    continue

            # Clicks the "convert" button after uploading the batch
            try:
                button = WebDriverWait(browser, 30).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "convert-button"))
                )
                browser.execute_script("arguments[0].scrollIntoView(true);", button)
                sleep(1)
                button.click()
                print("Convert button clicked. Waiting for processing...")
                WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "scanline-cell-content"))
                )
            except Exception as e:
                print(f"Error clicking the convert button: {e}")
                continue

            # Extracts the text from the pages and saves it in the Word file
            try:
                page_counter = browser.find_element(By.CLASS_NAME, "page-counter").text
                current_page, total_pages = map(int, page_counter.split(" ")[1].split("/"))

                while current_page <= total_pages:
                    textarea = browser.find_element(By.CLASS_NAME, "scanline-cell-content")
                    text_content = textarea.get_attribute("value")
                    if text_content.strip():
                        doc.add_paragraph(text_content)
                        doc.add_paragraph("")  # Adds an empty paragraph to separate pages

                    if current_page < total_pages:
                        next_button = browser.find_element(By.XPATH, "//div[@class='scanline-arrow']/img[@alt='next page']")
                        browser.execute_script("arguments[0].click();", next_button)
                        sleep(2)
                        page_counter = browser.find_element(By.CLASS_NAME, "page-counter").text
                        current_page, total_pages = map(int, page_counter.split(" ")[1].split("/"))
                    else:
                        break

                doc.save(output_file)
                print(f"Text extracted and saved in '{output_file}'.")
            except Exception as e:
                print(f"Error navigating or saving the text: {e}")
                continue

            # Clicks the "closeWindowButton" after processing the batch
            try:
                close_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "closeWindowButton"))
                )
                browser.execute_script("arguments[0].click();", close_button)
                print("'closeWindowButton' clicked successfully.")
                sleep(2)  # Waits for the window to close
            except Exception as e:
                print(f"Error clicking the 'closeWindowButton': {e}")

            # Updates the index for the next batch
            current_index += batch_size

            # Restarts the process for the remaining images
            if current_index < total_files:
                print("Restarting the process for the remaining images...")
                browser.get("https://www.pen-to-print.com/App/notes/")
                sleep(5)  # Waits for the homepage to load

        # After finishing the subfolder, returns to the homepage to process the next subfolder
        print(f"Subfolder '{subfolder}' processed successfully. Returning to the homepage...")
        browser.get("https://www.pen-to-print.com/App/notes/")
        sleep(5)  # Waits for the homepage to load

    print("Processing completed for all subfolders.")
    browser.quit()

if __name__ == "__main__":
  pass