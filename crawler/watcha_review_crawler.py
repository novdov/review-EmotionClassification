import requests
import pandas as pd
import time
import datetime
from tqdm import tqdm


def make_movie_url(unique_id, start, count=10):
    """
    Generate url for requesting api of each movie.
    Movies are listed in here. --> https://watcha.net/evalmore
    :param unique_id: unique id of each movie
    :param start: starting index of page
    :param count: number of contents to be shown (max: 10)
    :return: url for api of each movie
    """
    if count > 10:
        print("Count can't exceed 10.")

    return "https://watcha.net/comment/list?unique_id=" + unique_id +\
           "&start_index=" + str(start) +\
           "&count=" + str(count) +\
           "&type=like"


def review_crawler():
    """
    Get the review of requested movie.
    :return: Dataframe with titles, reviews, and rating of movies.
    """
    # load csv file contains movie codes and the number of reviews of each movie
    df_tmp = pd.read_csv("../data/watcha_codes_page.csv")
    # indices of page (total reviews // 10)
    page_split = df_tmp["page_split"]
    # unique id of movies
    codes = df_tmp["code"]
    zipped = zip(codes, page_split)

    df = pd.DataFrame(columns=["title", "review", "rating"])

    # number of contents to be shown for each iteration.
    count = 10

    for code, page in list(zipped):
        try:
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
            if KeyboardInterrupt:
                print("Iteration ended at movie {}".format(code))
                break

            pass
        # print("error occured")

    return df


df = review_crawler()
date = datetime.datetime.date(datetime.datetime.now())
df.to_csv('../../MovieReview/watcha_review_{}.csv'.format(date),
          encoding='utf-8', index=False)
