from enum import Enum


class BlueStackEnv:
    def __init__(self):
        self.env_state = None
        self.game_state = None
        self.game = None


class EnvState(Enum):
    home_screen = 1
    in_game = 2
    after_game = 3
    other = 4


class GameState(Enum):
    prepare_shopping = 1
    prepare_waiting = 2
    in_battle = 3

