class HeroState:
    def __init__(self):
        self.current_state = ServeState

    def new_state(self, new_state):
        self.current_state = new_state

    def act(self):
        raise NotImplementedError

class ServeState(HeroState):


class AttackState(HeroState):

class FleeState(HeroState):

class HealState(HeroState):