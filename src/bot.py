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
    def __init__(self):
        self.customer = None
        self.game = None
        self.next_state = self.init
        self.attempted_loc = None
        self.attempted_loc_idx = 0

    def init(self):
        self.next_state = self.get_fries
        self.customer = choice(self.game.customers)
        return 'Stay'

    def exec(self, state):
        self.game = Game(state)
        if self.customer is None:
            self.customer = choice(self.game.customers)
        return self.next_state()

    def get_fries(self):

        client_fries = self.customer.french_fries
        hero_fries = get_hero_fries(self.game)
        fries_loc = choice(list(self.game.fries_locs.keys()))

        if hero_fries >= client_fries:
            self.next_state = self.get_burgers
        else:
            self.next_state = self.get_fries

        print('getting fries: ' + str(fries_loc))
        return get_direction(self.game, fries_loc)

    def get_burgers(self):

        client_burgers = self.customer.burger
        hero_burgers = get_hero_burgers(self.game)
        burger_loc = choice(self.game.burger_locs.values())

        if hero_burgers >= client_burgers:
            self.next_state = self.goto_customer
        else:
            self.next_state = self.get_burgers

        return get_direction(self.game, burger_loc)

    def goto_customer(self):

        if self.attempted_loc is None:
            self.attempted_loc_idx = 0
            self.attempted_loc = list(self.game.customers_locs.values())[
                self.attempted_loc_idx]
            self.attempted_loc_idx += 1

        direction = get_direction(self.game, self.attempted_loc)
        if direction == 'Stay' or 'STAY' and self.attempted_loc_idx < len(
                self.game.customers_loc):
            self.attempted_loc = list(self.game.customers_locs.values())[
                self.attempted_loc_idx]
            self.attempted_loc_idx += 1
        elif self.attempted_loc_idx >= len(self.game.customers_locs):
            self.get_fries()

        return direction




def get_direction(game, destination, service=True):
    if service:
        try:
            print(destination)
            hero_pos = get_hero_pos(game)
            payload = {'map': game.state['game']['board']['tiles'],
                       'size': get_size(game.state),
                       'start': parse_pos(hero_pos),
                       'end': destination}
            r = requests.get(URL, params=payload)

            if r.status_code == 200:
                print("direction: " + r.json()['direction'])
                return r.json()['direction']
            else:
                print("Error HTTP %d\n%s\n" % (r.status_code, r.text))
                return 'Stay'

        except requests.exceptions.RequestException as e:
            print(e)
    else:
        #TODO: integration pathfinder custom
        pass

def get_hero_fries(game):
    return get_our_hero(game).fries

def get_hero_burgers(game):
    return get_our_hero(game).burgers

def get_hero_pos(game):
    return get_our_hero(game).pos

def get_our_hero(game):
    for hero in game.heroes:
        if hero.name == "Natural 20":
            return hero


def get_size(state):
    return state['game']['board']['size']

def parse_pos(pos):
    return "(" + str(pos['x']) + "," + str(pos['y']) + ")"
