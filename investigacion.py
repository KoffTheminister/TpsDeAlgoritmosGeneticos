#imports
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

#variables
cant_generaciones = 15 # 50
tam_generacion = 20
num_epochs_original = 5
funcs_act = ['relu', 'leaky_relu', 'tanh', 'softmax']
porcentaje_elitismo = 10
cant_elitismo = porcentaje_elitismo*tam_generacion/100
prob_crossover = 0.5
prob_mutacion_l_r = 0.2
prob_mutacion_f_a = 0.05

#funciones de AG
def ruleta_segun_rango(lista_de_orden, cantidad_de_parejas):  # no pasamos la generacion, si no mas bien pasamos la orden_f1_score
    lista = []
    totsum = 0
    for l in range(int(len(lista_de_orden))):
        totsum += l + 1
    for l in range(int(cantidad_de_parejas*2)):
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

def crear_universo(cantidad_generaciones, tamano_generacion, funciones_de_activacion, numero_de_epochs, cantidad_elitismo):
    dataframe_preparado = pd.read_csv("dataframe_preparado.csv")
    del dataframe_preparado['Unnamed: 0']
    generacion = crear_generacion_inicial(tamano_generacion, funciones_de_activacion)
    len_df = int(len(dataframe_preparado.index))
    orden_f1_score = []
    auxiliar_para_los_elites = []
    valores_minimos = list()
    valores_maximos = list()
    ejex = list()
    cant_parejas_en_crossover = (tam_generacion - cant_elitismo)
    for i in range(cantidad_generaciones):
        valores_maximos_auxiliar = []
        ejex.append(i)
        print(len(generacion)) #esto
        for j in range(tamano_generacion):
            train_set, val_set, test_set = particionar_dataset(dataframe_preparado, len_df, int(round(len_df*70/100)), int(round(len_df*20/100)), 
                                                               int(round(len_df*10/100)))
            train_set_y, train_set_x = dividir_features_y_clasificacion(train_set)
            val_set_y, val_set_x = dividir_features_y_clasificacion(val_set)
            test_set_y, test_set_x = dividir_features_y_clasificacion(test_set)
            generacion[j].fit(train_set_x, train_set_y, epochs = numero_de_epochs, batch_size = 32)  # batch_size es estatico
            generacion[j].evaluate(val_set_x, val_set_y)
            print(j) #esto
            predicted_ys = generacion[i].predict(test_set_x) 
            len_predicted = round(len(predicted_ys)) 
            true_predictions = []
            for k in range(len_predicted):
                if(predicted_ys[k] < 0):
                    true_predictions.append(0)
                else:
                    true_predictions.append(1)
            resulted_f1_score = calcular_f1_score(test_set_y, true_predictions)
            orden_f1_score.append([j, resulted_f1_score])
            resulted_precision = calcular_precision(test_set_y, true_predictions)
            valores_maximos_auxiliar.append(resulted_precision)

        ordered_auxiliar = sorted(valores_maximos_auxiliar)
        valores_maximos.append(ordered_auxiliar[-1])
        valores_minimos.append(ordered_auxiliar[0])
        orden_f1_score = ordenar(orden_f1_score)
        pointer = round(tam_generacion - 1)
        k = 0
        auxiliar_para_los_elites.clear()
        while(k <= round(cantidad_elitismo - 1)):
            auxiliar_para_los_elites.append(generacion[orden_f1_score[pointer][0]]) #esto va SIN copy()
            #generacion.pop(orden_f1_score[pointer][0]) #esto
            #m = 0
            #for m in range(round(len(orden_f1_score))):
            #    if(orden_f1_score[pointer][0] < orden_f1_score[m][0]):
            #        orden_f1_score[m][0] -= 1 #esto
            #orden_f1_score.pop(pointer) #esto
            k += 1
            pointer -= 1
        lista_para_crossover = ruleta_segun_rango(orden_f1_score, cant_parejas_en_crossover)
        generacion_siguiente = []
        k = 0
        while(k <= (round(len(lista_para_crossover)) - 1)):
            aw = lista_para_crossover[k]
            bw = lista_para_crossover[k + 1]
            a_loc = orden_f1_score[aw][0]
            b_loc = orden_f1_score[bw][0]
            a = crossover_promedio(generacion[a_loc], generacion[b_loc])
            generacion_siguiente.append(a)
            k += 2
        k = 0
        for k in range(round(len(generacion_siguiente))):
           generacion_siguiente[k] = mutacion_learning_rate(generacion_siguiente[k])
        k = 0
        for k in range(round(len(generacion_siguiente))):
           generacion_siguiente[k] = mutacion_func_act(generacion_siguiente[k])
        k = 0
        for k in range(round(cantidad_elitismo)):
            generacion_siguiente.append(auxiliar_para_los_elites[k])
        generacion = generacion_siguiente.copy()
        k = 0
    graficas_exactitud(valores_minimos, valores_maximos, ejex)
    generacion[orden_f1_score[tam_generacion - 1][0]].save("mejormodelo")
    
