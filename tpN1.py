import random

poblacion = 10
genes = 30
prob_crossover = 0.75
prob_mutacion = 0.05
ciclos = 20

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

def ruleta_segun_rango(cromosomas):
    tot = calcular_total(cromosomas)
    for i in range(len(cromosomas)):
        for j in range(i, len(cromosomas)):
            if(fitness(cromosomas[i],tot) > fitness(cromosomas[j],tot)):
                aux = cromosomas[j]
                cromosomas[j] = cromosomas[i]
                cromosomas[i] = aux

    indicesDeLosPadres = [None, None]

    totsum = 0
    for k in range(len(cromosomas)):
        totsum += k + 1

    for i in range(2):
        totRuleta = 0
        flecha = random.random()*100
        index = 0
        condicion = True
        while(condicion):
            totRuleta += ((index + 1)/totsum)*100
            if(totRuleta >= flecha and indicesDeLosPadres[0] != index):
                indicesDeLosPadres[i] = index
                condicion = False
            else:
                index += 1
    return indicesDeLosPadres

def ruleta_elite(cromosomas):
    tot = calcular_total(cromosomas)
    for i in range(len(cromosomas)):
        for j in range(i, len(cromosomas)):
            if(fitness(cromosomas[i],tot) > fitness(cromosomas[j],tot)):
                aux = cromosomas[j]
                cromosomas[j] = cromosomas[i]
                cromosomas[i] = aux
                                
    
def obtenerpadres(indices, cromosomes):   
    for i in range(2):
        padres = (cromosomes[indices[i-1]])
    return padres

#def crossover(padres, genes):
    num = random.randint(1,genes)
    for i in range(num):
        
    
#for i in range(ciclos):
cromosomes = create_population(genoma, poblacion)
padrecitos = ruleta_segun_rango(cromosomes)
padres = obtenerpadres(padrecitos, cromosomes)
#crossover(padres, genes)

   # print(cromosomes)
   # print("-----------------------------------------")
   # print(padrecitos)


   # torneo: 4 nors al azar