from random import choice
from .game import Game
from .state_machine import MoveState

class Bot:
    pass


class RandomBot(Bot):
    def move(self, state):
        game = Game(state)
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return choice(dirs)

class SimplePathedBot(Bot):
    def move(self, state):
        game = Game(state)
        return ['Stay']

class SimpleMoveBot(Bot):
    def __init__(self):
        self.dirState = MoveState

    def move(self, state):
        game = Game(state)
        return list(self.dirState.get_dir())