def crossover_promedio(model_a, model_b):  
    if(random.random() <= prob_crossover and model_a != model_b): # si bien no estaria mal que sean iguales, se sabe que new_model sera igual a las otras dos asi que omitimos todo el calculo
        new_model = Sequential()
        for layer in model_a.layers:
            config = layer.get_config()
            new_model.add(Dense(**config))           
        for i, layer in enumerate(model_a.layers):
            weights1, biases1 = model_a.layers[i].get_weights()
            weights2, biases2 = model_b.layers[i].get_weights()
            summed_weights = np.add(weights1, weights2)
            summed_biases = np.add(biases1, biases2)
            new_model.layers[i].set_weights([summed_weights, summed_biases])
            a_o_b = random.randint(0,1)
            if (a_o_b < 0.5):
                func_act = model_a.layers[i].activation
            else:
                func_act = model_b.layers[i].activation
        new_model.compile(optimizer='adam', loss='mse')
        return new_model
    else:
        a_o_b = random.randint(0,1)
        if(a_o_b < 0.5):
            return model_a
        else:
            return model_b

def mutacion_learning_rate(un_modelo):
    if (prob_mutacion_l_r >= random.random()):
        new_learning_rate = np.random.uniform(0.0001, 0.01)
        un_modelo.compile(optimizer = Adam(learning_rate = new_learning_rate), loss='mse') 
        return un_modelo
    else:
        return un_modelo
    
def mutacion_func_act(un_modelo):
    for layer in range(4):
        if (prob_mutacion_f_a >= random.random()):
            nueva_activacion = np.random.choice(funcs_act)
            layer_configuracion = un_modelo.layers[layer].get_config()
            layer_configuracion['activation'] = nueva_activacion
            un_modelo.layers[layer] = Dense.from_config(layer_configuracion)
    return un_modelo
    
def ordenar(el_array):
    len_array = len(el_array)
    for i1 in range(len_array):
        for j1 in range(i1, len_array):
            if(el_array[i1][1] > el_array[j1][1]):
                el_array[j1], el_array[i1] = el_array[i1], el_array[j1]
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
    for i1 in range(longitud_train):
        j = random.randint(0, longitud_dataset - 1)
        item = dataset.iloc[j].to_frame().T
        df_train = pd.concat([df_train, item], ignore_index=True)
        dataset.drop(j, inplace=True)
        dataset.reset_index(inplace=True)
        del dataset["index"]
        longitud_dataset = longitud_dataset - 1
    for i1 in range(longitud_val):
        j = random.randint(0, longitud_dataset - 1)
        item = dataset.iloc[j].to_frame().T
        df_val = pd.concat([df_val, item], ignore_index=True)
        dataset.drop(j, inplace=True)
        dataset.reset_index(inplace=True)
        del dataset["index"]
        longitud_dataset = longitud_dataset - 1
    for i1 in range(longitud_test):
        if (longitud_dataset > 1):
            j = random.randint(0, longitud_dataset - 1)
            item = dataset.iloc[j].to_frame().T
            df_test = pd.concat([df_test, item], ignore_index=True)
            dataset.drop(j, inplace=True)
            dataset.reset_index(inplace=True)
            del dataset["index"]
            longitud_dataset = longitud_dataset - 1
        elif (longitud_dataset == 1):
            item = dataset.iloc[0].to_frame().T
            df_test = pd.concat([df_test, item], ignore_index=True)
            dataset.drop(0, inplace=True)
            dataset.reset_index(inplace=True)
            del dataset["index"]
            longitud_dataset = longitud_dataset - 1
    return df_train, df_val, df_test

