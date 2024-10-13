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
argentina = [[None,	646	,792,	933,53	,986,	985	,989	,375	,834,	1127,	794,	2082,	979,	1080,	1334	,1282,	1005,	749,	393,	579,	939	,2373,	799], 
             [646,	None	,677	,824,	698,	340,	466,	907,	348	,919,	1321,	669	,2281	,362,	517	,809,	745,	412	,293,	330	,577	,401,	2618	,1047],
             [792,	677,	None,	157,	830,	814,	1131,	1534	,500	,291,	1845,	13	,2819	,691,	633,	742,	719,	1039	,969,	498	,1136,	535,	3131,	1527], #Aca llegue
             [933,	824,	157,	None,	968,	927,	1269,	1690	,656	,263	,1999	,161,	2974,	793,	703,	750	,741	,1169	,1117	,654	,1293,	629,	3284,	1681],  
             [53,	698,	830,	968	,None,	1038,	1029,	1005	,427,	857	,1116	,833,	2064,	1030,	1132,	1385,	1333,	1053,	795,	444,	602	,991	,2350	,789],  
             [986,	340,	814,	927	,1038	,None,	427,	1063,	659,	1098,	1548,	802,	2473,	149,	330,	600,	533	,283,	435,	640,	834,	311,	2821,	1311], 
             [985,	466	,1131,	1269	,1029,	427	,None,	676,	790,	1384,	1201	,1121	,2081,	569	,756,	1023,	957	,152	,235,	775,	586,	713	,2435,	1019],  
             [989,	907,	1534,	1690,	1005,	1063,	676,	None	,1053	,1709	,543,	1529,	1410,	1182	,1370	,1658	,1591	,824,	643,	1049	,422,	1286,	1762,	479],  
             [375,	348,	500,	656	,427,	659,	790,	1053,	None,	658,	1345,	498	,2320	,622	,707,	959	,906,	757	,574	,19	,642,	566,	2635,	1030], 
             [834,	919,	291,	263,	857,	1098	,1384	,1709	,658	,None	,1951	,305	,2914	,980	,924	,1007,	992	,1306	,1200	,664	,1293	,827,	3207	,1624], 
             [1127,	1321,	1845,	1999	,1116	,1548	,1201	,543,	1345,	1951,	None,	1843,	975,	1647,	1827,	2120,2054,	1340,	1113,	1349,	745	,1721,	1300,	327],   
             [794,	669,	13	,161	,833	,802	,1121	,1529,	498,	305,	1843,	None,	2818,	678,	620,	729,	706,	1029	,961	,495	,1132	,523,	3130,	1526], 
             [2082,	2281,	2819,	2974,	2064,	2473,	2081,	1410,	2320,	2914,	975,	2818,	None	,2587,	2773,	3063,	2997,	2231,	2046,	2325,	1712,	2677	,359,	1294], 
             [979,	362,	691,	793,	1030,	149	,569,	1182,	622	,980,	1647,	678,	2587,	None,	189,	477	,410	,430	,540	,602	,915	,166,	2931,	1391], 
             [1080,	517,	633	,703	,1132	,330	,756	,1370,	707	,924,	1827,	620,	2773,	189	,None	,293	,228	,612	,727,	689,	1088,	141,	3116,	1562], 
             [1334,	809,	742	,750	,1385	,600	,1023	,1658	,959,	1007,	2120,	729,	3063,	477,	293,	None,	67,	874,	1017,	942,	1382,	414,	3408,	1855], 
             [1282,	745,	719,	741,	1333,	533,	957,	1591,	906,	992,	2054,	706,	2997,	410,	228	,67,	None	,808	,950	,889	,1316,	353,	3341,	1790], 
             [1005,	412,	1039,	1169,	1053,	283,	152,	824,	757,	1306,	1340,	1029,	2231,	430,	612,	874,	808,	None,	284,	740,	686,	583	,2585	,1141], 
             [749,	293,969,1117,795,435,	235,643,574,	1200,	1113,	961,	2046,	540,	727,	1017,	950,	284,	None,	560,	412	,643,	2392,	882],  
             [393,	330,	498,	654	,444,	640,	775	,1049	,19,	664,	1349,	495	,2325,	602,	689,	942,	889,	740,	560,	None,	641,	547	,2641,	1035],   
             [579,	577	,1136	,1293,	602,	834,	586,	422,	642,	1293	,745,	1132,	1712,	915,1088,1382,	1316,686,412,641,None,977,2044,477],  
             [939,	401,	535,	629	,991	,311,	713	,1286	,566	,827	,1721	,523,	2677,	166	,141,	414,	353,	583	,643,	547	,977	,None	,3016	,1446], 
             [2373,2618,3131,3284,2350,2821,2435,1762,	2635,3207,	1300,3130,359,2931,	3116,3408,3341,	2585	,2392	,2641,	2044,	3016	,None,	1605], 
             [799,1047,1527,1681,789,1311,1019,479,1030,1624,327,1526,1294,1391,1562,1855,1790,1141,882,1035,477,1446,1605,None]]

