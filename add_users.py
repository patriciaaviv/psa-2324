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
    new_list = [temp_tokenized[x:x + 5] for x in range(0, len(temp_tokenized) - 2, 5)]
    df = pd.DataFrame(new_list, columns=['lrz_id', 'username', 'gecos', 'team', 'pub_key'])
    return df


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
    # format user data
    users = text_to_df(temp_text)
    # for every entry in user list create a new user if not already existing and add to group psa

