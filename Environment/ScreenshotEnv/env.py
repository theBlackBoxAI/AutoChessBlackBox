from Environment.BlueStackEnv.ScreenReader.window_manager import WindowManager
from Environment.BlueStackEnv.env import BlueStackEnv
from GameBasic.hero_factory import HeroFactory
from Training.data_processor import DataProcessor
from keras.models import load_model


class ScreenshotEnv(BlueStackEnv):
    def __init__(self, folder_name):
        """
        An environment runs on a series of screenshots taken from BlueStackEnv
        :param folder_name: The folder that contains the screenshots, all screenshots must be in the root folder.
        """
        super().__init__()
        self.window_manager.set_local_screenshot_folder(folder_name)

    def grab_current_screenshot(self):
        """
        This need to be called before all other actions, to update the screenshot
        :return:
        """
        super().grab_current_screenshot()
        self.current_screenshot.show()
        return self.current_screenshot
