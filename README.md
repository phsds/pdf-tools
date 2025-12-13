# PDF-Tools

**PDF-TOOLS** is a GUI tool for using PDFs, with functions included such as reading, mixing, conversion, etc ...

Quando o .exe for executado, duas pastas serão criadas na localização do executável. Sendo essas:

- **pdfs:** pasta em que se coloca os pdfs
- **results:** resultado convertido em docx após processamento

## Commands

Quando a interfaçe for executada, aparecerá essas opções para selecionar:

- Text Extraction: Extract text from PDF files
- Image Extraction: Extract images from PDF files
- PDF Merge: Merge multiple PDF files into one
- PDF Split/Combine: Split and combine specific pages of PDFs
- PDF - Handwritten: Use a temp account to automatize Pen-To-Print website's OCR process

Principais APIs são:

- PYPDF2 - PyPDF2==3.0.1
- Pillow - pillow==11.1.0
- Docx - python-docx==1.1.2
- Selenium - selenium==4.30.0

## Funcionamento

No geral, com excessão da última opção, todas as funcões são executadas diretamente pela GUI sem intervenção do navegador.

Após o processamento da opção **PDF - Handwritten**, os pdfs serão convertidos em imagens momentâneas que serão processadas no site e depois eliminadas.
