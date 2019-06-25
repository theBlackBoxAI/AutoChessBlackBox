import cv2
import math
import numpy as np
import os
import random
from Util.imge_util import ImageUtil

from keras.preprocessing.image import load_img
from keras.utils import to_categorical
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense


class ImageClassifier:
    def __init__(self):
        # All the image data and labels
        self.images = []
        self.images_label = []

        # All the image data and labels, split into training and testing.
        # 10% of the images will be turned into testing data.
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []

        self.image_width = 0
        self.image_height = 0
        self.labels = set()
        self.num_of_class = 0

        self.model = None

    def load_and_train(self, folder, model_name):
        """
        Load the data, train the model, and validate it

        :return:
        """
        self.load_subdir_as_label(folder)
        self.to_grey_scale()
        self.prepare_data()
        self.shuffle_training_data()
        self.data_reshape()
        self.define_model()
        #self.train()
        #self.evaluate()
        # self.model.save(model_name)
        self.load_model(model_name)

        print(self.model.predict_classes(np.array([self.x_train[0]])))
        ImageUtil.np_array_to_pil(self.x_train[0]).show()

    def load_model(self, model_name):
        self.model = load_model(model_name)

    def load_subdir_as_label(self, folder):
        """
        Load all the image in a folder, sub-folder name will be the label for the images

        :param folder: the root folder
        :return:
        """
        subfolders = [f for f in os.scandir(folder) if f.is_dir()]
        minw = 1000000
        minh = 1000000
        for f in subfolders:
            for image_file in os.scandir(f.path):
                image = load_img(image_file.path)
                minw = min(minw, image.size[0])
                minh = min(minh, image.size[1])
                self.images.append(image)
                self.images_label.append(f.name)

            self.labels.add(f.name)

        new_images = []
        for image in self.images:
            new_image = image.resize((minw, minh))
            new_images.append(new_image)

        self.images = new_images
        self.image_width = minw
        self.image_height = minh

        print("Training data loaded.")
        print("# of images: " + str(len(self.images)))
        print("Image width: " + str(minw))
        print("Image height: " + str(minh))
        print("Number of classes: " + str(len(self.labels)))

    def shuffle_training_data(self):
        """
        Shuffle all the training data into training and testing randomly

        :return:
        """
        images_and_labels = list(zip(self.np_images, self.images_label))
        random.shuffle(images_and_labels)

        training_size = math.floor(len(self.np_images) * 0.9)
        self.x_train, self.y_train = zip(*images_and_labels)
        self.x_test, self.y_test = zip(*images_and_labels[training_size:])

    def to_grey_scale(self):
        new_images = []
        for image in self.images:
            cv2_image = ImageUtil.pil_to_cv2(image)
            cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
            image = ImageUtil.cv2_to_pil(cv2_image)
            new_images.append(image)

        self.images = new_images

    def prepare_data(self):
        """
        Convert image into the training ready format

        :return:
        """
        np_images = []
        for image in self.images:
            np_image = np.array(image)
            np_images.append(np_image)

        self.np_images = np_images

    def data_reshape(self):
        """
        Reshape the training and testing data, to fit the model

        :return:
        """
        self.x_train = np.array(self.x_train)
        self.x_test = np.array(self.x_test)

        print("training images array: " + str(self.x_train.shape))
        print("testing images array: " + str(self.x_test.shape))

        self.y_train = to_categorical(self.y_train, len(self.labels))
        self.y_test = to_categorical(self.y_test, len(self.labels))

        print("training labels array: " + str(self.y_train.shape))
        print("testing labels array: " + str(self.y_test.shape))

    def define_model(self):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape=(self.image_height, self.image_width, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(len(self.labels), activation='softmax'))

        self.model = model

    def train(self):

        self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(self.x_train, self.y_train, batch_size = 50, epochs = 50, verbose = 1)

    def evaluate(self):
        loss, acc = self.model.evaluate(self.x_test, self.y_test, verbose=1)
        print(acc * 100)