ciudades = [
    "Cdad. de Bs. As.",
    "Córdoba",
    "Corrientes",
    "Formosa",
    "La Plata",
    "La Rioja",
    "Mendoza",
    "Neuquén",
    "Paraná",
    "Posadas",
    "Rawson",
    "Resistencia",
    "Río Gallegos",
    "S.F.d.V.d. Catamarca",
    "S.M. de Tucumán",
    "S.S. de Jujuy",
    "Salta",
    "San Juan",
    "San Luis",
    "Santa Fe",
    "Santa Rosa",
    "Sgo. Del Estero",
    "Ushuaia",
    "Viedma"
]

#librerias
import random
import matplotlib
from matplotlib import pyplot as plt 
from os import system

#parametros
ciclos = 10  #20 o 100 o 200
tamanio_poblacion = 50
minimo = [[], 1000000]
prob_crossover = 0.8
probabilidad_mutacion = 0.1
tamanio_torneo = 2 #cambiar a porcentaje
porcentaje_elitismo = 20 #porciento
cantidad_elite = porcentaje_elitismo*tamanio_poblacion/100

#----------------------------------------------------------------------------------------------------------------------------------------------------

def ver_ciudades(ruta):
    distancia_total = 0 
    recorrido = [] 
    for i in range(len(ruta)):
        ciudad_actual = ruta[i]
        recorrido.append(ciudades[ciudad_actual])
        if(i < len(ruta) - 1):
            ciudad_siguiente = ruta[i + 1]
            distancia = argentina[ciudad_actual][ciudad_siguiente]
            if(distancia is not None):  
                distancia_total += distancia
    ciudad_inicio = ruta[0]
    recorrido.append(ciudades[ciudad_inicio])
    distancia_de_vuelta = argentina[ruta[-1]][ciudad_inicio]
    if(distancia_de_vuelta is not None):
        distancia_total += distancia_de_vuelta
    # Imprimir el recorrido y la distancia total
    print("Recorrido de ciudades:", " -> ".join(recorrido))
    print("Distancia total:", distancia_total)

    return distancia_total  # Retorna la distancia total

def traducir_ruta(ruta_indices, ciudades):
    return [ciudades[i] for i in ruta_indices]

def traducir_generacion(generacion, ciudades):
    return [[traducir_ruta(ruta[0], ciudades), ruta[1]] for ruta in generacion]

def calcular_distancia(ruta):
    for camino in range(23):
        ruta[1] += argentina[ruta[0][camino]][ruta[0][camino + 1]]
    ruta[1] += argentina[ruta[0][23]][ruta[0][0]]

def calcular_distancia_con_comienzo(ruta, ciudad_comienzo):
    ruta[1] += argentina[ciudad_comienzo][ruta[0][0]]
    for camino in range(22): 
        ruta[1] += argentina[ruta[0][camino]][ruta[0][camino + 1]]
    ruta[1] += argentina[ruta[0][22]][ciudad_comienzo]

def calcular_distancia_heuristica(ruta):
    longitud = len(ruta) - 1
    cont = 0
    for camino in range(longitud):
        cont += argentina[ruta[camino]][ruta[camino + 1]]
    return cont

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
            if(generacion[m][1] < generacion[n][1]): # mayor a menor
                generacion[m], generacion[n] = generacion[n], generacion[m]

#----------------------------------------------------------------------------------------------------------------------------------------------------
def exhaustiva_2():
    posibles_ciudades = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23] #esto se puede hacer como un array de 1s y 0s y en vez de eliminar un elemento, 
    #simplemente se iguala a 0 entre otros cambios
    for ciudad in range(24):
        una_ruta = [ciudad]
        nuevas_posibles = posibles_ciudades.copy()
        del nuevas_posibles[ciudad]
        funcion_recursiva(una_ruta, nuevas_posibles)
    return minimo

