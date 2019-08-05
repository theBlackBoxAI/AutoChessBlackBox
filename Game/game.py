import time
import sys
import os
from GameBasic.game_state import GameState
from GameBasic.action import Action

from Util.Logger import Logger

DEBUG_FOLDER_ROOT = 'D:/AutoChess'

class Game:
    def __init__(self, environment):
        self.env = environment

        self.debug_mode = False
        self.debug_folder = None
        self.debug_log_file = None

        self.logger = None
        self.bot = None

    def install_bot(self, bot):
        self.bot = bot

    def toggle_debug_mode(self, enabled):
        self.debug_mode = enabled
        if enabled:
            self.debug_folder = DEBUG_FOLDER_ROOT + '/' + str(time.time()) + '/'
            if not os.path.exists(self.debug_folder):
                os.mkdir(self.debug_folder)
                print("New folder created: " + self.debug_folder)

            self.debug_log_file = self.debug_folder + 'log.txt'
            f = open(self.debug_log_file, 'w')
            f.close()

            self.logger = Logger(self.debug_log_file)
            sys.stdout = self.logger

    def grab_current_game_state(self):
        """
        Grab the game state for the current screenshot.
        :return: The game state of current screenshot
        """
        game_state = GameState()
        env_state = self.env.get_env_state()
        if env_state == 'InGame':
            game_state.is_active = True
            game_state.round = self.env.get_round()
            game_state.level = self.env.get_level()
            game_state.exp = self.env.get_exp()
            game_state.money = self.env.get_money()
            store_state = self.env.get_store_state()
            if store_state == 'StoreOpened':
                game_state.store.is_open = True
                heroes = self.env.get_heroes_in_store()
                game_state.store.update_store(heroes)
            if store_state == 'StoreClosed':
                game_state.hp = self.env.get_hp()

            battle_state = self.env.get_battle_state()
            if battle_state == 'InBattle':
                game_state.in_battle = True

        return game_state

    def start_observation_only_game(self, time_interval = 5):
        """
        Start a game that does not take any action. This is mostly used for debugging.
        :return:
        """
        while True:
            if self.env.grab_current_screenshot() is None:
                # If no screenshot is available, stop the game
                break
            if self.debug_mode:
                screenshot_file = self.debug_folder + str(time.time()) + '.jpg'
                self.env.current_screenshot.save(screenshot_file)
                print("Current Screenshot: " + screenshot_file)
            self.grab_current_game_state().print()

            time.sleep(time_interval)

    def start_game(self):
        """
        Start a game.
        :return:
        """
        while True:
            screenshot = self.env.grab_current_screenshot()
            if screenshot is None:
                # If no screenshot is available, stop the game
                break
            game_state = self.grab_current_game_state()
            if self.debug_mode:
                screenshot_file = self.debug_folder + str(time.time()) + '.jpg'
                self.env.current_screenshot.save(screenshot_file)
                print("Current Screenshot: " + screenshot_file)

            game_state.print()

            actions = self.bot.get_actions(game_state)
            for action in actions:
                if action.name == 'log':
                    self.env.grab_current_screenshot()
                    self.log_heroes_in_hand(game_state, action.param)
                else:
                    self.env.perform_action(action)

            time.sleep(1)

    def buy_hero_in_store(self, position):
        '''

        :param position: 0 to 4, the position in store.
        :return: False if failed to buy, True if succeed
        '''
        hero = self.store.get_hero(position)
        if hero is None:
            return False
        if hero.price > self.money:
            return False

        self.store.remove_hero(position)
        self.money -= hero.price
        return True

    def log_heroes_in_hand(self, game_state, match_array=[0, 1, 2, 3, 4]):
        """
        Log the heroes in hand with a guessed label for it.
        :param game_state: The old game_state with heroes all in the store.
        :param match_array: The in-store to in-hand mapping
        :return:
        """

        heroes_screenshot = self.env.grab_heroes_in_hand_images()
        for i in range(5):
            hero_name = 'Empty'
            if game_state.store.heroes[i]:
                hero_name = game_state.store.heroes[i].name + '_1'
            folder_name = 'D:/Python/AutoChessTrainingData/HeroInHand/' + hero_name
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
                print("New folder created: " + folder_name)
            file_name = folder_name + '/' + str(time.time()) + '.jpg'
            heroes_screenshot[match_array[i]].save(file_name)
            print("New image saved: " + file_name)

        time.sleep(1)



