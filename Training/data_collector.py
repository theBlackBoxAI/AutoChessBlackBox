import time
import os
from Environment.BlueStackEnv.env import BlueStackEnv

class DataCollector:
    def __init__(self):
        self.env = BlueStackEnv()


    def annotate_hero_in_store(self):
        """
        Use OCR to parse the heroes name in the store, if matched, annotate the according screenshot.

        :return:
        """
        while True:
            self.env.grab_current_screenshot()
            heroes = self.env.get_heroes_in_store()
            heroes_screenshot = self.env.grab_heroes_in_store_images()
            for hero, screenshot in zip(heroes, heroes_screenshot):
                if hero:
                    folder_name = 'D:/AutoChess/Data/HeroInStore/' + hero.name
                    if not os.path.exists(folder_name):
                        os.mkdir(folder_name)
                        print("New folder created: " + folder_name)
                    file_name = folder_name + '/' + str(time.time()) + '.jpg'
                    screenshot.save(file_name)
            time.sleep(30)








