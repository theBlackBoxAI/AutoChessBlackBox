from GameBasic.action import Action


class BuyAndSellBot:
    """
    A bot only buy and sell heroes.
    """
    def __init__(self):
        self.strategy = None

    def get_actions(self, game_state):
        """
        Suggest a series of actions based on the given game state
        :param game_state:
        :return: An array of actions
        """
        actions = []

        if not game_state.is_active:
            actions.append(Action('start_game'))
            actions.append(Action('leave_game'))
            return actions

        # Identify a game is ended.
        if (game_state.exp == -1) and (game_state.level == 0) and (not game_state.store.is_open):
            actions.append(Action('leave_game'))
            return actions

        if game_state.money < 15:
            actions.append(Action('wait', 5))
            return actions

        if game_state.money > 30:
            actions.append(Action('level_up'))
            return actions

        if not game_state.store.is_open:
            actions.append(Action('toggle_store'))
            return actions

        if game_state.store.heroes[0] is None:
            actions.append(Action('wait', 5))
            return actions

        for i in range(5):
            actions.append(Action('recruit', i))
        # Allow the game to log the heroes in hand.
        actions.append(Action('log'))
        for i in range(5):
            actions.append(Action('sell_hero_in_hand', i))
        return actions


