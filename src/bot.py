import requests
import json
from random import choice
from game import Game
from pathfinder import Pathfinder, get_our_hero_id
from game import TAVERN, AIR, WALL, SPIKE, FriesTile, BurgerTile

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
        self.min_heal = 30
        self.num_death = 0
        self.hero_health = 100

    def init(self):
        self.next_state = self.get_fries
        self.state_before_heal = self.get_fries
        self.customer = None
        self.customer_loc = None
        self.fries_loc = None
        self.drink_loc = None
        self.pathfinder = None

        return 'Stay'

    def exec(self, state):
        self.game = Game(state)
        self.pathfinder = Pathfinder(self.game)

        # Choix d'un nouveau client
        if self.customer is None:
            print("Selecting customer")
            _, self.customer_loc = self.pathfinder.get_closest_customer(get_hero_pos(self.game))
            self.customer = get_customer_by_pos(self.customer_loc, self.game)

        if (self.num_death >= 5) and (self.min_heal <= 45):
            self.min_heal += 5
            self.num_death = 0

        destination = self.next_state()

        self.hero_health = get_hero_life(self.game)

        # Reset de mort et check de healing
        if self.hero_health == 0:
            self.num_death += 1
            self.next_state = self.init
        elif (get_our_hero(self.game).calories > 30) and (self.hero_health < self.min_heal):
            if self.next_state != self.heal:
                self.state_before_heal = self.next_state
            self.next_state = self.heal

        return destination

    def get_fries(self):

        if self.fries_loc is None:
            print("Choosing new fries")
            fries_tile, self.fries_loc = self.pathfinder.get_closest_fries(get_hero_pos(
                self.game))

        client_fries = self.customer.french_fries
        hero_fries = get_hero_fries(self.game)

        direction = get_direction(self.game, self.fries_loc)

        # Opportunity move
        opportunity_direction = self.check_for_opportunity(direction)
        if opportunity_direction:
            return opportunity_direction

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

        # Opportuniy move
        opportunity_direction = self.check_for_opportunity(direction)
        if opportunity_direction:
            return opportunity_direction

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
        # Check si on a les calories pour guerir
        if (get_our_hero(self.game).calories <= 30):
            self.next_state = self.state_before_heal
            return 'STAY'

        hero_loc = get_hero_pos(self.game)
        if self.drink_loc is None:
            drink_tile, self.drink_loc = self.pathfinder.get_closest_drink(hero_loc)
        direction = get_direction(self.game, self.drink_loc)

        print("Healing time! drink pos: {}".format(self.drink_loc))
        if (self.pathfinder.get_distance(self.drink_loc, hero_loc) <= 1) \
                or (self.hero_health == 100):
            print("drink acquired")
            self.drink_loc = None
            self.min_heal -= (100 - self.hero_health)
            if self.min_heal < 30:
                self.min_heal = 30
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

    def check_for_opportunity(self, direction):
        cardinal_directions = ['WEST', 'EAST', 'NORTH', 'SOUTH']
        hero_loc = get_hero_pos(self.game)

        for dir in cardinal_directions:
            destination = self.game.board.to(hero_loc, direction)
            row, col = destination
            tile = self.game.board.tiles[row][col]

            print("Direction choisi: {} -- opportunite: {}".format(type(direction), type(dir)))
            if direction != dir and (isinstance(tile, FriesTile) or isinstance(tile, BurgerTile)):
                print(type(tile.hero_id))
                print(type(get_our_hero_id(self.game)))
                if tile.hero_id != get_our_hero_id(self.game):
                    return dir



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
    num_fries = 999
    num_burger = 999
    id = -1
    for customer in game.customers:
        if(customer.french_fries <= num_fries) and (customer.burger <= num_burger):
            num_fries = customer.french_fries
            num_burger = customer.burger
            id = customer.id
    return id, num_fries, num_burger

def get_order_highest_value(game):
    num_fries = 0
    num_burgers = 0
    id = -1
    for customer in game.customers:
        if(customer.french_fries >= num_fries) and (customer.burger >= num_burgers):
            num_fries = customer.french_fries
            num_burgers = customer.burger
            id = customer.id
    return id, num_fries, num_burgers

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

def get_hero_with_most_food(game):
    num_fries = 0
    num_burgers = 0
    id = -1
    our_id = get_our_hero_id(game)
    for hero in game.heroes:
        if (hero.id != our_id) and (hero.fries >= num_fries) and (hero.burger >= num_burgers):
            num_fries = hero.french_fries
            num_burgers = hero.burger
            id = hero.id
    return id, num_fries, num_burgers
