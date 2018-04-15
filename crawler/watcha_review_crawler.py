import requests
import pandas as pd
import time
import datetime
from tqdm import tqdm


def make_movie_url(unique_id, start, count):
    return "https://watcha.net/comment/list?unique_id=" + unique_id +\
           "&start_index=" + str(start) +\
           "&count=" + str(count) +\
           "&type=like"


def review_crawler():
    df_tmp = pd.read_csv("../data/watcha_codes_page.csv")
    page_split = df_tmp["page_split"]
    codes = df_tmp["code"]
    zipped = zip(codes, page_split)

    df = pd.DataFrame(columns=["title", "review", "rating"])

    count = 10
    try:
        for code, page in zipped:
            for i in tqdm(range(page)):
                url = make_movie_url(code, i, count)
                response = requests.get(url)
                data = response.json()

                contents = data["data"]

                for content in contents:
                    title = content["movie_title"]
                    review = content["text"]
                    rating = content["rating"]

                    df.loc[len(df)] = {
                        "title": title,
                        "review": review,
                        "rating": rating,
                    }
                time.sleep(0.2)

    except:
        pass
        # print("error occured")

    return df


df = review_crawler()
date = datetime.datetime.date(datetime.datetime.now())
df.to_csv('../../MovieReview/watcha_review_{}.csv'.format(date),
          encoding='utf-8', index=False)
