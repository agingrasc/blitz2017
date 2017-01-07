from game import Game, TAVERN, TavernTile
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
        closest_object = None
        closest_position = None
        for position in objects_positions:
            distance = self.get_distance(reference_pos, position)
            if distance < minimum_distance:
                minimum_distance = distance
                closest_object = self.game.board.tiles[position[0]][position[1]]
                closest_position = position
                if closest_object == TAVERN:
                    closest_object = TavernTile()
                closest_object.pos = position

        return closest_object, closest_position

    def get_distance(self, pos1, pos2):
        return math.fabs(pos2[0] - pos1[0]) + math.fabs(pos2[1] - pos1[1])

