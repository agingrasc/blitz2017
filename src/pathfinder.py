from game import Game
import math


class Pathfinder:

    def __init__(self, game):
        assert isinstance(game, Game)
        self.game = game

    def get_closest_fries(self, reference_pos):
        return self.get_closest(reference_pos, self.game.fries_locs.keys())

    def get_closest_burger(self, reference_pos):
        return self.get_closest(reference_pos, self.game.burger_locs.keys())

    def get_closest_customer(self, reference_pos):
        return self.get_closest(reference_pos, self.game.customers_locs)

    def get_closest_drink(self, reference_pos):
        return self.get_closest(reference_pos, self.game.taverns_locs)

    def get_closest(self, reference_pos, objects_positions):
        assert len(reference_pos) == 2

        minimum_distance = math.inf
        closest = None
        for position in objects_positions:
            distance = self.get_distance(reference_pos, position)
            if distance < minimum_distance:
                minimum_distance = distance
                closest = self.game.board.tiles[position[0]][position[1]]
        return closest, minimum_distance

    def get_distance(self, pos1, pos2):
        return math.fabs(pos2[0] - pos1[0]) + math.fabs(pos2[1] - pos1[1])

