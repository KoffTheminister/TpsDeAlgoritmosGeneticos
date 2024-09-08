#imports
import pandas as pd
import os, os.path
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import PIL
import PIL.Image
from pathlib import Path
import random

#variables
cant_generaciones = 50
tam_generacion = 20
min_TLUs_en_hidden_layers_adicionales = 35
max_TLUs_en_hidden_layers_adicionales = 70
num_epochs_original = 5
funcs_act = ['relu', 'tanh', 'softmax']
porcentaje_elitismo = 0.2
cant_elitismo = porcentaje_elitismo*tam_generacion/100
prob_crossover = 0.75
prob_mutacion = 0.05


#funciones de AG
def ruleta_segun_rango(lista_de_orden):  # no pasamos la generacion, si no mas bien pasamos la orden_f1_score
    lista = []
    totsum = 0
    for k in range(len(lista_de_orden)):
        totsum += k + 1
    for j in range(int(len(lista_de_orden)/2)):
        for i in range(2):
            totRuleta = 0
            flecha = random.random()*100
            index = 0
            condicion = True
            while(condicion):
                totRuleta += ((index + 1)/totsum)*100
                if(totRuleta >= flecha):
                    lista.append(index)
                    condicion = False
                else:
                    index += 1
    return lista

def crear_generacion_inicial(tamano_generacion, funciones_de_activacion, minimo_TLUs_en_hidden_layers_adicionales, maximo_TLUs_en_hidden_layers_adicionales):
    generacion_inicial = []
    
    for i in range(tamano_generacion):
        model_i = Sequential()
        index_de_func_act = random.randint(0, 2)
        cant_TLUs_de_primera_hidden_layer = random.randint(100, 130)
        model_i.add(Dense(cant_TLUs_de_primera_hidden_layer, activation = funciones_de_activacion[index_de_func_act], input_shape = (1000,)))   
        cant_adicional_de_hidden_layers = random.randint(2,3)
        cant_TLUs_de_hidden_layer_anterior = 71

        for j in range(cant_adicional_de_hidden_layers):
            cant_TLUs_de_hidden_layer = random.randint(minimo_TLUs_en_hidden_layers_adicionales, maximo_TLUs_en_hidden_layers_adicionales)

            while(cant_TLUs_de_hidden_layer_anterior < cant_TLUs_de_hidden_layer):
                cant_TLUs_de_hidden_layer = random.randint(minimo_TLUs_en_hidden_layers_adicionales, maximo_TLUs_en_hidden_layers_adicionales)
            cant_TLUs_de_hidden_layer_anterior = cant_TLUs_de_hidden_layer
            index_de_func_act = random.randint(0, 2)
            model_i.add(Dense(cant_TLUs_de_hidden_layer, activation = funciones_de_activacion[index_de_func_act]))
       
        model_i.add(Dense(1, activation = 'tanh')) # la output layer es la misma para todos los cromosomas. la funcion de activacion para esta capa NO cambia.
        generacion_inicial.append(model_i)
  
    return generacion_inicial

def crear_universo(cantidad_generaciones, tamano_generacion, funciones_de_activacion, minimo_TLUs_en_hidden_layers_adicionales, 
                   maximo_TLUs_en_hidden_layers_adicionales, numero_de_epochs, cantidad_elitismo):
    dataframe_preparado = pd.read_csv("dataframe_preparado.csv")
    del dataframe_preparado['Unnamed: 0']
    generacion = crear_generacion_inicial(tamano_generacion, funciones_de_activacion, minimo_TLUs_en_hidden_layers_adicionales, 
                                          maximo_TLUs_en_hidden_layers_adicionales)
    len_df = int(len(dataframe_preparado.index))
    orden_f1_score = []
    auxiliar = []
    cant_de_crossovers = int((tamano_generacion - cantidad_elitismo)/2)
    for i in range(cantidad_generaciones):
        for j in range(tamano_generacion):
            generacion[i].compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'], run_eagerly = True)
            train_set, val_set, test_set = particionar_dataset(dataframe_preparado, len_df, int(round(len_df*70/100)), int(round(len_df*20/100)), 
                                                               int(round(len_df*10/100)))
            train_set_y, train_set_x = dividir_features_y_clasificacion(train_set)
            generacion[i].fit(train_set_x, train_set_y, epochs = 5, batch_size = 32) # el batch size es estatico '''numero_de_epochs'''
            test_set_y, test_set_x = dividir_features_y_clasificacion(test_set)
            predicted_ys = generacion[i].predict(test_set_x)

            len_predicted = round(len(predicted_ys)) # reevaluar desde aca
            true_predictions = []
            for k in range(len_predicted):
                if(predicted_ys[k] < 0):
                    true_predictions.append(0)
                else:
                    true_predictions.append(1) # hasta aca

            resulted_f1_score = calcular_f1_score(test_set_y, true_predictions)
            orden_f1_score.append([i, resulted_f1_score])
        orden_f1_score = ordenar(orden_f1_score)
        auxiliar.clear()
        for k in range(round(cantidad_elitismo)):
            auxiliar.append(generacion[orden_f1_score[k][0]].copy())
            generacion.pop(orden_f1_score[k][0])
            orden_f1_score.pop(k)
        k = 0
        lista_para_crossover = ruleta_segun_rango(orden_f1_score)
        while(k <= cant_de_crossovers):
            model_a, model_b = crossover_mitad_mitad(orden_f1_score[lista_para_crossover[k]], orden_f1_score[lista_para_crossover[k + 1]])
            k += 2
        

        


