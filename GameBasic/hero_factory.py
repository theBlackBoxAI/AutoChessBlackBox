import csv
from .hero import Hero
from os import path
from Common.singleton import Singleton


class HeroFactory(metaclass=Singleton):
    def __init__(self):
        self.heroes = self.load_heroes()

    def load_heroes(self):
        with open(path.relpath('Data/heroes.csv'), encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            heroes = []
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    new_hero = Hero(row)
                    heroes.append(new_hero)
                    line_count += 1
            print(str(len(heroes)) + ' heroes loaded.')
            return heroes

    def get_hero_by_name(self, name, level):
        for hero in self.heroes:
            if (hero.name == name) and (hero.level == level):
                return hero
                break
        else:
            return None

    def get_hero_by_name_level_string(self, name_level_string):
        """
        :param name_level_string: Example:  战神_2
        :return:
        """
        strings = name_level_string.split('_')
        if len(strings) != 2:
            return None
        name = strings[0]
        level = int(strings[1])
        for hero in self.heroes:
            if (hero.name == name) and (hero.level == level):
                return hero
                break
        else:
            return None

    def get_all_hero_names(self, quality=None):
        hero_names = set()
        for hero in self.heroes:
            if quality is not None:
                if hero.quality != quality:
                    continue
            hero_names.add(hero.name)

        return sorted(hero_names)


