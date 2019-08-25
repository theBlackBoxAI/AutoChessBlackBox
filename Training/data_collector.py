import time
import os
from Environment.BlueStackEnv.env import BlueStackEnv

class DataCollector:
    def __init__(self, env=None):
        self.env = None
        if env is None:
            self.env = BlueStackEnv()
        else:
            self.env = env

    def full_screen_screenshot(self):
        """
        Keep taking full screen screenshot and store them in a folder.

        :return:
        """
        while True:
            self.env.grab_current_screenshot()
            screenshot = self.env.current_screenshot
            file_name = 'D:/Python/AutoChessTrainingData/Screenshots/Raw/'+ str(time.time()) + '.jpg'
            screenshot.save(file_name)
            print(file_name)
            time.sleep(1)

    def annotate_hero_in_store(self):
        """
        Use OCR to parse the heroes name in the store, if matched, annotate the according screenshot.

        :return:
        """
        while True:
            self.env.grab_current_screenshot()
            heroes = self.env.get_heroes_in_store()
            heroes_screenshot = self.env.grab_heroes_in_store_images()
            is_store_opened = False
            for hero in heroes:
                if hero:
                    is_store_opened = True
            for hero, screenshot in zip(heroes, heroes_screenshot):
                folder_name = None
                if hero:
                    folder_name = 'D:/Python/AutoChessTrainingData/HeroInStore/' + hero.name
                else:
                    if is_store_opened:
                        folder_name = 'D:/Python/AutoChessTrainingData/HeroInStore/undefined'
                if folder_name:
                    if not os.path.exists(folder_name):
                        os.mkdir(folder_name)
                        print("New folder created: " + folder_name)
                    file_name = folder_name + '/' + str(time.time()) + '.jpg'
                    screenshot.save(file_name)
                    print("New image saved: " + file_name)

            time.sleep(20)

    def screenshot_battle_state(self):
        """
        Crop out the battle state and store the screenshot of it

        :return:
        """
        folder_name = 'D:/Python/AutoChessTrainingData/BattleState/Raw'
        while True:
            self.env.grab_current_screenshot()
            image = self.env.grab_battle_state_image()
            file_name = folder_name + '/' + str(time.time()) + '.jpg'
            image.save(file_name)
            print("New image saved: " + file_name)

            time.sleep(1)

    def screenshot_hero_in_store(self):
        """
        Split all heroes in store and store the screenshot of them.

        :return:
        """
        while True:
            self.env.grab_current_screenshot()
            heroes_screenshot = self.env.grab_heroes_in_store_images()
            for screenshot in heroes_screenshot:
                folder_name = 'D:/Python/AutoChessTrainingData/HeroInStore/undefined'
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                    print("New folder created: " + folder_name)
                file_name = folder_name + '/' + str(time.time()) + '.jpg'
                screenshot.save(file_name)
                print("New image saved: " + file_name)

            time.sleep(1)


    def screenshot_hero_on_board(self):
        """
        Split all heroes in store and store the screenshot of them.

        :return:
        """
        while True:
            self.env.grab_current_screenshot()
            battle_state = self.env.get_battle_state()
            if battle_state == 'InBattle':
                continue
            store_state = self.env.get_store_state()
            if store_state == 'StoreClosed':
                heroes_screenshot = self.env.grab_heroes_on_board_images()
                flat_list = [item for sublist in heroes_screenshot for item in sublist]
                for screenshot in flat_list:
                    folder_name = 'D:/Python/AutoChessTrainingData/HeroOnBoard/undefined'
                    if not os.path.exists(folder_name):
                        os.mkdir(folder_name)
                        print("New folder created: " + folder_name)
                    file_name = folder_name + '/' + str(time.time()) + '.jpg'
                    screenshot.save(file_name)
                    print("New image saved: " + file_name)

                #time.sleep(1)

    def screenshot_hp(self):
        """
        Crop out all the hp section and store the screenshot of it

        :return:
        """
        folder_name = 'D:/Python/AutoChessTrainingData/Hp/undefined'
        while True:
            if not self.env.grab_current_screenshot():
                break
            if self.env.get_env_state() == 'InGame':
                if self.env.get_battle_state() == 'InPreparation':
                    if self.env.get_store_state() == 'StoreClosed':
                        for screenshot in self.env.grab_big_hp_images():
                            file_name = folder_name + '/' + str(time.time()) + '.jpg'
                            screenshot.save(file_name)
                            print("New image saved: " + file_name)

            #time.sleep(1)

    def screenshot_hero_upgrade_in_hand(self):
        """
        Split all heroes in store and store the screenshot of them.

        :return:
        """
        while True:
            self.env.grab_current_screenshot()
            if self.env.get_env_state() != 'InGame':
                continue
            heroes_screenshot = self.env.grab_heroes_in_hand_upgrade_images()
            for screenshot in heroes_screenshot:
                folder_name = 'D:/Python/AutoChessTrainingData/HeroInHandUpgrade/undefined'
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                    print("New folder created: " + folder_name)
                file_name = folder_name + '/' + str(time.time()) + '.jpg'
                screenshot.save(file_name)
                print("New image saved: " + file_name)

            time.sleep(1)

    def screenshot_hero_in_hand(self):
        """
        Split all heroes in store and store the screenshot of them.

        :return:
        """
        while True:
            self.env.grab_current_screenshot()
            if self.env.get_env_state() != 'InGame':
                continue
            heroes_screenshot = self.env.grab_heroes_in_hand_images()
            for screenshot in heroes_screenshot:
                folder_name = 'D:/Python/AutoChessTrainingData/HeroInHand/undefined'
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                    print("New folder created: " + folder_name)
                file_name = folder_name + '/' + str(time.time()) + '.jpg'
                screenshot.save(file_name)
                print("New image saved: " + file_name)

            time.sleep(1)




