#imports

import pandas as pd
import os, os.path
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
import tensorflow
import PIL
import PIL.Image
from pathlib import Path
import random
from sklearn.preprocessing import RobustScaler

vgg16 = tensorflow.keras.applications.VGG16(
    include_top=True,
    weights='imagenet',
    input_tensor=None,
    classes=1000,
    classifier_activation='softmax'
)

a_robust_scaler = RobustScaler()

def particionar_dataset(dataset, longitud_dataset, longitud_train, longitud_val, longitud_test):
    df_train = pd.DataFrame(columns = dataset.columns)
    df_val = pd.DataFrame(columns = dataset.columns)
    df_test = pd.DataFrame(columns = dataset.columns)
    for i in range(longitud_train):
        j = random.randint(0, longitud_dataset - 1)
        item = dataset.iloc[j].copy()
        pd.concat([df_train,item])
        dataset.drop([j], axis=0, inplace=True)
        dataset = dataset.reset_index(drop=True)
        longitud_dataset = longitud_dataset - 1

    for i in range(longitud_val):
        j = random.randint(0, longitud_dataset - 1)
        item = dataset.iloc[j].copy()
        pd.concat([df_val,item])
        dataset.drop([j], axis=0, inplace=True)
        dataset = dataset.reset_index(drop=True)
        longitud_dataset = longitud_dataset - 1
    for i in range(longitud_test):
        print(longitud_dataset)
        if longitud_dataset > 1:
            j = random.randint(0, longitud_dataset - 1)
            item = dataset.iloc[j].copy()
            pd.concat([df_test,item])
            dataset.drop([j], axis=0, inplace=True)
            dataset = dataset.reset_index(drop=True)
            longitud_dataset = longitud_dataset - 1
        elif longitud_dataset == 1 :
            item = dataset.iloc[0].copy()
            pd.concat([df_test,item])
            dataset.drop([0], axis=0, inplace=True)
            dataset = dataset.reset_index(drop=True)
            longitud_dataset = longitud_dataset - 1
    return df_train, df_val, df_test

def calcular_f1_score(y_verdaderas, y_predicciones):
    conf_matrix = [[0, 0], [0, 0]]
    for i in range(int(len(y_verdaderas))):
        if(y_verdaderas[i] == 1):
            if(y_verdaderas == y_predicciones):
                conf_matrix[0][0] += 1
            else:
                conf_matrix[0][1] += 1
        else:
            if(y_verdaderas == y_predicciones):
                conf_matrix[1][1] += 1
            else:
                conf_matrix[1][0] += 1     
    precision = (conf_matrix[0][0])/(conf_matrix[0][0] + conf_matrix[0][1])
    exhaustion = (conf_matrix[0][0])/(conf_matrix[0][0] + conf_matrix[1][0])
    f1_score = (2*precision*exhaustion)/(precision + exhaustion)
    return f1_score

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

dir_path = 'data/0'  # poner directorio donde estan las imagenes
features = []
for filesito in os.scandir(dir_path):
    aux = extraer_features(filesito)
    features.append(aux)

features = a_robust_scaler.fit_transform(features)
canmuestras = len(features)
df1 = pd.DataFrame(features)
classificatione = np.ones(canmuestras)
df1['Y'] = classificatione


dir_path = 'data/1'  # poner directorio donde estan las imagenes
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

len_df = len(df_final.index)
train_length = int(round(len_df*70/100))
val_length = int(round(len_df*20/100))
test_length = int(round(len_df*10/100))
df_train, df_val, df_test = particionar_dataset(df_final, len_df, train_length, val_length, test_length)

#print(df_train)

#df_final.to_csv("df_final.csv")