def calcular_f1_score(y_verdaderas, y_predicciones):
    conf_matrix = [[0, 0], [0, 0]]
    for i1 in range(int(len(y_verdaderas))):
        if(y_verdaderas.iloc[i1].loc['Y'] == 1):
            if(y_verdaderas.iloc[i1].loc['Y'] == y_predicciones[i1]):
                conf_matrix[0][0] += 1
            else:
                conf_matrix[0][1] += 1
        else:
            if(y_verdaderas.iloc[i1].loc['Y'] == y_predicciones[i1]):
                conf_matrix[1][1] += 1
            else:
                conf_matrix[1][0] += 1   
    if(conf_matrix[0][0] != 0 or conf_matrix[0][1] != 0):
        precision = (conf_matrix[0][0])/(conf_matrix[0][0] + conf_matrix[0][1])
    else:
        precision = 0
    if(conf_matrix[0][0] != 0 or conf_matrix[1][0] != 0):
        exhaustion = (conf_matrix[0][0])/(conf_matrix[0][0] + conf_matrix[1][0])
    else:
        exhaustion = 0
    if(precision != 0 and exhaustion != 0):
        f1_score = (2*precision*exhaustion)/(precision + exhaustion)
    else:
        f1_score = 0 
    return f1_score

def calcular_precision(y_verdaderas, y_predicciones):
    conf_matrix = [[0, 0], [0, 0]]
    for i1 in range(int(len(y_verdaderas))):
        if(y_verdaderas.iloc[i1].loc['Y'] == 1):
            if(y_verdaderas.iloc[i1].loc['Y'] == y_predicciones[i1]):
                conf_matrix[0][0] += 1
            else:
                conf_matrix[0][1] += 1
        else:
            if(y_verdaderas.iloc[i1].loc['Y'] == y_predicciones[i1]):
                conf_matrix[1][1] += 1
            else:
                conf_matrix[1][0] += 1   
    if(conf_matrix[0][0] != 0 or conf_matrix[0][1] != 0):
        precision = (conf_matrix[0][0])/(conf_matrix[0][0] + conf_matrix[0][1])
    else:
        precision = 0
    return precision


def graficas_exactitud(valores_minimos, valores_maximos, ejex):
    numeros = int(tam_generacion/10)

    fig, axs = plt.subplots(1, 2, figsize = (8, 4))

    fig.suptitle('Estadísticas Finales de las Exactitudes', fontsize = 16)
    
    # Primer gráfico: Valores mínimos
    axs[0].plot(ejex, valores_minimos, 'b')
    axs[0].set_title('Exactitud Mínima')
    axs[0].set_xlabel('Corrida')
    axs[0].set_ylabel('Exactitud')
    axs[0].set_xlim(0, tam_generacion - 1)
    axs[0].set_ylim(0, 1)
    axs[0].set_xticks(range(0, tam_generacion + 1, numeros))
    axs[0].set_yticks([i / 10 for i in range(0, 12)])
    axs[0].legend(loc='best')

    # Segundo gráfico: Valores máximos
    axs[1].plot(ejex, valores_maximos, 'r')
    axs[1].set_title('Exactitud Máxima')
    axs[1].set_xlabel('Corrida')
    axs[1].set_ylabel('Exactitud')
    axs[1].set_xlim(0, tam_generacion - 1)
    axs[1].set_ylim(0, 1)
    axs[1].set_xticks(range(0, tam_generacion + 1, numeros))
    axs[1].set_yticks([i / 10 for i in range(0, 12)])
    axs[1].legend(loc='best')

    # # Tercer gráfico: Valores promedio
    # axs[2].plot(ejex, valores_promedios, 'g')
    # axs[2].set_title('Exactitud Promedio')
    # axs[2].set_xlabel('Corrida')
    # axs[2].set_ylabel('Exactitud')
    # axs[2].set_xlim(0, tam_generacion - 1)
    # axs[2].set_ylim(0, 1)
    # axs[2].set_xticks(range(0, tam_generacion + 1, numeros))
    # axs[2].set_yticks([i / 10 for i in range(0, 12)])
    # axs[2].legend(loc='best')

    plt.tight_layout()
    plt.show()



crear_universo(cant_generaciones, tam_generacion, funcs_act, num_epochs_original, cant_elitismo)
