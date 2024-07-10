tablaDeValores = [[150, 20], [325, 40], [600, 50], [805, 36], [430, 25], [1200, 64], [770, 54], [60, 18], [930, 46], [353, 28]]
numero_de_items = len(tablaDeValores)
volMaximo = 4200
listasPosibles = []
cont_tot = 0

def precio_total(lista):
    tot = 0
    for i in range(len(lista)):
        tot += tablaDeValores[lista[i],1]
    return tot

def vol_total(lista):
    tot = 0
    for i in range(len(lista)):
        tot += tablaDeValores[lista[i],0]
    return tot

def agregar_o_no(lista):
    i = 0
    lock = True
    while (lock and i < len(listasPosibles)):
        lock2 = True
        i2 = 0
        while (lock2 == True and i2 < len(listasPosibles[i])):
            if (repeticion_de_item(lista[i2],listasPosibles[i]) == False):
                i2 += 1
            else:
                lock2 = False
        if(lock2):
            lock = False
        else:
            i += 1
    if(lock == True):
        listasPosibles.append(lista)

def repeticion_de_item(index, lista):
    i = 0
    while (i < len(lista)):
        if(index == lista[i]):
            return True
        else:
            i += 1
    return False


def funcion(passed_aux): #no se me ocurrio ningun otro nombre xd
    my_aux = passed_aux.copy()
    cont_de_inhabilidades = 0
    for j in range(numero_de_items):
        indice_repetido = repeticion_de_item(j, my_aux)
        if(indice_repetido == False):
            my_aux.append(j)
            if(vol_total(my_aux) > volMaximo):
                cont_de_inhabilidades += 1
                my_aux.pop(len(my_aux) - 1)
            else:
                me_agrego = funcion(my_aux)
                if(me_agrego == numero_de_items):
                    agregar_o_no(my_aux)
        else:
            cont_de_inhabilidades += 1
        return cont_de_inhabilidades
