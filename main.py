from Game.hero_factory import HeroFactory
from Environment.SimulatorEnv.Operator.operator import Operator
from Environment.SimulatorEnv.ScreenReader.window_manager import WindowManager
from Training.data_processor import DataProcessor


def main():
    winManager = WindowManager()
    winManager.main()
    #DataProcessor.extract_all_money_digit()

if __name__ == '__main__':
    main()
