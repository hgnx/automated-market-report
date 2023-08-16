import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from tools.url_shortener import get_shortened_url

USER_AGENT                  = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

def parse(url, user_agent=USER_AGENT, encoding="utf-8", max_retries=3, wait_time=5):
    headers                 = {"User-Agent": user_agent}
    for retry in range(max_retries):
        try:
            response        = requests.get(url, headers=headers)
            response.encoding = encoding
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Retrying {retry+1}/{max_retries}: Error fetching data from {url} - {e}")
            if retry < max_retries - 1:
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
    print("Max retries reached. Could not fetch data.")
    return None

def extract_reuters(parsed_content):
    titles, urls            = [], []
    base_url                = "https://www.reuters.com"

    # Hero article
    try:
        hero_link           = parsed_content.select("div.content-layout__item__SC_GG > div > div > div.static-media-maximizer__hero__3I-8O > div > a")[0]
        titles.append(hero_link.text)
        urls.append(base_url + hero_link.get("href"))
    except:
        print("Error extracting Reuters hero article.")

    # Other articles
    for i in range(1, 7):
        try:
            link            = parsed_content.select(f"div.content-layout__item__SC_GG > div > ul > li:nth-of-type({i}) > div > div > header > a")[0]
            titles.append(link.text)
            urls.append(base_url + link.get("href"))
        except:
            print(f"Error extracting Reuters article {i}.")

    unwanted_texts          = [", article with image", ", article with video", ", article with gallery"]
    titles                  = [title for title in titles
                                if all(unwanted not in title for unwanted in unwanted_texts)]

    return list(zip(titles, urls))

def extract_ft(parsed_content):
    titles, urls            = [], []
    base_url                = "https://www.ft.com"

    for i in range(1, 6):
        try:
            link            = parsed_content.select(f"div.css-grid__sidebar > div:nth-of-type(3) > div.js-track-scroll-event > div > ol > li:nth-of-type({i}) > div > div > div > a")[0]
            titles.append(link.text)
            urls.append(base_url + link.get("href"))
        except:
            print(f"Error extracting FT article {i}.")
    
    return list(zip(titles, urls))

def get_news(max_retries=3, wait_time=5):
    reuters_parsed_content  = parse("https://www.reuters.com/markets/macromatters", max_retries=max_retries, wait_time=wait_time)
    if not reuters_parsed_content:
        return [("Error", "Error")], [("Error", "Error")]
    reuters_news            = extract_reuters(reuters_parsed_content)

    ft_parsed_content       = parse("https://www.ft.com/markets", max_retries=max_retries, wait_time=wait_time)
    if not ft_parsed_content:
        return [("Error", "Error")], [("Error", "Error")]
    ft_news                 = extract_ft(ft_parsed_content)

    return reuters_news, ft_news

def get_shortened_news():
    reuters_news, ft_news   = get_news()

    reuters_news_shortened  = []
    for title, url in tqdm(reuters_news, desc="Shortening Reuters URLs"):
        shortened_url       = get_shortened_url(url)
        reuters_news_shortened.append((title, shortened_url))
        time.sleep(0.5)

    ft_news_shortened       = []
    for title, url in tqdm(ft_news, desc="Shortening FT URLs"):
        shortened_url       = get_shortened_url(url)
        ft_news_shortened.append((title, shortened_url))
        time.sleep(0.5)
    
    return reuters_news_shortened, ft_news_shortened

def get_shortened_news():
    reuters_news, ft_news   = get_news()

    reuters_news_shortened  = []
    for title, url in tqdm(reuters_news, desc="Shortening Reuters URLs"):
        shortened_url       = get_shortened_url(url) if url != "Error" else "Error"
        reuters_news_shortened.append((title, shortened_url))
        time.sleep(0.5)

    ft_news_shortened       = []
    for title, url in tqdm(ft_news, desc="Shortening FT URLs"):
        shortened_url       = get_shortened_url(url) if url != "Error" else "Error"
        ft_news_shortened.append((title, shortened_url))
        time.sleep(0.5)
    
    return reuters_news_shortened, ft_news_shortened

def format_news_title(title):
    return f"&nbsp;&nbsp;&nbsp;&nbsp;{title}"

def format_news_url(url):
    return f"&nbsp;&nbsp;&nbsp;&nbsp;<font color=blue>{url}</font>"