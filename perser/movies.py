import requests
from bs4 import BeautifulSoup

URL = "https://kinogo.biz/"

HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}


def get_html(url, params=''):
    req = requests.get(url, headers=HEADER, params=params)
    return req


def get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_="shortstory")
    movies = []
    for item in items:
        movies.append({
            'link': item.find('div', class_='shortimg').find('a').get('href'),
            'name': item.find('h2', class_='zagolovki').find("a").getText().split(' (')[0],
            'year': item.find('div', style='padding-top:7px').find('a').getText(),
            'country': f"{item.find('div', style='padding-top:7px').find_all('a')[1].getText()}, {item.find('div', style='padding-top:7px').find_all('a')[2].getText()}",
            'viewers': f"{soup.find('div', class_='icons').find('span', style='float:left; padding: 7px 20px 19px 20px;').find_all('span')[0].get('title')} {soup.find('div', class_='icons').find('span', style='float:left; padding: 7px 20px 19px 20px;').find_all('span')[1].get('title')}",
        })
    # print(movies)
    return movies
#
# html = get_html(URL)
# get_data(html.text)


def perser():
    html = get_html(URL)
    if html.status_code == 200:
        answer = []
        for page in range(1, 2):
            html = get_html(f"{URL}page/{page}/")
            answer.extend(get_data(html.text))
        return answer
    else:
        raise Exception("ой бой неправильный парсер!")
