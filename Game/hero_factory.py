import csv
from .hero import Hero
from os import path


class HeroFactory:
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
            print(f'Heroes loaded.')

    def get_hero_by_name(self, name, level):
        for hero in self.heroes:
            if (hero.name == name) and (hero.level == level):
                return hero
                break
        else:
            return None
