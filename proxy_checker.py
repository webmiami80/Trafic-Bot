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

def is_proxy_working(proxy):
    # Performing a series of tests to check the proxy quality
    # For example, making requests to multiple endpoints
    endpoints = ['http://example.com', 'https://api.ipify.org']
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, proxies={'http': proxy, 'https': proxy}, timeout=5)
            if response.status_code != 200:
                return False
        except requests.RequestException:
            return False
    return True

def check_socks_proxy(proxy):
    # Implementing the logic to check a SOCKS proxy.
    # This is just a placeholder as the actual implementation will depend on the SOCKS protocol version and other factors.
    pass
