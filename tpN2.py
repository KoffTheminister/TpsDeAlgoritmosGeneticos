tablaDeValores = [[150, 20], [325, 40], [600, 50], [805, 36], [430, 25], [1200, 64], [770, 54], [60, 18], [930, 46], [353, 28]]
numero_de_items = len(tablaDeValores)
volMaximo = 4200
listasPosibles = []
listas = []
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

def generar_exhaustiva():
    for i in range(1025):
        binario_sin_prefijo = bin(i)[2:]
        num = str(binario_sin_prefijo)
        num = list(binario_sin_prefijo)
        largo = 10 - len(num)
        if (largo > 0):
          for j in range(largo):
            num.append('0')
        if(vol_total(num) <= volMaximo):
            listasPosibles.append(num)
        listas.append(num)

def buscarElementos(lista):
    Elementos = []
    for i in range(len(lista)):
        for j in range(10):
            if lista[j] == '1':
                Elementos.append(tablaDeValores[j,0],tablaDeValores[j,1])

                
generar_exhaustiva()
ordenamiento(listas)
ordenamiento(listasPosibles)

print('todas las listas:')
print(listas)
print('')
print('')
print('')
print('')
print('todas las listas posibles:')
print(listasPosibles)
