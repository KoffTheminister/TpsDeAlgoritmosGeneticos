import random

def create_population(numberOfGenomes, numberOfIndividuals):
    cromosome = list()
    cromosomes = list()
    for i in range(numberOfIndividuals):
        for j in range(numberOfGenomes):
            cromosome.append(round(random.random()))
        cromosomes.append(cromosome)
        cromosome = list()
    return cromosomes

def bin_to_dec(cromosome):
    length = len(cromosome)
    numDec = 0
    for gen in cromosome:
        numDec += gen*(2**(length - 1))
        length -= 1
    return numDec

def fun_obj(cromosome):
    return (bin_to_dec(cromosome)/(2**30 - 1))**2

def fitness(cromosome, tot):
    return fun_obj(cromosome)/tot

def calcular_total(cromosomes):
    tot = 0
    for cromosome in cromosomes:
        tot += fun_obj(cromosome)
    return tot

def nueva_ruleta(cromosomas):
    total = calcular_total(cromosomas)
    indicesDeLosPadres = [None, None]
    for i in range(2):
        totRuleta = 0
        flecha = random.random()*100
        index = 0
        condicion = True
        while(condicion):
            totRuleta += fitness(cromosomas[index], total)*100
            if(totRuleta >= flecha and indicesDeLosPadres[0] != index):
                indicesDeLosPadres[i] = index
                condicion = False
            else:
                index += 1
    return indicesDeLosPadres




cromosomes = create_population(30, 10)
padrecitos = nueva_ruleta(cromosomes)
print(padrecitos)