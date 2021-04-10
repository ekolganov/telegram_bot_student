from bs4 import BeautifulSoup
import requests
import re

url = 'https://saharina.ru/dicts/'
my_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0)',
    'Accept': '*/*'
}


def get_html(url):
    """ф-я возращает ответ от url страницы"""
    resp = requests.get(url, headers=my_header)
    return resp


def get_content(html):
    """"""
    soup = BeautifulSoup(html, 'html.parser')
    main_container = soup.find(class_="tests-list")

    for items in main_container:
        header_grade = items.findNext(class_="tests_head").text
        theme_name = items.findNext(class_="list-item").find("a").text

        try:
            match = re.match(r"([5-9] класс).*", header_grade)
        except:
            pass
        if match:
            print(match.group(1))
            print(theme_name)


def parse():
    """ф-я парсинга если ответ ОК"""
    html = get_html(url)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print("Wrong status code")


parse()