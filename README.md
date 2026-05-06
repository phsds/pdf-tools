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

### **PDF - Handwritten (Advanced OCR)**

This feature automates the conversion of handwritten or complex PDFs using the Pen-to-Print website. The process follows these steps:

1. **Pre-processing**: The program merges all PDFs in the `pdfs` folder and converts them into high-quality images stored temporarily in `output-images`.
2. **Web Automation**: A Selenium-controlled browser opens the Pen-to-Print website.
3. **Authentication**:
    - The program attempts to retrieve credentials from `credentials.dpapi`.
    - If not found, it prompts you for your email and password via the GUI console.
4. **OCR Processing**:
    - Images are uploaded in batches of up to 50 pages.
    - The website processes the handwriting into digital text.
5. **Output**: The extracted text is compiled into a `.docx` document and saved in the `results` folder.
6. **Full Cleanup**:
    - Temporary images in `output-images` are deleted.
    - The Selenium browser is closed.
    - **Advanced System Cleanup**: The program automatically releases Selenium handles and uses the Windows Shell API (mimicking File Explorer behavior) to find and remove temporary Chrome folders (`scoped_dir*`). This ensures your system's Temp directory remains clean and free of "junk" folders. **Note**: An administrator prompt (UAC) may appear for each folder being processed to allow the Shell API to complete the deletion.

"**PDF - Split**" and "**PDF - Handwritten**" will show a popup "**PDF processing completed**" when the execution ends.

### **ATTENTION!**: When performing any function of the program, do not interrupt it and wait for the process to finish

## Licença

Este software é distribuído sob a licença **CC-BY-NC 4.0**.  
Uso comercial é **proibido**.  
Mais detalhes em [Creative Commons BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
