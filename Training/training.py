from Training.image_classifier import ImageClassifier
# File contains all the params used to train models.

def run_training_digit_classifier():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/Python/AutoChessTrainingData/Digit',
                              './Model/digit.h5',
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