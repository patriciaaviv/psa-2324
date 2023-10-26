#!/usr/bin/python3
import subprocess
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

URL = 'https://psa.in.tum.de/xwiki/bin/view/PSA%20WiSe%202023%20%202024/Public%20Keys/'


def remove_duplicates(x):
    return list(dict.fromkeys(x))


def add_team_user_numbers_col(df):
    mem_numbers = []
    member_nr_bool = df['team'].diff().eq(0)
    for x in member_nr_bool:
        if not x:
            mem_numbers.append(1)
        else:
            mem_numbers.append(2)
    df_res = df.assign(member_nr=mem_numbers)
    return df_res


def text_to_df(text):
    tokenized = text.split("|")
    temp_tokenized = tokenized
    del temp_tokenized[:6]
    new_list = [temp_tokenized[x:x + 5] for x in range(0, len(temp_tokenized) - 2, 5)]
    df = pd.DataFrame(new_list, columns=['lrz_id', 'username', 'gecos', 'team', 'pub_key'])
    df['team'] = [x.removeprefix("Team ") for x in df['team']]
    df['team'] = [int(x) for x in df['team']]
    add_team_user_numbers_col(df)
    return df


def add_users(user_df):
    # iterate over df and check if user exists
    usernames = user_df['username'].tolist()
    # usernames = remove_duplicates(usernames)
    for user in usernames:
        exists = subprocess.run(['grep', user, '/etc/passwd'], text=True)
        # if not, create user with specific uid and primary gid + secondary gid
        if exists.stdout == '':
            print()
            # adduser --disabled-password
            # uid = 1000 + 100 * <team-nr> + <member-nr-in-team>
            # gids = [1000 + (100 * int(x)) for x in user_df['team']]
            # subprocess.run([])


if __name__ == "__main__":
    # check if psa group already exists, if not create new group
    # exists = subprocess.run(['getent', 'group', 'psa2324'], capture_output=True, text=True)
    # if exists.stdout == '':
    #     subprocess.run(['sudo', 'groupadd', 'psa2324', '-g', '1099'], text=True)
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
    users = text_to_df(text=temp_text)
    # for every entry in user list create a new user if not already existing and add to group psa
    add_users(user_df=users)
