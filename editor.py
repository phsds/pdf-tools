import sys
import os
import fitz  # PyMuPDF
import PyQt5

from PyQt5.QtCore import Qt, QRectF, QSize
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QAction,
    QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QListWidget, QInputDialog, QSlider, QMessageBox, QSplitter
)


def pixmap_from_page(page, zoom=1.0):
    """Renderiza uma página do PDF em QPixmap com zoom."""
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
    return QPixmap.fromImage(img.copy())


class PDFPageView(QLabel):
    """
    Widget que exibe uma página do PDF e captura cliques.
    Converte coordenadas da tela em coordenadas do PDF.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setBackgroundRole(QLabel.Base)
        self.setScaledContents(False)

        self.page = None           # fitz.Page
        self.zoom = 1.0
        self.click_callback = None # função(page, pdf_x, pdf_y)

    def set_page(self, page, zoom=1.0):
        self.page = page
        self.zoom = zoom
        if page is None:
            self.setPixmap(QPixmap())
            return

        pix = pixmap_from_page(page, zoom=self.zoom)
        self.setPixmap(pix)

    def set_zoom(self, zoom):
        if self.page is None:
            return
        self.zoom = zoom
        pix = pixmap_from_page(self.page, zoom=self.zoom)
        self.setPixmap(pix)

    def mousePressEvent(self, event):
        if self.page is None or self.pixmap() is None:
            return
        if event.button() != Qt.LeftButton:
            return

        label_width = self.width()
        label_height = self.height()
        pixmap = self.pixmap()
        pix_w = pixmap.width()
        pix_h = pixmap.height()

        # Centralização da imagem no label
        offset_x = (label_width - pix_w) / 2 if label_width > pix_w else 0
        offset_y = (label_height - pix_h) / 2 if label_height > pix_h else 0

        mouse_x = event.x() - offset_x
        mouse_y = event.y() - offset_y

        if mouse_x < 0 or mouse_y < 0 or mouse_x > pix_w or mouse_y > pix_h:
            return  # clique fora da imagem

        # Mapeia coordenadas de imagem para coordenadas de página
        pdf_x = mouse_x / self.zoom
        pdf_y = mouse_y / self.zoom

        # PyMuPDF usa origem no canto superior esquerdo para get_text("dict"),
        # então não precisamos inverter Y aqui.

        if self.click_callback:
            self.click_callback(self.page, pdf_x, pdf_y)


class PDFEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Acrobat em Python - Editor de PDF")
        self.resize(1200, 800)

        self.doc = None            # fitz.Document
        self.current_page_index = 0
        self.current_zoom = 1.5

        self._create_actions()
        self._create_menu()
        self._create_ui()

    # ---------- UI / Menu ----------

    def _create_actions(self):
        self.open_action = QAction("Abrir PDF...", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_pdf)

        self.save_as_action = QAction("Salvar como...", self)
        self.save_as_action.setShortcut("Ctrl+S")
        self.save_as_action.triggered.connect(self.save_pdf_as)
        self.save_as_action.setEnabled(False)

        self.exit_action = QAction("Sair", self)
        self.exit_action.triggered.connect(self.close)

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Arquivo")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

    def _create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        splitter = QSplitter(Qt.Horizontal)

        # Lista de páginas (sidebar)
        self.page_list = QListWidget()
        self.page_list.currentRowChanged.connect(self.on_page_selected)

        # Visualizador de página
        self.page_view = PDFPageView()
        self.page_view.click_callback = self.on_page_clicked

        # Slider de zoom
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(5)   # 0.5x
        self.zoom_slider.setMaximum(30)  # 3.0x
        self.zoom_slider.setValue(int(self.current_zoom * 10))
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)

        zoom_label = QLabel("Zoom:")
        zoom_layout = QHBoxLayout()
        zoom_layout.addWidget(zoom_label)
        zoom_layout.addWidget(self.zoom_slider)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.page_view)
        right_layout.addLayout(zoom_layout)

        right_container = QWidget()
        right_container.setLayout(right_layout)

        splitter.addWidget(self.page_list)
        splitter.addWidget(right_container)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

    # ---------- Ações principais ----------

    def open_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecione um arquivo PDF", "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if not file_path:
            return

        try:
            doc = fitz.open(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível abrir o PDF:\n{e}")
            return

        self.doc = doc
        self.current_page_index = 0
        self.page_list.clear()

        for i in range(len(self.doc)):
            self.page_list.addItem(f"Página {i + 1}")

        if len(self.doc) > 0:
            self.page_list.setCurrentRow(0)
            self.load_page(0)

        self.save_as_action.setEnabled(True)
        self.setWindowTitle(f"Mini Acrobat - {os.path.basename(file_path)}")

    def load_page(self, index):
        if self.doc is None:
            return
        if index < 0 or index >= len(self.doc):
            return

        self.current_page_index = index
        page = self.doc[index]
        self.page_view.set_page(page, zoom=self.current_zoom)

    def on_page_selected(self, row):
        if row >= 0:
            self.load_page(row)

    def on_zoom_changed(self, value):
        self.current_zoom = value / 10.0
        if self.doc is not None:
            page = self.doc[self.current_page_index]
            self.page_view.set_page(page, zoom=self.current_zoom)

    # ---------- Edição de texto ----------

    def on_page_clicked(self, page, pdf_x, pdf_y):
        """
        Disparado quando o usuário clica na página.
        Vamos descobrir qual 'span' de texto foi clicado, mostrar
        um diálogo para edição e substituir o texto.
        """

        try:
            text_dict = page.get_text("dict")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao ler texto da página:\n{e}")
            return

        clicked_span = None
        clicked_bbox = None

        # Encontrar span clicado
        for block in text_dict.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    x0, y0, x1, y1 = span["bbox"]
                    if x0 <= pdf_x <= x1 and y0 <= pdf_y <= y1:
                        clicked_span = span
                        clicked_bbox = (x0, y0, x1, y1)
                        break
                if clicked_span:
                    break
            if clicked_span:
                break

        if not clicked_span:
            return  # clicou em área sem texto

        original_text = clicked_span["text"]

        novo_texto, ok = QInputDialog.getText(
            self,
            "Editar texto",
            f"Texto atual:\n{original_text}\n\nNovo texto:"
        )

        if not ok or novo_texto == original_text or novo_texto.strip() == "":
            return

        self.replace_text_in_span(page, clicked_span, clicked_bbox, novo_texto)

    def replace_text_in_span(self, page, span, bbox, novo_texto):
        """
        Remove o texto atual naquela área e insere o novo texto
        usando a mesma fonte e tamanho.
        """

        x0, y0, x1, y1 = bbox
        rect = fitz.Rect(x0, y0, x1, y1)

        fontname = span.get("font", "helv")
        fontsize = span.get("size", 12)
        color = span.get("color", 0)  # inteiro; converter para RGB

        # Converter cor do span (inteiro) em RGB 0-1
        # PyMuPDF guarda cor como inteiro com bits de R,G,B ou como float, varia por versão
        # Para simplificar, vamos usar preto:
        rgb = (0, 0, 0)

        try:
            page.add_redact_annot(rect, fill=(1, 1, 1))
            page.apply_redactions()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao apagar texto:\n{e}")
            return

        try:
            # Inserir texto novo
            page.insert_text(
                rect.tl,               # canto superior esquerdo
                novo_texto,
                fontsize=fontsize,
                fontname=fontname,
                color=rgb
            )
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao inserir texto:\n{e}")
            return

        # Atualizar visualização
        self.load_page(self.current_page_index)

    # ---------- Salvar ----------

    def save_pdf_as(self):
        if self.doc is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar PDF como", "",
            "PDF Files (*.pdf);;All Files (*)"
        )

        if not file_path:
            return

        try:
            self.doc.save(file_path)
            QMessageBox.information(self, "Sucesso", "PDF salvo com sucesso.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar PDF:\n{e}")


def main():
    app = QApplication(sys.argv)
    editor = PDFEditor()
    editor.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()