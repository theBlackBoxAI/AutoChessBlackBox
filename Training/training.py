from Training.image_classifier import ImageClassifier
# File contains all the params used to train models.

def run_training_digit_classifier():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/Python/AutoChessTrainingData/Digit',
                              './Model/digit.h5',
                              model_name='vgg')


def run_training_hero_in_store():
    classifier = ImageClassifier()
    classifier.load_folders_and_train(['D:/Python/AutoChessTrainingData/HeroInStore',
                                       'D:/Python/AutoChessTrainingData/HeroInStore_v2'],
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
    classifier.load_folders_and_train(
        ['D:/Python/AutoChessTrainingData/StoreScreenshots',
         'D:/Python/AutoChessTrainingData/StoreScreenshots_v2'],
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
                              resize_ratio=2)

def run_training_hero_upgrade_state():
    classifier = ImageClassifier()
    classifier.load_and_train('D:/Python/AutoChessTrainingData/HeroInHandUpgrade',
                              './Model/hero_upgrade_state.h5',
                              model_name='vgg',
                              resize_ratio=2)


def run_training_hero_in_hand():
    classifier = ImageClassifier()
    classifier.load_folders_and_train(
        ['D:/Python/AutoChessTrainingData/HeroInHand',
         'D:/Python/AutoChessTrainingData/HeroInHand_v2'],
        './Model/hero_in_hand.h5',
        model_name='vgg',
        resize_ratio=2)


def run_training_hero():
    classifier = ImageClassifier()
    classifier.load_folders_and_train(
        ['D:/Python/AutoChessTrainingData/HeroInHand',
         'D:/Python/AutoChessTrainingData/HeroInHand_v2',
         'D:/Python/AutoChessTrainingData/HeroOnBoard'],
        './Model/hero.h5',
        model_name='vgg',
        resize_ratio=1,
        maxh=115,
        maxw=119)