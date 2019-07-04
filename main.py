from Environment.BlueStackEnv.ScreenReader.window_manager import WindowManager
from Training.image_classifier import ImageClassifier
from Game.game import Game
from Environment.BlueStackEnv.env import BlueStackEnv
from Training.data_collector import DataCollector


def run_win_manager():
    winManager = WindowManager()
    winManager.main()


def run_training_money_classifier():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/AutoChess/Data/MoneyDigit/Raw', 'D:/Python/AutoChessBlackBox/Model/money_digit.h5')


def run_game_with_bluestack():
    game = Game(BlueStackEnv())
    game.start_observation_only_game()


def run_data_collector():
    data_collector = DataCollector()
    data_collector.annotate_hero_in_store()


if __name__ == '__main__':
    run_data_collector()

