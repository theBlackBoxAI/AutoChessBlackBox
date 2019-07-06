import time
import pyautogui

OPERATION_INTERVAL = 0.3
SHOP_CHESS_POSITION = [(640, 500), (960, 500), (1270, 500), (1580, 500), (1900, 500)]
HAND_CHESS_POSITION = [(640, 1220), (820, 1220), (1000, 1220), (1180, 1220),
                       (1360, 1220), (1540, 1220), (1720, 1220), (1900, 1220)]

BOARD_CHESS_POSITION = [(640, 1220), (820, 1220), (1000, 1220), (1180, 1220),
                        (1360, 1220), (1540, 1220), (1720, 1220), (1900, 1220)]

LEAVE_GAME_POSITION = (1280, 1100)

class Operator:
    def __init__(self):
        Operator.open_recruit()
        Operator.clickp(SHOP_CHESS_POSITION[0])

    @staticmethod
    def clickp(position):
        Operator.click(position[0], position[1])

    @staticmethod
    def click(x, y):
        pyautogui.click(x, y)
        time.sleep(OPERATION_INTERVAL)

    @staticmethod
    def drag(x1, y1, x2, y2):
        pyautogui.moveTo(x1, y1)
        time.sleep(OPERATION_INTERVAL)
        pyautogui.dragTo(x2, y2, 1)
        time.sleep(OPERATION_INTERVAL)

    @staticmethod
    def start_game():
        # Click Start Game
        Operator.click(2200, 1200)

    @staticmethod
    def recruit(position):
        # Click Start Game
        Operator.click(2200, 1200)

    @staticmethod
    def open_recruit():
        # Click Recruit button
        Operator.click(2300, 1200)
