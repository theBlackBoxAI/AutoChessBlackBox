from GameBasic.action import Action
from GameBasic.hero_factory import HeroFactory
from GameBasic.game_state import Hand
from GameBasic.game_state import Board
import random
import copy


class BuyOneHeroOnBoardBot:
    """
    A bot only buy and sell one specific hero.
    """
    def __init__(self, hero_names=None, rotate_on_update_only=False):
        self.hero_factory = HeroFactory()
        self.hero_names = hero_names
        if self.hero_names is None:
            self.hero_names = self.hero_factory.get_all_hero_names(quality='Common')
            self.hero_names.extend(self.hero_factory.get_all_hero_names(quality='Uncommon'))
            random.shuffle(self.hero_names)

        self.hero_index = 0

        self.hand = Hand()
        self.board = Board()
        self.hero_name = self.hero_names[self.hero_index]
        self.base_hero = self.hero_factory.get_hero_by_name(self.hero_name, 1)
        self.rotate_on_update_only = rotate_on_update_only
        self.level_up_times = 0

        self.is_game_started = False
        print('Start bot. Current hero:' + self.hero_name)

    def reset(self):
        if not self.is_game_started:
            return
        self.is_game_started = False
        self.hero_index = (self.hero_index + 1) % len(self.hero_names)
        self.hero_name = self.hero_names[self.hero_index]
        self.base_hero = self.hero_factory.get_hero_by_name(self.hero_name, 1)
        self.hand = Hand()
        self.level_up_times = 0

        print('Reset bot state. Current hero:' + self.hero_name)

    def need_level_up(self, game_state):
        if self.base_hero.quality == 'Common':
            return False
        if self.base_hero.quality == 'Uncommon':
            return False
        if self.base_hero.quality == 'Rare':
            return game_state.level < 6
        return game_state.level < 8

    def need_rotate(self, game_state):
        if game_state.in_battle:
            return False
        if game_state.num_hero_on_board == 0:
            return False
        return True

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
            self.reset()
            return actions

        self.is_game_started = True

        # Identify a game is ended.
        if (game_state.exp == -1) and (game_state.level == 0) and (not game_state.store.is_open):
            actions.append(Action('leave_game'))
            return actions

        if self.need_rotate(game_state):
            actions.extend(self.rotate_actions(game_state))
            return actions

        if game_state.money > 30:
            if self.need_level_up(game_state):
                actions.append(Action('level_up'))
                return actions

        if not game_state.store.is_open:
            actions.append(Action('toggle_store'))
            return actions

        if game_state.in_battle:
            actions.append(Action('wait', 5))
            return actions

        hero_positions = []
        for i in range(5):
            hero = game_state.store.heroes[i]
            if hero is None:
                continue
            if hero.name == self.hero_name:
                game_state.money = game_state.money - self.base_hero.price
                if game_state.money < 0:
                    break
                hero_positions.append(i)
        if len(hero_positions) == 0:
            if (game_state.money > 30) or (not self.need_level_up(game_state)
                                           and game_state.round > 10 and game_state.money >= 7):
                actions.append(Action('reroll'))
            else:
                actions.append(Action('wait', 5))
            return actions

        for i in range(5):
            if game_state.store.heroes[i] is None:
                continue
            if game_state.store.heroes[i].name == self.hero_name:
                actions.append(Action('recruit', i))
                self.hand.add_hero(game_state.store.heroes[i])
        if len(actions) == 0:
            actions.append(Action('wait', 5))
            return actions

        upgrade_position = self.hand.can_hero_upgrade()
        if upgrade_position is None:
            if self.rotate_on_update_only:
                if len(actions) == 0:
                    actions.append(Action('wait', 5))
                return actions
            else:
                actions.extend(self.move_hero_to_board(0))
                return actions

        actions.append(Action('upgrade_hero_in_hand', upgrade_position))
        self.hand.upgrade_hero(upgrade_position)
        self.level_up_times = self.level_up_times + 1

        new_upgrade_position = self.hand.can_hero_upgrade()

        if new_upgrade_position is None:
            return actions
        actions.append(Action('upgrade_hero_in_hand', new_upgrade_position))
        self.hand.upgrade_hero(new_upgrade_position)
        self.level_up_times = self.level_up_times + 1
        actions.extend(self.move_hero_to_board(0))

        return actions

    def rotate_actions(self, game_state):
        actions = []
        if game_state.in_battle:
            return actions
        if game_state.num_hero_on_board <= 0:
            return actions
        if game_state.store.is_open:
            actions.append(Action('toggle_store'))
            return actions
        heroes, positions = game_state.board.get_heroes_and_positions()
        if len(heroes) != 1:
            return actions

        position = positions[0]
        new_position = self.next_position(position)
        if new_position[0] == 0 and new_position[1] == 0:
            return self.move_hero_from_board(0)
        actions.append(Action('move_hero_on_board', [position, new_position]))
        board = copy.deepcopy(game_state.board)
        hero_level = 1
        if self.level_up_times > 0:
            hero_level = 2
        if self.level_up_times > 3:
            hero_level = 3
        hero_on_board = self.hero_factory.get_hero_by_name(self.hero_name, hero_level)
        board.replace(position, None)
        board.replace(new_position, hero_on_board)
        actions.append(Action('log_hero_on_board', copy.deepcopy(board)))

        return actions

    def move_hero_to_board(self, position=0):
        return [Action('move_hero_from_hand_to_board', [position, (0, 0)])]

    def move_hero_from_board(self, position=0):
        return [Action('move_hero_from_board_to_hand', [(3, 7), position])]

    def next_position(self, position):
        """
        The next position for the given one.
        :param position:
        :return:
        """
        new_x = position[0]
        new_y = position[1] + 1
        if new_y > 7:
            new_y = 0
            new_x = new_x + 1

        if new_x >= 5:
            new_x = 0

        return [new_x, new_y]

