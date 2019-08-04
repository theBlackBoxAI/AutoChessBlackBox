from GameBasic.action import Action

class Bot:
    def __init__(self):
        self.strategy = None

    def get_action(self, game_state):
        """
        Suggest an action based on the given game state.
        :param game_state: A GameState object
        :return:
        """
        return Action('wait')
