#!/usr/bin/python3
import subprocess
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

URL = 'https://psa.in.tum.de/xwiki/bin/view/PSA%20WiSe%202023%20%202024/Public%20Keys/'


def text_to_df(text):
    tokenized = text.split("|")
    temp_tokenized = tokenized
    del temp_tokenized[:6]
    index = 0
    count = 0
    for x in temp_tokenized:
        if count == 5:
            count = 0
            temp_tokenized.insert(index, "\n")
            index += 1
            continue
        count += 1
        index += 1
    print(temp_tokenized)
    df = pd.DataFrame()
    print(df)


if __name__ == "__main__":
    # check if psa group already exists, if not create new group
    # exists = subprocess.run(['getent', 'group', 'psa'], capture_output=True, text=True)
    # if exists.stdout == '':
    #     subprocess.run(['sudo', 'groupadd', 'psa'], text=True)
    username = "patricia.horvath@tum.de"
    password = input("Input password: ")

    # parse user list from website and save to csv

    s = requests.session()
    response = s.post(URL, auth=(username, password))
    index_page = s.get(URL)
    soup = bs(index_page.text, 'html.parser')
    results = soup.find(id="xwikicontent")
    temp_text = results.get_text("|")
    text_to_df(temp_text)
# for every entry in user list create a new user if not already existing and add to group psa
