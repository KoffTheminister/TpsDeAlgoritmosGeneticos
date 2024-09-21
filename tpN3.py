'''
El objetivo es encontrar una ruta que, comenzando y terminando en una ciudad concreta, pase una sola vez por cada una de las ciudades y minimice la distancia recorrida por el viajante.


Ejercicios:

1.Hallar la ruta de distancia mínima que logre unir todas las capitales de provincias de la República Argentina, utilizando un método exhaustivo. ¿Puede resolver el problema? Justificar de manera teórica.
2.Realizar un programa que cuente con un menú con las siguientes opciones:
a)Permitir ingresar una provincia y hallar la ruta de distancia mínima que logre unir todas las capitales de provincias de la República Argentina partiendo de dicha capital utilizando la siguiente heurística: “Desde cada ciudad
ir a la ciudad más cercana no visitada.”  Recordar regresar siempre a la ciudad de partida. Presentar un mapa de la República con el recorrido indicado. Además 
indicar la ciudad de partida, el recorrido completo y la longitud del trayecto. El programa deberá permitir seleccionar la capital que el usuario desee ingresar como inicio del recorrido.
b)Encontrar el recorrido mínimo para visitar todas las capitales de las provincias de la República Argentina siguiendo la heurística mencionada en el punto a. Deberá mostrar como salida el recorrido y la longitud del trayecto.
c)Hallar la ruta de distancia mínima que logre unir todas las capitales de provincias de la República Argentina, utilizando un algoritmo genético.


Recomendaciones para el algoritmo:

N = 50 Número de cromosomas de las poblaciones.

M = 200 Cantidad de ciclos.

Cromosomas: permutaciones de 23 números naturales del 1 al 23 donde cada gen es una ciudad.

Las frecuencias de crossover y de mutación quedan a criterio del grupo.

Se deberá usar crossover cíclico.

Comparar los resultados obtenidos  entre la resolución a través de heurísticas y con algoritmos genéticos a través de una conclusión que deberá anexarse al informe.
'''
#array de distancias por rutas y caminos
argentina = [[None, 715, 940, 1191, 61, 1150, 1050, 1158, 480, 1040, 1455, 1023, 2635, 1155, 1203, 1510, 1110, 790, 1543, 478, 620, 1043, 3228, 960], 
             [715, None, 898, 1043, 757, 435, 670, 1137, 361, 1213, 1455, 875, 3635, 440, 590, 879, 500, 420, 930, 330, 600, 430, 3228, 1194],
             [940, 898, None, 191, 978, 993, 1565, 1989, 590, 315, 2187, 23, 3367, 845, 791, 803, 1398, 1318, 883, 568, 1378, 633, 3960, 2046], 
             [1191, 1043, 191, None, 1253, 1136, 1710, 2060, 744, 506, 2378, 168, 3558, 988, 936, 948, 1543, 1463, 960, 713, 1523, 776, 4151, 2117], 
             [61, 757, 978, 1253, None, 1189, 1152, 1197, 555, 1061, 1414, 996, 2551, 1188, 1309, 1614, 1213, 894, 1645, 527, 670, 1184, 3132, 957], 
             [1150, 435, 993, 1136, 1189, None, 617, 1472, 796, 1308, 1890, 970, 3070, 156, 388, 695, 450, 550, 770, 765, 1035, 360, 3663, 1629], 
             [1050, 670, 1565, 1710, 1152, 617, None, 855, 916, 1925, 1620, 1587, 2800, 773, 1005, 1227, 167, 260, 1345, 885, 765, 977, 3393, 1359], 
             [1158, 1137, 1989, 2060, 1197, 1472, 855, None, 1378, 2198, 750, 2012, 1930, 1588, 1860, 2082, 1022, 883, 2200, 1347, 537, 1567, 2523, 660], 
             [480, 361, 590, 744, 555, 796, 916, 1378, None, 820, 1696, 576, 2876, 801, 798, 1105, 861, 656, 1138, 31, 841, 638, 3469, 1435], 
             [1040, 1213, 315, 506, 1061, 1308, 1925, 2198, 820, None, 2495, 338, 3675, 1160, 1106, 1118, 1758, 1633, 1198, 833, 1660, 948, 4298, 2000], 
             [1455, 1455, 2187, 2378, 1414, 1890, 1620, 750, 1696, 2495, None, 2210, 1180, 1895, 2045, 2352, 1680, 1360, 2385, 1665, 855, 1885, 1773, 495], 
             [1023, 875, 23, 168, 996, 970, 1587, 2012, 576, 338, 2210, None, 3390, 822, 765, 780, 1420, 1295, 860, 545, 1475, 610, 3983, 2069], 
             [2635, 2635, 3367, 3558, 2551, 3070, 2800, 1930, 2876, 3675, 1180, 3390, None, 3075, 3225, 3532, 2860, 2540, 3536, 2845, 2035, 3065, 593, 1675], 
             [1145, 440, 845, 988, 1188, 156, 773, 1588, 801, 1160, 1895, 822, 3075, None, 232, 593, 606, 705, 572, 770, 1040, 212, 3668, 1634], 
             [1203, 590, 791, 936, 1309, 338, 1005, 1860, 798, 1106, 2045, 768, 3225, 232, None, 307, 838, 938, 340, 767, 1190, 160, 3818, 1784], 
             [1510, 897, 803, 948, 1614, 695, 1227, 2082, 1105, 1118, 2352, 780, 3532, 539, 307, None, 1145, 1245, 99, 1074, 1497, 467, 4125, 2091], 
             [1110, 500, 1398, 1543, 1213, 450, 167, 1022, 861, 1758, 1680, 1420, 2860, 606, 838, 1145, None, 320, 1220, 830, 825, 810, 3453, 1419], 
             [790, 420, 1318, 1463, 894, 550, 260, 883, 656, 1633, 1360, 1295, 2540, 705, 938, 1245, 320, None, 1320, 625, 505, 850, 3133, 1099], 
             [1543, 930, 883, 960, 1645, 770, 1345, 220, 1138, 1198, 2385, 860, 3565, 572, 340, 99, 120, 1320, None, 1107, 1530, 500, 4158, 2124], 
             [478, 330, 568, 713, 527, 765, 885, 1347, 31, 883, 1665, 545, 2845, 770, 767, 1074, 830, 625, 1107, None, 810, 607, 3438, 1404], 
             [620, 600, 1378, 1523, 670, 1035, 765, 885, 1347, 31, 883, 1665, 545, 2845, 770, 767, 1074, 830, 625, 1107, None, 1030, 2628, 594], 
             [1043, 430, 633, 776, 1184, 360, 977, 1567, 638, 948, 1885, 610, 3065, 212, 160, 467, 810, 850, 500, 607, 1030, None, 3658, 1624], 
             [3228, 3228, 3960, 4151, 3132, 3660, 3393, 2523, 3469, 4268, 1773, 3983, 593, 3668, 3818, 4125, 3453, 3133, 4158, 3438, 2628, 3658, None, 2268],
             [960, 1194, 2046, 2117, 957, 1629, 1359, 660, 1435, 2000, 495, 2069, 1675, 1634, 1784, 2091, 1419, 1099, 2124, 1404, 594, 1624, 2268, None]]


