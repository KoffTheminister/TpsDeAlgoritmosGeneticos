#librerias
import random
import matplotlib
import matplotlib.pyplot as plt

#parametros
tam_poblacion = 10
genes = 30
prob_crossover = 0.75
prob_mutacion = 0.05
ciclos = 200  #20 o 100 o 200
tam_torneo = 2
porcentaje_elitismo = 20 #porciento
cant_elite = porcentaje_elitismo*tam_poblacion/100

#funciones soporte
def crear_poblacion(numeroDeGenomas, numeroDeIndividuos):
    cromosoma = list()
    cromosomas = list()
    for i in range(numeroDeIndividuos):
        for j in range(numeroDeGenomas):
            cromosoma.append(round(random.random()))
        cromosomas.append(cromosoma)
        cromosoma = list()
    return cromosomas

def bin_to_dec(cromosoma):
    length = len(cromosoma)
    numDec = 0
    for gen in cromosoma:
        numDec += gen*(2**(length - 1))
        length -= 1
    return numDec

def fun_obj(cromosoma):
    return (bin_to_dec(cromosoma)/(2**30 - 1))**2

def fitness(cromosoma, tot):
    return fun_obj(cromosoma)/tot

def calcular_total(cromosomas):
    tot = 0
    for e in range(tam_poblacion):
        tot += fun_obj(cromosomas[e])
    return tot

def ordenar(cromosomas):
    tot = calcular_total(cromosomas)
    aux = []
    for i in range(tam_poblacion):
        for j in range(i, tam_poblacion):
            if(fitness(cromosomas[i], tot) > fitness(cromosomas[j],tot)):
                aux = cromosomas[j]
                cromosomas[j] = cromosomas[i]
                cromosomas[i] = aux
                aux=[]
    return cromosomas

#selecciones
def ruleta_segun_rango(cromosomas):
    cromosomas = ordenar(cromosomas)
    indicesDeLosPadres=list()
    totsum = 0
    for k in range(len(cromosomas)):
        totsum += k + 1
    for j in range(int(tam_poblacion/2)):
        indicesDeLosPadres.append([None, None])
        for i in range(2):
            totRuleta = 0
            flecha = random.random()*100
            index = 0
            condicion = True
            while(condicion):
                totRuleta += ((index + 1)/totsum)*100
                if(totRuleta >= flecha and indicesDeLosPadres[j][0] != index):
                    indicesDeLosPadres[j][i] = index
                    condicion = False
                elif(totRuleta >= flecha and indicesDeLosPadres[j][0] == index):
                    index = 0
                    flecha = random.random()*100
                    totRuleta = 0
                else:
                    index += 1
    return indicesDeLosPadres

def ruleta_normal(cromosomas):
    total = calcular_total(cromosomas)
    indicesDeLosPadres = list()
    for j in range(int(tam_poblacion/2)):
        indicesDeLosPadres.append([None, None])
        for i in range(2):
            totRuleta = 0
            flecha = random.random()*100
            index = 0
            condicion = True
            while(condicion):
                totRuleta += (fitness(cromosomas[index], total))*100
                if(totRuleta >= flecha and indicesDeLosPadres[j][0] != index):
                    indicesDeLosPadres[j][i] = index
                    condicion = False
                elif(totRuleta >= flecha and indicesDeLosPadres[j][0] == index):
                    flecha = random.random()*100
                    index=0
                    totRuleta=0
                else:
                    index += 1
    return indicesDeLosPadres

def seleccion_torneo(cromosomas):
    indices_de_padres = list()
    for j in range(int(tam_poblacion/2)):
        for i in range(2):
            padres = list()
            mejor_indice = 0
            mejor_fitness = 0
            for j in range(tam_torneo):
                indice_elegido = random.randint(0,9)        
                if (fitness(cromosomas[indice_elegido],calcular_total(cromosomas)) > mejor_fitness):
                    mejor_fitness = fitness(cromosomas[indice_elegido],calcular_total(cromosomas))
                    mejor_indice = indice_elegido
            padres.append(mejor_indice)
        indices_de_padres.append(padres)
    return indices_de_padres

#funcion para obtener padres
def obtenerpadres(indices, cromosomes, indiceDePareja): 
    padres = list()
    padres= [[],[]]  
    for i in range(2):
        padres[i]=cromosomes[indices[indiceDePareja][i-1]].copy()
    return padres

#crossovers
def crossover_mitad_mitad(padres, poblacion):
    if(prob_crossover <= random.random()):
        cruce = random.randint(1, genes - 1)
        hijo1 = padres[0][:cruce]  + padres[1][cruce:]
        hijo2 = padres[1][:cruce] + padres[0][cruce:]
        poblacion.append(hijo1)
        poblacion.append(hijo2)
    else:
        poblacion.append(padres[0])
        poblacion.append(padres[1])

