from GameBasic.action import Action
from GameBasic.hero_factory import HeroFactory
from GameBasic.game_state import Board
import random
import copy


class SimpleWarriorBot:
    """
    A bot only buy warrior hero.
    This bot need to have auto deploy and auto level up enabled to work.
    """

    def __init__(self, hero_names=None):
        self.hero_factory = HeroFactory()

        self.board = Board()
        self.board_updated_round = 0
        self.no_action_this_round = False

        self.is_game_started = False

    def reset(self):
        if not self.is_game_started:
            return
        self.is_game_started = False
        self.no_action_this_round = False
        self.board = Board()
        self.board_updated_round = 0

    def get_inactive_game_actions(self, game_state):
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

        if (game_state.in_battle):
            actions.append(Action('wait', 2))
            return actions

        return actions

    def need_level_up(self, game_state):
        if game_state.level < 5 and game_state.round >= 6:
            return True
        if game_state.level < 6 and game_state.round >= 9:
            return True
        if game_state.level < 7 and game_state.round >= 13:
            return True
        if game_state.level < 8 and game_state.round >= 21:
            return True
        return False

    def level_up(self, game_state):
        actions = []
        if not self.need_level_up(game_state):
            return actions
        if not game_state.can_level_up():
            return actions
        actions.append(Action('level_up'))
        return actions

    def update_board(self, game_state):
        actions = []
        if game_state.round > self.board_updated_round:
            # If it's a new turn, re-enable actions
            self.no_action_this_round = False
            if game_state.store.is_open:
                actions.append(Action('toggle_store'))
            else:
                self.board = copy.deepcopy(game_state.board)
                self.board_updated_round = game_state.round
        return actions

    def can_buy_heroes(self, game_state):
        if not game_state.hand.has_empty_space():
            return False
        return True

    def buy_heroes(self, game_state):
        actions = []
        if not self.can_buy_heroes(game_state):
            return actions
        if not game_state.store.is_open:
            actions.append(Action('toggle_store'))
            return actions

        for i in range(5):
            hero = game_state.store.heroes[i]
            if hero is not None:
                if hero.hero_class == 'Warrior':
                    actions.append(Action('recruit', i))
                    return actions
        return actions

    def need_reroll(self, game_state):
        if game_state.money > 55:
            return True
        return False

    def reroll(self, game_state):
        actions = []
        if self.need_reroll(game_state):
            actions.append(Action('reroll'))
            return actions
        return actions

    def get_actions(self, game_state):
        """
        Suggest a series of actions based on the given game state
        :param game_state:
        :return: An array of actions
        """

        # Check whether is actionable in game state.
        actions = self.get_inactive_game_actions(game_state)
        if len(actions) > 0:
            return actions

        # Update board on start of the turn.
        actions = self.update_board(game_state)
        if len(actions) > 0:
            return actions

        # If we don't want to do anything this round, skip the check
        if self.no_action_this_round:
            actions.append(Action('wait', 2))
            return actions

        # Level up if needed.
        actions = self.level_up(game_state)
        if len(actions) > 0:
            return actions

        # Buy heroes if it's warrior
        actions = self.buy_heroes(game_state)
        if len(actions) > 0:
            return actions

        # Reroll if needed
        actions = self.reroll(game_state)
        if len(actions) > 0:
            return actions

        # No action needed, just wait
        self.no_action_this_round = True
        actions.append(Action('toggle_store'))
        actions.append(Action('wait', 2))
        return actions


