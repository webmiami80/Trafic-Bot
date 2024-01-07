import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class ProxyFetcherGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Proxy Fetcher')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.proxy_display = QTextEdit()
        self.proxy_display.setReadOnly(True)
        self.proxy_display.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")
        self.layout.addWidget(self.proxy_display)

        self.fetch_and_display_proxies()

    def fetch_and_display_proxies(self):
        proxy_sources = [
            'https://www.sslproxies.org/',
            'https://www.google-proxy.net/',
            # ... more sources as provided
        ]

        for source in proxy_sources:
            proxies = self.fetch_proxies(source)
            for proxy in proxies:
                self.proxy_display.append(proxy)

    def fetch_proxies(self, source_url):
        try:
            response = requests.get(source_url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            return ["192.168.0.1:8080 - Dummy Proxy", "192.168.0.2:8080 - Dummy Proxy"]
        except requests.RequestException as e:
            return [f"Error fetching proxies: {e}"]

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = ProxyFetcherGUI()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
