import requests
import concurrent.futures

def check_proxy(proxy_url):
    session = requests.Session()
    headers = {'User-Agent': 'YOUR_USER_AGENT'}
    session.headers.update(headers)
    try:
        response = session.get('https://www.google.com', proxies={'http': proxy_url, 'https': proxy_url}, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def get_proxy_info(proxy_url):
    response = requests.get(f'http://ipinfo.io/{proxy_url}/json', timeout=5)
    if response.status_code == 200:
        data = response.json()
        ip_address = data['ip']
        country = data['country']
        return ip_address, country
    else:
        return 'Unknown', 'Unknown'

with open('proxy.txt') as f:
    proxy_urls = [line.strip() for line in f]

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for proxy_url in proxy_urls:
        futures.append(executor.submit(check_proxy, proxy_url))

    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        if future.result():
            ip_address, country = get_proxy_info(proxy_urls[i])
            print(f"{proxy_urls[i]} is working with IP address {ip_address} from {country}.")
        else:
            print(f"{proxy_urls[i]} is not working or requires authentication.")
