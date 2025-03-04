class Environment:
    """
    Base class for Environment. All actions should return True if succeed, False if not.
    """

    def __init__(self):
        self.is_active = False

    def get_env_state(self):
        """
        Returns 'InGame' or 'Other', custom environment may return more values based on its use case
        :return:
        """
        return 'Other'

    def get_store_state(self):
        """
        Returns 'StoreOpened', 'StoreClosed'
        :return:
        """
        return 'StoreOpened'

    def get_battle_state(self):
        """
        Returns 'InBattle', 'InPreparation'
        :return:
        """
        return 'InPreparation'

    def get_heroes_in_store(self):
        return [None, None, None, None, None]

    def get_money(self):
        return 0

    def get_round(self):
        return 0

    def get_hp(self):
        return 0

    def get_num_hero_on_board(self):
        return 0

    def get_heroes_in_hand(self):
        return [None, None, None, None, None, None, None, None]

    def get_hero_upgrade_state(self):
        return [False, False, False, False, False, False, False, False]

    def get_heroes_on_board(self):
        return [[None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None]]

    def put_hero_on_board(self, position, x, y):
        """
        :param position: 0-7, the position for the hero in hand
        :param x: 0-7, the x position on board
        :param y: 0-3, the y position on board
        :return:
        """
        return False

    def drag_hero_from_board(self, x, y, position):
        """
        :param x: 0-7, the x position on board
        :param y: 0-3, the y position on board
        :param position: 0-7, the position to move to in hand
        :return:
        """
        return False

    def sell_hero_in_hand(self, position):
        """
        :param position: 0-7, the position in hand to sell
        :return:
        """
        return False

    def sell_hero_on_board(self, x, y):
        """
        :param x: 0-7, the x position on board
        :param y: 0-3, the y position on board
        :return:
        """
        return False

    def buy_hero_in_store(self, position):
        return False

    def level_up(self):
        return False

    def lock_store(self):
        return False

    def unlock_store(self):
        return False

    def open_store(self):
        return False

    def close_store(self):
        return False
