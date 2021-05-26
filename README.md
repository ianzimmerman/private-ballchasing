# private-ballchasing
Analytics for private matches from ballchasing.com

## Setup
 1. Create a virtual environment with python 3.8+
 2. pip install -r requirements.txt
 3. rename `config.py.temp` to `config.py`
 4. add your ballchasing api token to `config.py` and make any other modifications needed.

## Usage
 1. run `python get_balls.py members` then `python get_balls.py groups`
 2. run `python player_stats.py rating` then `python player_stats.py headsup --p1=zimm --p2=cybs`


## Examples

`python player_stats.py rating --min=50 --mc=3 --pc=6`
| display_name      |   trueskill |   games_won |   games_played |   win_rate |   expected_win_rate |   wae |
|:------------------|------------:|------------:|---------------:|-----------:|--------------------:|------:|
| Cybs              |        25   |         253 |            395 |      0.641 |               0.643 |  -0.2 |
| Crispy            |        23.7 |          45 |             70 |      0.643 |               0.64  |   0.3 |
| Rune              |        23.6 |         167 |            347 |      0.481 |               0.486 |  -0.5 |
| 40 Piece McNugget |        22.8 |         223 |            372 |      0.599 |               0.589 |   1   |
| Advice Cookie     |        22.8 |          54 |            113 |      0.478 |               0.426 |   5.2 |
| zimmian           |        22.7 |         118 |            228 |      0.518 |               0.456 |   6.2 |
| yogrt             |        22.6 |          98 |            206 |      0.476 |               0.471 |   0.5 |
| Phorenzic         |        20.1 |          64 |            130 |      0.492 |               0.486 |   0.6 |

```
python player_stats.py headsup --p1=yog --p2=zim
 
yogrt (96), Yogurt (80), yogurt (59), gurt (12)
zimmian (330)
```
 
| display_name   |   trueskill |   games_won |   games_played |   win_rate |   expected_win_rate |   wae |
|:---------------|------------:|------------:|---------------:|-----------:|--------------------:|------:|
| yogrt          |        22.6 |         139 |            294 |      0.473 |               0.475 |  -0.2 |
| zimmian        |        22.7 |         169 |            330 |      0.512 |               0.459 |   5.3 |
|                |             |             |                |            |                     |       |
|                |        -0.1 |         -30 |            -36 |     -0.039 |               0.016 |  -5.5 |
 
| p1    | p2      |   games_played |   match_rate % |   win_together % |   expected_win % |   +/- |   p1_beats_p2 % |
|:------|:--------|---------------:|---------------:|-----------------:|-----------------:|------:|----------------:|
| yogrt | zimmian |            100 |             47 |             53.2 |               44 |   9.2 |            43.4 |
