import requests
from bs4 import BeautifulSoup

URL = "https://www.kivano.kg/myshi-kompyuternye/"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}


def get_html(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_="pull-right rel")
    mouse = []
    for item in items:
        mouse.append({
            'name': item.find('div', class_='listbox_title oh').find("a").getText(),
            'link': item.find('div', class_='listbox_title oh').find('a').get('href'),
            'price': item.find('div', class_='listbox_price text-center').find('strong').getText(),
            'na sklade': item.find('div', class_='listbox_motive text-center').find('span').getText()
        })
    return mouse


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        answer = []
        for page in range(1, 2):
            html = get_html(f"{URL}page/{page}/")
            answer.extend(get_data(html.text))
        return answer
    else:
        raise Exception("ой бой неправильный парсер!")
