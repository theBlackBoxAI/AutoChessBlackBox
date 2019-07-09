import json
import numpy as np
from Environment.BlueStackEnv.ScreenReader.window_manager import WindowManager
from Environment.environment import Environment
from GameBasic.hero_factory import HeroFactory
from Training.data_processor import DataProcessor
from keras.models import load_model


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

        # Model consumes image with shape (22, 41)
        self.money_model = load_model('./Model/money_digit_v2.h5')

        # Model consumes image with shape (77, 127)
        self.hero_in_store_model = load_model('./Model/hero_in_store_v2.h5')
        self.hero_in_store_class_map = None
        with open('./Model/hero_in_store_v2.json') as json_file:
            reverse_map = json.load(json_file)
            self.hero_in_store_class_map = {v: k for k, v in reverse_map.items()}

        # Model consumes image with shape (160, 87)
        self.env_state_model = load_model('./Model/simulator_state_v2.h5')
        self.env_state_map = None
        with open('./Model/simulator_state_v2.json') as json_file:
            reverse_map = json.load(json_file)
            self.env_state_map = {v: k for k, v in reverse_map.items()}

        # Model consumes image with shape (160, 87)
        self.store_state_model = load_model('./Model/store_state_v1.h5')
        self.store_state_map = None
        with open('./Model/store_state_v1.json') as json_file:
            reverse_map = json.load(json_file)
            self.store_state_map = {v: k for k, v in reverse_map.items()}

        # Model consumes image with shape (42, 28)
        self.battle_state_model = load_model('./Model/battle_state_v1.h5')
        self.battle_state_map = None
        with open('./Model/battle_state_v1.json') as json_file:
            reverse_map = json.load(json_file)
            self.battle_state_map = {v: k for k, v in reverse_map.items()}


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
        images = self.grab_heroes_in_store_images()
        hero1 = self.hero_in_store_class_map[
            self.hero_in_store_model.predict_classes(np.array([np.array(images[0].resize((77, 127)))]))[0]]
        hero2 = self.hero_in_store_class_map[
            self.hero_in_store_model.predict_classes(np.array([np.array(images[1].resize((77, 127)))]))[0]]
        hero3 = self.hero_in_store_class_map[
            self.hero_in_store_model.predict_classes(np.array([np.array(images[2].resize((77, 127)))]))[0]]
        hero4 = self.hero_in_store_class_map[
            self.hero_in_store_model.predict_classes(np.array([np.array(images[3].resize((77, 127)))]))[0]]
        hero5 = self.hero_in_store_class_map[
            self.hero_in_store_model.predict_classes(np.array([np.array(images[4].resize((77, 127)))]))[0]]

        heroes_name = [hero1, hero2, hero3, hero4, hero5]
        heroes = []
        for name in heroes_name:
            heroes.append(self.hero_factory.get_hero_by_name(name, 1))

        return heroes

    def get_money(self):
        images = DataProcessor.extract_money_digit(self.current_screenshot)
        money = 0
        # Model has shape (22, 41)
        for image in images:
            image = image.resize((22, 41))
            np_image = np.array(image)
            prediction = self.money_model.predict_classes(np.array([np_image]))[0]
            money = money * 10 + int(prediction)
        return money

    def get_env_state(self):
        """
        Returns 'InGame', 'InLobby' or 'Other'
        :return:
        """
        image = self.current_screenshot.resize((160, 87))
        np_image = np.array(image)
        prediction = self.env_state_map[self.env_state_model.predict_classes(np.array([np_image]))[0]]
        return prediction

    def get_store_state(self):
        """
        Returns 'StoreOpened', 'StoreClosed'
        :return:
        """
        image = self.current_screenshot.resize((160, 87))
        np_image = np.array(image)
        prediction = self.store_state_map[self.store_state_model.predict_classes(np.array([np_image]))[0]]
        return prediction

    def get_battle_state(self):
        """
        Returns 'InBattle', 'InPreparation'
        :return:
        """
        image = self.grab_battle_state_image().resize((42, 28))
        np_image = np.array(image)
        prediction = self.battle_state_map[self.battle_state_model.predict_classes(np.array([np_image]))[0]]
        return prediction

    def grab_heroes_in_store_images(self):
        return self.window_manager.grab_heroes_pool_images(self.current_screenshot)

    def grab_battle_state_image(self):
        return self.window_manager.grab_battle_state_image(self.current_screenshot)