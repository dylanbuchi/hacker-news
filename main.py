import requests
import json
import os
from pprint import pprint
from bs4 import BeautifulSoup


def sort_news_by_upvotes(news: list):
    return sorted(news, reverse=True, key=lambda i: i['upvotes'])


def get_custom_news(links, subtexts):
    news = []

    for i, item in enumerate(links):
        title = item.getText()
        link = item.get('href', None)
        upvote = subtexts[i].select('.score')

        if len(upvote):
            upvotes = int(upvote[0].getText().replace(' points', ''))

            if upvotes >= 70:
                temp = {'title': title, 'link': link, 'upvotes': upvotes}
                news.append(temp)

    return sort_news_by_upvotes(news)


def web_scrap(url: str, page: int):
    #Get N pages from url and write it to json file
    for i in range(1, page + 1):
        response = requests.get(f'{url}?p={i}')

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.storylink')
        subtexts = soup.select('.subtext')

        news = get_custom_news(links, subtexts)

        temp = json.dumps(news)
        temp = json.loads(temp)

        json.dump(temp,
                  open(os.path.join(os.getcwd(), 'data', f'news_page{i}.json'),
                       'w'),
                  ensure_ascii=True,
                  indent=4,
                  separators=(',', ':'))


if __name__ == '__main__':

    web_scrap(url='https://news.ycombinator.com/', page=5)
