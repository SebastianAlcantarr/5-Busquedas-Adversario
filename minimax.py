"""
Modulo con el minimax con algunos los poderes

    1- Poda alfa-beta
    2- Ordenamiento de jugadas
    3- Evaluacion de estados
    4- Busqueda iterativa
    5- Tablas de transposicion
    6- Trazabilidad
"""
from random import shuffle
from time import time

def negamax(
    juego, estado, jugador,
    alpha=-1e10, beta=1e10, ordena=None, 
    d=None, evalua=None,
    transp={}, traza=[]
    ):
    """
    Devuelve la mejor jugada para el jugador en el estado
    
    Parametros
    ----------
    juego (ModeloJuegoZT): Modelo del juego
    estado (tuple): Estado del juego
    jugador (-1, 1): Jugador que realiza la jugada
    alpha (float): Limite inferior
    beta (float): Limite superior
    ordena (function:) Funcion de ordenamiento
        si None, ordena aleatoriamente
    d (int): Profundidad. 
        Si None, busca hasta el final
    evalua: function de evaluación
        Siempre evalua para el jugador 1
    transp (dict): Tabla de transposición
    traza (list): Trazabilidad
    
    Regresa
    -------
    tuple: (lista mejores jugadas, valor)
    
    """
    if d != None and evalua == None:
        raise ValueError("Se necesita evalua si d no es None")
    if type(ordena) != type(None) and type(ordena) != type(lambda x: x):
        raise ValueError("ordena debe ser una función")
    if type(evalua) != type(None) and type(evalua) != type(lambda x: x):
        raise ValueError("evalua debe ser una función")
    if type(transp) != dict:
        raise ValueError("transp debe ser un diccionario")
    if type(traza) != list: 
        raise ValueError("traza debe ser una lista")

    if juego.terminal(estado):
        return [], jugador * juego.ganancia(estado)
    if d == 0:
        return [], jugador * evalua(estado)
    if d != None and estado in transp and transp[estado][1] >= d:
        return [], transp[estado][0]
    
    v = -1e10
    jugadas = list(juego.jugadas_legales(estado, jugador))
    if ordena != None:
        jugadas = ordena(jugadas, jugador)
    else:
        shuffle(jugadas)
    if traza:
        a_pref = traza.pop(0)
        if a_pref in jugadas:
            jugadas = [a_pref] + [a for a in jugadas if a != a_pref]
    for a in jugadas:
        traza_actual, v2 = negamax(
            juego, juego.transicion(estado, a, jugador), -jugador, 
            -beta, -alpha, ordena, d if d == None else d - 1, 
            evalua, transp, traza
        )
        v2 = -v2
        if v2 > v:
            v = v2
            mejor = a
            mejores = traza_actual[:]

        if v >= beta:
            break

        if v > alpha:
            alpha = v

    transp[estado] = (v, d)

    return [mejor] + mejores, v 


def jugador_negamax(
    juego, estado, jugador, ordena=None, d=None, evalua=None
    ):
    """
    Funcion burrito para el negamax
    
    """
    traza, _ = negamax(
        juego=juego, estado=estado, jugador=jugador, 
        alpha=-1e10, beta=1e10, ordena=ordena, d=d, 
        evalua=evalua, transp={}, traza=[])
    return traza[0]


def minimax_iterativo(
    juego, estado, jugador, tiempo=10,
    ordena=None, d=None, evalua=None,
    ):  
    """
    Devuelve la mejor jugada para el jugador en el estado
    acotando a un periodo de tiempo
    
    """
    t0 = time()
    d, traza = 2, []
    while time() - t0 < tiempo/2:
        traza, v = negamax(
            juego=juego, estado=estado, jugador=jugador,  
            alpha=-1e10, beta=1e10, ordena=ordena, d=d, evalua=evalua, 
            transp={}, traza=traza
        )
        d += 1
    return traza[0]
