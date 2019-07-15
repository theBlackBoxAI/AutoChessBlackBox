from Environment.BlueStackEnv.env import BlueStackEnv
from Util.imge_util import ImageUtil
import cv2


class ScreenshotEnv(BlueStackEnv):
    def __init__(self, folder_name, text_only=False):
        """
        An environment runs on a series of screenshots taken from BlueStackEnv
        :param folder_name: The folder that contains the screenshots, all screenshots must be in the root folder.
        """
        super().__init__()
        self.window_manager.set_local_screenshot_folder(folder_name)
        self.text_only = text_only

    def grab_current_screenshot(self):
        """
        This need to be called before all other actions, to update the screenshot
        :return:
        """
        super().grab_current_screenshot()
        if not self.text_only:
            if self.current_screenshot:
                cv2.destroyAllWindows()
                cv2.imshow("Screenshot", ImageUtil.pil_to_cv2(self.current_screenshot))
                cv2.waitKey(1)
        return self.current_screenshot
