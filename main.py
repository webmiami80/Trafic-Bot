import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import QSize
from proxy_scraper import get_all_proxies
from proxy_checker import check_proxies

class ProxyFetcherGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Proxy Fetcher")
        self.setGeometry(100, 100, 800, 600)

        # Ustawienie tła
        oImage = QPixmap('/mnt/data/tlo.jpg')
        sImage = oImage.scaled(QSize(800, 600))
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
        self.fetch_proxies_button = QPushButton("Fetch Proxies")
        self.tab1.layout.addWidget(self.fetch_proxies_button)
        self.check_proxies_button = QPushButton("Check Proxies")
        self.tab1.layout.addWidget(self.check_proxies_button)
        self.tab1.setLayout(self.tab1.layout)

        # Ustawianie zakładek jako centralnego widgetu
        self.setCentralWidget(self.tabs)

        # Połączenie sygnałów z przyciskami
        self.fetch_proxies_button.clicked.connect(self.fetch_and_display_proxies)
        self.check_proxies_button.clicked.connect(self.check_and_display_proxies)

    def fetch_and_display_proxies(self):
        proxies = get_all_proxies()
        self.text_edit.append("\n".join(proxies))

    
    def check_and_display_proxies(self):
        # Uruchomienie procesu sprawdzania proxy w oddzielnym wątku
        threading.Thread(target=self.run_check_proxies_thread).start()

    def run_check_proxies_thread(self):
        # Ta metoda będzie uruchamiana w oddzielnym wątku
        proxies = self.text_edit.toPlainText().split('\n')
        working_proxies = check_proxies(proxies)
        # Wywołanie metody aktualizacji interfejsu w głównym wątku
        self.text_edit.clear()
        self.text_edit.append("\n".join(working_proxies))
def check_and_display_proxies(self):
        proxies = self.text_edit.toPlainText().split('\n')
        working_proxies = check_proxies(proxies)
        self.text_edit.clear()
        self.text_edit.append("\n".join(working_proxies))

def main():
    app = QApplication(sys.argv)
    ex = ProxyFetcherGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


# Integrated proxy_scraper logic
import requests
from bs4 import BeautifulSoup
import time
import threading

# Lista źródeł proxy
proxy_sources = [
    'https://www.sslproxies.org/',
    'https://www.google-proxy.net/',
    'https://free-proxy-list.net/',
    'https://free-proxy-list.net/uk-proxy.html',
    'https://www.us-proxy.org/',
    'https://free-proxy-list.net/',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt',
    'https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=all&ssl=all&anonymity=all',
    'https://www.proxynova.com/proxy-server-list/',
    'https://www.proxy-list.download/HTTP',
    'https://www.proxy-list.download/HTTPS',
    'https://www.proxy-list.download/SOCKS4',
    'https://www.proxy-list.download/SOCKS5',
    # Dodaj więcej źródeł według potrzeb
]

def get_proxies_from_source(url):
    proxies = []
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        if table is not None:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) > 1:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.append(f"{ip}:{port}")
    except Exception as e:
        print(f"Error fetching proxies from {url}: {e}")
    return proxies

def get_all_proxies():
    all_proxies = []
    for source in proxy_sources:
        all_proxies.extend(get_proxies_from_source(source))
    return all_proxies

def refresh_proxies(interval=60):
    while True:
        global proxies
        proxies = get_all_proxies()
        time.sleep(interval)

# Uruchomienie odświeżania proxy w oddzielnym wątku
threading.Thread(target=refresh_proxies).start()


# Integrated proxy_checker logic
import requests
import concurrent.futures

def check_proxy(proxy):
    try:
        response = requests.get('http://example.com', proxies={"http": proxy, "https": proxy}, timeout=5)
        return proxy if response.status_code == 200 else None
    except requests.RequestException:
        return None

def check_proxies(proxy_list):
    working_proxies = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_proxy, proxy) for proxy in proxy_list]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                working_proxies.append(result)
    return working_proxies


# Integrated traffic_generator logic
import requests
from selenium import webdriver
import time
import random
import logging