def funcion_recursiva(ruta, posibles_c):
    print(ruta)
    if(calcular_distancia_heuristica(ruta) < minimo[1]):
        lon = int(len(posibles_c))
        for ciudad in range(lon):
            una_ruta = ruta.copy()
            una_ruta.append(posibles_c[ciudad])
            nuevas_posibles = posibles_c.copy()
            del nuevas_posibles[ciudad]
            funcion_recursiva(una_ruta, nuevas_posibles)
        if(lon == 0):
            distancia = calcular_distancia_heuristica(ruta)
            if(distancia < (minimo[1])):
                print('nuevo minimo:', ruta)
                minimo[0] = ruta
                minimo[1] = distancia
#----------------------------------------------------------------------------------------------------------------------------------------------------


# def heuristica():
#     mejor_distancia = float
#     mejor_ruta = []

#     for ciudad_inicial in range(24):
#         ruta = [ciudad_inicial]
#         posibles_ciudades = []

#         for k in range(24):
#             if(k != ciudad_inicial):
#                 posibles_ciudades.append(k)
#         index = 0
#         posicion_actual = ciudad_inicial

#         while(index <= 22):
#             min = 10000
#             min_i = None
#             i = 0
#             for i in range(len(posibles_ciudades)):
#                 if(argentina[posicion_actual][posibles_ciudades[i]] < min):
#                     min = argentina[posicion_actual][posibles_ciudades[i]]
#                     min_i = i
#             ruta.append(posibles_ciudades[min_i])
#             posicion_actual = posibles_ciudades[min_i]
#             del posibles_ciudades[min_i]
#             index += 1
#         ruta.append(ciudad_inicial)
        
#         distancia_total = ver_ciudades(ruta)

#         if distancia_total < mejor_distancia:
#             mejor_distancia = distancia_total
#             mejor_ruta = ruta

#     return mejor_ruta 
def heuristicainicial(ciudad_ini):
    mejor_distancia = float('inf') 
    mejor_ruta = [] 

    # Inicia la ruta desde la ciudad seleccionada
    ruta = [ciudad_ini]
    posibles_ciudades = [k for k in range(len(ciudades)) if k != ciudad_ini]
    posicion_actual = ciudad_ini

    while(posibles_ciudades):
        distancia_min = float('inf')
        min_i = None
        
        # Encuentra la ciudad más cercana no visitada
        for i in range(len(posibles_ciudades)):
            distancia = argentina[posicion_actual][posibles_ciudades[i]]
            if distancia is not None and distancia < distancia_min:
                distancia_min = distancia
                min_i = i
        
        # Agrega la ciudad más cercana a la ruta
        if(min_i is not None):
            ruta.append(posibles_ciudades[min_i])
            posicion_actual = posibles_ciudades[min_i]
            del posibles_ciudades[min_i]

    # Cierra el ciclo volviendo a la ciudad inicial
    ruta.append(ciudad_ini)

    # Calcula la distancia total de la ruta
    distancia_total = calcular_distancia_heuristica(ruta)

    # Actualiza la mejor ruta si es necesario
    if(distancia_total < mejor_distancia):
        mejor_distancia = distancia_total
        mejor_ruta = ruta

    return mejor_ruta, mejor_distancia # Retorna la mejor ruta y su distancia

def ver_ciudadeini(ruta):
    recorrido = []
    for ciudad_index in ruta:  # Asegúrate de que 'ruta' es una lista de índices enteros
        recorrido.append(ciudades[ciudad_index])  # Agrega la ciudad actual al recorrido
    print("Recorrido de ciudades:", " -> ".join(recorrido))


def heuristica():
    mejor_distancia = float('inf') 
    mejor_ruta = [] 

    for ciudad_inicial in range(24):
        ruta = [ciudad_inicial]
        posibles_ciudades = [k for k in range(24) if k != ciudad_inicial]
        posicion_actual = ciudad_inicial

        while(posibles_ciudades):
            distancia_min = float('inf')
            min_i = None
            for i in range(len(posibles_ciudades)):
                distancia = argentina[posicion_actual][posibles_ciudades[i]]
                if(distancia is not None and distancia < distancia_min):
                    distancia_min = distancia
                    min_i = i
            
            if(min_i is not None):
                ruta.append(posibles_ciudades[min_i])
                posicion_actual = posibles_ciudades[min_i]
                del posibles_ciudades[min_i]
        ruta.append(ciudad_inicial)
        distancia_total = calcular_distancia_heuristica(ruta)
        if(distancia_total < mejor_distancia):
            mejor_distancia = distancia_total
            mejor_ruta = ruta

    return mejor_ruta  # Retorna la mejor ruta



#----------------------------------------------------------------------------------------------------------------------------------------------------
def calcular_total(generacion, tam_gen):
    tot = 0
    for c in range(tam_gen):
        tot += generacion[c][1]
    return tot


