#!/usr/bin/python3

from constants import BASE_URL
import argparse
import csv
import pandas as pd
import re

PATH = 'players'
REGEX = r'(\d+)\-(\d+)'
COLS = {'unnamed: 4_level_2': 'is_home', 'g#': 'game_num', 'FantPt': 'fantasy_pts'}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='csv file of player_slug, season', type=str)
    parser.add_argument('-o', '--output', default='stats.json')
    return parser.parse_args()


def build_url(player_slug: str, season: int) -> str:
    return f'{BASE_URL}/{PATH}/{player_slug[0]}/{player_slug}/fantasy/{season}'


def calculate_margin(margin: str) -> int:
    match = re.search(REGEX, margin)
    if match:
        score_1 = int(match.group(1))
        score_2 = int(match.group(2))
        return score_1 - score_2


def is_home(is_home_col: str) -> bool:
    return is_home_col != '@'


def is_win(result_col: str) -> bool:
    return result_col[0] == 'W'


def get_fantasy_stats(player_slug: str, season: int) -> dict:
    url = build_url(player_slug, season)
    df = pd.read_html(url)[0]
    return df


def format_fantasy_stats_df(df, player_slug, season):
    df.columns = [col.lower() for col in df.columns.get_level_values(-1)]
    df = df.rename(columns=COLS)
    df = df.iloc[:-1]
    df['is_home'] = [is_home(r) for r in df['is_home']]
    df['is_win'] = [is_win(result) for result in df['result']]
    df['margin'] = [calculate_margin(margin) for margin in df['result']]
    df = df.iloc[:, [1, 2, 3, 4, 5, 6, 7, -3, -2, -1]]
    df['player_slug'] = player_slug
    df['season'] = season
    return df


def main():
    args = parse_args()
    with open(args.file, 'r') as f, open(args.output, 'w') as w:
        reader = csv.DictReader(f)
        for row in reader:
            player_slug = row['player_slug']
            season = row['season']
            print(f"getting stats for {player_slug} in {season}")
            df = get_fantasy_stats(player_slug, season)
            if len(df) > 0:
                stats = format_fantasy_stats_df(df, player_slug, season)
                w.write(stats.to_json(orient='records', lines=True))
        f.close()
        w.close()


if __name__ == '__main__':
    main()
