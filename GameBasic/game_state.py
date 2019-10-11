from GameBasic.hero_factory import HeroFactory

EXP_DIC = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 16, 7: 24, 8: 32, 9: 40}


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
        self.num_hero_on_board = 0

        self.in_battle = False

        self.battle_record = []

    def can_level_up(self):
        if (EXP_DIC[self.level] - self.exp + 3) / 4 * 5 <= self.money:
            return True
        return False

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
        print("Num Heroes: " + str(self.num_hero_on_board))
        self.store.print()
        if not self.in_battle:
            self.board.print()
        self.hand.print()


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
            print("STORE")
        else:
            return

        for hero in self.heroes:
            if hero:
                print(hero.name + " ", end="")
            else:
                print("Empty ", end="")
        print()


class Hand:
    def __init__(self):
        self.hero_factory = HeroFactory()
        self.heroes = [None, None, None, None, None, None, None, None]
        self.upgrade_state = [False, False, False, False, False, False, False, False]

    def has_empty_space(self):
        for hero in self.heroes:
            if hero is None:
                return True
        return False

    def add_hero(self, hero):
        for index in range(len(self.heroes)):
            if self.heroes[index] is None:
                self.heroes[index] = hero
                return True
        else:
            return False

    def can_hero_upgrade(self):
        """
        :return: The first position for the hero that can upgrade, None if not exist.
        """
        for i in range(len(self.heroes)):
            if self.heroes[i] is None:
                continue
            hero_count = 1
            for j in range(i + 1, len(self.heroes)):
                if self.heroes[j] is None:
                    continue
                if self.heroes[i].name == self.heroes[j].name and self.heroes[i].level == self.heroes[j].level:
                    hero_count = hero_count + 1
                    if hero_count == 3:
                        return i
        return None

    def print(self):
        print("HAND")
        for hero in self.heroes:
            if hero:
                print(hero.to_string_name_and_level() + " ", end="")
            else:
                print("Empty ", end="")
        print()

        can_upgrade = False
        for i in range(8):
            if self.upgrade_state[i]:
                can_upgrade = True
                break
        if can_upgrade:
            print("Can upgrade: ")
            for i in range(8):
                if self.upgrade_state[i] and self.heroes[i]:
                    print(self.heroes[i].to_string_name_and_level() + " at position " + str(i))

    def upgrade_hero(self, position):
        if (self.can_hero_upgrade()) != position:
            return
        hero = self.heroes[position]
        self.heroes[position] = self.hero_factory.get_hero_by_name(hero.name, hero.level + 1)
        hero_count = 1
        for i in range(len(self.heroes) - 1, position, -1):
            if self.heroes[i] is None:
                continue
            if hero.name == self.heroes[i].name and hero.level == self.heroes[i].level:
                self.heroes[i] = None
                hero_count = hero_count + 1
                if hero_count == 3:
                    return


class Board:
    def __init__(self):
        self.is_visible = False
        self.board = [[None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None]]

    def update_board(self, board):
        self.board = board

    def replace(self, position, new_hero):
        self.board[position[0]][position[1]] = new_hero

    def is_empty(self):
        for row in self.board:
            for hero in row:
                if hero is not None:
                    return False
        return True

    def get_heroes_and_positions(self):
        """
        Returns a list of hero and its positions
        :return:
        """
        heroes = []
        positions = []
        for i in range(4):
            for j in range(8):
                if self.board[i][j] is not None:
                    heroes.append(self.board[i][j])
                    positions.append((i, j))
        return heroes, positions

    def print(self):
        print("BOARD")
        for row in self.board:
            for hero in row:
                if hero:
                    print(hero.to_string_name_and_level() + " ", end="")
                else:
                    print("Empty ", end="")
            print()