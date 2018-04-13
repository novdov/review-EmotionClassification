import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
from tqdm import tqdm


def review_crawler():
    nv_reviews = pd.DataFrame(columns=["title", "review"])

    for i in tqdm(range(1, 500+1)):
        url = "https://movie.naver.com/movie/point/af/list.nhn?&page={}".format(i)
        response = requests.get(url)
        dom = BeautifulSoup(response.content, "html.parser")
        reviews_pre = dom.find_all("td", "title")

        for idx, rvw in enumerate(reviews_pre):
            title = rvw.a.text
            review = rvw.text.split('\n')[2].split(' \r')[0]
            nv_reviews.loc[len(nv_reviews)] = {
                "title": title+"\t",
                "review": review
            }
        time.sleep(0.3)

    return nv_reviews


df = review_crawler()
date = datetime.datetime.date(datetime.datetime.now())
df.to_csv('../../MovieReview/movie_reviews_{}'.format(date),
          index=False, encoding='utf-8')