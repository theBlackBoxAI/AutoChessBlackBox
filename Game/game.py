import time
import sys
import os

from Util.Logger import Logger

DEBUG_FOLDER_ROOT = 'D:/AutoChess'

class Game:
    def __init__(self, environment):
        self.hand = Hand()
        self.board = Board()
        self.store = Store()
        self.money = 0
        self.turn = 0
        self.battle_record = []
        self.hp = 0
        self.level = 0
        self.exp = 0
        self.score = 0

        self.env = environment

        self.debug_mode = False
        self.debug_folder = None
        self.debug_log_file = None

        self.logger = None

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

    def start_observation_only_game(self, time_interval = 5):
        """
        Start a game that does not take any action. This is mostly used for debugging.
        :return:
        """
        f = open(self.debug_log_file, 'w')
        while True:
            self.env.grab_current_screenshot()
            if self.debug_mode:
                screenshot_file = self.debug_folder + str(time.time()) + '.jpg'
                self.env.current_screenshot.save(screenshot_file)
                print("Current Screenshot: " + screenshot_file)
            env_state = self.env.get_env_state()
            print("Env State: " + env_state)
            if env_state == 'InGame':
                store_state = self.env.get_store_state()
                print("Store State: " + store_state)
                if store_state == 'StoreOpened':
                    print("Current Heroes in store: ")
                    for hero in self.env.get_heroes_in_store():
                        if hero:
                            print(hero.name + ' ', end='')
                        else:
                            print('Empty ', end='')
                    print()
                if store_state == 'StoreClosed':
                    hp = self.env.get_hp()
                    if hp:
                        print('Hp: ' + str(hp))
                    else:
                        print("No Hp image is found")

                print("Current Money: " + str(self.env.get_money()))

                battle_state = self.env.get_battle_state()
                print("Battle State: " + battle_state)
                print()
            time.sleep(time_interval)

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


class Store:
    def __init__(self):
        self.heroes = [None, None, None, None, None]

    def get_hero(self, position):
        return self.heroes[position]

    def remove_hero(self, position):
        self.heroes[position] = None

    def update_store(self, heroes):
        self.heroes = heroes



class Hand:
    def __init__(self):
        self.heroes = [None, None, None, None, None, None, None, None]

    def put_hero_in_hand(self, hero):
        for index in range(len(self.heroes)):
            if self.heroes[index] is None:
                self.heroes[index] = hero
                return True
        else:
            return False


class Board:
    def __init__(self):
        self.board = [[None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None]]






