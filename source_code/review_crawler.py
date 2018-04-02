import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def review_crawler():

    nv_reviews = pd.DataFrame(columns=["title", "review"])

    for i in tqdm_notebook(range(1, 1000+1)):
        url = "https://movie.naver.com/movie/point/af/list.nhn?&page={}".format(i)
        response = requests.get(url)
        dom = BeautifulSoup(response.content, "html.parser")
        dom.find_all("a", "movie")
        reviews_pre = dom.find_all("td", "title")

        for idx, rvw in enumerate(reviews_pre):
            title = rvw.a.text
            review = rvw.text.split('\n')[2].split(' \r')[0]
            nv_reviews.loc[len(nv_reviews)] = {
                "title": title,
                "review": review
            }

        time.sleep(0.5)
    return nv_reviews
