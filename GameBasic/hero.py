class Hero:
    def __init__(self, attr):
        self.name = None
        self.level = None
        self.quality = None
        self.hp = None
        self.atk = None
        self.armor = None
        self.atk_speed = None
        self.magic_resistant = None
        self.atk_range = None
        self.race = None
        self.hero_class = None

        self.parse_hero_from_array(attr)

    def parse_hero_from_array(self, attr_array):
        self.name = attr_array[0]
        self.level = int(attr_array[1])
        self.quality = attr_array[2]
        self.hp = int(attr_array[3])
        self.atk = int(attr_array[4])
        self.armor = int(attr_array[5])
        self.atk_speed = float(attr_array[6])
        self.magic_resistant = float(attr_array[7])
        self.atk_range = int(attr_array[8])
        self.race = [attr_array[9]]
        if (attr_array[10]) != '':
            self.race.append(attr_array[10])
        self.hero_class = attr_array[11]