def crossover_mascara(padres, poblacion_siguiente):
    if(prob_crossover <= random.random()):
        for j in range(2):
            hijo = list()
            mascara = list()
            i = 0
            for i in range(genes):
                mascara.append(round(random.random()))
            i = 0
            for i in range(genes):
                if(mascara[i] == 1):
                    hijo.append(padres[0][i])
                else:
                    hijo.append(padres[1][i])
            poblacion_siguiente.append(hijo)
    else:
        poblacion_siguiente.append(padres[0])
        poblacion_siguiente.append(padres[1])

#mutaciones
def mutacion_indice_aleatorio(individuo):
    if (prob_mutacion >= random.random()):
        cruce = random.randint(1, genes - 1)
        individuo[cruce] = 1 - individuo[cruce]  # Cambiar de 0 a 1 o de 1 a 0 con probabilidad prob_mutacion
    return individuo

def mutacion_mascara(individuo):
    if (prob_mutacion >= random.random()):
        mascara = list()
        i = 0
        for i in range(genes):
            mascara.append(round(random.random()))
        i = 0
        for i in range(genes):
            if(mascara[i] == 1):
                individuo[i] = 1 - individuo[i]
    return individuo

def mutacion_mascara_probabilidad(individuo):
    if (prob_mutacion >= random.random()):
        mascara = list()
        i = 0
        for i in range(genes):
            mascara.append(random.random())
        i = 0
        for i in range(genes):
            flecha = random.random()
            if(mascara[i] <= flecha):
                individuo[i] = 1 - individuo[i]
    return individuo

#funcion utilizada para crear las tablas de valores
def imprimir(minimos,maximos,promedios,poblacion, cromosomas,cromosoma_maximo):
    valor_maximo = 0
    print("Ciclo       Valor minimo          Valor maximo       Valor promedio               Cromosoma Maximo  \n")
    for i in range(ciclos):
        print(i+1, "          ", round(minimos[i],6),"            ",round(maximos[i],6),"            ", round(promedios[i],6),"             ",cromosomas[i])
        if (maximos[i] > valor_maximo):
                valor_maximo = maximos[i]
    print("El cromosoma con valor maximo fue: ", cromosoma_maximo)

#funcion para crear un universo con especificos metodos de desarrollo
def crear_universo(metodo_seleccion, metodo_crossover, metodo_mutacion):
    ejex = list()
    valores_minimos = list()
    valores_maximos = list()
    valores_promedio = list()
    cromosomas_maximos = list()
    cromosoma_maximo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    poblacion = crear_poblacion(genes, tam_poblacion)
    for j in range(ciclos):
        ejex.append(j)
        valor_promedio = 0
        valor_minimo = 1
        valor_maximo = 0
        tot_sum = 0
        poblacion2 = list()
        padrecitos = metodo_seleccion(poblacion)
        for k in range(int(tam_poblacion / 2)):
            metodo_crossover(obtenerpadres(padrecitos, poblacion, k), poblacion2)
        for p in range(tam_poblacion):
            poblacion2[p] = metodo_mutacion(poblacion2[p])
        poblacion2 = ordenar(poblacion2)
        valor_maximo = fun_obj(poblacion2[9])
        cromosomas_maximos.append(poblacion2[9])
        valor_minimo = fun_obj(poblacion2[0])
        for i in range(int(tam_poblacion)):
            tot_sum += fun_obj(poblacion2[i])
        if(fun_obj(poblacion2[9]) > fun_obj(cromosoma_maximo)):
            cromosoma_maximo = poblacion2[9]
        promedio = tot_sum / tam_poblacion
        valores_minimos.append(valor_minimo)
        valores_maximos.append(valor_maximo)
        valores_promedio.append(promedio)
        poblacion = poblacion2


    numeros = int(ciclos/10)

    fig, axs = plt.subplots(1, 3, figsize=(12, 4))  # Reducimos el tamaño de la figura

    fig.suptitle('Estadísticas Finales sin Elitismo', fontsize=16)
    # Primer gráfico: Valores mínimos
    axs[0].plot(ejex, valores_minimos, 'b')
    axs[0].set_title('Valores Mínimos')
    axs[0].set_xlabel('Corrida')
    axs[0].set_ylabel('Valores')
    axs[0].set_xlim(0, ciclos - 1)
    axs[0].set_ylim(0, 1)
    axs[0].set_xticks(range(0, ciclos + 1, numeros))
    axs[0].set_yticks([i / 10 for i in range(0, 12)])
    axs[0].legend(loc='best')

    # Segundo gráfico: Valores máximos
    axs[1].plot(ejex, valores_maximos, 'r')
    axs[1].set_title('Valores Máximos')
    axs[1].set_xlabel('Corrida')
    axs[1].set_ylabel('Valores')
    axs[1].set_xlim(0, ciclos - 1)
    axs[1].set_ylim(0, 1)
    axs[1].set_xticks(range(0, ciclos + 1, numeros))
    axs[1].set_yticks([i / 10 for i in range(0, 12)])
    axs[1].legend(loc='best')

    # Tercer gráfico: Valores promedio
    axs[2].plot(ejex, valores_promedio, 'g')
    axs[2].set_title('Valores Promedios')
    axs[2].set_xlabel('Corrida')
    axs[2].set_ylabel('Valores')
    axs[2].set_xlim(0, ciclos - 1)
    axs[2].set_ylim(0, 1)
    axs[2].set_xticks(range(0, ciclos + 1, numeros))
    axs[2].set_yticks([i / 10 for i in range(0, 12)])
    axs[2].legend(loc='best')

    plt.tight_layout()
    plt.show()

    imprimir(valores_minimos, valores_maximos, valores_promedio, poblacion, cromosomas_maximos, cromosoma_maximo)

