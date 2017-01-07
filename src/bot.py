import requests
import json
from random import choice
from game import Game

URL = "http://game.blitz.codes:8081/pathfinding/direction"
HERO_NAME = "Natural 20"

class Bot:
    pass


class RandomBot(Bot):
    def move(self, state):
        game = Game(state)
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return choice(dirs)


class SimpleBot(Bot):
    def move(self, state):
        game = Game(state)
        return get_direction(game, None)


def get_direction(game, destination, service=True):
    if service:
        try:
            hero_pos = get_hero_pos(game)
            dest = list(game.fries_locs.keys())[0]
            payload = {'map': game.state['game']['board']['tiles'],
                       'size': get_size(game.state),
                       'start': parse_pos(hero_pos),
                       'end': dest}
            r = requests.get(URL, params=payload)

            if r.status_code == 200:
                return r.json()['direction']
            else:
                print("Error HTTP %d\n%s\n" % (r.status_code, r.text))
                return 'Stay'

        except requests.exceptions.RequestException as e:
            print(e)
    else:
        #TODO: integration pathfinder custom
        pass


def get_hero_pos(game):
    for hero in game.heroes:
        if hero.name == "Natural 20":
            return hero.pos

def get_size(state):
    return state['game']['board']['size']

def parse_pos(pos):
    return "(" + str(pos['x']) + "," + str(pos['y']) + ")"
