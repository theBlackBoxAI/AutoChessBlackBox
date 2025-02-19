import time
import sys
import os
import threading
from pynput import keyboard
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

    def on_press(self, key):
        print('{0} pressed'.format(
            key))
        if key == keyboard.Key.esc:
            return False

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
                heroes = self.env.get_heroes_on_board()
                game_state.board.update_board(heroes)

            battle_state = self.env.get_battle_state()
            if battle_state == 'InBattle':
                game_state.in_battle = True
            else:
                game_state.num_hero_on_board = self.env.get_num_hero_on_board()

            game_state.hand.upgrade_state = self.env.get_hero_upgrade_state()
            game_state.hand.heroes = self.env.get_heroes_in_hand()

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
        with keyboard.Listener(on_press=self.on_press) as listener:
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
                        self.log_hero_in_hand_with_guess(game_state, action.param)
                        continue
                    if action.name == 'log_hero_in_hand':
                        self.env.grab_current_screenshot()
                        self.log_hero_in_hand(action.param)
                        continue
                    if action.name == 'log_hero_in_store':
                        #self.env.grab_current_screenshot()
                        #self.log_hero_in_store(game_state)
                        continue
                    if action.name == 'log_hero_on_board':
                        self.env.grab_current_screenshot()
                        self.log_hero_on_board(action.param)
                    self.env.perform_action(action)
                    if not listener.running:
                        break

                time.sleep(1)
                if not listener.running:
                    break

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

    def log_hero_in_store(self, game_state):
        if game_state.store.is_open:
            hero_images = self.env.grab_heroes_in_store_images()
            for i in range(5):
                hero = game_state.store.heroes[i]
                if hero is None:
                    continue
                folder_name = 'D:/Python/AutoChessTrainingData/HeroInStore_v3/' + hero.name
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                    print("New folder created: " + folder_name)
                file_name = folder_name + '/' + str(time.time()) + '.jpg'
                hero_images[i].save(file_name)
                print("New image saved: " + file_name)

    def log_hero_in_hand(self, hand):
        """
        Log the heroes in hand..
        :param game_state: The old game_state with heroes all in the store.
        :param hand: the Hand object for the current screenshot.
        :return:
        """
        heroes_screenshot = self.env.grab_heroes_in_hand_images()
        for i in range(8):
            if hand.heroes[i]:
                hero_name = hand.heroes[i].name + '_' + str(hand.heroes[i].level)
            else:
                continue
            folder_name = 'D:/Python/AutoChessTrainingData/HeroInHand_v3/' + hero_name
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
                print("New folder created: " + folder_name)
            file_name = folder_name + '/' + str(time.time()) + '.jpg'
            heroes_screenshot[i].save(file_name)
            print("New image saved: " + file_name)

    def log_hero_in_hand_with_guess(self, game_state, match_array=[0, 1, 2, 3, 4]):
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
            folder_name = 'D:/Python/AutoChessTrainingData/HeroInHand_v3/' + hero_name
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
                print("New folder created: " + folder_name)
            file_name = folder_name + '/' + str(time.time()) + '.jpg'
            heroes_screenshot[match_array[i]].save(file_name)
            print("New image saved: " + file_name)

    def log_hero_on_board(self, board):
        """
        Log the heroes on board.
        :param game_state: The old game_state with heroes all in the store.
        :param board: the Board object for the current screenshot.
        :return:
        """
        heroes_screenshot = self.env.grab_heroes_on_board_images()
        heroes, positions = board.get_heroes_and_positions()
        for hero, position in zip(heroes, positions):
            hero_name = hero.name + '_' + str(hero.level)
            folder_name = 'D:/Python/AutoChessTrainingData/HeroOnBoard_v2/' + hero_name
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
                print("New folder created: " + folder_name)
            file_name = folder_name + '/' + str(time.time()) + '.jpg'
            heroes_screenshot[position[0]][position[1]].save(file_name)
            print("New image saved: " + file_name)