def generar_gen_inicial(tam_pob):
    generacion_inicial = []
    posibles_ciudades = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    tam_p_c = 23
    for cambrian in range(tam_pob):
        new_cambrian = [[], 0]
        for ciudad in range(24):
            i_random = random.randint(0, tam_p_c - ciudad )
            new_cambrian[0].append(posibles_ciudades[i_random])
            del posibles_ciudades[i_random]
        calcular_distancia(new_cambrian)
        generacion_inicial.append(new_cambrian)
        posibles_ciudades = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        ordenar(generacion_inicial, cambrian + 1)
    return generacion_inicial

def generar_ruta_individual():
    posibles_ciudades = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    tam_p_c = 23
    nueva_ruta = [[], 0]
    for ciudad in range(24):
        i_random = random.randint(0, tam_p_c - ciudad )
        nueva_ruta[0].append(posibles_ciudades[i_random])
        del posibles_ciudades[i_random]
    calcular_distancia(nueva_ruta)
    return nueva_ruta

#selecciones
def ruleta_segun_rango(cromosomas, tam_gen):
    padres = []
    totsum = 0
    k = 0
    for k in range(len(cromosomas)):
        totsum += k + 1
    for padre in range(int(tam_gen)):
        totRuleta = 0
        flecha = random.random()*100
        index = 0
        condicion = True
        while(condicion):
            totRuleta += ((index + 1)/totsum)*100
            if(totRuleta >= flecha):
                padres.append(cromosomas[index])
                condicion = False
            else:
                index += 1
    return padres

# hay un problema con ruleta normal, una ruta que es mas larga tiene mas chances de ser elegida ya que su (cromosomas[index][1]/total)*100 es 
# mayor al de una ruta mas pequeña. ruleta segun ratngo resuelve este problema
def ruleta_normal(cromosomas, tam_gen):
    total = calcular_total(cromosomas, tam_gen)
    padres = []
    for padre in range(int(tam_gen)):
        totRuleta = 0
        flecha = random.random()*100
        index = 0
        condicion = True
        while(condicion):
            totRuleta += (cromosomas[index][1]/total)*100
            if(totRuleta >= flecha):
                padres.append(cromosomas[index])
                condicion = False
            else:
                index += 1
    return padres

def seleccion_torneo(cromosomas, tam_gen):
    padres = []
    total = calcular_total(cromosomas, tam_gen)
    for j in range(int(tam_gen/2)):
        for i in range(2):
            mejor_indice = 0
            mejor_fitness = 0
            for j in range(tamanio_torneo):
                indice_elegido = random.randint(0, tam_gen - 1)
                if((cromosomas[indice_elegido][1]/total) > mejor_fitness):
                    mejor_fitness = cromosomas[indice_elegido][1]/total
                    mejor_indice = indice_elegido
            padres.append(cromosomas[mejor_indice])
    return padres

def comprobar(n1, n2):
    band = False
    comp = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    for i in range(24):
        if (comp[i] not in n1) or (comp[i] not in n2):
            band =True
    return band


def crossover_ciclico(padres, tam_pob):
    pareja = 0
    nuevo_gen1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    nuevo_gen2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    next_generation = []
    while (pareja < tam_pob):
        if(random.random() < prob_crossover):
            aux1 = padres[pareja][0].copy()
            aux2 = padres[pareja + 1][0].copy()
            nuevo_gen1[0] = aux1[0]
            buscador = aux2[0]
            nuevo_gen2[0]= aux2[0]
            c=1
            band = 0
            while (band != 1) and (c <len(aux1)):
                if(nuevo_gen1[0] == aux2[c]):
                    for k in range(c, len(aux1)):
                        nuevo_gen1[k]= aux1[k]
                        nuevo_gen2[k]= aux2[k]
                    band = 1
                elif(band != 1) and(buscador == aux1[c]):
                    nuevo_gen1[c]= aux1[c]
                    buscador= aux2[c]
                    nuevo_gen2[c]= aux2[c]
                elif (band !=1):
                    nuevo_gen1[c] = aux2[c]
                    nuevo_gen2[c] = aux1[c]
                c+=1
            if(comprobar(nuevo_gen1,nuevo_gen2) ):
                pasar1 = padres[pareja].copy()
                pasar2 = padres[pareja + 1].copy()      
            else:
                pasar1 = [[], 0]
                pasar2 = [[], 0]
                pasar1[0] = nuevo_gen1.copy()
                pasar2[0] = nuevo_gen1.copy()
                calcular_distancia(pasar1)
                calcular_distancia(pasar2)
            next_generation.append(pasar1)
            next_generation.append(pasar2)
        else:
            next_generation.append(padres[pareja].copy())
            next_generation.append(padres[pareja + 1].copy())
        pareja +=2
    return next_generation

