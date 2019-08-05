from Environment.BlueStackEnv.ScreenReader.window_manager import WindowManager
from Training import training
from Game.game import Game
from Environment.BlueStackEnv.env import BlueStackEnv
from Environment.ScreenshotEnv.env import ScreenshotEnv
from Training.data_collector import DataCollector
from Training.data_processor import DataProcessor
from Environment.BlueStackEnv.Operator.operator import Operator
from Bot.BuyAndSellBot.bot import BuyAndSellBot


def run_win_manager():
    screenshot = WindowManager.grab_current_screenshot()
    images = WindowManager.grab_heroes_in_hand_images(screenshot)


def run_observation_game_with_bluestack():
    game = Game(BlueStackEnv())
    game.toggle_debug_mode(True)
    game.start_observation_only_game()


def run_observation_game_with_screenshots():
    game = Game(ScreenshotEnv('D:/AutoChess/1563243945.0482247'))
    #game.toggle_debug_mode(True)
    game.start_observation_only_game(time_interval=10)


def run_game_with_buy_and_sell_bot():
    game = Game(BlueStackEnv())
    game.install_bot(BuyAndSellBot())
    game.start_game()


def run_data_collector():
    data_collector = DataCollector()
    #data_collector.annotate_hero_in_store()
    data_collector.screenshot_hero_in_store()
    #data_collector.full_screen_screenshot()
    #data_collector.screenshot_battle_state()
    #data_collector.screenshot_hero_in_hand()


if __name__ == '__main__':
    run_game_with_buy_and_sell_bot()
