import sys
import tools
from art import tprint

tprint("-PDF-Tools", font="avatar")

print("This is a terminal tool for reading, merging, splitting, and other functionalities with PDFs.")

def Main_Menu():
    if tools.check_path() is True:
        Checking()
    else:
        pass
    while True:
        option = int(input("""What option do you desire?
(1) - Text Extraction
(2) - Image Extraction
(3) - Pdf Merge
(4) - Pdf Split/Combine
(5) - Converter Docx
(6) - Finish the program

Option : """))
        options(option)
        
        condition = input("Deseja continuar:")
        if condition == "y":
            continue
        else:
            print("Encerrando programa")
            break

def Checking():
    print('Checking if path exists and creating one if not.')
    tools.check_path()
    if tools.check_pdfs():
        tools.check_pdfs()

# Define what options você deseja
def options(option):
    if option == 1:
        print('Inserting the extracted texts...\n')
        tools.extractText()
    elif option == 2:
        print('Extracting images from pdfs.')
        tools.extractImage()
    elif option == 3:
        print('Combining the pdfs and saving "merged.pdf" at "results" directory.\n')
        tools.merge_pdfs()
    elif option == 4:
        print('Crooping the selected range of pages and merging them at "results" directory with "splited_combined" name.\n')
        tools.split_combine()
    elif option == 6:
        print("Finishing Program")
        sys.exit(0)
    else:
        print('Please, select one of the options above.')

Main_Menu()