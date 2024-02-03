# import the necessary packages
from keras.models import Sequential
from keras.layers import BatchNormalization
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import AveragePooling2D
from keras.layers import GlobalAveragePooling2D
from keras.layers import Activation
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Dense
from keras import backend as K
from keras import regularizers

import tensorflow as tf
import cv2
import numpy as np
import os
import shutil
from keras.preprocessing.image import img_to_array

from PIL import Image
from io import BytesIO
import base64

import tensorflow as tf



# creator must tell us which splits to work
global supported_splits
supported_splits = [[(0,7,0),(7,17,0),(17,27,0),(27,34,0)],
                    [(0,7,0),(7,27,0),(27,34,0)],
                    [(0,17,0),(17,27,0),(27,34,0)],
                    [(0,7,0),(7,34,0)],
                    [(0,17,0),(17,34,0)],
                    [(0,27,0),(27,34,0)], [(0,34,0)]] 

# TO DO: add in the supported splits for the defo net

max_layers = 34

class DefoNet:
    @staticmethod
    def build(width, height, depth, classes, finalAct="softmax"):
        model = Sequential()
        inputShape = (height, width, depth)
        chanDim = -1
        l = 0.001
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)
            chanDim = 1

        # (CONV => RELU) * 2 => POOL  # layers 1-7
        model.add(Conv2D(32, (3, 3), padding="same",
                          input_shape=inputShape, kernel_regularizer=regularizers.l2(l)))   # 1. conv2d
        model.add(Activation("relu"))                                                       # 2. relu activation              
        model.add(BatchNormalization(axis=chanDim))                                         # 3. batch normalization                 
        model.add(Conv2D(32, (3, 3), padding="same",
                         input_shape=inputShape, kernel_regularizer=regularizers.l2(l)))    # 4. conv2s
        model.add(Activation("relu"))                                                       # 5. relu activation_1
        model.add(BatchNormalization(axis=chanDim))                                         # 6. batch normalization_1
        model.add(MaxPooling2D(pool_size=(2, 2)))                                           # 7. max pooling2d

        # (CONV => RELU) * 3 => POOL # layers 8-17
        model.add(Conv2D(64, (3, 3), padding="same", kernel_regularizer=regularizers.l2(l))) # 8. conv2d_2
        model.add(Activation("relu"))                                                        # 9. relu activation_2
        model.add(BatchNormalization(axis=chanDim))                                          # 10. batch normalization_2
        model.add(Conv2D(64, (3, 3), padding="same", kernel_regularizer=regularizers.l2(l))) # 11. conv2d_3
        model.add(Activation("relu"))                                                        # 12. relu activation_3
        model.add(BatchNormalization(axis=chanDim))                                          # 13. batch normalization_3
        model.add(Conv2D(64, (3, 3), padding="same", kernel_regularizer=regularizers.l2(l))) # 14. conv2d_4
        model.add(Activation("relu"))                                                        # 15. relu activation_4
        model.add(BatchNormalization(axis=chanDim))                                          # 16. batch normalization_4
        model.add(MaxPooling2D(pool_size=(2, 2)))                                            # 17. max pooling2d_1         

        # (CONV => RELU) * 3 => POOL # layers 18-27
        model.add(Conv2D(128, (3, 3), padding="same", kernel_regularizer=regularizers.l2(l))) # 18. conv2d_5
        model.add(Activation("relu"))                                                         # 19. relu activation_5 
        model.add(BatchNormalization(axis=chanDim))                                           # 20. batch normalization_5
        model.add(Conv2D(128, (3, 3), padding="same", kernel_regularizer=regularizers.l2(l))) # 21. conv2d_6
        model.add(Activation("relu"))                                                         # 22. relu activation_6                  
        model.add(BatchNormalization(axis=chanDim))                                           # 23. batch normalization_6
        model.add(Conv2D(128, (3, 3), padding="same", kernel_regularizer=regularizers.l2(l))) # 24. conv2d_7
        model.add(Activation("relu"))                                                         # 25. relu activation_7
        model.add(BatchNormalization(axis=chanDim))                                           # 26. batch normalization_7                
        model.add(MaxPooling2D(pool_size=(2, 2)))                                             # 27. max pooling2d_2

        # first (and only) set of FC => RELU layers # layers 28-32
        model.add(Flatten())                                                                  # 28. flatten
        model.add(Dense(1024, kernel_regularizer=regularizers.l2(l)))                         # 29. dense
        model.add(Activation("relu"))                                                         # 30. relu activation_8
        model.add(BatchNormalization())                                                       # 31. batch normalization_8
        model.add(Dropout(0.35))                                                              # 32. dropout

        # softmax classifier 
        model.add(Dense(classes))                                                             # 33. dense_1
        model.add(Activation(finalAct))                                                       # 34. relu activation_9
        # return the constructed network architecture
        return model

    
def decode_image_from_base64(image_base64):
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data)).convert('L')
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    img = cv2.resize(image, (108, 108))
    img = img.astype('float') / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = tf.convert_to_tensor(img) # convert to tensor
    return img

def predict(model, input_data, start_layer, end_layer):
    print(f"Predict function called with start_layer={start_layer}, end_layer={end_layer}")

    # Check and print the type and shape of input_data
    if start_layer != 0:
        print("Received intermediate input data. Converting to tensor if necessary.")
        if isinstance(input_data, list):
            print(f"Input data is a list with length {len(input_data)}. Converting to tensor.")
            input_data = tf.convert_to_tensor(input_data)
        else:
            print(f"Input data is already a tensor with shape {input_data.shape}")
    else:
        print("Received initial input data. Decoding from base64.")
        input_data = decode_image_from_base64(input_data)
        print(f"Decoded image to tensor with shape {input_data.shape}")

    # Perform inference from start_layer to end_layer
    for layer in range(start_layer, end_layer):
        input_data = model.layers[layer](input_data)
        print(f"After processing layer {layer}, data shape: {input_data.shape}")

    # Convert the result to a JSON serializable format
    if isinstance(input_data, tf.Tensor):
        print("Converting TensorFlow tensor to list for JSON serialization.")
        output = input_data.numpy().tolist()
    else:
        print("Output is not a TensorFlow tensor. Returning as is.")
        output = input_data

    print("Predict function completed.")
    return output


                    
# Function to get the model instance
model_instance = None

def getModel():
    global model_instance
    if model_instance is None:
        model_instance = DefoNet.build(108, 108, 3, 2)
    return model_instance

# print number of layers in model
model = getModel()
print("len model:", len(model.layers))

# from client_send.py for testing
def encode_image_to_base64(image_path):
    with Image.open(image_path) as image:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    

########### TESTING ###############
#test prediction
photo = ('/home/austin/Desktop/canary_jenna/canary3/client/defonet_test_DJI_0004_hw_0_0.jpg')
photo = encode_image_to_base64(photo)
pred = predict(getModel(), photo, 0 , 34)
pred = pred[0][1] 
pred = float(pred)
print(pred)
