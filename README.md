# PDF-Tools

**PDF-TOOLS** is a GUI tool for using PDFs, with functions included such as reading, mixing, conversion, etc ...

When the .exe is run, two folders will be created in the executable's location. They are:

- **pdfs:** folder where you place the PDF files
- **results:** converted DOCX results after processing

## Commands

When the interface runs, the following options will be available:

- Text Extraction: Extract text from PDF files
- Image Extraction: Extract images from PDF files
- PDF - Merge: Merge multiple PDF files into one
- PDF - Split: Split specific pages of PDFs
- PDF - Handwritten: Use your account to automatize Pen-To-Print website's OCR process

Main APIs used:

- pypdf
- Pillow
- python-docx
- Selenium
- Others listed in `requirements.txt`

## How it works

"**Text Extraction**" and "**Image Extraction**" will not work on PDFs that do not have searchable text and inserted images.

When using "**PDF - Split**", the application will ask in its terminal how many pages should be grouped/separated.

In general, except for the last option, all features run directly from the GUI without browser interaction.

After processing the "**PDF - Handwritten**" option, the PDFs are converted into temporary images that are uploaded to the website for processing and then removed:
- You need to create an account on the [Pen-to-Print](https://www.pen-to-print.com/App/notes/) website.
- A file named "credentials.dpapi" will be generated and should be placed in the same folder as the executable if you want your email and password to be saved.
- To use a different account, simply delete the "credentials.dpapi" file.
  
"**PDF - Split**" and "**PDF - Handwritten**" will show a poppup "**PDF processing completed**" when the execution ends.

### **ATTENTION!**: When performing any function of the program, do not interrupt it and wait for the process to finish.

## Licença

Este software é distribuído sob a licença **CC-BY-NC 4.0**.  
Uso comercial é **proibido**.  
Mais detalhes em [Creative Commons BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
