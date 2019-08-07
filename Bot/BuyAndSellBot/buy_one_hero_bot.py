from GameBasic.action import Action
from GameBasic.hero_factory import HeroFactory
from GameBasic.game_state import Hand
import random
import copy


class BuyOneHeroBot:
    """
    A bot only buy and sell one specific hero.
    """
    def __init__(self, hero_names = None):
        self.hero_factory = HeroFactory()
        self.hero_names = hero_names
        if self.hero_names is None:
            self.hero_names = self.hero_factory.get_all_common_hero_names()
            random.shuffle(self.hero_names)

        self.hero_index = 0

        self.hand = Hand()
        self.hero_name = self.hero_names[self.hero_index]
        self.base_hero = self.hero_factory.get_hero_by_name(self.hero_name, 1)

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

        print('Reset bot state. Current hero:' + self.hero_name)

    def need_level_up(self, game_state):
        if self.base_hero.quality == 'Common':
            return False
        if self.base_hero.quality == 'Uncommon':
            return False
        if self.base_hero.quality == 'Rare':
            return game_state.level < 6
        return game_state.level < 8

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

        if game_state.money > 30:
            if self.need_level_up(game_state):
                actions.append(Action('level_up'))
                return actions

        if not game_state.store.is_open:
            actions.append(Action('toggle_store'))
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
                                           and game_state.round > 10 and game_state.money >= 2):
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
        # Allow the game to log the heroes in hand before upgrade.
        actions.append(Action('log_hero_in_hand', copy.deepcopy(self.hand)))

        upgrade_position = self.hand.can_hero_upgrade()
        if upgrade_position is None:
            if len(actions) == 0:
                actions.append(Action('wait', 5))
            return actions
        actions.append(Action('upgrade_hero_in_hand', upgrade_position))
        self.hand.upgrade_hero(upgrade_position)
        actions.append(Action('log_hero_in_hand', copy.deepcopy(self.hand)))

        new_upgrade_position = self.hand.can_hero_upgrade()
        if new_upgrade_position is None:
            actions.extend(self.rotate_actions(upgrade_position))
            return actions
        actions.append(Action('upgrade_hero_in_hand', new_upgrade_position))
        self.hand.upgrade_hero(new_upgrade_position)
        actions.append(Action('log_hero_in_hand', copy.deepcopy(self.hand)))
        actions.extend(self.rotate_actions(new_upgrade_position))

        return actions

    def rotate_actions(self, rotate_position):
        actions = []
        current_position = rotate_position
        for i in range(8):
            if current_position == i:
                continue
            actions.append(Action('move_hero_in_hand', [current_position, i]))
            self.hand.heroes[current_position], self.hand.heroes[i] = \
                self.hand.heroes[i], self.hand.heroes[current_position]
            actions.append(Action('log_hero_in_hand', copy.deepcopy(self.hand)))
            current_position = i
        return actions







