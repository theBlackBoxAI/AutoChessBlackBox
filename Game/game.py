import time

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

    def start_observation_only_game(self):
        """
        Start a game that does not take any action. This is mostly used for debugging.
        :return:
        """
        while True:
            self.env.grab_current_screenshot()
            print("Current Money: " + str(self.env.get_money()))
            print("Current Heroes in store: ")
            for hero in self.env.get_heroes_in_store():
                if hero:
                    print(hero.name)
            time.sleep(5)

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