#librerias
import random
import matplotlib
import matplotlib.pyplot as plt

#parametros
ciclos = 200  #20 o 100 o 200
tamanio_poblacion = 50
# prob_crossover = 0.75
# prob_mutacion = 0.05
# tam_torneo = 2 #cambiar a porcentaje
# porcentaje_elitismo = 20 #porciento
# cant_elite = porcentaje_elitismo*tamanio_poblacion/100

# [[24 ciudades], distancia]

def calcular_distancia(ruta):
    for camino in range(23): 
        ruta[1] += argentina[ruta[0][camino]][ruta[0][camino + 1]]

def calcular_distancia_con_comienzo(ruta, ciudad_comienzo):
    ruta[1] += argentina[ciudad_comienzo][ruta[0][0]]
    for camino in range(22): 
        ruta[1] += argentina[ruta[0][camino]][ruta[0][camino + 1]]
    ruta[1] += argentina[ruta[0][22]][ciudad_comienzo]

def calcular_distancia_heuristica(ruta):
    cont = 0
    for camino in range(24):
        print(ruta[camino],' y', ruta[camino + 1])
        cont += argentina[ruta[camino]][ruta[camino + 1]]
    return cont

def calcular_total(generacion, tam_gen):
    tot = 0
    for c in range(tam_gen):
        tot += generacion[c][1]
    return tot

def verificar_repeticion_ciudad(ruta, ciudad):
    repeticion = False
    tam = len(ruta) - 1
    index = 0
    while(repeticion == False and index <= tam):
        if(ruta[index] == ciudad):
            repeticion = True
        else:
            index += 1
    return repeticion

def verificar_repeticion_ruta(rutas, posible_ruta):
    repeticion = False
    tam = len(rutas) - 1
    index = 0
    while(repeticion == False and index <= tam):
        if(rutas[index] == posible_ruta):
            repeticion = True
        else:
            index += 1
    return repeticion

def ordenar(generacion, tam_gen):
    for m in range(tam_gen):
        for n in range(m, tam_gen):
            if(generacion[m][1] > generacion[n][1]): # menor a mayor
                generacion[m], generacion[n] = generacion[n], generacion[m]

def exhaustiva_1():
    min = [[], 1000000]
    rutas = []
    for ruta in range(16777216):
        print(ruta)
        entro = False
        while(entro == False):
            posibles_ciudades = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
            len = 23
            una_ruta = [[], 0]
            paso = 0
            while(paso <= 23): #lo bajamos a 22 por que el primer elemento ya esta ocupado
                posible_ciudad_indice = random.randint(0,len)
                una_ruta[0].append(posibles_ciudades[posible_ciudad_indice])
                del posibles_ciudades[posible_ciudad_indice]
                len -= 1
                paso += 1
            if(verificar_repeticion_ruta(rutas, una_ruta) == True):
                una_ruta[0] = []
            else:
                #calcular_distancia_con_comienzo(una_ruta, ciudad_inicial)
                calcular_distancia(una_ruta)
                if(min[1] > una_ruta[1]):
                    min = una_ruta
                rutas.append(una_ruta)
                entro = True
    return min

def exhaustiva_2():
    for ruta in range(23):
        raiz = [ruta]
        funcion_recursiva(raiz,ruta)

def heuristica(ciudad_inicial):
    ruta = [ciudad_inicial]
    posibles_ciudades = []
    for k in range(24):
        if(k != ciudad_inicial):
            posibles_ciudades.append(k)
    index = 0
    posicion_actual = ciudad_inicial
    while(index <= 22):
        min = 10000
        min_i = None
        i = 0
        for i in range(len(posibles_ciudades)):
            if(argentina[posicion_actual][posibles_ciudades[i]] < min):
                min = argentina[posicion_actual][posibles_ciudades[i]]
                min_i = i
        ruta.append(posibles_ciudades[min_i])
        posicion_actual = posibles_ciudades[min_i]
        del posibles_ciudades[min_i]
        index += 1
    ruta.append(ciudad_inicial)
    return ruta



print(exhaustiva(1))

















