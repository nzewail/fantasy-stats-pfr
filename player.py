#!/usr/bin/python3

import re

REGEX = r'\/[A-Z]\/(.*)\.htm'


class Player():
    def __init__(self, path, name, position):
        self.slug = self.parse_slugs_from_player_path(path)
        self.name = name
        self.position = position

    def to_string(self) -> str:
        return f'{self.slug},{self.name},{self.position}'

    def parse_slugs_from_player_path(self, path: str) -> str:
        match = re.search(REGEX, path)
        if match:
            return match.group(1)
