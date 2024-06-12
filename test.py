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
    for cromosoma in cromosomas:
        tot += fun_obj(cromosoma)
    return tot

def ordenar(cromosomas):
    tot = calcular_total(cromosomas)
    for i in range(tam_poblacion):
        for j in range(i, tam_poblacion):
            if(fitness(cromosomas[i], tot) > fitness(cromosomas[j],tot)):
                aux = cromosomas[j]
                cromosomas[j] = cromosomas[i]
                cromosomas[i] = aux
    return cromosomas

poblacion = crear_poblacion(genes,tam_poblacion)
ordenar(poblacion)
print(fun_obj(poblacion[0]))
print(fun_obj(poblacion[9]))