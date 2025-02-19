import cv2
import math
import json
import numpy as np
import os
import random
from Util.imge_util import ImageUtil

from keras.preprocessing.image import load_img, ImageDataGenerator
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
        self.np_images = None

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

    def load_folders_and_train(self,
                               folders,
                               model_file_name,
                               model_name = 'vgg',
                               resize_ratio=1,
                               maxw=1000000,
                               maxh=1000000,
                               width_shift=0,
                               height_shift=0):
        """
        Load the data, train the model, and validate it.
        This can be used to load multiple folders together, to help better migrate from an old data set to a new one.

        :param folders: The folder that contains the data, each sub-folder is a class, with examples inside
        :param model_file_name: The file name to save the model as
        :param model_name: The model to use to train. right now 'vgg' and 'simple' is supported
        :param resize_ratio Whether to resize the image with a given ratio, ratio should be bigger or equal to 1
        :param maxw The maximum resize with, if samples are smaller then this will be changed.
        :param maxh The maximum resize height, if samples are smaller then this will be changed.
        :param width_shift The random shift range for image width.
        :param height_shift The random shift range for image height.
        :return:
        """
        for folder in folders:
            self.load_subdir_as_label(folder)
        self.process_labels()
        self.resize_images(resize_ratio, maxw, maxh)
        #self.to_grey_scale()
        self.prepare_data()
        self.shuffle_training_data()
        self.data_reshape()

        if model_name == 'simple':
            self.define_model()
        if model_name == 'vgg':
            self.define_smaller_vgg_model()

        if width_shift == 0 and height_shift == 0:
            self.train(32, 8)
        else:
            self.train_with_generator(batch_size=32, epochs=8, width_shift=width_shift, height_shift=height_shift)
        self.save_model(model_file_name)
        #self.load_model(model_file_name)
        self.evaluate()
        # self.load_model(model_file_name)

        print(self.model.predict_classes(np.array([self.x_train[0]])))
        print(self.reverse_labels_dictionary)
        print(self.reverse_labels_dictionary[self.model.predict_classes(np.array([self.x_train[0]]))[0]])
        # Show an image and its label to verify the classifier is working as intended
        ImageUtil.np_array_to_pil(self.x_train[0]).show()

    def load_and_train(self, folder, model_file_name, model_name = 'vgg', resize_ratio = 1):
        """
        Load the data, train the model, and validate it

        :param folder: The folder that contains the data, each sub-folder is a class, with examples inside
        :param model_file_name: The file name to save the model as
        :param model_name: The model to use to train. right now 'vgg' and 'simple' is supported
        :param resize_ratio Whether to resize the image with a given ratio, ratio should be bigger or equal to 1
        :return:
        """
        self.load_subdir_as_label(folder)
        self.process_labels()
        self.resize_images(resize_ratio)
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
        self.process_labels()
        self.resize_images()
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
        :param resize_ratio: the resize ratio used to down scale the image
        :return:
        """
        subfolders = [f for f in os.scandir(folder) if f.is_dir()]
        for f in subfolders:
            for image_file in os.scandir(f.path):
                image = load_img(image_file.path)
                # Force loading the image to prevent `Too many open files` error
                image.load()
                self.images.append(image)
                self.images_label.append(f.name)

            self.labels.add(f.name)
        print("Training data loaded.")
        print("# of images: " + str(len(self.images)))

    def process_labels(self):
        sorted_labels = sorted(self.labels)
        self.labels_dictionary = dict(zip(sorted_labels, np.arange(len(sorted_labels))))
        self.reverse_labels_dictionary = {v: k for k, v in self.labels_dictionary.items()}

        # Change the text label to int based on dictionary
        self.images_label = [self.labels_dictionary.get(label) for label in self.images_label]

    def resize_images(self, resize_ratio=1, minw=1000000, minh=1000000):
        for image in self.images:
            minw = min(minw, image.size[0])
            minh = min(minh, image.size[1])

        new_images = []
        minw = minw // resize_ratio
        minh = minh // resize_ratio
        for image in self.images:
            if (image.size[0] != minw) or (image.size[1] != minh):
                new_image = image.resize((minw, minh))
                new_images.append(new_image)
            else:
                new_images.append(image)

        self.images = new_images
        self.image_width = minw
        self.image_height = minh

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

    def train(self, batch_size=50, epochs=50):
        self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(self.x_train, self.y_train, batch_size=batch_size, epochs=epochs, verbose=1)

    def train_with_generator(self, batch_size=0, epochs=50, width_shift=0, height_shift=0):
        data_generator = ImageDataGenerator(
            width_shift_range=width_shift,
            height_shift_range=height_shift)
        data_generator.fit(self.x_train)

        self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

        self.model.fit_generator(data_generator.flow(self.x_train, self.y_train, batch_size=batch_size),
                                 steps_per_epoch=len(self.x_train) / batch_size * 5,
                                 epochs=epochs)

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




