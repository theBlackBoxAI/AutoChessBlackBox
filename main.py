from Environment.BlueStackEnv.ScreenReader.window_manager import WindowManager
from Training.image_classifier import ImageClassifier
from Game.game import Game
from Environment.BlueStackEnv.env import BlueStackEnv
from Training.data_collector import DataCollector


def run_win_manager():
    win_manager = WindowManager()
    win_manager.main()


def run_training_money_classifier():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/AutoChess/Data/MoneyDigit/Raw',
                              './Model/money_digit.h5',
                              model_name='vgg')


def run_training_hero_in_store():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/AutoChess/Data/HeroInStore',
                              './Model/hero_in_store.h5',
                              model_name='vgg',
                              resize_ratio=4)


def run_training_simulator_state():
    classifier = classifier = ImageClassifier()
    classifier.load_and_train('D:/AutoChess/Data/Screenshots',
                              './Model/simulator_state.h5',
                              model_name='vgg',
                              resize_ratio=16)


def run_observation_game_with_bluestack():
    game = Game(BlueStackEnv())
    game.start_observation_only_game()


def run_data_collector():
    data_collector = DataCollector()
    #data_collector.annotate_hero_in_store()
    #data_collector.screenshot_hero_in_store()
    data_collector.full_screen_screenshot()


if __name__ == '__main__':
    run_training_hero_in_store()

