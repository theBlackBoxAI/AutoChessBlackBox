class GameState:
    def __init__(self):
        self.hand = Hand()
        self.board = Board()
        self.store = Store()

        self.is_active = False
        self.money = 0
        self.round = 0
        self.hp = 0
        self.level = 0
        self.exp = 0

        self.in_battle = False

        self.battle_record = []

    def print(self):
        if self.is_active:
            print("In Game")
        else:
            print("Not Active")
            return

        if self.in_battle:
            print("In Battle")

        print("Round: " + str(self.round))
        print("Level: " + str(self.level))
        print("Exp: " + str(self.exp))
        print("Money: " + str(self.money))
        print("Hp: " + str(self.hp))
        self.store.print()


class Store:
    def __init__(self):
        self.is_open = False
        self.is_locked = False
        self.heroes = [None, None, None, None, None]

    def get_hero(self, position):
        return self.heroes[position]

    def remove_hero(self, position):
        self.heroes[position] = None

    def update_store(self, heroes):
        self.heroes = heroes

    def print(self):
        if self.is_open:
            print("Store is open")
        else:
            return

        print("Current Heroes in store: ")
        for hero in self.heroes:
            if hero:
                print(hero.name + ' ', end='')
            else:
                print("Empty ", end="")
        print()


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
        self.is_visible = False
        self.board = [[None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None]]
