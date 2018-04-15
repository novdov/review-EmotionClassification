import json
import pandas as pd

with open('category.json') as f:
    json_data = json.loads(f.read())

total_cards = json_data['cards']
code_df = pd.DataFrame(columns=["code", "title", "title_url"])

for card in total_cards:
    code = card['items'][0]['item']['code']
    title = card['items'][0]['item']['title']
    title_url = card['items'][0]['item']['title_url']

    code_df.loc[len(code_df)] = {
        "code": code,
        "title": title,
        "title_url": title_url,
    }
