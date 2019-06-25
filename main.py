from Game.hero_factory import HeroFactory
from Environment.SimulatorEnv.Operator.operator import Operator
from Environment.SimulatorEnv.ScreenReader.window_manager import WindowManager
from Training.data_processor import DataProcessor
from Training.image_classifier import ImageClassifier


def run_win_manager():
    winManager = WindowManager()
    winManager.main()


def run_training_money_classifier():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/AutoChess/Data/MoneyDigit/Raw', 'D:/Python/AutoChessBlackBox/Model/money_digit.h5')


if __name__ == '__main__':
    run_win_manager()

