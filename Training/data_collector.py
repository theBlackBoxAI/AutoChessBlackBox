import time
import os
from Environment.BlueStackEnv.env import BlueStackEnv

class DataCollector:
    def __init__(self):
        self.env = BlueStackEnv()

    def full_screen_screenshot(self):
        while True:
            self.env.grab_current_screenshot()
            screenshot = self.env.current_screenshot
            file_name = 'D:/AutoChess/Data/Screenshots/'+ str(time.time()) + '.jpg'
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
                    folder_name = 'D:/AutoChess/Data/HeroInStore/' + hero.name
                else:
                    if is_store_opened:
                        folder_name = 'D:/AutoChess/Data/HeroInStore/undefined'
                if folder_name:
                    if not os.path.exists(folder_name):
                        os.mkdir(folder_name)
                        print("New folder created: " + folder_name)
                    file_name = folder_name + '/' + str(time.time()) + '.jpg'
                    screenshot.save(file_name)
                    print("New image saved: " + file_name)

            time.sleep(20)

    def screenshot_hero_in_store(self):
        """
        Split all heroes in store and store the screenshot of them.

        :return:
        """
        while True:
            self.env.grab_current_screenshot()
            heroes_screenshot = self.env.grab_heroes_in_store_images()
            for screenshot in heroes_screenshot:
                folder_name = 'D:/AutoChess/Data/HeroInStore/undefined'
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                    print("New folder created: " + folder_name)
                file_name = folder_name + '/' + str(time.time()) + '.jpg'
                screenshot.save(file_name)
                print("New image saved: " + file_name)

            time.sleep(1)








