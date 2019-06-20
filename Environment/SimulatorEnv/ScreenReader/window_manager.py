import win32gui
import time
import pytesseract
import cv2
import imutils
import numpy as np
from .imge_util import ImageUtil

from PIL import Image
from desktopmagic.screengrab_win32 import getRectAsImage


class WindowManager:
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
        print(window_rect)
        src_image: Image = getRectAsImage(window_rect)
        return src_image

    @staticmethod
    def grab_heroes_pool(screenshot):
        """
        Grabs the 5 names of the heroes in the pool. Empty if already empty
        :param PIL.Image screenshot: The screenshot to grab from
        :rtype: Array the names
        """

        screenshot = WindowManager.preprocess_image(screenshot)
        screenshot.show()
        return [pytesseract.image_to_string(screenshot.crop((490, 670, 810, 725)), lang='chi_sim'),
                pytesseract.image_to_string(screenshot.crop((810, 670, 1130, 725)), lang='chi_sim'),
                pytesseract.image_to_string(screenshot.crop((1100, 670, 1430, 725)), lang='chi_sim'),
                pytesseract.image_to_string(screenshot.crop((1440, 670, 1730, 725)), lang='chi_sim'),
                pytesseract.image_to_string(screenshot.crop((1740, 670, 2050, 725)), lang='chi_sim')]

    @staticmethod
    def grab_money(screenshot):
        img = WindowManager.preprocess_image(screenshot.crop((1885, 68, 1953, 114)))
        img.show()
        img = ImageUtil.pil_to_cv2(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
        # find all the digits
        cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the digit area candidates
        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)
            print(x, y, w, h)
            digitImg = img[y:y+h, x:x+w]
            ImageUtil.cv2_to_pil(digitImg).show()





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
    def main1():
        for i in range(1000):
            src_image = WindowManager.grab_screenshot("BlueStacks")
            file_name = 'D:/AutoChess/Screenshots/Sample' + str(i) +  '.jpg'
            WindowManager.save_img(src_image, file_name)
            print(file_name)
            time.sleep(10)

    @staticmethod
    def main():
        pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"
        src_image = Image.open('D:/AutoChess/Screenshots/Sample23.jpg')
        #src_image = Image.open('D:/AutoChess/Sample1.jpg')
        #src_image = WindowManager.grab_screenshot("BlueStacks")
        #WindowManager.save_img(src_image, 'D:/AutoChess/Sample3.jpg')
        #print(WindowManager.grab_heroes_pool(src_image))
        #src_image.show()
        #src_image.crop((204, 50, 249, 86)).show()
        WindowManager.grab_money(src_image)