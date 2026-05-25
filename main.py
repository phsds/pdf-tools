import sys
import os
import tools
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import scrapper
import threading
import time
import queue
import pypdfium2 as pdfium
from PIL import Image, ImageTk
import pytesseract

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
    root = tk.Tk()
    root.title("PDF Tools (ABBYY Style)")

    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    
    # Light Theme
    bg_main = "#f0f0f0"
    bg_canvas = "#e0e0e0"
    bg_text = "#ffffff"
    root.configure(bg=bg_main)

    # 1. Top Toolbar
    toolbar = tk.Frame(root, bg=bg_main, bd=1, relief=tk.RAISED)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    
    btn_style = {"bg": bg_main, "fg": "black", "relief": "flat", "font": ("Helvetica", 10)}
    
    # 2. Main PanedWindow (Vertical: top=Workspace, bottom=Log)
    v_paned = tk.PanedWindow(root, orient=tk.VERTICAL, bg=bg_main, sashwidth=5)
    v_paned.pack(fill=tk.BOTH, expand=True)

    # 3. Workspace PanedWindow (Horizontal: Left=Thumbnails, Right=Dual Viewer)
    h_paned = tk.PanedWindow(v_paned, orient=tk.HORIZONTAL, bg=bg_main, sashwidth=5)
    v_paned.add(h_paned, minsize=500)

    # 4. Left Sidebar for Thumbnails
    sidebar_frame = tk.Frame(h_paned, bg=bg_main, width=150)
    h_paned.add(sidebar_frame, minsize=100)
    
    # 5. Dual Viewer PanedWindow
    dual_paned = tk.PanedWindow(h_paned, orient=tk.HORIZONTAL, bg=bg_main, sashwidth=5)
    h_paned.add(dual_paned, minsize=600)
    
    # 5a. PDF Viewer (Left of Dual Viewer)
    pdf_viewer_frame = tk.Frame(dual_paned, bg=bg_canvas)
    dual_paned.add(pdf_viewer_frame, minsize=300)
    
    # 5b. OCR Text Editor (Right of Dual Viewer)
    ocr_viewer_frame = tk.Frame(dual_paned, bg=bg_text)
    dual_paned.add(ocr_viewer_frame, minsize=300)

    # 6. Bottom Console
    console_frame = tk.Frame(v_paned, bg=bg_main)
    v_paned.add(console_frame, minsize=100)

    # --- Setup PDF Viewer ---
    viewer_controls = tk.Frame(pdf_viewer_frame, bg=bg_main)
    viewer_controls.pack(side=tk.TOP, fill=tk.X)
    
    canvas_container = tk.Frame(pdf_viewer_frame, bg=bg_canvas)
    canvas_container.pack(fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(canvas_container, bg=bg_canvas, highlightthickness=0, cursor="crosshair")
    vbar = tk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=canvas.yview)
    hbar = tk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=canvas.xview)
    canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)
    hbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # --- Setup OCR Text Editor ---
    ocr_label = tk.Label(ocr_viewer_frame, text="Recognized Text", bg=bg_main, font=("Helvetica", 10, "bold"))
    ocr_label.pack(side=tk.TOP, fill=tk.X)
    
    ocr_text = ScrolledText(ocr_viewer_frame, wrap=tk.WORD, bg=bg_text, fg="black", font=("Times New Roman", 12))
    ocr_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # --- Setup Console ---
    console_label = tk.Label(console_frame, text="Terminal Output", bg=bg_main, anchor="w")
    console_label.pack(side=tk.TOP, fill=tk.X)
    output_text = ScrolledText(console_frame, wrap=tk.WORD, height=8, bg="#2e2e3e", fg="#ffffff", font=("Consolas", 10))
    output_text.pack(fill=tk.BOTH, expand=True)

    # PDF State
    draw_mode = tk.StringVar(value="text")
    viewer_state = {
        'pdf': None,
        'current_page': 0,
        'num_pages': 0,
        'scale': 1.0,
        'photo_img': None,
        'pil_image': None,
        'img_id': None,
        'rectangles': [],
        'temp_rect_id': None
    }
    
    page_label = tk.Label(viewer_controls, text="No PDF loaded", bg=bg_main)
    
    def show_page():
        if not viewer_state['pdf']: return
        page = viewer_state['pdf'][viewer_state['current_page']]
        bitmap = page.render(scale=viewer_state['scale'])
        pil_image = bitmap.to_pil()
        viewer_state['pil_image'] = pil_image
        viewer_state['photo_img'] = ImageTk.PhotoImage(pil_image)
        
        canvas.delete("all")
        viewer_state['img_id'] = canvas.create_image(0, 0, anchor=tk.NW, image=viewer_state['photo_img'])
        canvas.config(scrollregion=canvas.bbox("all"))
        page_label.config(text=f"Page {viewer_state['current_page'] + 1} of {viewer_state['num_pages']}")
        viewer_state['rectangles'] = []
        viewer_state['temp_rect_id'] = None

    def prev_page():
        if viewer_state['current_page'] > 0:
            viewer_state['current_page'] -= 1
            show_page()

    def next_page():
        if viewer_state['current_page'] < viewer_state['num_pages'] - 1:
            viewer_state['current_page'] += 1
            show_page()

    def zoom_in():
        viewer_state['scale'] *= 1.2
        show_page()

    def zoom_out():
        viewer_state['scale'] /= 1.2
        show_page()

    def load_pdf():
        filepath = filedialog.askopenfilename(title="Select a PDF", filetypes=[("PDF files", "*.pdf")])
        if not filepath:
            return
        try:
            viewer_state['pdf'] = pdfium.PdfDocument(filepath)
            viewer_state['num_pages'] = len(viewer_state['pdf'])
            viewer_state['current_page'] = 0
            viewer_state['scale'] = 1.0
            show_page()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PDF: {e}")

    # Bounding Box Logic
    HANDLE_SIZE = 7   # pixels — radius of corner resize handle squares
    start_x = start_y = 0
    drag_state = {
        'mode': None,         # 'draw' | 'move' | 'resize'
        'target': None,       # dict entry from viewer_state['rectangles']
        'offset_x': 0,
        'offset_y': 0,
        'anchor': None,       # (ax, ay) — fixed corner when resizing
        'handle_ids': [],     # canvas IDs of the small corner squares
    }

    # -----------------------------------------------------------------
    # Helper: draw/refresh small square handles on all rectangles
    # -----------------------------------------------------------------
    def refresh_handles():
        for hid in drag_state['handle_ids']:
            canvas.delete(hid)
        drag_state['handle_ids'] = []

        for r in viewer_state['rectangles']:
            x1, y1, x2, y2 = r['coords']
            corners = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
            for cx, cy in corners:
                hid = canvas.create_rectangle(
                    cx - HANDLE_SIZE, cy - HANDLE_SIZE,
                    cx + HANDLE_SIZE, cy + HANDLE_SIZE,
                    fill='white', outline=('green' if r['type'] == 'text' else 'blue'),
                    width=2, tags='handle'
                )
                drag_state['handle_ids'].append(hid)

    # -----------------------------------------------------------------
    # Helper: find which corner handle (and its parent rect) was clicked
    # Returns (rect_dict, anchor_x, anchor_y) or None
    # -----------------------------------------------------------------
    def find_handle_at(cx, cy):
        for r in viewer_state['rectangles']:
            x1, y1, x2, y2 = r['coords']
            corners = [(x1, y1, x2, y2), (x2, y1, x1, y2),
                       (x1, y2, x2, y1), (x2, y2, x1, y1)]
            # (hx, hy) is the handle corner; (ax, ay) is the opposite (anchor)
            for hx, hy, ax, ay in corners:
                if abs(cx - hx) <= HANDLE_SIZE + 2 and abs(cy - hy) <= HANDLE_SIZE + 2:
                    return r, ax, ay
        return None

    def find_rect_at(cx, cy):
        """Return the topmost rectangle body that contains (cx, cy), or None."""
        for r in reversed(viewer_state['rectangles']):
            x1, y1, x2, y2 = r['coords']
            if x1 <= cx <= x2 and y1 <= cy <= y2:
                return r
        return None

    def on_button_press(event):
        nonlocal start_x, start_y
        cx = canvas.canvasx(event.x)
        cy = canvas.canvasy(event.y)

        # Priority 1: resize handle
        result = find_handle_at(cx, cy)
        if result:
            r, ax, ay = result
            drag_state['mode'] = 'resize'
            drag_state['target'] = r
            drag_state['anchor'] = (ax, ay)
            canvas.config(cursor="sizing")
            return

        # Priority 2: move existing rect
        hit = find_rect_at(cx, cy)
        if hit:
            drag_state['mode'] = 'move'
            drag_state['target'] = hit
            drag_state['offset_x'] = cx - hit['coords'][0]
            drag_state['offset_y'] = cy - hit['coords'][1]
            canvas.config(cursor="fleur")
            return

        # Priority 3: draw new rectangle
        start_x, start_y = cx, cy
        drag_state['mode'] = 'draw'
        drag_state['target'] = None
        if viewer_state['temp_rect_id']:
            canvas.delete(viewer_state['temp_rect_id'])
        color = 'green' if draw_mode.get() == 'text' else 'blue'
        viewer_state['temp_rect_id'] = canvas.create_rectangle(cx, cy, cx, cy, outline=color, width=2)
        canvas.config(cursor="crosshair")

    def on_move_press(event):
        cx = canvas.canvasx(event.x)
        cy = canvas.canvasy(event.y)
        mode = drag_state['mode']

        if mode == 'resize':
            r = drag_state['target']
            ax, ay = drag_state['anchor']
            x1, x2 = min(ax, cx), max(ax, cx)
            y1, y2 = min(ay, cy), max(ay, cy)
            r['coords'] = (x1, y1, x2, y2)
            canvas.coords(r['id'], x1, y1, x2, y2)
            refresh_handles()
            refresh_dividers(r)

        elif mode == 'move':
            r = drag_state['target']
            x1, y1, x2, y2 = r['coords']
            w = x2 - x1
            h = y2 - y1
            dx = (cx - drag_state['offset_x']) - x1
            dy = (cy - drag_state['offset_y']) - y1
            new_x1 = x1 + dx
            new_y1 = y1 + dy
            new_x2 = new_x1 + w
            new_y2 = new_y1 + h
            # also shift dividers
            for div in r.get('dividers', []):
                if div['type'] == 'col':
                    div['x'] += dx
                else:
                    div['y'] += dy
            r['coords'] = (new_x1, new_y1, new_x2, new_y2)
            canvas.coords(r['id'], new_x1, new_y1, new_x2, new_y2)
            refresh_handles()
            refresh_dividers(r)

        elif mode == 'draw' and viewer_state['temp_rect_id']:
            canvas.coords(viewer_state['temp_rect_id'], start_x, start_y, cx, cy)

    def on_button_release(event):
        mode = drag_state['mode']

        if mode in ('resize', 'move'):
            drag_state['mode'] = None
            drag_state['target'] = None
            canvas.config(cursor="crosshair")
            refresh_handles()
            return

        if mode != 'draw':
            return

        drag_state['mode'] = None
        end_x = canvas.canvasx(event.x)
        end_y = canvas.canvasy(event.y)

        x1, x2 = min(start_x, end_x), max(start_x, end_x)
        y1, y2 = min(start_y, end_y), max(start_y, end_y)

        if x2 - x1 < 10 or y2 - y1 < 10:
            if viewer_state['temp_rect_id']:
                canvas.delete(viewer_state['temp_rect_id'])
                viewer_state['temp_rect_id'] = None
            return

        viewer_state['rectangles'].append({
            'id': viewer_state['temp_rect_id'],
            'type': draw_mode.get(),
            'coords': (x1, y1, x2, y2),
            'dividers': []
        })
        viewer_state['temp_rect_id'] = None
        refresh_handles()

    # -----------------------------------------------------------------
    # Refresh divider lines for a single rectangle
    # -----------------------------------------------------------------
    def refresh_dividers(r):
        """Redraw all divider lines of rectangle r to clamp inside its bounds."""
        rx1, ry1, rx2, ry2 = r['coords']
        for div in r.get('dividers', []):
            if div.get('line_id'):
                canvas.delete(div['line_id'])
            if div['type'] == 'col':
                x = max(rx1, min(div['x'], rx2))   # clamp
                div['line_id'] = canvas.create_line(x, ry1, x, ry2, fill='blue', width=1, dash=(4, 2))
            else:
                y = max(ry1, min(div['y'], ry2))
                div['line_id'] = canvas.create_line(rx1, y, rx2, y, fill='blue', width=1, dash=(4, 2))

    # -----------------------------------------------------------------
    # Right-click context menu: add divider lines to TABLE rectangles
    # -----------------------------------------------------------------
    def on_right_click(event):
        cx = canvas.canvasx(event.x)
        cy = canvas.canvasy(event.y)
        r = find_rect_at(cx, cy)
        if not r or r['type'] != 'table':
            return   # only for table rectangles

        menu = tk.Menu(root, tearoff=0)

        def add_col_line():
            rx1, ry1, rx2, ry2 = r['coords']
            if not (rx1 < cx < rx2):
                return
            div = {'type': 'col', 'x': cx, 'line_id': None}
            r['dividers'].append(div)
            refresh_dividers(r)

        def add_row_line():
            rx1, ry1, rx2, ry2 = r['coords']
            if not (ry1 < cy < ry2):
                return
            div = {'type': 'row', 'y': cy, 'line_id': None}
            r['dividers'].append(div)
            refresh_dividers(r)

        def remove_last_divider():
            if r['dividers']:
                div = r['dividers'].pop()
                if div.get('line_id'):
                    canvas.delete(div['line_id'])

        menu.add_command(label="Add Column Line", command=add_col_line)
        menu.add_command(label="Add Row Line", command=add_row_line)
        menu.add_separator()
        menu.add_command(label="Remove Last Line", command=remove_last_divider)
        menu.tk_popup(event.x_root, event.y_root)


    def clear_rectangles():
        for r in viewer_state['rectangles']:
            canvas.delete(r['id'])
            for div in r.get('dividers', []):
                if div.get('line_id'):
                    canvas.delete(div['line_id'])
        viewer_state['rectangles'] = []
        for hid in drag_state['handle_ids']:
            canvas.delete(hid)
        drag_state['handle_ids'] = []
        if viewer_state['temp_rect_id']:
            canvas.delete(viewer_state['temp_rect_id'])
            viewer_state['temp_rect_id'] = None

    def recognize_areas():
        if not viewer_state['pil_image'] or not viewer_state['rectangles']:
            messagebox.showinfo("Info", "Please draw selection areas first.")
            return
            
        def do_ocr():
            try:
                def update_ui_start():
                    ocr_text.delete(1.0, tk.END)
                    ocr_text.insert(tk.END, "[Recognizing selected areas...]\n\n")
                root.after(0, update_ui_start)
                
                if os.path.exists(r'C:\Users\phsds\Programming\PDF-Tools\tesseract\tesseract.exe'):
                    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\phsds\Programming\PDF-Tools\tesseract\tesseract.exe'
                    
                full_text = ""
                
                for i, r in enumerate(viewer_state['rectangles']):
                    crop = viewer_state['pil_image'].crop(r['coords'])
                    rx1, ry1, rx2, ry2 = r['coords']

                    full_text += f"--- Block {i+1} ({r['type'].upper()}) ---\n"

                    if r['type'] == 'table' and r.get('dividers'):
                        # Build sorted cut positions
                        col_cuts = sorted(set(
                            int(d['x'] - rx1) for d in r['dividers'] if d['type'] == 'col'
                        ))
                        row_cuts = sorted(set(
                            int(d['y'] - ry1) for d in r['dividers'] if d['type'] == 'row'
                        ))
                        w = rx2 - rx1
                        h = ry2 - ry1
                        col_boundaries = [0] + col_cuts + [int(w)]
                        row_boundaries = [0] + row_cuts + [int(h)]

                        rows_text = []
                        for ri in range(len(row_boundaries) - 1):
                            row_cells = []
                            for ci in range(len(col_boundaries) - 1):
                                cell = crop.crop((
                                    col_boundaries[ci], row_boundaries[ri],
                                    col_boundaries[ci+1], row_boundaries[ri+1]
                                ))
                                cell_text = pytesseract.image_to_string(
                                    cell, lang='eng', config='--psm 6'
                                ).strip().replace('\n', ' ')
                                row_cells.append(cell_text)
                            rows_text.append(' | '.join(row_cells))
                        full_text += '\n'.join(rows_text) + '\n\n'
                    else:
                        config = '--psm 6' if r['type'] == 'table' else ''
                        text = pytesseract.image_to_string(crop, lang='eng', config=config)
                        full_text += text.strip() + '\n\n'
                    
                def update_ui_end(text):
                    ocr_text.delete(1.0, tk.END)
                    ocr_text.insert(tk.END, text)
                root.after(0, update_ui_end, full_text)
                
            except Exception as e:
                def update_ui_err(err):
                    print(f"OCR Error: {err}")
                root.after(0, update_ui_err, e)
                
        threading.Thread(target=do_ocr, daemon=True).start()

    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_move_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)
    canvas.bind("<ButtonPress-3>", on_right_click)

    # Viewer controls
    btn_prev = tk.Button(viewer_controls, text="◄ Prev", command=prev_page, **btn_style)
    btn_prev.pack(side=tk.LEFT, padx=5, pady=2)
    page_label.pack(side=tk.LEFT, padx=5, pady=2)
    btn_next = tk.Button(viewer_controls, text="Next ►", command=next_page, **btn_style)
    btn_next.pack(side=tk.LEFT, padx=5, pady=2)
    
    tk.Label(viewer_controls, text="|", bg=bg_main).pack(side=tk.LEFT, padx=5)
    
    tk.Radiobutton(viewer_controls, text="Text", variable=draw_mode, value="text", bg=bg_main).pack(side=tk.LEFT)
    tk.Radiobutton(viewer_controls, text="Table", variable=draw_mode, value="table", bg=bg_main).pack(side=tk.LEFT)
    
    tk.Button(viewer_controls, text="Clear", command=clear_rectangles, **btn_style).pack(side=tk.LEFT, padx=5)
    
    btn_recognize = tk.Button(viewer_controls, text="Recognize Page", command=recognize_areas, bg="#4a90e2", fg="white", relief="flat", font=("Helvetica", 10, "bold"))
    btn_recognize.pack(side=tk.RIGHT, padx=5, pady=2)
    
    btn_zout = tk.Button(viewer_controls, text="Zoom Out (-)", command=zoom_out, **btn_style)
    btn_zout.pack(side=tk.RIGHT, padx=5, pady=2)
    btn_zin = tk.Button(viewer_controls, text="Zoom In (+)", command=zoom_in, **btn_style)
    btn_zin.pack(side=tk.RIGHT, padx=5, pady=2)
    btn_zin = tk.Button(viewer_controls, text="Zoom In (+)", command=zoom_in, **btn_style)
    btn_zin.pack(side=tk.LEFT, padx=5, pady=2)
    btn_zout = tk.Button(viewer_controls, text="Zoom Out (-)", command=zoom_out, **btn_style)
    btn_zout.pack(side=tk.LEFT, padx=5, pady=2)

    # Top Toolbar Buttons
    tk.Button(toolbar, text="Open PDF", command=load_pdf, **btn_style).pack(side=tk.LEFT, padx=5, pady=5)
    
    def make_action(func):
        def wrapper():
            func()
        return wrapper
        
    tk.Button(toolbar, text="Text Extraction", command=make_action(text_extraction), **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Image Extraction", command=make_action(image_extraction), **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Merge PDFs", command=make_action(pdf_merge), **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Split PDFs", command=make_action(pdf_split_combine), **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar, text="Handwritten OCR", command=make_action(pdf_requests), **btn_style).pack(side=tk.LEFT, padx=5)
    
    tk.Button(toolbar, text="Exit", command=finish_program, bg="#e74c3c", fg="white", relief="flat").pack(side=tk.RIGHT, padx=5)

    # Terminal Logic
    class GuiStdin:
        def __init__(self, text_widget):
            self.text_widget = text_widget
            self.queue = queue.Queue()
            self.last_prompt_index = None

        def _show_prompt(self):
            try:
                end_index = self.text_widget.index('end-1c')
                last_char = self.text_widget.get(f"{end_index}", f"{end_index}")
            except Exception:
                last_char = "\n"
            if not last_char.endswith("\n"):
                self.text_widget.insert('end', "\n")
            self.text_widget.insert('end', ">>> ")
            self.text_widget.see('end')
            self.last_prompt_index = self.text_widget.index('end-1c')
            self.text_widget.focus_set()

        def readline(self, *args, **kwargs):
            try:
                self.text_widget.after(0, self._show_prompt)
            except Exception:
                pass
            line = self.queue.get()
            return line + "\n"

        def read(self, *args, **kwargs):
            return self.readline()

    gui_stdin = GuiStdin(output_text)

    def _on_enter(event):
        try:
            if gui_stdin.last_prompt_index:
                start = gui_stdin.last_prompt_index
                user_text = output_text.get(start, 'end-1c')
                user_text = user_text.rstrip('\n')
                gui_stdin.queue.put(user_text)
                output_text.insert('end', '\n')
                gui_stdin.last_prompt_index = None
                return 'break'
            else:
                line = output_text.get('insert linestart', 'insert lineend')
                gui_stdin.queue.put(line)
                output_text.insert('end', '\n')
                return 'break'
        except Exception as e:
            print(f"Error handling input: {e}")
            return None

    output_text.config(state='normal')
    output_text.bind('<Return>', _on_enter)
    import sys as _sys
    _sys.stdin = gui_stdin
    sys.stdout = RedirectOutput(output_text)
    sys.stderr = RedirectOutput(output_text)

    def initialize_check_path():
        print("Initializing check_path function...\n")
        tools.check_paths()
        def clear_terminal():
            output_text.delete(1.0, tk.END)
        root.after(1000, clear_terminal)

    root.after(100, initialize_check_path)

    try:
        def _show_attention_popup():
            def _create():
                    top = tk.Toplevel(root)
                    top.title("ATENÇÃO!")
                    popup_w, popup_h = 520, 160
                    screen_w = root.winfo_screenwidth()
                    screen_h = root.winfo_screenheight()
                    pos_x = (screen_w - popup_w) // 2
                    pos_y = (screen_h - popup_h) // 2
                    top.geometry(f"{popup_w}x{popup_h}+{pos_x}+{pos_y}")
                    top.attributes("-topmost", True)
                    top.lift()
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