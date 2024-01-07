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
