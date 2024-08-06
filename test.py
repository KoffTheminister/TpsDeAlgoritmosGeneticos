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

def generar_exhaustiva():
    for i in range(1025):
        numfin = list()
        binario_sin_prefijo = bin(i)[2:]
        #num = str(binario_sin_prefijo)
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

generar_exhaustiva()
print(listas)