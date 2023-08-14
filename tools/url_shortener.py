import requests
from urllib.parse import urlencode

user_agent                  = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
headers                     = {"User-Agent": user_agent}

def isgd(url):
    response                = requests.get(f"https://is.gd/create.php?format=simple&url={url}", headers=headers)
    response.encoding       = "utf-8"
    return response.text

def vgd(url):
    response                = requests.get(f"https://v.gd/create.php?format=simple&url={url}", headers=headers)
    response.encoding       = "utf-8"
    return response.text

def tinyurl(url):
    response                = requests.get(f"https://tinyurl.com/api-create.php?{urlencode({'url':url})}", headers=headers)
    response.encoding       = "utf-8"
    return response.text

def get_shortened_url(url):
    services                = [isgd, vgd, tinyurl]
    for service in services:
        try:
            return service(url)
        except requests.RequestException:
            continue
    return "URL Shortener connection error."