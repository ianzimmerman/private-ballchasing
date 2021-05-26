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

`python player_stats.py rating --pc=6 --mc=4 --min=25`
| display_name   |   trueskill |   games_won |   games_played |   win_rate |   expected_win_rate |   wae |
|:---------------|------------:|------------:|---------------:|-----------:|--------------------:|------:|
| drewt          |        24.7 |          32 |             49 |      0.653 |               0.583 |   7   |
| Pengy          |        24.3 |          64 |            112 |      0.571 |               0.569 |   0.3 |
| NoaBoa         |        21.9 |         111 |            207 |      0.536 |               0.532 |   0.5 |
| Shagoliath     |        21.6 |          47 |             92 |      0.511 |               0.499 |   1.1 |
| Liam           |        20.9 |          57 |             95 |      0.6   |               0.607 |  -0.7 |
| corn pop       |        17.8 |          36 |             76 |      0.474 |               0.463 |   1.1 |
| Jyxz           |        17.7 |          75 |            160 |      0.469 |               0.469 |  -0   |
| mikecm20       |        16.7 |          63 |            144 |      0.438 |               0.487 |  -5   |
| Azy            |        16.4 |          38 |             81 |      0.469 |               0.532 |  -6.3 |
| IPwnedAIDS     |        16.1 |          34 |             63 |      0.54  |               0.486 |   5.4 |
| Volts          |        13   |          33 |             80 |      0.412 |               0.41  |   0.2 |
| Lan            |        12.5 |          26 |             65 |      0.4   |               0.478 |  -7.8 |
| keizzy44       |         9.1 |          13 |             39 |      0.333 |               0.4   |  -6.6 |

`python player_stats.py headsup --pc=6 --mc=4 --p1=drewt`
```
drewt (108)
TrueSkill: 24.7
```
 
| p1    | p2         |   trueskill_delta |   games_played |   match_rate % |   win_together % |   expected_win % |   +/- |   p1_beats_p2 % |
|:------|:-----------|------------------:|---------------:|---------------:|-----------------:|-----------------:|------:|----------------:|
| drewt | NoaBoa     |               2.8 |             48 |           39.6 |             78.9 |             70.8 |   8.1 |            55.2 |
| drewt | Pengy      |               0.4 |             32 |           50   |             81.2 |             70.4 |  10.8 |            62.5 |
| drewt | mikecm20   |               7.9 |             29 |           24.1 |             28.6 |             49.8 | -21.2 |            68.2 |
| drewt | Jyxz       |               7   |             28 |           39.3 |             45.5 |             56.8 | -11.3 |            76.5 |
| drewt | Azy        |               8.3 |             24 |           62.5 |             73.3 |             63.7 |   9.6 |            55.6 |
| drewt | IPwnedAIDS |               8.5 |             16 |           62.5 |             70   |             50.6 |  19.4 |           100   |
| drewt | corn pop   |               6.9 |             13 |           38.5 |             60   |             72.4 | -12.4 |            75   |
| drewt | Shagoliath |               3   |             13 |           38.5 |             60   |             65.1 |  -5.1 |            87.5 |
| drewt | Lan        |              12.2 |             11 |           27.3 |             33.3 |             28.4 |   4.9 |            62.5 |


`python player_stats.py headsup --pc=6 --mc=4 --p1=drewt --p2=pengy`
 
| display_name   |   trueskill |   games_won |   games_played |   win_rate |   expected_win_rate |   wae |
|:---------------|------------:|------------:|---------------:|-----------:|--------------------:|------:|
| drewt          |        24.7 |          32 |             49 |      0.653 |               0.583 |   7   |
| Pengy          |        24.3 |          64 |            112 |      0.571 |               0.569 |   0.3 |
|                |             |             |                |            |                     |       |
|                |         0.4 |         -32 |            -63 |      0.082 |               0.014 |   6.7 |
 
| p1    | p2    |   trueskill_delta |   games_played |   match_rate % |   win_together % |   expected_win % |   +/- |   p1_beats_p2 % |
|:------|:------|------------------:|---------------:|---------------:|-----------------:|-----------------:|------:|----------------:|
| drewt | Pengy |               0.4 |             32 |             50 |             81.2 |             70.4 |  10.8 |            62.5 |


`python player_stats.py team --pc=6`

| team_name                    |   games_played |   win_rate |   exp_win_rate |   delta |
|:-----------------------------|---------------:|-----------:|---------------:|--------:|
| Jyxz, mikecm20, NoaBoa       |             16 |       43.8 |           41.7 |     2.1 |
| Pengy, Jyxz, NoaBoa          |             12 |       75   |           44.4 |    30.6 |
| Jyxz, Azy, NoaBoa            |             12 |       16.7 |           52.2 |   -35.5 |
| Pengy, mikecm20, NoaBoa      |             12 |       66.7 |           69.4 |    -2.7 |
| Jyxz, NoaBoa, corn pop       |             10 |       40   |           38.1 |     1.9 |
| Pengy, mikecm20, Azy         |             10 |       40   |           49.8 |    -9.8 |
| Volts, Jyxz, NoaBoa          |              9 |       22.2 |           38.1 |   -15.9 |
| mikecm20, NoaBoa, Liam       |              9 |       55.6 |           77.3 |   -21.7 |
| Jyxz, Shagoliath, NoaBoa     |              8 |       62.5 |           53.5 |     9   |
| drewt, Jyxz, NoaBoa          |              8 |       62.5 |           50.7 |    11.8 |
| Jyxz, NoaBoa, Liam           |              8 |       62.5 |           60.4 |     2.1 |
| Shagoliath, NoaBoa, corn pop |              8 |       50   |           58.9 |    -8.9 |
| Pengy, drewt, NoaBoa         |              8 |       87.5 |           82.8 |     4.7 |
| mikecm20, NoaBoa, corn pop   |              8 |       62.5 |           79.9 |   -17.4 |
| Pengy, Jyxz, Liam            |              8 |       87.5 |           63.4 |    24.1 |
| Volts, Jyxz, mikecm20        |              8 |       37.5 |           51.3 |   -13.8 |
