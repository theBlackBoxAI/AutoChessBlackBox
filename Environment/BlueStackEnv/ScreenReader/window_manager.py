import time
import os

import pytesseract
import win32gui
from PIL import Image
from desktopmagic.screengrab_win32 import getRectAsImage

from Util.imge_util import ImageUtil


class WindowManager:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"
        # Whether to use local screenshot instead of taking real time ones.
        self.use_local_screenshot = False
        self.local_screenshot_iter = None

    def set_local_screenshot_folder(self, folder):
        """
        Set the manager to take local screenshots instead of real time ones from simulator.
        :param folder: The folder to take screenshots from, screenshots have to be in the root of the folder, not in
        sub folders.
        :return:
        """
        self.use_local_screenshot = True
        self.local_screenshot_iter = iter(os.scandir(folder))

    def grab_current_screenshot(self):
        if self.use_local_screenshot:
            try:
                file = next(self.local_screenshot_iter)
                #print(file.path)
                return Image.open(file.path)
            except StopIteration:
                return None
        else:
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

    @staticmethod
    def grab_heroes_pool_text(screenshot):
        """
        Grabs the 5 names of the heroes in the pool using OCR. Empty if already empty
        :param screenshot: PIL.Image screenshot to grab from
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
        :param screenshot: PIL.Image screenshot to grab from
        :rtype: Array the images
        """

        #screenshot = WindowManager.preprocess_image(screenshot)
        return [screenshot.crop((509, 280, 820, 790)),
                screenshot.crop((820, 280, 1131, 790)),
                screenshot.crop((1131, 280, 1442, 790)),
                screenshot.crop((1442, 280, 1753, 790)),
                screenshot.crop((1753, 280, 2064, 790))]

    @staticmethod
    def grab_heroes_in_hand_images(screenshot):
        """
        Grabs the 8 image of heroes in hand.
        :param screenshot: PIL.Image screenshot. The screenshot to grab from
        :return:
        """

        return [screenshot.crop((550, 1140, 731, 1325)),
                screenshot.crop((731, 1140, 912, 1325)),
                screenshot.crop((912, 1140, 1093, 1325)),
                screenshot.crop((1093, 1140, 1274, 1325)),
                screenshot.crop((1274, 1140, 1455, 1325)),
                screenshot.crop((1455, 1140, 1636, 1325)),
                screenshot.crop((1636, 1140, 1817, 1325)),
                screenshot.crop((1817, 1140, 1998, 1325))]

    @staticmethod
    def grab_battle_state_image(screenshot):
        """
        Crop out the battle state image and return it.
        :param screenshot:
        :return:
        """
        return screenshot.crop((445, 50, 615, 165))

    @staticmethod
    def grab_hp_images(screenshot):
        """
        Grab all the hp images on the side.
        :param screenshot:
        :return:
        """
        return [screenshot.crop((230, 208, 400, 254)),
                screenshot.crop((230, 316, 400, 362)),
                screenshot.crop((230, 424, 400, 470)),
                screenshot.crop((230, 532, 400, 578)),
                screenshot.crop((230, 640, 400, 686)),
                screenshot.crop((230, 748, 400, 794)),
                screenshot.crop((230, 856, 400, 902)),
                screenshot.crop((230, 964, 400, 1010))]

    @staticmethod
    def grab_round_image(screenshot):
        return screenshot.crop((204, 58, 320, 87))

    @staticmethod
    def grab_level_image(screenshot):
        return screenshot.crop((350, 1183, 453, 1219))

    @staticmethod
    def grab_exp_image(screenshot):
        return screenshot.crop((355, 1233, 452, 1270))

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
            file_name = 'D:/AutoChess/Screenshots/Sample' + str(i) + '.jpg'
            WindowManager.save_img(src_image, file_name)
            print(file_name)
            time.sleep(10)