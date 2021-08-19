import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Flatten, BatchNormalization, Conv2D, MaxPool2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os


# Location of all folders
folders = "D:\\CNN\\"
classes = [name for name in os.listdir(folders + "images\\temp") if os.path.isdir(os.path.join(folders + "images\\temp", name))]

train_path = folders + "images\\train\\"
valid_path = folders + "images\\valid\\"
test_path = folders + "images\\test\\"

'''
Using the VGG16 image processing for RBG images
Preprocessing the training, validation, and testing images
'''
train_batches = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.vgg16.preprocess_input
).flow_from_directory(
    directory=train_path,
    target_size=(224, 224),
    classes=classes,
    batch_size=10
)

valid_batches = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.vgg16.preprocess_input
).flow_from_directory(
    directory=valid_path,
    target_size=(224, 224),
    classes=classes,
    batch_size=10
)

test_batches = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.vgg16.preprocess_input
).flow_from_directory(
    directory=test_path,
    target_size=(224, 224),
    classes=classes,
    batch_size=10,
    shuffle=False
)

# Initializing the architecture of model
model = Sequential([
    Conv2D(                         # Hidden layer
        filters=32,                 # Standard value
        kernel_size=(3, 3),         # Standard value
        activation='relu',          # Standard activation
        padding='same',             # No padding
        input_shape=(224, 224, 3)   # Shape of image
    ),
    MaxPool2D(                      # Max pooling for dimension reduction
        pool_size=(2, 2),           # Filter size
        strides=2                   # Cut in half
    ),
    Conv2D(                         # Hidden layer
        filters=64,                 # Increase filters as you add layers
        kernel_size=(3, 3),
        activation='relu',
        padding='same'
    ),
    MaxPool2D(                      # Max pooling for dimension reduction
        pool_size=(2, 2),
        strides=2
    ),
    # Conv2D(                         # Hidden layer
    #     filters=128,
    #     kernel_size=(3, 3),
    #     activation='relu',
    #     padding='same'
    # ),
    # MaxPool2D(                      # Max pooling for dimension reduction
    #     pool_size=(2, 2),
    #     strides=2
    # ),
    Flatten(),                      # Flatten for output layer
    Dense(                          # Output layer
        units=len(classes),
        activation='softmax'
    )
])

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    x=train_batches,
    validation_data=valid_batches,
    epochs=10,
    verbose=2
)

model.save("D:\CNN")