# Ustawienia logowania
logging.basicConfig(filename='traffic_generation.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Lista przykładowych kodów krajów (ISO 3166-1 alpha-2)
country_codes = [
    'PL', 'US', 'CA', 'GB', 'AU', 'DE', 'FR', 'IT', 'ES', 'PT',
    'NL', 'BE', 'CH', 'SE', 'NO', 'FI', 'DK', 'AT', 'GR', 'IE',
    'NZ', 'JP', 'CN', 'IN', 'BR', 'AR', 'CL', 'MX', 'CO', 'PE',
    'VE', 'UY', 'PY', 'BO', 'EC', 'CR', 'SV', 'GT', 'HN', 'PA',
    'CU', 'DO', 'HT', 'JM', 'BS', 'TT', 'BB', 'GD', 'KN', 'LC',
    'VC', 'AG', 'DM', 'PM', 'BZ', 'NI'
]

def check_proxy(proxy):
    try:
        response = requests.get('http://example.com', proxies={"http": proxy, "https": proxy}, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        logging.error(f'Proxy {proxy} failed with error: {e}.')
        return False

def generate_traffic(proxy_list, url, browser, language, depth, country_code='PL'):
    # Filtruj proxy według podanego kodu kraju
    valid_proxies = [proxy for proxy in proxy_list if proxy['country_code'] == country_code.upper()]
    
    for proxy in valid_proxies:
        if check_proxy(proxy['ip']):
            # Konfiguracja proxy dla przeglądarki
            proxy_options = {
                'http': proxy['ip'],
                'https': proxy['ip']
            }

            # Ustawienia przeglądarki
            options = webdriver.ChromeOptions() if browser == 'chrome' else webdriver.FirefoxOptions()
            options.add_argument('--proxy-server=%s' % proxy['ip'])

            # Uruchomienie przeglądarki z wybranymi opcjami
            driver = webdriver.Chrome(options=options) if browser == 'chrome' else webdriver.Firefox(options=options)
            
            # Otwórz stronę
            driver.get(url)
            time.sleep(random.uniform(0.5, 3.0))  # Losowe opóźnienie

            # Symulacja interakcji użytkownika
            for _ in range(depth):
                # Tutaj możesz dodać logikę interakcji, np. kliknięcia, przewijanie strony
                pass

            driver.quit()
            logging.info(f'Traffic generated for {url} using proxy: {proxy["ip"]}')

# Przykładowa lista proxy
proxy_list = [{'ip': '192.168.1.1:8080', 'country_code': cc} for cc in country_codes]

# Generowanie ruchu
generate_traffic(proxy_list, "https://www.example.com", "chrome", "pl", 3)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_headless_browser():
    options = Options()
    options.headless = True  # Uruchomienie przeglądarki w trybie headless
    browser = webdriver.Chrome(options=options)  # Zastąp ścieżką do swojego sterownika Chrome, jeśli jest konieczne
    return browser

def generate_traffic(url, proxy=None):
    browser = create_headless_browser()
    if proxy:
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy,
            "proxyType": "MANUAL",
        }

    try:
        browser.get(url)
        # Tutaj można dodać dodatkowe interakcje z przeglądarką, np. przewijanie strony, klikanie itp.
        # ...
    finally:
        browser.quit()  # Zawsze zamknij przeglądarkę po zakończeniu

# Przykładowe wywołanie funkcji
generate_traffic("http://example.com", proxy="123.123.123.123:8080")

def create_browser_with_language_and_proxy(language_code, proxy=None):
    options = Options()
    options.add_argument(f"--lang={language_code}")  # Ustawienie języka przeglądarki

    if proxy:
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy,
            'ftpProxy': proxy,
            'sslProxy': proxy,
            'noProxy': ''  # no proxy for localhost and other necessary addresses
        })
        proxy.add_to_capabilities(options)

    browser = webdriver.Chrome(options=options)
    return browser

def generate_traffic_with_language_and_proxy(url, language_code, proxy=None):
    browser = create_browser_with_language_and_proxy(language_code, proxy)
    try:
        browser.get(url)
        # Dodaj tutaj więcej interakcji z przeglądarką
        # ...
    finally:
        browser.quit()

