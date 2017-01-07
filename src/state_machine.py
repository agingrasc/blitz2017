class MoveState:
    def __init__(self):
        self.current_state = StayState

    def new_state(self, new_state):
        self.current_state = new_state

    def get_dir(self):
        pass

    def move(self):
        dir = self.current_state.get_dir()
        return dir


class StayState(MoveState):
    def get_dir(self):
        # envoie la direction
        return 'STAY'


class NorthState(MoveState):
    def get_dir(self):
        # envoie la direction
        return 'NORTH'


class SouthState(MoveState):
    def get_dir(self):
        # envoie la direction
        return 'SOUTH'


class EastState(MoveState):
    def get_dir(self):
        # envoie la direction
        return 'EAST'


class WestState(MoveState):
    def get_dir(self):
        # envoie la direction
        return 'WEST'
