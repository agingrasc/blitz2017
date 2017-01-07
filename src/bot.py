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
        self.customer_loc = None
        self.game = None
        self.next_state = self.init
        self.state_before_heal = self.init
        self.fries_loc = None
        self.burger_loc = None
        self.drink_loc = None
        self.pathfinder = None

    def init(self):
        self.next_state = self.get_fries
        self.customer = choice(self.game.customers)
        return 'Stay'

    def exec(self, state):
        self.game = Game(state)
        self.pathfinder = Pathfinder(self.game)
        if self.customer is None:
            print("Selecting customer")
            _, self.customer_loc = self.pathfinder.get_closest_customer(get_hero_pos(self.game))
            self.customer = get_customer_by_pos(self.customer_loc, self.game)

        if get_hero_life(self.game) < 25:
            if self.next_state != self.heal:
                self.state_before_heal = self.next_state
                print(str(self.state_before_heal))
            self.next_state = self.heal

        return self.next_state()

    def get_fries(self):

        if self.fries_loc is None:
            print("Choosing new fries")
            fries_tile, self.fries_loc = self.pathfinder.get_closest_fries(get_hero_pos(
                self.game))

        client_fries = self.customer.french_fries
        hero_fries = get_hero_fries(self.game)

        direction = get_direction(self.game, self.fries_loc)
        hero_loc = get_hero_pos(self.game)

        if self.pathfinder.get_distance(self.fries_loc, hero_loc) <= 1:
            print("Fries acquired")
            self.fries_loc = None

        if hero_fries >= client_fries:
            self.next_state = self.get_burgers
        else:
            self.next_state = self.get_fries

        return direction

    def get_burgers(self):

        if self.burger_loc is None:
            print("Choosing new burger")
            burger_tile, self.burger_loc = \
                self.pathfinder.get_closest_burger(get_hero_pos(self.game))

        client_burgers = self.customer.burger
        hero_burgers = get_hero_burgers(self.game)
        hero_loc = get_hero_pos(self.game)

        direction = get_direction(self.game, self.burger_loc)

        if self.pathfinder.get_distance(self.burger_loc, hero_loc) <= 1:
            print("Burger acquired")
            self.burger_loc = None

        if hero_burgers >= client_burgers:
            if get_hero_fries(self.game) >= self.customer.french_fries:
                self.next_state = self.goto_customer
            else:
                self.next_state = self.get_fries
        else:
            self.next_state = self.get_burgers

        return direction

    def heal(self):
        hero_loc = get_hero_pos(self.game)
        if self.drink_loc is None:
            drink_tile, self.drink_loc = self.pathfinder.get_closest_drink(hero_loc)
        direction = get_direction(self.game, self.drink_loc)

        print("Healing time! drink pos: {}".format(self.drink_loc))
        if self.pathfinder.get_distance(self.drink_loc, hero_loc) <= 1:
            print("drink acquired")
            self.next_state = self.state_before_heal

        return direction


    def goto_customer(self):
        direction = get_direction(self.game, self.customer_loc)
        hero_loc = get_hero_pos(self.game)
        if self.pathfinder.get_distance(self.customer_loc, hero_loc) <= 1:
            self.customer = None
            self.customer_loc = None
            self.next_state = self.get_fries

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

def get_hero_life(game):
    return get_our_hero(game).life


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

def get_customer_by_pos(pos, game):
    state = game.state
    tiles = state['game']['board']['tiles']
    size = state['game']['board']['size']
    vector = [tiles[i:i+2] for i in range(0, len(tiles), 2)]
    matrix = [vector[i:i+size] for i in range(0, len(vector), size)]
    row, col = pos
    raw_tile = matrix[row][col]
    customer_id = int(raw_tile[1])

    for customer in game.customers:
        if customer.id == customer_id:
            return customer

