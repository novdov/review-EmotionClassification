import json
import pandas as pd
import requests

# def make_url_evalmore(page, per):
#     return "https://watcha.net/evalmore/category.json?" +\
#            "page={}&per={}&category_idx=19".format(page, per)

# url = make_url_evalmore(1, 601)
#
# response = requests.get(url)
# json_data = response.json()

with open('category.json') as f:
    json_data = json.loads(f.read())

total_cards = json_data['cards']
code_df = pd.DataFrame(columns=["code", "title"])

for card in total_cards:
    code = card['items'][0]['item']['code']
    title = card['items'][0]['item']['title']

    code_df.loc[len(code_df)] = {
        "code": code,
        "title": title
    }
