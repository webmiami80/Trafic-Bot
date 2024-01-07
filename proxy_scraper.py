
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
    'https://www.proxynova.com/proxy-server-list/'
    'https://www.proxy-list.download/HTTP'
    'https://www.proxy-list.download/HTTPS'
    'https://www.proxy-list.download/SOCKS4'
    'https://www.proxy-list.download/SOCKS5'
    # Dodaj więcej źródeł według potrzeb
]

def get_proxies_from_source(url):
    proxies = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 2:
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxies.append(f'{ip}:{port}')
    except requests.exceptions.RequestException:
        pass
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
