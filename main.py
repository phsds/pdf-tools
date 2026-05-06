import sys
import os
import tools
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import scrapper
import threading
import time
import queue

"""
If you want to convert to .exe, use the following command.
OBS: you will need to install pyinstaller first: pip install pyinstaller

pyinstaller --onefile --windowed --icon=Logo.ico main.py

"""


#command for conversion to executable: pyinstaller --onefile --windowed --icon=Logo.ico main.py 
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
        thread.daemon = True  # Killed automatically when the main process exits
        thread.start()
    return wrapper


def require_pdfs(func):
    """Decorator: aborts execution if the /pdfs directory is empty."""
    def wrapper(*args, **kwargs):
        if not tools.check_pdfs():
            print("Directory /pdfs is empty, please put a PDF file in it.")
            return
        return func(*args, **kwargs)
    return wrapper

@run_in_thread
@require_pdfs
def text_extraction():
    print('Starting text extraction...\n')
    time.sleep(1)
    print('Opening PDF file...\n')
    time.sleep(1)
    tools.extract_text()
    print('Text extraction completed.\n')
    messagebox.showinfo("Success", "Text extraction completed!")


@run_in_thread
@require_pdfs
def image_extraction():
    print('Starting image extraction...\n')
    time.sleep(1)
    print('Processing PDF pages...\n')
    time.sleep(1)
    tools.extract_images()
    print('Image extraction completed.\n')
    messagebox.showinfo("Success", "Image extraction completed!")


@run_in_thread
@require_pdfs
def pdf_merge():
    print('Starting PDF merge...\n')
    time.sleep(1)
    print('Reading PDF files...\n')
    time.sleep(1)
    tools.merge_pdfs()
    print('PDF merge completed.\n')
    messagebox.showinfo("Success", "PDFs merged successfully!")


@run_in_thread
@require_pdfs
def pdf_split_combine():
    print('Starting PDF split and combine...\n')
    time.sleep(1)
    print('Splitting selected pages...\n')
    time.sleep(1)
    tools.split_combine()
    print('PDF split and combine completed.\n')
    messagebox.showinfo("Success", "PDF split and combine completed!")


@run_in_thread
@require_pdfs
def pdf_requests():
    print('Starting PDF to PNG conversion and uploading to the website...\n')
    time.sleep(1)
    scrapper.pen_to_print(scrapper.activation())
    print('PDF processing completed.\n')
    messagebox.showinfo("Success", "PDF processing completed!")