def crossover_mitad_mitad(model_a, model_b):
    new_model_a = Sequential()
    new_model_b = Sequential()

    # Generar puntos de corte para ambos modelos
    corte_a = random.randint(1, len(model_a.layers) - 2)  # Evitar la capa de entrada y salida
    corte_b = random.randint(1, len(model_b.layers) - 2)  # Evitar la capa de entrada y salida

    # Hijo 1: primeras capas de model_b hasta el punto de corte_b, luego capas de model_a
    for i in range(corte_b):
        capa = model_b.layers[i]
        new_model_a.add(capa)

    for i in range(corte_a, len(model_a.layers) - 1):
        capa = model_a.layers[i]
        new_model_a.add(capa)

    # Hijo 2: primeras capas de model_a hasta el punto de corte_a, luego capas de model_b
    for i in range(corte_a):
        capa = model_a.layers[i]
        new_model_b.add(capa)

    for i in range(corte_b, len(model_b.layers) - 1):
        capa = model_b.layers[i]
        new_model_b.add(capa)

    # Añadir la capa de salida de model_a a new_model_a
    output_layer_a = model_a.layers[-1]
    new_model_a.add(output_layer_a)

    # Añadir la capa de salida de model_b a new_model_b
    output_layer_b = model_b.layers[-1]
    new_model_b.add(output_layer_b)

    return new_model_a, new_model_b


def mutacion():
    new_model = Sequential()
    if (prob_mutacion >= random.random()):
        corte = random.randint(1, len(new_model.layers) - 2)
        

    return new_model


def ordenar(el_array):
    len_array = len(el_array)
    for i in range(len_array):
        for j in range(i, len_array):
            if(el_array[i][1] < el_array[j][1]):
                el_array[j], el_array[i] = el_array[i], el_array[j]
    return el_array


#funciones de la NN
def dividir_features_y_clasificacion(df):
    set_y = df[['Y']].copy()
    set_x = df.drop(['Y'], axis = 1)  
    return set_y, set_x

def particionar_dataset(original_dataset, longitud_dataset, longitud_train, longitud_val, longitud_test):
    dataset = original_dataset.copy()
    df_train = pd.DataFrame(columns = dataset.columns)
    df_val = pd.DataFrame(columns = dataset.columns)
    df_test = pd.DataFrame(columns = dataset.columns)
    for i in range(longitud_train):
        j = random.randint(0, longitud_dataset - 1)
        item = dataset.iloc[j].to_frame().T
        df_train = pd.concat([df_train, item], ignore_index=True)
        dataset.drop(j, inplace=True)
        dataset.reset_index(inplace=True)
        del dataset["index"]
        longitud_dataset = longitud_dataset - 1
    for i in range(longitud_val):
        j = random.randint(0, longitud_dataset - 1)
        item = dataset.iloc[j].to_frame().T
        df_val = pd.concat([df_val, item], ignore_index=True)
        dataset.drop(j, inplace=True)
        dataset.reset_index(inplace=True)
        del dataset["index"]
        longitud_dataset = longitud_dataset - 1
    for i in range(longitud_test):
        if longitud_dataset > 1:
            j = random.randint(0, longitud_dataset - 1)
            item = dataset.iloc[j].to_frame().T
            df_test = pd.concat([df_test, item], ignore_index=True)
            dataset.drop(j, inplace=True)
            dataset.reset_index(inplace=True)
            del dataset["index"]
            longitud_dataset = longitud_dataset - 1

        elif longitud_dataset == 1 :
            item = dataset.iloc[0].to_frame().T
            df_test = pd.concat([df_test, item], ignore_index=True)
            dataset.drop(0, inplace=True)
            dataset.reset_index(inplace=True)
            del dataset["index"]
            longitud_dataset = longitud_dataset - 1

    return df_train, df_val, df_test

def calcular_f1_score(y_verdaderas, y_predicciones):
    conf_matrix = [[0, 0], [0, 0]]
    for i in range(int(len(y_verdaderas))):
        if(y_verdaderas.iloc[i].loc['Y'] == 1):
            if(y_verdaderas.iloc[i].loc['Y'] == y_predicciones[i]):
                conf_matrix[0][0] += 1
            else:
                conf_matrix[0][1] += 1
        else:
            if(y_verdaderas.iloc[i].loc['Y'] == y_predicciones[i]):
                conf_matrix[1][1] += 1
            else:
                conf_matrix[1][0] += 1   
    print(conf_matrix)
    if(conf_matrix[0][0] != 0 and conf_matrix[0][1] != 0):
        precision = (conf_matrix[0][0])/(conf_matrix[0][0] + conf_matrix[0][1])
    else:
        precision = 0
    if(conf_matrix[0][0] != 0 and conf_matrix[1][0] != 0):
        exhaustion = (conf_matrix[0][0])/(conf_matrix[0][0] + conf_matrix[1][0])
    else:
        exhaustion = 0
    if(precision != 0 and exhaustion != 0):
        f1_score = (2*precision*exhaustion)/(precision + exhaustion)
    else:
        f1_score = 0
    
    return f1_score

crear_universo(cant_generaciones, tam_generacion, funcs_act, min_TLUs_en_hidden_layers_adicionales, 
               max_TLUs_en_hidden_layers_adicionales, num_epochs_original, cant_elitismo)