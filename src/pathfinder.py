from game import Game
import math


class Pathfinder:

    def __init__(self, game):
        assert isinstance(game, Game)
        self.game = game

    def get_closest_fries(self, reference_pos):
        return self.get_closest(reference_pos, self.game.fries_locs)

    def get_closest_burger(self, reference_pos):
        return self.get_closest(reference_pos, self.game.burger_locs)

    def get_closest(self, reference_pos, objects):
        assert len(reference_pos) == 2
        assert isinstance(objects, dict)

        minimum_distance = math.inf
        closest = None
        for object_position in objects.keys():
            distance = self.get_distance(reference_pos, object_position)
            if distance < minimum_distance:
                minimum_distance = distance
                closest = objects[object_position]
        return closest, minimum_distance

    def get_distance(self, pos1, pos2):
        return math.fabs(pos2[0] - pos1[0]) + math.fabs(pos2[1] - pos1[1])

