#imports
import pandas as pd
import os, os.path
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
import tensorflow
from sklearn.preprocessing import RobustScaler

vgg16 = tensorflow.keras.applications.VGG16(
    include_top = True,
    weights = 'imagenet',
    input_tensor = None,
    classes = 1000,
    classifier_activation = 'softmax'
)

a_robust_scaler = RobustScaler()

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


dir_path = '/home/tenet7750/Desktop/vsc/tpsAG/ims_sin_quemaduras/ims_sin_quemaduras'  # poner directorio donde estan las imagenes
features = []
for filesito in os.scandir(dir_path):
    aux = extraer_features(filesito)
    features.append(aux)

features = a_robust_scaler.fit_transform(features)
canmuestras = len(features)
df1 = pd.DataFrame(features)
classificatione = np.ones(canmuestras)
df1['Y'] = classificatione

dir_path = '/home/tenet7750/Desktop/vsc/tpsAG/ims_con_quemaduras/ims_con_quemaduras'  # poner directorio donde estan las imagenes
features = []
for filesito in os.scandir(dir_path):
    aux = extraer_features(filesito)
    features.append(aux)

features = a_robust_scaler.fit_transform(features)
canmuestras = len(features)
df2 = pd.DataFrame(features)
classificatione = np.zeros(canmuestras)
df2['Y'] = classificatione

df_final = pd.concat([df1, df2])
df_final = df_final.reset_index(drop=True)

print(df_final)

df_final.to_csv("dataframe_preparado.csv")




