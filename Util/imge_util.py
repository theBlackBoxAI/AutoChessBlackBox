import cv2
import numpy as np
from PIL import Image

class ImageUtil:
    # All images input should be PIL
    @staticmethod
    #
    def to_grey_and_smooth(img):
        img = ImageUtil.pil_to_cv2(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(img, (5, 5), 0)
        ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return ImageUtil.cv2_to_pil(th)

    @staticmethod
    def pil_to_cv2(img):
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    @staticmethod
    def cv2_to_pil(img):
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
