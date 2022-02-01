import os
import sys
import glob
import numpy as np
import pyautogui
import tensorflow as tf

from contextlib import contextmanager
from PIL import Image
from columnar import columnar
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

folder = '/Users/russellland/Documents/projects/convolutionalNeuralNet/'

# A function to suppress output of ImageDataGenerator
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


# Load model and initiate variables
model = keras.models.load_model(folder + 'models')
classes = [name for name in os.listdir(folder + 'images/temp') if
           os.path.isdir(os.path.join(folder + 'images/temp/', name))]

# Remove temporary files from previous run
for i in classes:
    files = glob.glob(folder + 'images/temp/' + i + '/*')
    for f in files:
        os.remove(f)


def make_predictions(model, folder, classes):
    activeScreenshot = pyautogui.screenshot()
    activeScreenshot = activeScreenshot.convert('RGB')
    activeScreenshot.save(folder + 'images/temp/' + classes[0] + '/tempImage.jpg')

    # Make images 512px x 512px
    img = Image.open(folder + 'images/temp/' + classes[0] + '/tempImage.jpg')
    cropped_img = img.crop((625, 230, 1137, 742))
    # cropped_img = cropped_img.convert('RGB')
    cropped_img.save(folder + 'images/temp/' + classes[0] + '/tempImage.jpg')

    with suppress_stdout():
        temp_preprocess = ImageDataGenerator(
            preprocessing_function=tf.keras.applications.vgg16.preprocess_input
        ).flow_from_directory(
            directory=folder + 'images/temp',
            target_size=(224, 224),
            classes=classes,
            batch_size=10,
            shuffle=False
        )

    temp_predictions = np.round(model.predict(x=temp_preprocess, verbose=0).astype(float), 3)

    table = columnar(temp_predictions.tolist(), classes, no_borders=True)
    print(table)


while True:
    make_predictions(model, folder, classes)
