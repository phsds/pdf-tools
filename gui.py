import sys
import tools
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import scrapper
import time
import threading


class RedirectOutput:
    """Class to redirect stdout and stderr to the text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)  # Inserts the message at the end of the widget
        self.text_widget.see(tk.END)  # Automatically scrolls to the end
        self.text_widget.update_idletasks()  # Immediately updates the GUI

    def flush(self):
        pass  # Required for compatibility with sys.stdout and sys.stderr


def run_in_thread(func):
    """Decorator to run a function in a separate thread."""
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper


@run_in_thread
def text_extraction():
    print('Starting text extraction...\n')
    time.sleep(1)
    print('Opening PDF file...\n')
    time.sleep(1)
    tools.extractText()
    print('Text extraction completed.\n')
    messagebox.showinfo("Success", "Text extraction completed!")


@run_in_thread
def image_extraction():
    print('Starting image extraction...\n')
    time.sleep(1)
    print('Processing PDF pages...\n')
    time.sleep(1)
    tools.extractImage()
    print('Image extraction completed.\n')
    messagebox.showinfo("Success", "Image extraction completed!")


@run_in_thread
def pdf_merge():
    print('Starting PDF merge...\n')
    time.sleep(1)
    print('Reading PDF files...\n')
    time.sleep(1)
    tools.merge_pdfs()
    print('PDF merge completed.\n')
    messagebox.showinfo("Success", "PDFs merged successfully!")


@run_in_thread
def pdf_split_combine():
    print('Starting PDF split and combine...\n')
    time.sleep(1)
    print('Splitting selected pages...\n')
    time.sleep(1)
    tools.split_combine()
    print('PDF split and combine completed.\n')
    messagebox.showinfo("Success", "PDF split and combine completed!")


@run_in_thread
def pdf_requests():
    print('Starting PDF to JPG conversion and uploading to the website...\n')
    time.sleep(1)
    scrapper.Pen_to_Print(scrapper.activation())
    print('PDF processing completed.\n')
    messagebox.showinfo("Success", "PDF processing completed!")


def finish_program():
    print("Closing the program...\n")
    sys.exit(0)


def main_menu():
    # Creates the main window
    root = tk.Tk()
    root.title("PDF Tools")

    # Sets the window size
    window_width = 600
    window_height = 600

    # Calculates the position to open the window on the right side and center vertically
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = screen_width - window_width - 50
    position_y = (screen_height // 2) - (window_height // 2)

    # Sets the window geometry
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    root.configure(bg="#1e1e2f")  # Dark blue-gray background

    # Title
    title_label = tk.Label(root, text="PDF Tools", font=("Helvetica", 20, "bold"), bg="#1e1e2f", fg="#ffffff")
    title_label.pack(pady=20)

    # Description label for hover effect
    description_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#1e1e2f", fg="#a9a9b3")
    description_label.pack(pady=10)

    # Function to update the description on hover
    def on_hover(event, text, button):
        description_label.config(text=text)
        button.config(bg="#4a90e2", fg="#ffffff")  # Highlight with blue

    def on_leave(event, button):
        description_label.config(text="")
        button.config(bg="#2e2e3e", fg="#ffffff")  # Reset to original colors

    # Buttons for the options
    btn_text_extraction = tk.Button(root, text="Text Extraction", command=text_extraction, width=30, bg="#2e2e3e", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_text_extraction.pack(pady=5)
    btn_text_extraction.bind("<Enter>", lambda e: on_hover(e, "Extract text from PDF files.", btn_text_extraction))
    btn_text_extraction.bind("<Leave>", lambda e: on_leave(e, btn_text_extraction))

    btn_image_extraction = tk.Button(root, text="Image Extraction", command=image_extraction, width=30, bg="#2e2e3e", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_image_extraction.pack(pady=5)
    btn_image_extraction.bind("<Enter>", lambda e: on_hover(e, "Extract images from PDF files.", btn_image_extraction))
    btn_image_extraction.bind("<Leave>", lambda e: on_leave(e, btn_image_extraction))

    btn_pdf_merge = tk.Button(root, text="PDF Merge", command=pdf_merge, width=30, bg="#2e2e3e", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_pdf_merge.pack(pady=5)
    btn_pdf_merge.bind("<Enter>", lambda e: on_hover(e, "Merge multiple PDF files into one.", btn_pdf_merge))
    btn_pdf_merge.bind("<Leave>", lambda e: on_leave(e, btn_pdf_merge))

    btn_pdf_split_combine = tk.Button(root, text="PDF Split/Combine", command=pdf_split_combine, width=30, bg="#2e2e3e", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_pdf_split_combine.pack(pady=5)
    btn_pdf_split_combine.bind("<Enter>", lambda e: on_hover(e, "Split and combine specific pages of PDFs.", btn_pdf_split_combine))
    btn_pdf_split_combine.bind("<Leave>", lambda e: on_leave(e, btn_pdf_split_combine))

    btn_pdf_requests = tk.Button(root, text="PDF - Handwritten", command=pdf_requests, width=30, bg="#2e2e3e", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_pdf_requests.pack(pady=5)
    btn_pdf_requests.bind("<Enter>", lambda e: on_hover(e, "Convert PDFs to JPG and upload to a website.", btn_pdf_requests))
    btn_pdf_requests.bind("<Leave>", lambda e: on_leave(e, btn_pdf_requests))

    btn_finish = tk.Button(root, text="Finish Program", command=finish_program, width=30, bg="#e74c3c", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_finish.pack(pady=20)
    btn_finish.bind("<Enter>", lambda e: on_hover(e, "Close the application.", btn_finish))
    btn_finish.bind("<Leave>", lambda e: on_leave(e, btn_finish))

    # Text widget to display terminal output
    output_text = ScrolledText(root, wrap=tk.WORD, height=50, width=70, bg="#2e2e3e", fg="#ffffff", font=("Consolas", 10), relief="flat")
    output_text.pack(pady=10)

    # Redirects stdout and stderr to the text widget
    sys.stdout = RedirectOutput(output_text)
    sys.stderr = RedirectOutput(output_text)

    # Starts the main GUI loop
    root.mainloop()


if __name__ == "__main__":
    main_menu()