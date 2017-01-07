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

def get_client_pos(game, customer):
    client_index = get_client_string_index(game, customer)
    [row, col] = client_index_to_pose(game, client_index)
    return [row, col]

def get_client_string_index(game, customer):
    map = game.state['board']['tiles']
    start_index = 0
    for i in range(0, 3):
        client_index = map.index('C', start_index)
        if map[client_index+1] == customer.id:
            return client_index
        else:
            start_index = client_index

def client_index_to_pose(game, client_index):
    [row, col] = get_size(game.state)
    cust_row = client_index // col
    cust_col = client_index - (col*cust_row)
    return [cust_row, cust_col]