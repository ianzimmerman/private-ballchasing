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
