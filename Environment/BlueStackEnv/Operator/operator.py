import time
import pyautogui

OPERATION_INTERVAL = 1
SHOP_CHESS_POSITION = [(640, 500), (960, 500), (1270, 500), (1580, 500), (1900, 500)]
HAND_CHESS_POSITION = [(640, 1220), (820, 1220), (1000, 1220), (1180, 1220),
                       (1360, 1220), (1540, 1220), (1720, 1220), (1900, 1220)]
BOARD_CHESS_POSITION = [(640, 1220), (820, 1220), (1000, 1220), (1180, 1220),
                        (1360, 1220), (1540, 1220), (1720, 1220), (1900, 1220)]

SELL_HERO_POSITION = (320, 900)
LEVEL_UP_POSITION = (250, 1200)
LOCK_STORE_POSITION = (290, 670)
REROLL_STORE_POSITION = (2250, 670)

START_GAME_POSITION = (2200, 1200)
LEAVE_GAME_POSITION = [(1280, 1100), (1065, 1266)]


class Operator:
    @staticmethod
    def perform_action(action):
        """
            The current supported actions are:
            start_game
            leave_game
            recruit (param 0 - 4)
            sell_hero_in_hand (param 0 - 7)
            level_up
            toggle_store
            lock_store
            reroll
            wait
        :param action: GameBasic.Action
        :return:
        """
        if action.param is None:
            action.param = 0
        print("Action: " + action.name + ' ' + str(action.param))

        if action.name == 'start_game':
            Operator.start_game()
            return
        if action.name == 'leave_game':
            Operator.leave_game()
            return
        if action.name == 'recruit':
            Operator.recruit(action.param)
            return
        if action.name == 'sell_hero_in_hand':
            Operator.click_hero_in_hand(action.param)
            Operator.sell_hero()
            return
        if action.name == 'level_up':
            Operator.level_up()
            return
        if action.name == 'toggle_store':
            Operator.click_store()
            return
        if action.name == 'lock_store':
            Operator.lock_store()
            return
        if action.name == 'reroll':
            Operator.reroll()
        if action.name == 'wait':
            Operator.sleep(action.param)

    @staticmethod
    def press(key):
        pyautogui.press(key)
        time.sleep(OPERATION_INTERVAL)

    @staticmethod
    def click(position):
        """
        :param position: (x, y) tuple, for a position on screen
        :return:
        """
        pyautogui.click(position[0], position[1])
        time.sleep(OPERATION_INTERVAL)

    @staticmethod
    def drag(position1, position2):
        pyautogui.moveTo(position1[0], position1[1])
        pyautogui.dragTo(position2[1], position2[1], 1)
        time.sleep(OPERATION_INTERVAL)

    @staticmethod
    def sleep(duration):
        time.sleep(duration)

    @staticmethod
    def start_game():
        # Click Start Game
        Operator.click(START_GAME_POSITION)

    @staticmethod
    def leave_game():
        Operator.click(LEAVE_GAME_POSITION[0])
        Operator.click(LEAVE_GAME_POSITION[1])

    @staticmethod
    def click_store():
        Operator.click((2300, 1200))

    @staticmethod
    def recruit(position):
        """
        :param position: 0 - 4, the hero position in store
        :return:
        """
        # Click Start Game
        Operator.click(SHOP_CHESS_POSITION[position])

    @staticmethod
    def click_hero_in_hand(position):
        """
        :param position: 0 - 7, the hero position in hand
        :return:
        """
        # Click Start Game
        Operator.click(HAND_CHESS_POSITION[position])

    @staticmethod
    def sell_hero():
        Operator.click(SELL_HERO_POSITION)

    @staticmethod
    def level_up():
        Operator.click(LEVEL_UP_POSITION)

    @staticmethod
    def lock_store():
        Operator.click(LOCK_STORE_POSITION)

    @staticmethod
    def reroll():
        Operator.click(REROLL_STORE_POSITION)
