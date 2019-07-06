import win32gui
import time
import pytesseract
import json
import numpy as np
from Util.imge_util import ImageUtil
from Training.data_processor import DataProcessor
from keras.models import load_model

from PIL import Image
from desktopmagic.screengrab_win32 import getRectAsImage


class WindowManager:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"
        # Model consumes image with shape (22, 41)
        self.money_model = load_model('./Model/money_digit_v2.h5')
        # Model consumes image with shape (311, 510)
        self.hero_in_store_model = load_model('./Model/hero_in_store_v1.h5')
        # Reverse mapping from number to string, used to parse the model's prediction result
        self.hero_in_store_class_map = None
        with open('./Model/hero_in_store_v1.json') as json_file:
            hero_in_store_reverse_class_map = json.load(json_file)
            self.hero_in_store_class_map = {v: k for k, v in hero_in_store_reverse_class_map.items()}

    def grab_current_screenshot(self):
        return WindowManager.grab_screenshot("BlueStacks")

    @staticmethod
    def grab_screenshot(windows_name):
        """
        Grabs the current screenshot

        :param str windows_name: The windows name for the window, which can be find with Spy++
        :return: the screenshot
        :rtype: PIL.Image
        """
        hwnd_main = win32gui.FindWindow(None, windows_name)
        if not hwnd_main:
            print('window not found!')

        window_rect = win32gui.GetWindowRect(hwnd_main)
        #print(window_rect)
        src_image: Image = getRectAsImage(window_rect)
        return src_image

    def grab_heroes_pool(self, screenshot):
        """
        Grabs the 5 names of the heroes in the pool. 'Empty' if already empty
        :param PIL.Image screenshot: The screenshot to grab from
        :rtype: Array the names
        """
        # Model has shape (311, 510)
        images = WindowManager.grab_heroes_pool_images(screenshot)
        hero1 = self.hero_in_store_class_map[
            self.hero_in_store_model.predict_classes(np.array([np.array(images[0])]))[0]]
        hero2 = self.hero_in_store_class_map[
            self.hero_in_store_model.predict_classes(np.array([np.array(images[1])]))[0]]
        hero3 = self.hero_in_store_class_map[
            self.hero_in_store_model.predict_classes(np.array([np.array(images[2])]))[0]]
        hero4 = self.hero_in_store_class_map[
            self.hero_in_store_model.predict_classes(np.array([np.array(images[3])]))[0]]
        hero5 = self.hero_in_store_class_map[
            self.hero_in_store_model.predict_classes(np.array([np.array(images[4])]))[0]]
        return [hero1, hero2, hero3, hero4, hero5]

    @staticmethod
    def grab_heroes_pool_text(screenshot):
        """
        Grabs the 5 names of the heroes in the pool using OCR. Empty if already empty
        :param PIL.Image screenshot: The screenshot to grab from
        :rtype: Array the names
        """

        screenshot = WindowManager.preprocess_image(screenshot)
        return [pytesseract.image_to_string(screenshot.crop((490, 670, 810, 725)), lang='chi_sim'),
                pytesseract.image_to_string(screenshot.crop((810, 670, 1130, 725)), lang='chi_sim'),
                pytesseract.image_to_string(screenshot.crop((1100, 670, 1430, 725)), lang='chi_sim'),
                pytesseract.image_to_string(screenshot.crop((1440, 670, 1730, 725)), lang='chi_sim'),
                pytesseract.image_to_string(screenshot.crop((1740, 670, 2050, 725)), lang='chi_sim')]

    @staticmethod
    def grab_heroes_pool_images(screenshot):
        """
        Grabs the 5 image of the heroes in the pool.
        :param PIL.Image screenshot: The screenshot to grab from
        :rtype: Array the images
        """

        #screenshot = WindowManager.preprocess_image(screenshot)
        return [screenshot.crop((509, 280, 820, 790)),
                screenshot.crop((820, 280, 1131, 790)),
                screenshot.crop((1131, 280, 1442, 790)),
                screenshot.crop((1442, 280, 1753, 790)),
                screenshot.crop((1753, 280, 2064, 790))]

    def grab_money(self, screenshot):
        images = DataProcessor.extract_money_digit(screenshot)
        money = 0
        # Model has shape (22, 41)
        for image in images:
            image = image.resize((22, 41))
            np_image = np.array(image)
            prediction = self.money_model.predict_classes(np.array([np_image]))[0]
            money = money * 10 + int(prediction)

        #print("Current money: " + str(money))
        return money

    @staticmethod
    def grab_turn(screenshot):
        return pytesseract.image_to_string(screenshot.crop((204, 50, 249, 86)), lang='eng')

    @staticmethod
    def save_img(image, file_name):
        image.save(file_name)

    @staticmethod
    def preprocess_image(image):
        return ImageUtil.to_grey_and_smooth(image)

    @staticmethod
    def grab_screenshot_and_save():
        for i in range(1000):
            src_image = WindowManager.grab_screenshot("BlueStacks")
            file_name = 'D:/AutoChess/Screenshots/Sample' + str(i) +  '.jpg'
            WindowManager.save_img(src_image, file_name)
            print(file_name)
            time.sleep(10)

    def main(self):
        #src_image = Image.open('D:/AutoChess/Data/Screenshots/Sample132.jpg')
        #src_image = Image.open('D:/AutoChess/Sample1.jpg')
        src_image = WindowManager.grab_screenshot("BlueStacks")

        #WindowManager.save_img(src_image, 'D:/AutoChess/Sample3.jpg')
        #print(WindowManager.grab_heroes_pool(src_image))
        #src_image.show()
        #window_manager = WindowManager()
        #src_image.show()
        #window_manager.grab_money(src_image)
        #print(window_manager.grab_heroes_pool(src_image))