tablaDeValores = [[150, 20], [325, 40], [600, 50], [805, 36], [430, 25], [1200, 64], [770, 54], [60, 18], [930, 46], [353, 28]]
numero_de_items = len(tablaDeValores)
volMaximo = 4200
listasPosibles = []
listas = []
elementos = []
cont_tot = 0


def precio_total(lista):
    tot = 0
    for i in range(len(lista)):
        if(lista[i] == '1'):
            tot += tablaDeValores[i][1]
    return tot

def vol_total(lista):
    tot = 0
    for i in range(len(lista)):
        if(lista[i] == '1'):
            tot += tablaDeValores[i][0]
    return tot

def ordenamiento(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if precio_total(arr[j]) > precio_total(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

#Exaustiva
def generar_exhaustiva():
    for i in range(1025):
        numfin=list()
        binario_sin_prefijo = bin(i)[2:]
        num = str(binario_sin_prefijo)
        num = list(binario_sin_prefijo)
        largo = 10 - len(num)
        if (largo > 0):
          for j in range(largo):
            numfin.append('0')
          for k in range(10-largo):
            numfin.append(num[k])
        else:
            numfin= num
        if(vol_total(num) <= volMaximo):
            listasPosibles.append(numfin)
        listas.append(numfin)

def armar_listas_de_objetos(lista):
    listas_de_objetos = []
    totales = []

    for elemento in lista:
        objetos = []
        total_volumen = 0
        total_precio = 0
        
        for j in range(10):
            if (elemento[j] == '1'):
                objetos.append(tablaDeValores[j])
                total_volumen += tablaDeValores[j][0]
                total_precio += tablaDeValores[j][1]
        
        listas_de_objetos.append(objetos)
        totales.append((total_volumen, total_precio))

    return listas_de_objetos, totales



#Greedy
def valorProporcional():
    valoresProporcionales = []
    for i in range(len(tablaDeValores)):
       valoresProporcionales.append([i, tablaDeValores[i][1]/tablaDeValores[i][0]])
   
    #ordenamiento
    n = len(valoresProporcionales)
    for i in range(n):
        for j in range(0, n - i - 1):
            if (valoresProporcionales[j][1] > valoresProporcionales[j + 1][1]):
                valoresProporcionales[j], valoresProporcionales[j + 1] = valoresProporcionales[j + 1], valoresProporcionales[j]
            
    lock = True
    indice = 0
    lista = ['0','0','0','0','0','0','0','0','0','0']
    while (lock):
        lista[valoresProporcionales[indice][0]] = '1'
        if(vol_total(lista) <= volMaximo):
            indice += 1
        else:
            lista[valoresProporcionales[indice][0]] = '0'
            lock = False

    return lista   

def armar_listas_de_objeto_greedy(lista):
    listas_de_objetos = []
    totales = []
    total_volumen = 0
    total_precio = 0

    for i in range(len(lista)):
        objetos = []
        if (lista[i] == '1'):
            objetos.append(tablaDeValores[i])
            total_volumen += tablaDeValores[i][0]
            total_precio += tablaDeValores[i][1]
        
        listas_de_objetos.append(objetos)
    totales.append((total_volumen, total_precio))

    return listas_de_objetos, totales



#exhaustivo
generar_exhaustiva()

ordenamiento(listas)
ordenamiento(listasPosibles)

listas_de_objetos, totales = armar_listas_de_objetos(listas)

print('exhaustiva')
print('Todas las listas posibles:')
for i, (lista_objetos, total) in enumerate(zip(listas_de_objetos, totales)):
    print(f"Lista {i + 1}: {lista_objetos} - Volumen Total: {total[0]}, Precio Total: {total[1]}")

#greedy
listas_de_objetos, totales = armar_listas_de_objeto_greedy(valorProporcional())
print('')
print('')
print('')
print('')
print('Greedy')
print('lista: ', listas_de_objetos, ' - Volumen Total ', totales[0][0], ' - Valor Total ', totales[0][1])
print()