def crossover_corte(padres, tam_pob):
    pareja = 0
    next_generation = []
    while (pareja < tam_pob):
        if(random.random() < prob_crossover):
            nuevo_gen1 = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 0]
            nuevo_gen2 = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 0]
            corte1 = random.randint(0, 23)
            corte2 = random.randint(0, 23)
            while(corte1 == corte2):
                corte2 = random.randint(0, 23)
            if(corte1 > corte2):
                corte1, corte2 = corte2, corte1
            nuevo_gen1[0][corte1:corte2] = padres[pareja][0][corte1:corte2]
            ciudad = 0
            pointer = 0
            for ciudad in range(24):
                while(nuevo_gen1[0][ciudad] == -1):
                    if((padres[pareja + 1][0][pointer] in nuevo_gen1[0])):
                        pointer += 1
                    else:
                        nuevo_gen1[0][ciudad] = padres[pareja + 1][0][pointer]
                        pointer += 1

            corte1 = random.randint(0, 23)
            corte2 = random.randint(0, 23)
            while(corte1 == corte2):
                corte2 = random.randint(0, 23)
            if(corte1 > corte2):
                corte1, corte2 = corte2, corte1
            nuevo_gen2[0][corte1:corte2] = padres[pareja + 1][0][corte1:corte2]
            ciudad = 0
            pointer = 0
            for ciudad in range(24):
                while(nuevo_gen2[0][ciudad] == -1):
                    if((padres[pareja][0][pointer] in nuevo_gen2[0])):
                        pointer += 1
                    else:
                        nuevo_gen2[0][ciudad] = padres[pareja][0][pointer]
                        pointer += 1
            calcular_distancia(nuevo_gen1)
            calcular_distancia(nuevo_gen2)
            next_generation.append(nuevo_gen1.copy())
            next_generation.append(nuevo_gen2.copy())
        else:
            next_generation.append(padres[pareja].copy())
            next_generation.append(padres[pareja + 1].copy())
        pareja +=2
    return next_generation

def mutacion_cambio(ruta, prob):
    nueva_ruta = ruta[:]
    if(prob >= random.random()):
        indice1 = -1
        indice2 = -1
        while(indice1 == indice2):
            indice1 = random.randrange(0, len(ruta))
            indice2 = random.randrange(0, len(ruta))
        nueva_ruta[indice1] = ruta[indice2]
        nueva_ruta[indice2] = ruta[indice1]
    return nueva_ruta

def mutacion_cambio_doble(ruta, prob):
    nueva_ruta = ruta[:]
    if(prob >= random.random()):
        for vez in range(2):
            indice1 = -1
            indice2 = -1
            while(indice1 == indice2):
                indice1 = random.randrange(0, len(ruta))
                indice2 = random.randrange(0, len(ruta))
            nueva_ruta[indice1] = ruta[indice2]
            nueva_ruta[indice2] = ruta[indice1]
    return nueva_ruta

def mutacion_inversion(ruta, prob):
    nueva_ruta = ruta[:]
    if(prob >= random.random()):
        indice1 = random.randint(0, len(ruta) - 1)
        indice2 = random.randint(0, len(ruta) - 1)
        if(indice1 > indice2):
            indice1, indice2 = indice2, indice1
        nueva_ruta[indice1:indice2 + 1] = reversed(nueva_ruta[indice1:indice2 + 1])
    return nueva_ruta

#def crossover_multiversal_1(multiverso, column):
#    if(0.667 > random.random()):


