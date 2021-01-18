#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import argparse
import re
from constants import BASE_URL

PATH = 'years'
REGEX = r'\/[A-Z]\/(.*)\.htm'


def parse_args():
    parser = argparse.ArgumentParser(description='For a given NFL season return all player slugs')
    parser.add_argument('-s', '--season', nargs='+', default=[2020])
    return parser.parse_args()


def build_url(season: int) -> str:
    return f'{BASE_URL}/{PATH}/{str(season)}/fantasy.htm'


def get_fantasy_leaders_page(url: str):
    r = requests.get(url)
    print(f'{url} returned {r.status_code}')
    if r.status_code == 200:
        return r
    else:
        return None


def parse_response(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    parsed_table = soup.find_all('table')[0]
    # first 2 rows are headers
    for row in parsed_table.find_all('tr')[2:]:
        data_row = row.find('td', attrs={'data-stat': 'player'})
        try:
            player_path = data_row.a.get('href')
            yield parse_slugs_from_player_path(player_path)
        except AttributeError:
            yield None


def parse_slugs_from_player_path(path: str) -> str:
    match = re.search(REGEX, path)
    if match:
        return match.group(1)


def main():
    args = parse_args()
    seasons = args.season
    for season in seasons:
        url = build_url(season)
        response = get_fantasy_leaders_page(url)
        if response:
            with open(f'players_{season}.csv', 'w') as f:
                f.write('player_slug,season\n')
                for row in parse_response(response):
                    if row:
                        f.write(f'{row},{season}\n')
                f.close()


if __name__ == '__main__':
    main()
