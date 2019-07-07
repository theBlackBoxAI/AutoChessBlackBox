import cv2
import math
import json
import numpy as np
import os
import random
from Util.imge_util import ImageUtil

from keras.preprocessing.image import load_img
from keras.utils import to_categorical
from keras.models import load_model
from keras.models import save_model
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.layers.normalization import BatchNormalization


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
        self.labels_dictionary = None
        self.reverse_labels_dictionary = None
        self.num_of_class = 0

        self.model = None

    def load_and_train(self, folder, model_file_name, model_name = 'vgg'):
        """
        Load the data, train the model, and validate it

        :param folder: The folder that contains the data, each sub-folder is a class, with examples inside
        :param model_file_name: the file name to save the model as
        :param model_name: the model to use to train. right now 'vgg' and 'simple' is supported
        :return:
        """
        self.load_subdir_as_label(folder)
        #self.to_grey_scale()
        self.prepare_data()
        self.shuffle_training_data()
        self.data_reshape()

        if model_name == 'simple':
            self.define_model()
        if model_name == 'vgg':
            self.define_smaller_vgg_model()

        self.train(32, 8)
        self.save_model(model_file_name)
        #self.load_model(model_file_name)
        self.evaluate()
        # self.load_model(model_file_name)

        print(self.model.predict_classes(np.array([self.x_train[0]])))
        print(self.reverse_labels_dictionary)
        print(self.reverse_labels_dictionary[self.model.predict_classes(np.array([self.x_train[0]]))[0]])
        # Show an image and its label to verify the classifier is working as intended
        ImageUtil.np_array_to_pil(self.x_train[0]).show()

    def load_and_continue_train(self, folder, model_name):
        """
        Load the data, and the model, train the model, and validate it

        :return:
        """
        self.load_subdir_as_label(folder)
        #self.to_grey_scale()
        self.prepare_data()
        self.shuffle_training_data()
        self.data_reshape()
        self.load_model(model_name)
        for i in range(100):
            self.train(100, 10)
            self.save_model(model_name)
        self.evaluate()

        print(self.reverse_labels_dictionary(self.model.predict_classes(np.array([self.x_train[0]]))))
        ImageUtil.np_array_to_pil(self.x_train[0]).show()

    def load_model(self, model_name):
        """
        Load an existing model, with the associate multi-class labels, from json file

        :param model_name:
        :return:
        """
        self.model = load_model(model_name)
        dic_name = model_name.replace('.h5', '.json')
        with open(dic_name) as json_file:
            self.labels_dictionary = json.load(json_file)
            self.reverse_labels_dictionary = {v: k for k, v in self.labels_dictionary.items()}

    def save_model(self, model_name, overwrite=True):
        """
        Save the label with the multi-class labels as json with the same name
        :param model_name:
        :param overwrite: Whether to overwrite the file
        :return:
        """
        save_model(self.model, model_name, overwrite)
        dic_name = model_name.replace('.h5', '.json')
        with open(dic_name, 'w') as json_file:
            json.dump(self.labels_dictionary, json_file, cls=NpJSONEncoder)

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

        sorted_labels = sorted(self.labels)
        self.labels_dictionary = dict(zip(sorted_labels, np.arange(len(sorted_labels))))
        self.reverse_labels_dictionary = {v: k for k, v in self.labels_dictionary.items()}

        # Change the text label to int based on dictionary
        self.images_label = [self.labels_dictionary.get(label) for label in self.images_label]

        new_images = []
        # If the image is too big, reduce its size
        if minw > 1000:
            minw = minw // 5
            minh = minh // 5
        for image in self.images:
            if (image.size[0] != minw) or (image.size[1] != minh):
                new_image = image.resize((minw, minh))
                new_images.append(new_image)
            else:
                new_images.append(image)

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
        model.add(Dense(128))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(len(self.labels), activation='softmax'))

        self.model = model

    def define_smaller_vgg_model(self):
        model = Sequential()

        model.add(Conv2D(32, (3, 3), padding='same', input_shape=(self.image_height, self.image_width, 3)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(3, 3)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (3,3), padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Conv2D(64, (3,3), padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(128, (3,3), padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Conv2D(128, (3,3), padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(1024))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        model.add(Dense(len(self.labels), activation='softmax'))

        self.model = model


    def train(self, batch_size = 50, epochs = 50):

        self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(self.x_train, self.y_train, batch_size = batch_size, epochs = epochs, verbose = 1)

    def evaluate(self):
        loss, acc = self.model.evaluate(self.x_test, self.y_test, verbose=1)
        print(acc * 100)


class NpJSONEncoder(json.JSONEncoder):
    """
    A JSONEncoder that can save np objects
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpJSONEncoder, self).default(obj)




