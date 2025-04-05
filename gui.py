import sys
import tools
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import time  # Para simular atrasos entre etapas, se necessário

class RedirectOutput:
    """Classe para redirecionar stdout e stderr para o widget de texto."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)  # Insere a mensagem no final do widget
        self.text_widget.see(tk.END)  # Rola automaticamente para o final
        self.text_widget.update_idletasks()  # Atualiza a GUI imediatamente

    def flush(self):
        pass  # Necessário para compatibilidade com sys.stdout e sys.stderr

def text_extraction():
    print('Iniciando extração de texto...\n')
    time.sleep(1)  # Simula uma etapa demorada
    print('Abrindo arquivo PDF...\n')
    time.sleep(1)  # Simula outra etapa
    tools.extractText()  # Certifique-se de que esta função exibe mensagens de progresso
    print('Extração de texto concluída.\n')
    messagebox.showinfo("Success", "Text extraction completed!")

def image_extraction():
    print('Iniciando extração de imagens...\n')
    time.sleep(1)  # Simula uma etapa demorada
    print('Processando páginas do PDF...\n')
    time.sleep(1)  # Simula outra etapa
    tools.extractImage()  # Certifique-se de que esta função exibe mensagens de progresso
    print('Extração de imagens concluída.\n')
    messagebox.showinfo("Success", "Image extraction completed!")

def pdf_merge():
    print('Iniciando combinação de PDFs...\n')
    time.sleep(1)  # Simula uma etapa demorada
    print('Lendo arquivos PDF...\n')
    time.sleep(1)  # Simula outra etapa
    tools.merge_pdfs()  # Certifique-se de que esta função exibe mensagens de progresso
    print('Combinação de PDFs concluída.\n')
    messagebox.showinfo("Success", "PDFs merged successfully!")

def pdf_split_combine():
    print('Iniciando divisão e combinação de PDFs...\n')
    time.sleep(1)  # Simula uma etapa demorada
    print('Dividindo páginas selecionadas...\n')
    time.sleep(1)  # Simula outra etapa
    tools.split_combine()  # Certifique-se de que esta função exibe mensagens de progresso
    print('Divisão e combinação de PDFs concluída.\n')
    messagebox.showinfo("Success", "PDF split and combine completed!")

def finish_program():
    print("Encerrando o programa...\n")
    sys.exit(0)

def main_menu():
    # Cria a janela principal
    root = tk.Tk()
    root.title("PDF Tools")
    root.geometry("600x500")

    # Título
    title_label = tk.Label(root, text="PDF Tools", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # Botões para as opções
    btn_text_extraction = tk.Button(root, text="Text Extraction", command=text_extraction, width=30)
    btn_text_extraction.pack(pady=5)

    btn_image_extraction = tk.Button(root, text="Image Extraction", command=image_extraction, width=30)
    btn_image_extraction.pack(pady=5)

    btn_pdf_merge = tk.Button(root, text="PDF Merge", command=pdf_merge, width=30)
    btn_pdf_merge.pack(pady=5)

    btn_pdf_split_combine = tk.Button(root, text="PDF Split/Combine", command=pdf_split_combine, width=30)
    btn_pdf_split_combine.pack(pady=5)

    btn_finish = tk.Button(root, text="Finish Program", command=finish_program, width=30, bg="red", fg="white")
    btn_finish.pack(pady=20)

    # Widget de texto para exibir a saída do terminal
    output_text = ScrolledText(root, wrap=tk.WORD, height=15, width=70)
    output_text.pack(pady=10)

    # Redireciona stdout e stderr para o widget de texto
    sys.stdout = RedirectOutput(output_text)
    sys.stderr = RedirectOutput(output_text)

    # Inicia o loop principal da interface gráfica
    root.mainloop()

if __name__ == "__main__":
    main_menu()