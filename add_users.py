#!/usr/bin/python3
import subprocess
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

URL = 'https://psa.in.tum.de/xwiki/bin/view/PSA%20WiSe%202023%20%202024/Public%20Keys/'


def check_group_exists(name):
    try:
        subprocess.run(['getent', 'group', name], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


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
    df = pd.DataFrame(new_list, columns=['username', 'gecos', 'team', 'pub_key', 'lrz_id'])
    df['team'] = [x.removeprefix("Team ") for x in df['team']]
    df['team'] = [int(x) for x in df['team']]
    df = add_team_user_numbers_col(df)
    return df


def add_users(user_df):
    temp_df = user_df[['username', 'team', 'member_nr']]
    # iterate over df and check if user exists
    for index, row in temp_df.iterrows():
        try:
            subprocess.run(['id', row['username']], check=True)
            print(f"User '{username}' already exists.")
            return
        except subprocess.CalledProcessError:
            pass
        # calculate uid
        uid = 1000 + 100 * int(row['team']) + int(row['member_nr'])
        # calculate secondary gid, primary gid = uid
        gid = 1000 + 100 * int(row['team'])
        subprocess.run(['sudo', 'groupadd', '-g', str(gid), f'psa2324team{row["team"]}'])
        subprocess.run(
            ['sudo', 'useradd', '-u', str(uid), '-g', str(uid), '-G', str(gid), row['username'], '--disabled-password'],
            check=True)


if __name__ == "__main__":
    # check if psa group already exists, if not create new group
    if not check_group_exists('psa2324'):
        subprocess.run(['sudo', 'groupadd', 'psa2324', '-g', '1099'], text=True)

    username = input("Input email: ")
    password = input("Input password: ")

    # parse user list from website
    s = requests.session()
    response = s.post(URL, auth=(username, password))
    index_page = s.get(URL)
    soup = bs(index_page.text, 'html.parser')
    results = soup.find(id="xwikicontent")
    temp_text = results.get_text("|")
    # TODO temporary bug fix weil falscher input in der liste
    temp_text = temp_text.replace(
        '|ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFbetiUdtIMVZ+x0VR0PCdL+IOhcVu5CW++xbEIJZTGd domi-fresh@domifresh-hplaptop15dw1xxx|',
        '')

    # format user data
    users = text_to_df(text=temp_text)
    # for every entry in user list create a new user if not already existing and add to group psa
    add_users(user_df=users)