def crear_universo(cant_ciclos, seleccion, crossover, mutacion, tam_pob, prob_mutacion):
    ejex = list()
    valores_minimos = list()
    valores_maximos = list()
    valores_promedio = list()
    generacion = generar_gen_inicial(tam_pob)
    for ciclo in range(cant_ciclos): 
        ejex.append(ciclo)
        valor_promedio = 0
        tot_sum = 0
        padres = seleccion(generacion, tam_pob)
        siguiente_pob = crossover(padres, tam_pob)
        i = 0
        for i in range(len(siguiente_pob) - 1):
            siguiente_pob[i][0] = mutacion(siguiente_pob[i][0], prob_mutacion)
            calcular_distancia(siguiente_pob[i])
        
        ordenar(siguiente_pob, tam_pob)
        generacion = siguiente_pob.copy()
        i = 0
        for i in range(len(generacion) - 1):
            tot_sum += generacion[i][1]
        valor_promedio = tot_sum/(len(generacion) - 1)
        valores_minimos.append(generacion[tam_pob - 1][1])
        valores_maximos.append(generacion[0][1])
        if(generacion[tam_pob - 1][1] > generacion[0][1]):
            print(generacion)
        valores_promedio.append(valor_promedio)
        
        

    print(" ")
    print(" ")
    print(" ")
    print(" ")
    print("Ultima generacion")
    for idx, individuo in enumerate(generacion):
        ruta_traducida = traducir_ruta(individuo[0], ciudades)
        distancia_total = individuo[1]
        # Visualización mejorada
        print(f"Ruta {idx + 1}:")
        print(f"  Ciudades: {' -> '.join(ruta_traducida)}")
        print(f"  Distancia total: {distancia_total}\n")
        
    numeros = int(cant_ciclos/10)
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))  # Reducimos el tamaño de la figura
    fig.suptitle('Estadísticas Finales sin Elitismo', fontsize=16)
    # Primer gráfico: Valores mínimos
    axs[0].plot(ejex, valores_minimos, 'b')
    axs[0].set_title('Valores Mínimos')
    axs[0].set_xlabel('Corrida')
    axs[0].set_ylabel('Valores')
    axs[0].set_xlim(0, cant_ciclos - 1)
    axs[0].set_ylim(0, 60000)
    axs[0].set_xticks(range(0, cant_ciclos + 1, numeros))
    axs[0].set_yticks(range(0, 60000, int(60000/10)))
    axs[0].legend(loc='best')
    # Segundo gráfico: Valores máximos
    axs[1].plot(ejex, valores_maximos, 'r')
    axs[1].set_title('Valores Máximos')
    axs[1].set_xlabel('Corrida')
    axs[1].set_ylabel('Valores')
    axs[1].set_xlim(0, cant_ciclos - 1)
    axs[1].set_ylim(0, 100000)
    axs[1].set_xticks(range(0, cant_ciclos + 1, numeros))
    axs[1].set_yticks(range(0, 100000, int(100000/10)))
    axs[1].legend(loc='best')
    # Tercer gráfico: Valores promedio
    axs[2].plot(ejex, valores_promedio, 'g')
    axs[2].set_title('Valores Promedios')
    axs[2].set_xlabel('Corrida')
    axs[2].set_ylabel('Valores')
    axs[2].set_xlim(0, cant_ciclos - 1)
    axs[2].set_ylim(0, 100000)
    axs[2].set_xticks(range(0, cant_ciclos + 1, numeros))
    axs[2].set_yticks(range(0, 100000, int(100000/10)))
    axs[2].legend(loc='best')
    plt.tight_layout()
    plt.show()