#funcion para crear un universo con especificos metodos de desarrollo y que hace uso del elitismo
def crear_universo_con_elitismo(metodo_seleccion, metodo_crossover, metodo_mutacion):
    ejex = list()
    error = 0
    valores_minimos = list()
    valores_maximos = list()
    valores_promedio = list()
    cromosomas_maximos = list()
    cromosoma_maximo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    poblacion = crear_poblacion(genes, tam_poblacion)
    tot_sum =0
    poblacion = ordenar(poblacion).copy()
    for i in range(int(tam_poblacion)):
            tot_sum += fun_obj(poblacion[i])
    promedio = tot_sum/tam_poblacion
    print("Poblacion inicial:  ")
    print("Valor minimo          Valor maximo        Valor promedio         Cromosoma Maximo  \n")
    print( round(fun_obj(poblacion[0]),6),"            ",fun_obj(poblacion[9]),"            ", round(promedio,6),"           ",poblacion[9])
    for j in range(ciclos):
        ejex.append(j)
        valor_minimo = 1
        tot_sum = 0
        auxiliar= []
        poblacion2 = []
        poblacion = ordenar(poblacion).copy()
        auxiliar = [poblacion[8], poblacion[9]].copy()
        padrecitos = metodo_seleccion(poblacion).copy()

        for k in range(int((tam_poblacion - cant_elite)/2)):
            metodo_crossover(obtenerpadres(padrecitos,poblacion,k), poblacion2)

        for p in range(tam_poblacion-2):
            poblacion2[p] = metodo_mutacion(poblacion2[p])

        poblacion2.extend(auxiliar)
        poblacion2 = ordenar(poblacion2).copy()
        cromosomas_maximos.append(poblacion2[9])
        valor_minimo = fun_obj(poblacion2[0])
        for i in range(int(tam_poblacion)):
            tot_sum += fun_obj(poblacion2[i])
        poblacion2 = ordenar(poblacion2).copy()
        if(fun_obj(poblacion2[9]) > fun_obj(cromosoma_maximo)):
            cromosoma_maximo = poblacion2[9]
        promedio = tot_sum/tam_poblacion
        valores_minimos.append(valor_minimo)
        valores_maximos.append(fun_obj(poblacion2[9]))
        valores_promedio.append(promedio)

        poblacion = poblacion2.copy()
    numeros = int(ciclos/10)

    fig, axs = plt.subplots(1, 3, figsize=(12, 4))  # Reducimos el tamaño de la figura
    fig.suptitle('Estadísticas Finales usando Elitismo', fontsize=16)

    # Primer gráfico: Valores mínimos
    axs[0].plot(ejex, valores_minimos, 'b')
    axs[0].set_title('Valores Mínimos')
    axs[0].set_xlabel('Corrida')
    axs[0].set_ylabel('Valores')
    axs[0].set_xlim(0, ciclos)
    axs[0].set_ylim(0, 1)
    axs[0].set_xticks(range(0, ciclos + 1, numeros))
    axs[0].set_yticks([i / 10 for i in range(0, 12)])
    axs[0].legend(loc='best')

    # Segundo gráfico: Valores máximos
    axs[1].plot(ejex, valores_maximos, 'r')
    axs[1].set_title('Valores Máximos')
    axs[1].set_xlabel('Corrida')
    axs[1].set_ylabel('Valores')
    axs[1].set_xlim(0, ciclos)
    axs[1].set_ylim(0, 1)
    axs[1].set_xticks(range(0, ciclos + 1, numeros))
    axs[1].set_yticks([i / 10 for i in range(0, 12)])
    axs[1].legend(loc='best')

    # Tercer gráfico: Valores promedio
    axs[2].plot(ejex, valores_promedio, 'g')
    axs[2].set_title('Valores Promedio')
    axs[2].set_xlabel('nro de ciclo')
    axs[2].set_ylabel('Valores')
    axs[2].set_xlim(0, ciclos)
    axs[2].set_ylim(0, 1)
    axs[2].set_xticks(range(0, ciclos + 1, numeros))
    axs[2].set_yticks([i / 10 for i in range(0, 12)])
    axs[2].legend(loc='best')

    plt.tight_layout()
    plt.show()


    imprimir(valores_minimos, valores_maximos, valores_promedio, poblacion, cromosomas_maximos, cromosoma_maximo)

#crear_universo(ruleta_segun_rango, crossover_mitad_mitad, mutacion_indice_aleatorio)
#crear_universo(seleccion_torneo, crossover_mascara, mutacion_indice_aleatorio)
crear_universo(ruleta_normal, crossover_mitad_mitad, mutacion_mascara_probabilidad)