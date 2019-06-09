class Game:
    def __init__(self):
        self.hand = Hand()
        self.board = Board()
        self.heroes_in_store = []
        self.money = 0
        self.turn = 0
        self.battle_record = []
        self.hp = 0
        self.level = 0
        self.exp = 0
        self.score = 0

    def buy_hero_in_store(self, position):
        hero = self.heroes_in_store[position]
        if hero is None:
            return
        if hero.price > self.money:
            return
        self.heroes_in_store[position]


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






