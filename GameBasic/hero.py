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
        self.price = None

        self.parse_hero_from_array(attr)

    def parse_hero_from_array(self, attr_array):
        self.name = attr_array[0]
        self.level = int(attr_array[1])
        self.quality = attr_array[2].strip()
        self.hp = int(attr_array[3])
        self.atk = int(attr_array[4])
        self.armor = int(attr_array[5])
        self.atk_speed = float(attr_array[6])
        self.magic_resistant = float(attr_array[7])
        self.atk_range = int(attr_array[8])
        self.race = [attr_array[9].strip()]
        if (attr_array[10]) != '':
            self.race.append(attr_array[10].strip())
        self.hero_class = attr_array[11].strip()

        if self.quality == 'Common':
            self.price = 1
        if self.quality == 'Uncommon':
            self.price = 2
        if self.quality == 'Rare':
            self.price = 3
        if self.quality == 'Mythical':
            self.price = 4
        if self.quality == 'Legendary':
            self.price = 5

        if self.level == 2:
            self.price = self.price + 2
        if self.level == 3:
            self.price = self.price + 4

        if self.hero_class == 'Druid' and self.level == 3:
            self.price = self.price - 1
