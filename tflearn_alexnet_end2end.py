#author TJM
from __future__ import division, print_function, absolute_import
import pickle
import numpy as np 
from PIL import Image   #PIL 图像处理模块
import tensorflow as tf
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

#加载图像
def load_image(img_path):
    img = Image.open(img_path)
    return img


def resize_image(in_image, new_width, new_height, out_image=None,
                 resize_mode=Image.ANTIALIAS):
    img = in_image.resize((new_width, new_height), resize_mode)
    if out_image:
        img.save(out_image)
    return img

#nparray 数据类型
def pil_to_nparray(pil_image):
    pil_image.load()
    return np.asarray(pil_image, dtype="float32")


#获取图像 和标签
def load_data(datafile, num_clss, save=False, save_path='dataset.pkl'):
    train_list = open(datafile,'r')
    labels = []
    images = []
    for line in train_list:
        tmp = line.strip().split(' ')
        fpath = tmp[0]
        print(fpath)
        img = load_image(fpath)
        img = resize_image(img,224,224)
        np_img = pil_to_nparray(img)
        images.append(np_img)

        index = int(tmp[1])
        label = np.zeros(num_clss)
        label[index] = 1
        labels.append(label)
    if save:
        pickle.dump((images, labels), open(save_path, 'wb'))
    return images, labels


def load_from_pkl(dataset_file):
    X, Y = pickle.load(open(dataset_file, 'rb'))
    return X,Y


def create_alexnet(num_classes):
    # Building 'AlexNet'
    network = input_data(shape=[None, 224, 224, 3])
    network = conv_2d(network, 96, 11, strides=4, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = conv_2d(network, 256, 5, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = conv_2d(network, 384, 3, activation='relu')
    network = conv_2d(network, 384, 3, activation='relu')
    network = conv_2d(network, 256, 3, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    network = fully_connected(network, num_classes, activation='softmax')
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=0.001)
    return network


def train(network, X, Y):
    # Training
    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=2, tensorboard_dir='output')
    model.fit(X, Y, n_epoch=1000, validation_set=0.2, shuffle=True,
              show_metric=True, batch_size=128, snapshot_step=200,
              snapshot_epoch=False, run_id='alexnet_oxflowers17')

def predict(network, modelfile,images):
    model = tflearn.DNN(network)
    model.load(modelfile)
    return model.predict(images)
def train_():
    X, Y = load_data('train.txt', 17)
    # X, Y = load_from_pkl('dataset.pkl')
    net = create_alexnet(17)
    train(net, X, Y)

def test_():
    image = load_image(img_path='./17flowers/jpg/6/image_0481.jpg')
    image = resize_image(image, 224, 224)
    image = pil_to_nparray(image)
    image = np.expand_dims(image, 0)
    net = create_alexnet(17)
    a = predict(net, modelfile='model_alexnet-2600', images=image)
    # print(a)
    a = np.argmax(a)
    print(a)



if __name__ == '__main__':
    #train_()
    test_()