# Przykładowe wywołanie funkcji
generate_traffic_with_language_and_proxy("http://example.com", "en-US", proxy="123.123.123.123:8080")

import logging
from datetime import datetime

# Ustawienia logowania
logging.basicConfig(filename='bot_activity.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_activity(activity):
    logging.info(activity)

def generate_traffic_with_logging(url, proxy=None):
    start_time = datetime.now()
    try:
        # Przykładowa symulacja działania bota (np. otwarcie strony)
        log_activity(f"Odwiedzanie strony: {url}")

        # Symulacja zakończenia działania
        log_activity(f"Zakończono działanie na stronie: {url}")
    except Exception as e:
        log_activity(f"Błąd podczas działania na stronie {url}: {e}")
    finally:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log_activity(f"Czas trwania działania na stronie {url}: {duration} sekund")

# Przykładowe wywołanie funkcji
generate_traffic_with_logging("http://example.com", proxy="123.123.123.123:8080")

import random

# Funkcja symulująca opóźnienia dla realistycznego ruchu
def simulate_delay(min_delay=1, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))

# Funkcja do symulacji różnych przeglądarek i urządzeń
def set_user_agent(browser, user_agent):
    browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

# Funkcje do generowania różnych typów ruchu
def generate_direct_traffic(url, browser):
    browser.get(url)
    simulate_delay()

def generate_referential_traffic(url, referer_url, browser):
    browser.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': {'Referer': referer_url}})
    browser.get(url)
    simulate_delay()

def generate_social_media_traffic(url, browser):
    # Dodaj logikę dla ruchu z mediów społecznościowych
    pass

def generate_paid_ad_traffic(url, browser):
    # Dodaj logikę dla płatnych reklam
    pass

# Przykładowe wywołania funkcji
browser = create_browser_with_language_and_proxy("en-US", proxy="123.123.123.123:8080")
generate_direct_traffic("http://example.com", browser)
generate_referential_traffic("http://example.com", "http://referrer.com", browser)

import itertools

# Lista proxy do rotacji
proxy_list = ['123.123.123.123:8080', '124.124.124.124:8080', '125.125.125.125:8080']
proxy_pool = itertools.cycle(proxy_list)  # Tworzenie cyklicznego iteratora

def rotate_proxy():
    return next(proxy_pool)

def generate_traffic_with_proxy_rotation(url, language_code):
    proxy = rotate_proxy()
    browser = create_browser_with_language_and_proxy(language_code, proxy)
    try:
        browser.get(url)
        # Dodaj tutaj więcej interakcji z przeglądarką
        # ...
    finally:
        browser.quit()

# Przykładowe wywołanie funkcji
generate_traffic_with_proxy_rotation("http://example.com", "en-US")

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def simulate_clicks_and_forms(browser):
    # Symulacja kliknięcia na linki
    links = browser.find_elements(By.TAG_NAME, 'a')
    if links:
        random.choice(links).click()
        simulate_delay()

    # Powrót do głównej strony (dla przykładu)
    browser.back()

    # Symulacja wypełnienia formularza (jeśli istnieje)
    input_fields = browser.find_elements(By.TAG_NAME, 'input')
    for field in input_fields:
        if field.get_attribute('type') == 'text':
            field.send_keys('Przykładowy tekst')
        elif field.get_attribute('type') == 'submit':
            field.click()
            simulate_delay()
            break

def generate_advanced_traffic(url, language_code, proxy=None):
    browser = create_browser_with_language_and_proxy(language_code, proxy)
    try:
        browser.get(url)
        simulate_clicks_and_forms(browser)
    finally:
        browser.quit()

# Przykładowe wywołanie funkcji
generate_advanced_traffic("http://example.com", "en-US")

import schedule
import time

def job():
    print("Wykonanie zaplanowanego zadania...")
    # Tutaj można umieścić logikę bota, na przykład wywołanie funkcji generate_advanced_traffic

# Przykład ustawienia harmonogramu: uruchomienie funkcji job co godzinę
schedule.every(1).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
