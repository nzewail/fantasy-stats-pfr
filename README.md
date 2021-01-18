# Fantasy Stats PFR

Some scripts that I have written to scrape fantasy stats from [PFR](https://www.pro-football-reference.com/)

## Get Started

```
pip3 install -r requirements.txt
```

## Scripts

### `player_slugs.py`

This script returns all the player slugs from PFR for a given season. Script takes in multiple season arguments to pull slugs from different seasons. PFR uses a weird slug for their player pages. This script takes the fantasy leaderboard [page](https://www.pro-football-reference.com/years/2020/fantasy.htm) and parses the href in each row to get the slug for a given player and outputs to a csv. The methodology uses code from [here](https://stmorse.github.io/journal/pfr-scrape-python.html)

```
python3 player_slugs.py --help
usage: player_slugs.py [-h] [-s SEASON [SEASON ...]]

For a given NFL season return all player slugs

optional arguments:
  -h, --help            show this help message and exit
  -s SEASON [SEASON ...], --season SEASON [SEASON ...]
```

Output will be in a file `players_{season}.csv` that will look like

```
head players_2020.csv 
player_slug,season
HenrDe00,2020
KamaAl00,2020
CookDa01,2020
AdamDa01,2020
KelcTr00,2020
HillTy00,2020
AlleJo02,2020
RodgAa00,2020
MurrKy00,2020

```

### `fantasy_stats.py`

```
python3 fantasy_stats.py  --help
usage: fantasy_stats.py [-h] [-f FILE] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  csv file of player_slug, season
  -o OUTPUT, --output OUTPUT
```

Input file expected for `fantasy_stats.py` is equivalent to the output file from above. Running for an input file that covers all the players in a given season will take some time. 

Output will default to `stats.json` with the following sample row:
```json
{
  "game_num": 1,
  "date": "2020-09-14",
  "tm": "TEN",
  "is_home": false,
  "opp": "DEN",
  "result": "W 16-14",
  "pos": "RB",
  "fdpt": 14.6,
  "is_win": true,
  "margin": 2,
  "player_slug": "HenrDe00",
  "season": "2020"
}
```