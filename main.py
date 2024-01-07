import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import QSize

class ProxyFetcherGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Proxy Fetcher")
        self.setGeometry(100, 100, 800, 600)

        # Ustawienie tła (upewnij się, że ścieżka do obrazu jest poprawna)
        oImage = QPixmap(r'H:\bot\tlo.jpg')  # Zmień na właściwą ścieżkę
        sImage = oImage.scaled(QSize(800, 600))  # Dostosuj rozmiar do potrzeb
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        # Tworzenie zakładek
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Dodawanie zakładek
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        # Tworzenie layoutów dla zakładek
        self.tab1.layout = QVBoxLayout()
        self.tab2.layout = QVBoxLayout()

        # Dodawanie widgetów do pierwszej zakładki
        self.text_edit = QTextEdit()
        self.tab1.layout.addWidget(self.text_edit)
        self.button = QPushButton("Fetch Proxies")
        self.tab1.layout.addWidget(self.button)
        self.tab1.setLayout(self.tab1.layout)

        # Tutaj możesz dodać widgety do drugiej zakładki

        # Ustawianie zakładek jako centralnego widgetu
        self.setCentralWidget(self.tabs)

        # Połączenie sygnałów z przyciskiem (jeśli potrzebne)
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        # Logika obsługi przycisku
        self.text_edit.append("Button clicked!")

def main():
    app = QApplication(sys.argv)
    ex = ProxyFetcherGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
