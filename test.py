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
cant_generaciones = 2
tam_generacion = 20
min_TLUs_en_hidden_layers_adicionales = 35
max_TLUs_en_hidden_layers_adicionales = 70
num_epochs_original = 5
funcs_act = ['relu', 'tanh', 'softmax']
porcentaje_elitismo = 0.2
cant_elitismo = porcentaje_elitismo*tam_generacion/100
prob_crossover = 0.75
prob_mutacion = 0.05

def crear_generacion_inicial(tamano_generacion, funciones_de_activacion):
    generacion_inicial = []
    for i in range(tamano_generacion):
        model_i = Sequential()
        index_de_func_act = random.randint(0, 2)
        model_i.add(Dense(115, activation = funciones_de_activacion[index_de_func_act], input_shape = (1000,)))
        for j in range(3):
            model_i.add(Dense(70, activation = funciones_de_activacion[index_de_func_act]))
        model_i.add(Dense(1, activation = 'tanh')) # la output layer es la misma para todos los cromosomas. la funcion de activacion para esta capa NO cambia.
        model_i.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'], run_eagerly = True)
        generacion_inicial.append(model_i)
    return generacion_inicial


def ruleta_segun_rango(lista_de_orden):  # no pasamos la generacion, si no mas bien pasamos la orden_f1_score
    lista = []
    totsum = 0
    for l in range(int(len(lista_de_orden))):
        totsum += l + 1
    for l in range(int(len(lista_de_orden)*2)):
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

#gen_1 = crear_generacion_inicial(tam_generacion, funcs_act)

lista_de_co = ruleta_segun_rango([2,3,4,2,4,1,5,7,8,9])
print(lista_de_co)




