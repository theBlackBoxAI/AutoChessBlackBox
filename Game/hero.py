class Hero:
    def __init__(self, attr):
        self.parse_hero_from_array(attr)

    def parse_hero_from_array(self, attr_array):
        self.name = attr_array[0]
        self.level = attr_array[1]
        self.quality = attr_array[2]
        self.price = attr_array[3]
        self.hp = attr_array[4]
        self.atk = attr_array[5]
        self.armor = attr_array[6]
        self.atk_speed = attr_array[7]
        self.magic_resistant = attr_array[8]
        self.atk_range = attr_array[9]


