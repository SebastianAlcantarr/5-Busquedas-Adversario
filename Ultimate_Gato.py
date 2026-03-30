"""Ultimate Tic-Tac-Toe con motor para minimax/negamax."""

from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from minimax import jugador_negamax
from minimax import minimax_iterativo

LINEAS_3X3 = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def ganador_3x3(tablero):
    """Regresa 1/-1 si alguien gano ese tablero de 3x3, si no 0."""
    for a, b, c in LINEAS_3X3:
        if tablero[a] == tablero[b] == tablero[c] != 0:
            return tablero[a]
    return 0


def _linea_puntaje(linea):
    """Puntaje heuristico de una linea de 3 casillas para jugador 1."""
    if 2 in linea:
        return 0
    c1 = linea.count(1)
    c2 = linea.count(-1)
    if c1 and c2:
        return 0
    if c1 == 3:
        return 150
    if c2 == 3:
        return -150
    if c1 == 2 and c2 == 0:
        return 18
    if c2 == 2 and c1 == 0:
        return -18
    if c1 == 1 and c2 == 0:
        return 3
    if c2 == 1 and c1 == 0:
        return -3
    return 0


def evalua_tablero_local(tablero):
    """Evalua un subtablero no terminal para el jugador 1."""
    ganador = ganador_3x3(tablero)
    if ganador:
        return 100 * ganador

    puntaje = 0
    for linea in LINEAS_3X3:
        puntaje += _linea_puntaje([tablero[i] for i in linea])

    # Preferencias posicionales simples.
    if tablero[4] == 1:
        puntaje += 4
    elif tablero[4] == -1:
        puntaje -= 4

    for i in (0, 2, 6, 8):
        if tablero[i] == 1:
            puntaje += 1
        elif tablero[i] == -1:
            puntaje -= 1
    return puntaje


class UltimateGato(ModeloJuegoZT2):
    """Modelo de Ultimate Tic-Tac-Toe sobre `ModeloJuegoZT2`."""

    def inicializa(self):
        tablero_global = tuple(9 * [0])
        tableros_locales = tuple(tuple(9 * [0]) for _ in range(9))
        sub_forzado = -1
        return (tablero_global, tableros_locales, sub_forzado), 1

    def jugadas_legales(self, s, j):
        tablero_global, tableros_locales, sub_forzado = s
        jugadas = []

        if sub_forzado != -1 and tablero_global[sub_forzado] == 0:
            for pos in range(9):
                if tableros_locales[sub_forzado][pos] == 0:
                    jugadas.append((sub_forzado, pos))
            return jugadas

        for sub in range(9):
            if tablero_global[sub] == 0:
                for pos in range(9):
                    if tableros_locales[sub][pos] == 0:
                        jugadas.append((sub, pos))
        return jugadas

    def transicion(self, s, a, j):
        tablero_global, tableros_locales, sub_forzado = s
        sub, pos = a
        legales = self.jugadas_legales(s, j)
        if (sub, pos) not in legales:
            raise ValueError(f"Jugada ilegal: {(sub, pos)}")

        nuevo_global = list(tablero_global)
        nuevos_locales = [list(tab) for tab in tableros_locales]
        nuevos_locales[sub][pos] = j

        ganador_local = ganador_3x3(nuevos_locales[sub])
        if ganador_local != 0:
            nuevo_global[sub] = ganador_local
        elif 0 not in nuevos_locales[sub]:
            nuevo_global[sub] = 2

        siguiente_forzado = pos if nuevo_global[pos] == 0 else -1

        return (
            tuple(nuevo_global),
            tuple(tuple(tab) for tab in nuevos_locales),
            siguiente_forzado,
        )

    def terminal(self, s):
        tablero_global, _, _ = s
        return ganador_3x3(tablero_global) != 0 or 0 not in tablero_global

    def ganancia(self, s):
        tablero_global, _, _ = s
        return ganador_3x3(tablero_global)


