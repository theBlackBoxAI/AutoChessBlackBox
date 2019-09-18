from Environment.BlueStackEnv.ScreenReader.window_manager import WindowManager
from Training import training
from Game.game import Game
from Environment.BlueStackEnv.env import BlueStackEnv
from Environment.ScreenshotEnv.env import ScreenshotEnv
from Training.data_collector import DataCollector
from Bot.BuyAndSellBot.buy_all_bot import BuyAllBot
from Bot.BuyAndSellBot.buy_one_hero_bot import BuyOneHeroBot
from Bot.BuyAndSellBot.buy_one_hero_on_board_bot import BuyOneHeroOnBoardBot


def run_win_manager():
    screenshot = WindowManager.grab_current_screenshot()
    images = WindowManager.grab_heroes_in_hand_images(screenshot)


def run_observation_game_with_bluestack():
    game = Game(BlueStackEnv())
    game.toggle_debug_mode(True)
    game.start_observation_only_game(time_interval=5)


def run_observation_game_with_screenshots():
    game = Game(ScreenshotEnv('D:/AutoChess/1568771642.6894803'))
    #game.toggle_debug_mode(True)
    game.start_observation_only_game(time_interval=1000)


def run_game_with_buy_and_sell_bot():
    game = Game(BlueStackEnv())
    game.install_bot(BuyAllBot())
    game.start_game()


def run_game_with_buy_one_hero_bot():
    game = Game(BlueStackEnv())
    game.install_bot(BuyOneHeroBot())
    #game.toggle_debug_mode(True)
    game.start_game()

def run_game_with_buy_one_hero_on_board_bot():
    game = Game(BlueStackEnv())
    game.install_bot(BuyOneHeroOnBoardBot())
    game.start_game()


def run_data_collector():
    #data_collector = DataCollector()
    data_collector = DataCollector(ScreenshotEnv('D:/AutoChess/1568774803.6374059'))
    #data_collector.annotate_hero_in_store()
    #data_collector.screenshot_hero_in_store()
    #data_collector.full_screen_screenshot()
    #data_collector.screenshot_battle_state()
    #data_collector.screenshot_hero_in_hand()
    data_collector.screenshot_hero_on_board()


if __name__ == '__main__':
    run_game_with_buy_one_hero_on_board_bot()
    #training.run_training_hero()
