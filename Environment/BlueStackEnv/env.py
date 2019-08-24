import json
import numpy as np
from Environment.BlueStackEnv.ScreenReader.window_manager import WindowManager
from Environment.environment import Environment
from GameBasic.hero_factory import HeroFactory
from Training.data_processor import DataProcessor
from Environment.BlueStackEnv.Operator.operator import Operator
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
        self.digit_model = load_model('./Model/digit_v1.h5')

        # Model consumes image with shape (22, 41)
        self.digit_with_slash_model = load_model('./Model/digit_with_slash_v1.h5')
        self.digit_with_slash_map = None
        with open('./Model/digit_with_slash_v1.json') as json_file:
            reverse_map = json.load(json_file)
            self.digit_with_slash_map = {v: k for k, v in reverse_map.items()}

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

        # Model consumes image with shape (90, 35)
        self.hero_upgrade_state_model = load_model('./Model/hero_upgrade_state_v1.h5')
        self.hero_upgrade_state_map = None
        with open('./Model/hero_upgrade_state_v1.json') as json_file:
            reverse_map = json.load(json_file)
            self.hero_upgrade_state_map = {v: k for k, v in reverse_map.items()}

        # Model consumes image with shape (277, 94)
        self.hp_state_model = load_model('./Model/hp_state_v1.h5')
        self.hp_state_map = None
        with open('./Model/hp_state_v1.json') as json_file:
            reverse_map = json.load(json_file)
            self.hp_state_map = {v: k for k, v in reverse_map.items()}

        # Model consumes image with shape (181, 185)
        self.hero_in_hand_model = load_model('./Model/hero_in_hand_v1.h5')
        self.hero_in_hand_class_map = None
        with open('./Model/hero_in_hand_v1.json') as json_file:
            reverse_map = json.load(json_file)
            self.hero_in_hand_class_map = {v: k for k, v in reverse_map.items()}

    def convert_img_digit_to_number(self, digit_images):
        """
        Convert a list of digit images into one number

        :param digit_images: the digit images
        :return:
        """
        number = 0
        # Model has shape (22, 41)
        for image in digit_images:
            image = image.resize((22, 41))
            np_image = np.array(image)
            prediction = self.digit_model.predict_classes(np.array([np_image]))[0]
            number = number * 10 + int(prediction)
        return number

    def grab_current_screenshot(self):
        """
        This need to be called before all other actions, to update the screenshot
        :return:
        """
        self.current_screenshot = self.window_manager.grab_current_screenshot()
        return self.current_screenshot

    def get_heroes_in_hand(self):
        """
        Get all 8 heroes object in hand, if the hero cannot be recognized or is empty, a None will be in the list.

        :return:
        """
        images = self.grab_heroes_in_hand_images()
        np_images = []
        for image in images:
            np_image = np.array(image)
            np_images.append(np_image)
        predictions = [self.hero_in_hand_class_map[p]
                       for p in self.hero_in_hand_model.predict_classes(np.array(np_images))]

        heroes = []
        for prediction in predictions:
            heroes.append(self.hero_factory.get_hero_by_name_level_string(prediction))

        return heroes

    def get_heroes_in_store(self):
        """
        Get all 5 heroes object in store, if the hero cannot be recognized or is empty, a None will be in the list.

        :return:
        """
        images = self.grab_heroes_in_store_images()
        #for image in images:
        #    image.save('D:/AutoChess/TempData/' + str(time.time()) + '.jpg')
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
        money = self.convert_img_digit_to_number(images)
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

    def get_hero_upgrade_state(self):
        """
        Returns an array with length 8
        :return:
        """
        images = self.grab_heroes_in_hand_upgrade_images()
        np_images = []
        for image in images:
            np_image = np.array(image.resize((90, 35)))
            np_images.append(np_image)
        predictions = [self.hero_upgrade_state_map[p]
                       for p in self.hero_upgrade_state_model.predict_classes(np.array(np_images))]
        result = []
        for prediction in predictions:
            if prediction == 'CanUpgrade':
                result.append(True)
            else:
                result.append(False)
        return result

    def get_hp(self):
        """
        Returns the current hp, if not found, return None
        Hp image's type is one of the following: 'EnemyHP', 'MyHP', 'Other'
        :return:
        """
        hp_images = self.grab_big_hp_images()
        np_images = []
        for image in hp_images:
            np_image = np.array(image)
            np_images.append(np_image)
        predictions = [self.hp_state_map[p] for p in self.hp_state_model.predict_classes(np.array(np_images))]
        my_hp_image = None
        for hp_image, prediction in zip(hp_images, predictions):
            if prediction == 'MyHP':
                if my_hp_image:
                    # if there are 2 images classified as MyHp, consider none of them are true and return None.
                    return None
                my_hp_image = hp_image

        if my_hp_image is None:
            return None

        digit_images = DataProcessor.extract_hp_digit(my_hp_image)
        hp = self.convert_img_digit_to_number(digit_images)
        return hp

    def get_round(self):
        """
        Return the current turn, if not found, return None
        :return:
        """
        images = DataProcessor.extract_round_digit(self.grab_round_image())
        current_round = self.convert_img_digit_to_number(images)
        return current_round

    def get_level(self):
        images = DataProcessor.extract_level_digit(self.grab_level_image())
        level = self.convert_img_digit_to_number(images)
        return level

    def get_exp(self):
        """
        Grab the exp value of current screen
        :return: the exp value, if the image is broken(No slash detected), returns -1
        """
        images = DataProcessor.extract_exp_digit(self.grab_exp_image())
        #for image in images:
        #    image = image.resize((22,41))
        #    image.save('D:/AutoChess/TempData/' + str(time.time()) + '.jpg')
        exp = 0
        # Model has shape (22, 41)
        for image in images:
            image = image.resize((22, 41))
            np_image = np.array(image)
            prediction = self.digit_with_slash_map[self.digit_with_slash_model.predict_classes(np.array([np_image]))[0]]
            if prediction == 'Slash':
                return exp
            exp = exp * 10 + int(prediction)
        return -1

    def perform_action(self, action):
        """
        Perform the given action.
        :param action:
        :return:
        """
        Operator.perform_action(action)

    def grab_heroes_in_store_images(self):
        return self.window_manager.grab_heroes_pool_images(self.current_screenshot)

    def grab_heroes_in_hand_images(self):
        return self.window_manager.grab_heroes_in_hand_images(self.current_screenshot)

    def grab_heroes_in_hand_upgrade_images(self):
        return self.window_manager.grab_heroes_in_hand_upgrade_images(self.current_screenshot)

    def grab_battle_state_image(self):
        return self.window_manager.grab_battle_state_image(self.current_screenshot)

    def grab_hp_images(self):
        return self.window_manager.grab_hp_images(self.current_screenshot)

    def grab_big_hp_images(self):
        return self.window_manager.grab_big_hp_images(self.current_screenshot)

    def grab_round_image(self):
        return self.window_manager.grab_round_image(self.current_screenshot)

    def grab_level_image(self):
        return self.window_manager.grab_level_image(self.current_screenshot)

    def grab_exp_image(self):
        return self.window_manager.grab_exp_image(self.current_screenshot)