def evalua_ultimate(s):
    """Evalua el estado completo para el jugador 1."""
    tablero_global, tableros_locales, _ = s
    ganador_global = ganador_3x3(tablero_global)
    if ganador_global != 0:
        return 1_000_000 * ganador_global

    puntaje = 0

    # Prioriza estructura del metatablero.
    for linea in LINEAS_3X3:
        puntaje += 20 * _linea_puntaje([tablero_global[i] for i in linea])

    if tablero_global[4] == 1:
        puntaje += 60
    elif tablero_global[4] == -1:
        puntaje -= 60

    for i in (0, 2, 6, 8):
        if tablero_global[i] == 1:
            puntaje += 18
        elif tablero_global[i] == -1:
            puntaje -= 18

    # En subtableros abiertos, valora amenazas y control local.
    for sub in range(9):
        if tablero_global[sub] == 0:
            puntaje += evalua_tablero_local(tableros_locales[sub])
        elif tablero_global[sub] == 1:
            puntaje += 120
        elif tablero_global[sub] == -1:
            puntaje -= 120

    return puntaje


def ordena_ultimate(jugadas, jugador):
    prioridad = {4: 0, 0: 1, 2: 1, 6: 1, 8: 1, 1: 2, 3: 2, 5: 2, 7: 2}
    return sorted(jugadas, key=lambda a: (prioridad[a[0]], prioridad[a[1]]))


def pprint_gato_ultimate(s):
    """Imprime el tablero 9x9 agrupado por subtableros."""
    tablero_global, tableros_locales, sub_forzado = s

    def celda(v):
        return "X" if v == 1 else "O" if v == -1 else "."

    print(f"Subtablero forzado: {sub_forzado if sub_forzado != -1 else 'libre'}")
    print("Estado del metatablero (X/O ganados, # empatado):")
    meta = ["X" if v == 1 else "O" if v == -1 else "#" if v == 2 else "." for v in tablero_global]
    for r in range(3):
        print(" ".join(meta[3 * r:3 * (r + 1)]))

    print("\nTableros locales:")
    for bloque_fila in range(3):
        for fila_local in range(3):
            partes = []
            for bloque_col in range(3):
                sub = 3 * bloque_fila + bloque_col
                base = 3 * fila_local
                partes.append(" ".join(celda(v) for v in tableros_locales[sub][base:base + 3]))
            print(" || ".join(partes))
        if bloque_fila != 2:
            print("=" * 29)


def jugador_manual_ultimate(juego, s, j):
    """Jugador manual para Ultimate Tic-Tac-Toe."""
    print("\nEstado actual:")
    pprint_gato_ultimate(s)
    jugadas = list(juego.jugadas_legales(s, j))
    print("Jugador:", "X" if j == 1 else "O")
    print("Jugadas legales (sub, pos):", jugadas)

    while True:
        try:
            texto = input("Jugada 'sub pos': ").strip()
            sub_s, pos_s = texto.split()
            jugada = (int(sub_s), int(pos_s))
            if jugada in jugadas:
                return jugada
        except Exception:
            pass
        print("Entrada invalida. Intenta de nuevo.")


def jugador_negamax_profundo(d):
    return lambda juego, s, j: jugador_negamax(
        juego, s, j, ordena=ordena_ultimate, d=d, evalua=evalua_ultimate
    )


def jugador_negamax_tiempo(t):
    return lambda juego, s, j: minimax_iterativo(
        juego, s, j, tiempo=t, ordena=ordena_ultimate, evalua=evalua_ultimate
    )


if __name__ == '__main__':
    modelo = UltimateGato()
    print("=" * 44)
    print("ULTIMATE TIC-TAC-TOE".center(44))
    print("=" * 44)

    jugs = []
    for j in [1, -1]:
        print(f"\nSeleccion de jugador para {'X' if j == 1 else 'O'}:")
        print(" 1. Jugador manual")
        print(" 2. IA negamax (profundidad fija)")
        print(" 3. IA negamax (tiempo)")

        sel = 0
        while sel not in [1, 2, 3]:
            sel = int(input("Opcion: "))

        if sel == 1:
            jugs.append(jugador_manual_ultimate)
        elif sel == 2:
            d = 0
            while d < 1:
                d = int(input("Profundidad (>=1): "))
            jugs.append(jugador_negamax_profundo(d))
        else:
            t = 0
            while t < 1:
                t = int(input("Tiempo por jugada en segundos (>=1): "))
            jugs.append(jugador_negamax_tiempo(t))

    g, s_final = juega_dos_jugadores(modelo, jugs[0], jugs[1])
    print("\nSE ACABO EL JUEGO\n")
    pprint_gato_ultimate(s_final)
    if g == 1:
        print("\nGana X")
    elif g == -1:
        print("\nGana O")
    else:
        print("\nEmpate")
