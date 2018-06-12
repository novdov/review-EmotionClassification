import requests
from bs4 import BeautifulSoup
import pandas as pd

# TODO: staticmethod 제거
class GetDaumNews:

    def __init__(self):
        pass

    @staticmethod
    def get_url(page, date):
        return 'http://media.daum.net/breakingnews/politics?page={}&regDate={}'.format(page, date)

    @staticmethod
    def get_ind_news(urls):
        news_urls = []
        for url in urls:
            response = requests.get(url)
            contents = BeautifulSoup(response.content, "html.parser")
            news_list = contents.find_all('div', 'cont_thumb')
            news_list = news_list[:-2]
            for news in news_list:
                news_urls.append(news.a['href'])
        return news_urls

    @staticmethod
    def get_news_text(urls):
        df = pd.DataFrame(columns=['sentence'])
        for url in urls:
            response = requests.get(url)
            contents = BeautifulSoup(response.content, "html.parser")

            news_texts = contents.find_all('p')[:-1]
            if len(news_texts) > 3:  # 포토 뉴스 제외
                for text in news_texts:
                    if text.text == '':
                        continue
                    df.loc[len(df)] = {
                        'sentence': text.text
                    }
        return df
