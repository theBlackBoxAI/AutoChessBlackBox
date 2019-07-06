from enum import Enum
from Environment.BlueStackEnv.ScreenReader.window_manager import WindowManager
from Environment.environment import Environment
from GameBasic.hero_factory import HeroFactory


class BlueStackEnv(Environment):
    def __init__(self):
        super().__init__()
        self.is_active = True

        self.env_state = None
        self.game_state = None
        self.game = None
        self.current_screenshot = None

        self.window_manager = WindowManager()
        self.hero_factory = HeroFactory()

    def grab_current_screenshot(self):
        """
        This need to be called before all other actions, to update the screenshot
        :return:
        """
        self.current_screenshot = self.window_manager.grab_current_screenshot()

    def get_heroes_in_store(self):
        """
        Get all 5 heroes object in store, if the hero cannot be recognized or is empty, a None will be in the list.

        :return:
        """
        heroes_name = self.window_manager.grab_heroes_pool(self.current_screenshot)
        heroes = []
        print("Heroes name with classifier: ")
        print(heroes_name)
        for name in heroes_name:
            heroes.append(self.hero_factory.get_hero_by_name(name, 1))

        return heroes

    def grab_heroes_in_store_images(self):
        return self.window_manager.grab_heroes_pool_images(self.current_screenshot)

    def get_money(self):
        return self.window_manager.grab_money(self.current_screenshot)


class EnvState(Enum):
    home_screen = 1
    in_game = 2
    after_game = 3
    other = 4


class GameState(Enum):
    prepare_shopping = 1
    prepare_waiting = 2
    in_battle = 3

