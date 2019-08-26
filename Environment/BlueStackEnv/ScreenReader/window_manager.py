import time
import os

import win32gui
from PIL import Image
from desktopmagic.screengrab_win32 import getRectAsImage

from Util.imge_util import ImageUtil


class WindowManager:
    def __init__(self):
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
                while file.path.endswith('.txt'):
                    file = next(self.local_screenshot_iter)
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
        Grabs the 8 image of heroes in hand. (181, 185)
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
    def grab_heroes_on_board_images(screenshot):
        """
        Grabs the 32 image of heroes on board. (181, 185)
        :param screenshot: PIL.Image screenshot. The screenshot to grab from
        :return:
        """

        row3 = [screenshot.crop((609, 897, 790, 1082)),
                screenshot.crop((774, 897, 955, 1082)),
                screenshot.crop((939, 897, 1120, 1082)),
                screenshot.crop((1104, 897, 1285, 1082)),
                screenshot.crop((1269, 897, 1450, 1082)),
                screenshot.crop((1434, 897, 1615, 1082)),
                screenshot.crop((1599, 897, 1780, 1082)),
                screenshot.crop((1764, 897, 1945, 1082))]

        row2 = [screenshot.crop((633, 764, 808, 941)),
                screenshot.crop((792, 764, 967, 941)),
                screenshot.crop((951, 764, 1126, 941)),
                screenshot.crop((1110, 764, 1285, 941)),
                screenshot.crop((1269, 764, 1444, 941)),
                screenshot.crop((1428, 764, 1603, 941)),
                screenshot.crop((1587, 764, 1762, 941)),
                screenshot.crop((1746, 764, 1921, 941))]

        row1 = [screenshot.crop((654, 640, 822, 808)),
                screenshot.crop((808, 640, 976, 808)),
                screenshot.crop((962, 640, 1130, 808)),
                screenshot.crop((1116, 640, 1284, 808)),
                screenshot.crop((1270, 640, 1438, 808)),
                screenshot.crop((1424, 640, 1592, 808)),
                screenshot.crop((1578, 640, 1746, 808)),
                screenshot.crop((1732, 640, 1900, 808))]

        row0 = [screenshot.crop((654, 524, 824, 684)),
                screenshot.crop((820, 524, 986, 684)),
                screenshot.crop((970, 524, 1136, 684)),
                screenshot.crop((1120, 524, 1286, 684)),
                screenshot.crop((1270, 524, 1436, 684)),
                screenshot.crop((1420, 524, 1586, 684)),
                screenshot.crop((1570, 524, 1736, 684)),
                screenshot.crop((1720, 524, 1886, 684))]

        return [row0, row1, row2, row3]

    @staticmethod
    def grab_heroes_in_hand_upgrade_images(screenshot):
        """
        Grabs the 8 image of heroes upgrade icon in hand.
        :param screenshot: PIL.Image screenshot. The screenshot to grab from
        :return:
        """

        return [screenshot.crop((550, 1070, 731, 1140)),
                screenshot.crop((731, 1070, 912, 1140)),
                screenshot.crop((912, 1070, 1093, 1140)),
                screenshot.crop((1093, 1070, 1274, 1140)),
                screenshot.crop((1274, 1070, 1455, 1140)),
                screenshot.crop((1455, 1070, 1636, 1140)),
                screenshot.crop((1636, 1070, 1817, 1140)),
                screenshot.crop((1817, 1070, 1998, 1140))]

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
        DEPRECATED
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
    def grab_big_hp_images(screenshot):
        """
        Grab all the hp images on the side.
        :param screenshot:
        :return:
        """
        return [screenshot.crop((123, 160, 400, 254)),
                screenshot.crop((123, 268, 400, 362)),
                screenshot.crop((123, 376, 400, 470)),
                screenshot.crop((123, 484, 400, 578)),
                screenshot.crop((123, 592, 400, 686)),
                screenshot.crop((123, 700, 400, 794)),
                screenshot.crop((123, 808, 400, 902)),
                screenshot.crop((123, 916, 400, 1010))]

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