def finish_program():
    print("Closing the program...\n")
    scrapper.close_browser()   # Close Selenium browser if open
    scrapper.delete_images()   # Remove output-images folder if it exists
    os._exit(0)  # Force-terminates the process; daemon threads are killed automatically


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

    # Event constants to prevent magic strings code smell
    EVENT_ENTER = "<Enter>"
    EVENT_LEAVE = "<Leave>"

    # Buttons for the options
    btn_text_extraction = tk.Button(root, text="Text Extraction", command=text_extraction, width=30, bg="#2e2e3e", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_text_extraction.pack(pady=5)
    btn_text_extraction.bind(EVENT_ENTER, lambda e: on_hover(e, "Extract text from PDF files.", btn_text_extraction))
    btn_text_extraction.bind(EVENT_LEAVE, lambda e: on_leave(e, btn_text_extraction))

    btn_image_extraction = tk.Button(root, text="Image Extraction", command=image_extraction, width=30, bg="#2e2e3e", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_image_extraction.pack(pady=5)
    btn_image_extraction.bind(EVENT_ENTER, lambda e: on_hover(e, "Extract images from PDF files.", btn_image_extraction))
    btn_image_extraction.bind(EVENT_LEAVE, lambda e: on_leave(e, btn_image_extraction))

    btn_pdf_merge = tk.Button(root, text="PDF - Merge", command=pdf_merge, width=30, bg="#2e2e3e", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_pdf_merge.pack(pady=5)
    btn_pdf_merge.bind(EVENT_ENTER, lambda e: on_hover(e, "Merge multiple PDF files into one.", btn_pdf_merge))
    btn_pdf_merge.bind(EVENT_LEAVE, lambda e: on_leave(e, btn_pdf_merge))

    btn_pdf_split_combine = tk.Button(root, text="PDF - Split", command=pdf_split_combine, width=30, bg="#2e2e3e", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_pdf_split_combine.pack(pady=5)
    btn_pdf_split_combine.bind(EVENT_ENTER, lambda e: on_hover(e, "Split specific pages of PDFs.", btn_pdf_split_combine))
    btn_pdf_split_combine.bind(EVENT_LEAVE, lambda e: on_leave(e, btn_pdf_split_combine))

    btn_pdf_requests = tk.Button(root, text="PDF - Handwritten", command=pdf_requests, width=30, bg="#2e2e3e", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_pdf_requests.pack(pady=5)
    btn_pdf_requests.bind(EVENT_ENTER, lambda e: on_hover(e, "Use your account to automatize Pen-To-Print website's OCR process", btn_pdf_requests))
    btn_pdf_requests.bind(EVENT_LEAVE, lambda e: on_leave(e, btn_pdf_requests))

    btn_finish = tk.Button(root, text="Finish Program", command=finish_program, width=30, bg="#e74c3c", fg="#ffffff", relief="flat", font=("Helvetica", 12))
    btn_finish.pack(pady=20)

    # Add hover effect for the Finish Program button
    def on_hover_finish(event):
        btn_finish.config(bg="#ff6b6b")  # Lighter red on hover

    def on_leave_finish(event):
        btn_finish.config(bg="#e74c3c")  # Reset to original red

    btn_finish.bind(EVENT_ENTER, on_hover_finish)
    btn_finish.bind(EVENT_LEAVE, on_leave_finish)
    btn_finish.bind(EVENT_ENTER, lambda e: description_label.config(text="Close the application."))
    btn_finish.bind(EVENT_LEAVE, lambda e: description_label.config(text=""))

    # Text widget to display terminal output
    output_text = ScrolledText(root, wrap=tk.WORD, height=50, width=70, bg="#2e2e3e", fg="#ffffff", font=("Consolas", 10), relief="flat")
    output_text.pack(pady=10)

    # Make the log widget interactive: allow typing and connect to sys.stdin
    class GuiStdin:
        def __init__(self, text_widget):
            self.text_widget = text_widget
            self.queue = queue.Queue()
            self.last_prompt_index = None

        def _show_prompt(self):
            # Insert a prompt marker where user can type
            try:
                # Ensure widget ends with a newline before inserting prompt
                end_index = self.text_widget.index('end-1c')
                last_char = self.text_widget.get(f"{end_index}", f"{end_index}")
            except Exception:
                last_char = "\n"
            if not last_char.endswith("\n"):
                self.text_widget.insert('end', "\n")
            self.text_widget.insert('end', ">>> ")
            self.text_widget.see('end')
            # store the index where user input starts
            self.last_prompt_index = self.text_widget.index('end-1c')
            self.text_widget.focus_set()

        def readline(self, *args, **kwargs):
            # Schedule prompt insertion in the GUI thread
            try:
                self.text_widget.after(0, self._show_prompt)
            except Exception:
                pass
            # Wait for user input from the queue
            line = self.queue.get()  # blocks until GUI puts input
            return line + "\n"

        def read(self, *args, **kwargs):
            return self.readline()

    gui_stdin = GuiStdin(output_text)

    def _on_enter(event):
        # Called when user presses Enter inside the text widget
        try:
            if gui_stdin.last_prompt_index:
                start = gui_stdin.last_prompt_index
                # Get user-typed content from prompt start to end
                user_text = output_text.get(start, 'end-1c')
                # Clean trailing newline if present
                user_text = user_text.rstrip('\n')
                gui_stdin.queue.put(user_text)
                # Echo newline to the widget
                output_text.insert('end', '\n')
                gui_stdin.last_prompt_index = None
                return 'break'  # prevent default newline insertion
            else:
                # Fallback: send current line
                line = output_text.get('insert linestart', 'insert lineend')
                gui_stdin.queue.put(line)
                output_text.insert('end', '\n')
                return 'break'
        except Exception as e:
            print(f"Error handling input: {e}")
            return None

    # Allow typing and bind Enter
    output_text.config(state='normal')
    output_text.bind('<Return>', _on_enter)
    # Replace sys.stdin with our GUI stdin
    import sys as _sys
    _sys.stdin = gui_stdin

    # Redirects stdout and stderr to the text widget
    sys.stdout = RedirectOutput(output_text)
    sys.stderr = RedirectOutput(output_text)

    # Automatically call tools.check_path() after the GUI is initialized
    def initialize_check_path():
        print("Initializing check_path function...\n")
        tools.check_paths()

        # Clear the terminal after 2 seconds
        def clear_terminal():
            output_text.delete(1.0, tk.END)

        root.after(1000, clear_terminal)  # Schedule terminal clearing after 2 seconds

    root.after(100, initialize_check_path)  # Calls the function after 100ms

    # Starts the main GUI loop
    # Register scrapper popup callback so scrapper can request GUI popups
    try:
        def _show_attention_popup():
            def _create():
                    top = tk.Toplevel(root)
                    top.title("ATENÇÃO!")
                    # Increase size and center on screen; make topmost so it's between GUI and browser
                    popup_w, popup_h = 520, 160
                    screen_w = root.winfo_screenwidth()
                    screen_h = root.winfo_screenheight()
                    pos_x = (screen_w - popup_w) // 2
                    pos_y = (screen_h - popup_h) // 2
                    top.geometry(f"{popup_w}x{popup_h}+{pos_x}+{pos_y}")
                    top.attributes("-topmost", True)
                    top.lift()
                    # message in red, larger font
                    msg = tk.Label(top, text="Enter your email and password in the PROGRAM'S TERMINAL, not in the browser.", fg="red", font=("Helvetica", 14, "bold"), wraplength=480, justify='center')
                    msg.pack(fill='both', expand=True, padx=20, pady=12)
                    btn = tk.Button(top, text="OK", command=lambda: (top.attributes('-topmost', False), top.destroy()))
                    btn.pack(pady=(0, 12))
                    top.transient(root)
                    try:
                        top.grab_set()
                    except Exception:
                        pass
            root.after(0, _create)

        import scrapper as _scr
        _scr.show_attention_popup = _show_attention_popup
    except Exception:
        pass

    root.mainloop()


if __name__ == "__main__":
    main_menu()