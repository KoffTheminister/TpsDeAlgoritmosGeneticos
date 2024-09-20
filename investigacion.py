import cv2
import pandas as pd
import os, os.path
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
import tensorflow
import PIL
import PIL.Image
from pathlib import Path



vgg16 = tensorflow.keras.applications.VGG16(
    include_top=True,
    weights='imagenet',
    input_tensor=None,
    classes=1000,
    classifier_activation='softmax'
)

#model = vgg16(weights = 'imagenet', include_top = False, pooling = 'avg')


def extraer_features(imagen):

    # Cargar la imagen y redimensionarla
    img = Image.open(imagen)
    img = img.convert('RGB')  # Asegurarse de que la imagen esté en RGB
    img = img.resize((224, 224))  # Redimensionar para VGG16
    img_array = np.array(img)

    # Preprocesar la imagen
    img_array = tensorflow.keras.applications.vgg16.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)  # Añadir dimensión batch

    # Extraer características
    features = vgg16.predict(img_array)
    return features.flatten()

    '''  
    im_transformada = np.asarray(Image.open(imagen))
    im_transformada = cv2.cvtColor(im_transformada, cv2.COLOR_RGB2BGR)
    features = vgg16.predict(im_transformada)
    return features
    '''



dir_path = 'data/0'  # poner directorio donde estan las imagenes
features = []
for filesito in os.scandir(dir_path):
    aux = extraer_features(filesito)
    features.append(aux)

canmuestras = len(features)
df1 = pd.DataFrame(features)
classificatione = np.ones(canmuestras)
df1['Y'] = classificatione

dir_path = 'data/1'  # poner directorio donde estan las imagenes
features = []
for filesito in os.scandir(dir_path):
    aux = extraer_features(filesito)
    features.append(aux)


canmuestras = len(features)
df2 = pd.DataFrame(features)
classificatione = np.zeros(canmuestras)
df2['Y'] = classificatione
#print(df1.head)

df_final = pd.concat([df1, df2])
df_final = df_final.reset_index(inplace=True)

df_final.to_csv("df_final.csv")


'''1
dir_path2 = 'data/1'
for filesito2 in os.scandir(dir_path2):
    features.append(extraer_features(filesito2))

for i, feature in enumerate(features):
    print(f"Feature {i} shape: {feature.shape}")
'''



'''

print(tensorflow.__version__)
#my_df = pd.DataFrame(features, columns = )




#for c in list(Path('data/0').iterdir()):
#    if c.suffix != 'jpeg':
#        nuevo= c.with_suffix(".JPEG")
#        c.rename(nuevo)

#for c in list(Path('data/1').iterdir()):
#    if c.suffix != 'jpeg':
#        nuevo= c.with_suffix(".JPEG")
#        c.rename(nuevo)



batch_size = 32
img_height = 180
img_width = 180



model = keras.Sequential(
    [
        layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(2)
    ]
)


ds_train = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    labels="inferred",
    label_mode="int",  # categorical, binary
    class_names=['0', '1'],
    color_mode="rgb",
    batch_size=batch_size,
    image_size=(img_height, img_width),  # reshape if not in this size
    shuffle=True,
    seed=123,
    validation_split=0.1,
    subset="training",
)

ds_validation = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    labels="inferred",
    label_mode="int",  # categorical, binary
    class_names=['0', '1'],
    color_mode="rgb",
    batch_size=batch_size,
    image_size=(img_height, img_width),  # reshape if not in this size
    shuffle=True,
    seed=123,
    validation_split=0.1,
    subset="validation",
)

model.compile(
optimizer = keras.optimizers.Adam(),
    loss = [keras.losses.SparseCategoricalCrossentropy(from_logits=True),],
    metrics = ["accuracy"],
)

model.fit(ds_train, epochs=4, verbose=2)
'''
