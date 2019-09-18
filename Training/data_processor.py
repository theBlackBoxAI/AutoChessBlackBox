import win32gui
import time
import cv2
import imutils
from imutils import contours
import numpy as np
from Util.imge_util import ImageUtil

from PIL import Image
from PIL import ImageFilter


class DataProcessor:
    @staticmethod
    def extract_contours(img):
        img = ImageUtil.to_grey_and_smooth(img)
        img = ImageUtil.pil_to_cv2(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # find all the digits
        cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            cnts = contours.sort_contours(cnts, method="left-to-right")[0]

        return img, cnts

    @staticmethod
    def extract_money_digit(src_image):
        """
        Extract the digit images.

        :param src_image: the full screen screenshot image
        :return:
        """
        # Crop from the position of the money area
        img = src_image.crop((1885, 68, 1953, 114))
        img, cnts = DataProcessor.extract_contours(img)

        images = []
        # loop over the digit area candidates
        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)
            if w < 15 or w > 35 or h < 35 or h > 45:
                continue
            #print(x, y, w, h)
            digit_img = img[y:y+h, x:x+w]
            digit_img = ImageUtil.cv2_to_pil(digit_img)
            images.append(digit_img)
        return images

    @staticmethod
    def extract_hp_digit(cropped_image):
        """
        Extract the digit images, of size (277, 94)

        :param cropped_image: The image contains the player's hp information.
        :return:
        """
        # Makes all not-so-white color into black, especially green color. To extract only the white text.
        cropped_image = cropped_image.crop((102, 73, 277, 94))
        img = cropped_image.convert("RGBA")
        pix_data = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b, a = img.getpixel((x, y))
                if (r < 220) & (b < 220):
                    pix_data[x, y] = (0, 0, 0, 1)
        img = ImageUtil.to_grey_and_smooth(img, 1)

        img = ImageUtil.pil_to_cv2(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # find all the digits
        cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            cnts = contours.sort_contours(cnts, method="left-to-right")[0]

        images = []
        # loop over the digit area candidates
        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)
            if w < 5 or w > 20 or h < 13 or h > 25:
                continue
            #print(x, y, w, h)
            digit_img = img[y:y+h, x:x+w]
            digit_img = ImageUtil.cv2_to_pil(digit_img)
            images.append(digit_img)
        return images

    @staticmethod
    def extract_round_digit(cropped_image):
        """
        Extract the digit images.

        :param cropped_image: The image contains the player's turn information.
        :return:
        """
        img = cropped_image
        img, cnts = DataProcessor.extract_contours(cropped_image)

        images = []
        # loop over the digit area candidates
        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)
            # Throw away the last two characters '回合'
            if w >= 20:
                continue
            #print(x, y, w, h)
            digit_img = img[y:y+h, x:x+w]
            digit_img = ImageUtil.cv2_to_pil(digit_img)
            images.append(digit_img)
        return images

    @staticmethod
    def extract_level_digit(cropped_image):
        """
        Extract the digit images.

        :param cropped_image: The image contains the player's turn information.
        :return:
        """
        img = cropped_image
        img, cnts = DataProcessor.extract_contours(cropped_image)

        images = []
        # loop over the digit area candidates
        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)
            # Throw away the first two characters '等级'
            if w < 10 or w > 18 or h < 20 or h > 26:
                continue
            #print(x, y, w, h)
            digit_img = img[y:y+h, x:x+w]
            digit_img = ImageUtil.cv2_to_pil(digit_img)
            images.append(digit_img)
        return images

    @staticmethod
    def extract_exp_digit(cropped_image):
        """
        Extract the digit images.

        :param cropped_image: The image contains the player's exp information
        :return:
        """
        # Makes all not-so-white color into black
        img = cropped_image.convert("RGBA")
        pix_data = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b, a = img.getpixel((x, y))
                if (g < 130) and (r < 150) and (b < 100):
                    pix_data[x, y] = (0, 0, 0, 1)
        img = ImageUtil.to_grey_and_smooth(img, 1)

        img = ImageUtil.pil_to_cv2(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # find all the digits
        cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            cnts = contours.sort_contours(cnts, method="left-to-right")[0]

        images = []
        # loop over the digit area candidates
        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)
            if w < 10 or w > 20 or h < 15 or h > 30:
                continue
            #print(x, y, w, h)
            digit_img = img[y:y+h, x:x+w]
            digit_img = ImageUtil.cv2_to_pil(digit_img)
            images.append(digit_img)
        return images


    @staticmethod
    def extract_hero_on_board_digit(cropped_image):
        """
        Extract the digit images.

        :param cropped_image: The image contains the player's exp information
        :return:
        """
        # Makes all not-so-white color into black
        img = cropped_image.convert("RGBA")
        pix_data = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b, a = img.getpixel((x, y))
                if (g < 130) and (r < 150) and (b < 100):
                    pix_data[x, y] = (0, 0, 0, 1)
        img = ImageUtil.to_grey_and_smooth(img, 1)

        img = ImageUtil.pil_to_cv2(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # find all the digits
        cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            cnts = contours.sort_contours(cnts, method="left-to-right")[0]

        images = []
        # loop over the digit area candidates
        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)
            if w < 20 or w > 40 or h < 30 or h > 60:
                continue
            digit_img = img[y:y+h, x:x+w]
            digit_img = ImageUtil.cv2_to_pil(digit_img)
            images.append(digit_img)
        return images


    @staticmethod
    def extract_all_money_digit():
        for i in range(4, 199):
            file_name = 'D:/AutoChess/Data/Screenshots/Sample' + str(i) + '.jpg'
            to_file_prefix = 'D:/AutoChess/Data/MoneyDigit/Raw/Sample' + str(i) + '_'
            src_image = Image.open(file_name)
            images = DataProcessor.extract_money_digit(src_image)
            index = 0
            for image in images:
                image.save(to_file_prefix + str(index) + '.jpg')
                index = index + 1
            print(file_name)

