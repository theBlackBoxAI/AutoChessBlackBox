class Action:
    """
    A class to represent all user oriented actions.
    """
    def __init__(self, action_name, action_param=None):
        """
        :param action_name: The current supported actions are:
            start_game
            leave_game
            recruit :param 0 - 4
            sell_hero_in_hand :param 0 - 7
            level_up
            toggle_store
            lock_store
            reroll
            wait
            move_hero_in_hand :param [0 - 7, 0 - 7]
            upgrade_hero_in_hand :param 0 - 7

            log
        :param action_param: The parameter associate with the action. All position start from 0.
        """
        self.name = action_name
        self.param = action_param