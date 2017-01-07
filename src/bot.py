import requests
import json
from random import choice
from game import Game
from pathfinder import Pathfinder

URL = "http://game.blitz.codes:8081/pathfinding/direction"
HERO_NAME = "Natural 20"

class Bot:
    pass


class RandomBot(Bot):
    def exec(self, state):
        return self.move(state)

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
        self.fries_loc = None
        self.burger_loc = None
        self.pathfinder = None

    def init(self):
        self.next_state = self.get_fries
        self.customer = choice(self.game.customers)
        return 'Stay'

    def exec(self, state):
        self.game = Game(state)
        self.pathfinder = Pathfinder(self.game)
        if self.customer is None:
            self.customer = choice(self.game.customers)
        return self.next_state()

    def get_fries(self):

        if self.fries_loc is None:
            print("Choosing new fries")
            fries_tile = self.pathfinder.get_closest_fries(get_hero_pos(
                self.game))
            _ , self.fries_loc = fries_tile
            print(self.fries_loc)

        client_fries = self.customer.french_fries
        hero_fries = get_hero_fries(self.game)

        direction = get_direction(self.game, self.fries_loc)
        hero_loc = get_hero_pos(self.game)

        print(type(self.fries_loc))
        print(hero_loc)
        if self.pathfinder.get_distance(self.fries_loc, hero_loc) <= 1:
            print("Fries acquired")
            self.fries_loc = None

        if hero_fries >= client_fries:
            self.next_state = self.get_burgers
        else:
            self.next_state = self.get_fries

        print('hero pos: ' + str(parse_pos(get_hero_pos(self.game))))
        print('getting fries: ' + str(self.fries_loc))
        return direction

    def get_burgers(self):

        if self.burger_loc is None:
            print("choosing new fries")
            self.burger_loc = choice(list(self.game.burger_locs.keys()))
            print(type(self.burger_loc))

        client_burgers = self.customer.burger
        hero_burgers = get_hero_burgers(self.game)
        hero_loc = get_hero_pos(self.game)

        direction = get_direction(self.game, self.burger_loc)

        if self.pathfinder.get_distance(self.burger_loc, hero_loc) <= 1:
            print("Burger acquired")
            self.burger_loc = None

        if hero_burgers >= client_burgers:
            self.next_state = self.goto_customer
        else:
            self.next_state = self.get_burgers

        return direction

    def goto_customer(self):

        if self.attempted_loc is None:
            self.attempted_loc_idx = 0
            self.attempted_loc = list(self.game.customers_locs)[
                self.attempted_loc_idx]
            self.attempted_loc_idx += 1

        direction = get_direction(self.game, self.attempted_loc)
        hero_loc = get_hero_pos(self.game)
        if self.pathfinder.get_distance(self.attempted_loc, hero_loc) <= 1:
            self.attempted_loc = list(self.game.customers_locs)[
                self.attempted_loc_idx]
            self.attempted_loc_idx += 1
        elif self.attempted_loc_idx >= len(self.game.customers_locs):
            self.get_fries()

        return direction




def get_direction(game, destination, service=True):
    if service:
        try:
            hero_pos = parse_pos(get_hero_pos(game))
            payload = {'map': game.state['game']['board']['tiles'],
                       'size': get_size(game.state),
                       'start': hero_pos,
                       'target': parse_pos(destination)}
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

def get_hero_fries(game):
    return get_our_hero(game).fries

def get_hero_burgers(game):
    return get_our_hero(game).burgers

def get_hero_pos(game):
    pos = get_our_hero(game).pos
    return pos['x'], pos['y']

def get_our_hero(game):
    for hero in game.heroes:
        if hero.name == "Natural 20":
            return hero


def get_size(state):
    return state['game']['board']['size']

def parse_pos(pos):
    if type(pos) is tuple:
        x, y = pos
        return "(" + str(x) + "," + str(y) + ")"
    else:
        return "(" + str(pos['x']) + "," + str(pos['y']) + ")"

def get_order_lowest_value(game):
    orders = dict()
    num_fries = 999
    num_burger = 999
    id = -1
    for customer in game.customers:
        if(customer.french_fries < num_fries) and (customer.burger < num_burger):
            num_fries = customer.french_fries
            num_burger = customer.burger
            id = customer.id

    return id, num_fries, num_burger