def crear_universo_con_elitismo(cant_ciclos, seleccion, crossover, mutacion, tam_pob, cant_elite, prob_mutacion):
    ejex = list()
    valores_minimos = list()
    valores_maximos = list()
    valores_promedio = list()
    generacion = generar_gen_inicial(tam_pob)
    for ciclo in range(cant_ciclos): 
        ejex.append(ciclo)
        valor_promedio = 0
        tot_sum = 0
        elites = []
        ciudad = 0
        prob_mutacion += 0.001
        for ciudad in range(int(cant_elite)):
            elites.append(generacion[tam_pob - 1 - ciudad].copy())
        padres = seleccion(generacion, tam_pob)
        siguiente_pob = crossover(padres, tam_pob)

        for i in range(len(siguiente_pob) - 1):
            siguiente_pob[i][0] = mutacion(siguiente_pob[i][0], prob_mutacion)
            calcular_distancia(siguiente_pob[i])

        ordenar(siguiente_pob, tam_pob)
        ciudad = 0
        for ciudad in range(int(cant_elite)):
            siguiente_pob[ciudad] = elites[ciudad].copy()

        
        ciudad = 0
        for ciudad in range(tam_pob):
            ciudad_2 = 0
            for ciudad_2 in range(ciudad, tam_pob):
                if(siguiente_pob[ciudad] == siguiente_pob[ciudad_2] and ciudad != ciudad_2):
                    siguiente_pob[ciudad] = generar_ruta_individual()
        
        ordenar(siguiente_pob, tam_pob)
        generacion = siguiente_pob.copy() 

        for i in range(len(generacion)-1):
            tot_sum += generacion[i][1]
        valor_promedio = tot_sum / len(generacion)-1
        valores_minimos.append(generacion[tam_pob - 1][1])
        valores_maximos.append(generacion[0][1]) 
        valores_promedio.append(valor_promedio)
    
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    print("Ultima generacion")
    for idx, individuo in enumerate(generacion):
        ruta_traducida = traducir_ruta(individuo[0], ciudades)
        distancia_total = individuo[1]
        # Visualización mejorada
        print(f"Ruta {idx + 1}:")
        print(f"  Ciudades: {' -> '.join(ruta_traducida)}")
        print(f"  Distancia total: {distancia_total}\n")
    numeros = int(cant_ciclos/10)
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))  # Reducimos el tamaño de la figura
    fig.suptitle('Estadísticas Finales con Elitismo', fontsize=16)
    # Primer gráfico: Valores mínimos
    axs[0].plot(ejex, valores_minimos, 'b')
    axs[0].set_title('Valores Mínimos')
    axs[0].set_xlabel('Corrida')
    axs[0].set_ylabel('Valores')
    axs[0].set_xlim(0, cant_ciclos - 1)
    axs[0].set_ylim(0, 40000)
    axs[0].set_xticks(range(0, cant_ciclos + 1, numeros))
    axs[0].set_yticks(range(0, 40000, int(40000/10)))
    axs[0].legend(loc='best')
    # Segundo gráfico: Valores máximos
    axs[1].plot(ejex, valores_maximos, 'r')
    axs[1].set_title('Valores Máximos')
    axs[1].set_xlabel('Corrida')
    axs[1].set_ylabel('Valores')
    axs[1].set_xlim(0, cant_ciclos - 1)
    axs[1].set_ylim(0, 100000)
    axs[1].set_xticks(range(0, cant_ciclos + 1, numeros))
    axs[1].set_yticks(range(0, 100000, int(100000/10)))
    axs[1].legend(loc='best')
    # Tercer gráfico: Valores promedio
    axs[2].plot(ejex, valores_promedio, 'g')
    axs[2].set_title('Valores Promedios')
    axs[2].set_xlabel('Corrida')
    axs[2].set_ylabel('Valores')
    axs[2].set_xlim(0, cant_ciclos - 1)
    axs[2].set_ylim(0, 100000)
    axs[2].set_xticks(range(0, cant_ciclos + 1, numeros))
    axs[2].set_yticks(range(0, 100000, int(100000/10)))
    axs[2].legend(loc='best')
    plt.tight_layout()
    plt.show()

