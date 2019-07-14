from Environment.BlueStackEnv.ScreenReader.window_manager import WindowManager
from Training.image_classifier import ImageClassifier
from Game.game import Game
from Environment.BlueStackEnv.env import BlueStackEnv
from Environment.ScreenshotEnv.env import ScreenshotEnv
from Training.data_collector import DataCollector
from Training.data_processor import DataProcessor

from PIL import Image


def run_win_manager():
    win_manager = WindowManager()
    win_manager.main()


def run_training_money_classifier():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/Python/AutoChessTrainingData/MoneyDigit/Raw',
                              './Model/money_digit.h5',
                              model_name='vgg')


def run_training_hero_in_store():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/Python/AutoChessTrainingData/HeroInStore',
                              './Model/hero_in_store.h5',
                              model_name='vgg',
                              resize_ratio=4)


def run_training_simulator_state():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/Python/AutoChessTrainingData/Screenshots',
                              './Model/simulator_state.h5',
                              model_name='vgg',
                              resize_ratio=16)


def run_training_store_state():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/Python/AutoChessTrainingData/StoreScreenshots',
                              './Model/store_state.h5',
                              model_name='vgg',
                              resize_ratio=16)


def run_training_battle_state():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/Python/AutoChessTrainingData/BattleState',
                              './Model/battle_state.h5',
                              model_name='vgg',
                              resize_ratio=4)

def run_training_hp_state():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/Python/AutoChessTrainingData/Hp',
                              './Model/hp_state.h5',
                              model_name='vgg',
                              resize_ratio=1)


def run_observation_game_with_bluestack():
    game = Game(BlueStackEnv())
    game.start_observation_only_game()


def run_observation_game_with_screenshots():
    game = Game(ScreenshotEnv('D:/Python/AutoChessTrainingData/StoreScreenshots/test'))
    game.toggle_debug_mode(True)
    game.start_observation_only_game(time_interval=10)


def run_data_collector():
    data_collector = DataCollector()
    #data_collector.annotate_hero_in_store()
    #data_collector.screenshot_hero_in_store()
    #data_collector.full_screen_screenshot()
    #data_collector.screenshot_battle_state()
    data_collector.screenshot_hp()


if __name__ == '__main__':
    run_observation_game_with_screenshots()