#hace un tiempo descubri el concepto de algoritmos geneticos inspirados en quantica, lo que hace basicamente es crear varios universos que corren de manera normal solo que se introduce un operador llamado crossover quantico
#el cual toma todos los cromosomas en la posicion i de cada universo y hace uno solo nuevo. si sale algo lindo capaz lo podemos poner como una curiosidad.
def crear_multiverso_con_elitismo(cant_ciclos, seleccion, crossover, mutacion, tam_pob, cant_elite, prob_mutacion):
    ejex = list()
    valores_minimos = list()
    valores_maximos = list()
    valores_promedio = list()
    multiverso = []
    for universo in range(24):
        multiverso.append(generar_gen_inicial(tam_pob))
    for ciclo in range(cant_ciclos):
        universo = 0
        ejex.append(ciclo)
        valor_promedio = 0
        tot_sum = 0
        valor_minimo = [[], 100000]
        valor_maximo = [[], 0]
        prob_mutacion += 0.001
        for universo in range(24):
            elites = []
            ciudad = 0
            for ciudad in range(int(cant_elite)):
                elites.append(multiverso[universo][tam_pob - 1 - ciudad].copy())
            padres = seleccion(multiverso[universo], tam_pob)
            siguiente_pob = crossover(padres, tam_pob)

            for i in range(len(siguiente_pob) - 1):
                siguiente_pob[i][0] = mutacion(siguiente_pob[i][0], prob_mutacion)
                calcular_distancia(siguiente_pob[i])

            ordenar(siguiente_pob, tam_pob)
            for column in range(tam_pob):
                freak = crossover_multiversal_1(multiverso, column)
            ordenar(siguiente_pob, tam_pob)
            ciudad = 0
            for ciudad in range(int(cant_elite)):
                siguiente_pob[ciudad] = elites[ciudad].copy()
            ordenar(siguiente_pob, tam_pob)
            multiverso[universo] = siguiente_pob.copy() 

            for i in range(len(multiverso[universo]) - 1):
                tot_sum += multiverso[universo][i][1]
            if(multiverso[universo][tam_pob - 1][1] < valor_minimo[1]):
                 valor_minimo = multiverso[universo][int(len(multiverso[universo]) - 1)].copy()
            if(multiverso[universo][0][1] > valor_maximo[1]):
                 valor_maximo = multiverso[universo][0].copy()
        valor_promedio = (tot_sum)/(24*(len(multiverso[0])))
        valores_minimos.append(valor_minimo[1])
        valores_maximos.append(valor_maximo[1])
        valores_promedio.append(valor_promedio)
    print(valor_minimo)


    numeros = int(cant_ciclos/10)
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))  # Reducimos el tamaño de la figura
    fig.suptitle('Estadísticas Finales con Elitismo y Multiverso', fontsize=16)
    # Primer gráfico: Valores mínimos
    axs[0].plot(ejex, valores_minimos, 'b')
    axs[0].set_title('Valores Mínimos')
    axs[0].set_xlabel('Corrida')
    axs[0].set_ylabel('Valores')
    axs[0].set_xlim(0, cant_ciclos - 1)
    axs[0].set_ylim(0, 100000)
    axs[0].set_xticks(range(0, cant_ciclos + 1, numeros))
    axs[0].set_yticks(range(0, 100000, int(100000/10)))
    axs[0].legend(loc='best')
    # Segundo gráfico: Valores máximos
    axs[1].plot(ejex, valores_maximos, 'r')
    axs[1].set_title('Valores Máximos')
    axs[1].set_xlabel('Corrida')
    axs[1].set_ylabel('Valores')
    axs[1].set_xlim(0, cant_ciclos - 1)
    axs[1].set_ylim(0, 100000)
    axs[1].set_xticks(range(0, cant_ciclos + 1, numeros))
    axs[1].set_yticks(range(0, 100000, int(100000/10)))
    axs[1].legend(loc='best')
    # Tercer gráfico: Valores promedio
    axs[2].plot(ejex, valores_promedio, 'g')
    axs[2].set_title('Valores Promedios')
    axs[2].set_xlabel('Corrida')
    axs[2].set_ylabel('Valores')
    axs[2].set_xlim(0, cant_ciclos - 1)
    axs[2].set_ylim(0, 100000)
    axs[2].set_xticks(range(0, cant_ciclos + 1, numeros))
    axs[2].set_yticks(range(0, 100000, int(100000/10)))
    axs[2].legend(loc='best')
    plt.tight_layout()
    plt.show()



opc = -1
opc2 = -1

while(opc != 0 and opc < 4):
    print("1: Heuristica con ciudad inicial")
    print("2: Heuristica sin ciudad inicial, ruta mas optima")
    print("3: Algoritmos geneticos")
    print("0: Salir")
    opc = int(input("Ingrese una opcion: "))
    if(opc == 1):
        for i in range(22):
            print(i, "     ", ciudades[i])
        ciudadini = int(input("Ingrese el numero de ciudad inicial: "))
        mejorruta, mejordistancia = heuristicainicial(ciudadini)
        print("Mejor Ruta x Heuristica")
        ver_ciudadeini(mejorruta)
        print("La distancia de la mejor ruta es: ", mejordistancia)
        #ver_ciudades(mejorruta) 
    elif(opc == 2):
        print(ver_ciudades(heuristica()))    
    elif(opc == 3):
        ciclos = 5000
        params = input("Desea cambiar los parametros? Y / N: ")
        if(params.lower() == "y"):
            prob_crossover = int(input("Ingrese la probabilidad de crossover (0-100): ")) / 100
            prob_mutacion = int(input("Ingrese la probabilidad de mutacion (0-100): ")) / 100
            ciclos = int(input("Ingrese la cantidad de ciclos: "))
            
            print(f"Probabilidad de crossover: {prob_crossover}")
            print(f"Probabilidad de mutación: {prob_mutacion}")
        print("1_ Sin elitismo. ")
        print("2_ Con elitismo. ")

        opc2 = int(input("Cual algoritmo geentico elige? (1/2)"))
        if(opc2 == 1):
            crear_universo(ciclos, ruleta_segun_rango, crossover_corte, mutacion_inversion, 30,  probabilidad_mutacion)
        else:
            crear_universo_con_elitismo(ciclos, ruleta_segun_rango, crossover_corte, mutacion_inversion, 30, cantidad_elite, probabilidad_mutacion)
    input()
    system("cls")



#crear_multiverso_con_elitismo(1000, ruleta_segun_rango, crossover_corte, mutacion_inversion, 30, cantidad_elite, probabilidad_mutacion)


