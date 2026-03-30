import pygame
import pygame.freetype
import sys
from Ultimate_Gato import UltimateGato, jugador_negamax_profundo

# --- Configuración visual ---
ANCHO, ALTO = 620, 670
MARGEN = 20
CELDA_GRANDE = 185
CELDA_CHICA = 55
RELLENO = 7

FONDO         = (26, 26, 46)
LINEA_GRANDE  = (0, 0, 0)
LINEA_CHICA   = (0, 0, 0)
COLOR_X       = (79, 142, 247)
COLOR_O       = (232, 64, 64)
COLOR_TEXTO   = (255, 255, 255)
COLOR_ACTIVO  = (44, 122, 21)


def dibujar_cuadricula(pantalla, ox, oy, celda, grosor, color):
    total = celda * 3
    for i in range(1, 3):
        x = ox + i * celda
        pygame.draw.line(pantalla, color, (x, oy), (x, oy + total), grosor)
        y = oy + i * celda
        pygame.draw.line(pantalla, color, (ox, y), (ox + total, y), grosor)


def dibujar_fichas(pantalla, fuente, fuente_chica, ox, oy, celda, indice_sub, sub):
    for fila in range(3):
        for col in range(3):
            val = sub[fila * 3 + col]
            cx = ox + col * celda + celda // 2
            cy = oy + fila * celda + celda // 2
            if val == 1:
                surf, rect = fuente.render("X", COLOR_X)
            elif val == -1:
                surf, rect = fuente.render("O", COLOR_O)
            else:
                surf, rect = fuente_chica.render(str(fila * 3 + col), (170, 170, 170))
            rect.center = (cx, cy)
            pantalla.blit(surf, rect)

    # Poner Indices
    surf, rect = fuente_chica.render(str(indice_sub), (225, 225, 225))
    rect.topleft = (ox + 2, oy + 1)
    pantalla.blit(surf, rect)


def dibujar_estado(pantalla, fuente_chica, juego, estado, turno):
    if juego.terminal(estado):
        g = juego.ganancia(estado)
        texto = "Gana X" if g == 1 else "Gana O" if g == -1 else "Empate"
    else:
        texto = f"Turno: {'X' if turno == 1 else 'O'}"
    surf, rect = fuente_chica.render(texto, COLOR_TEXTO)
    rect.topleft = (MARGEN, ALTO - 38)
    pantalla.blit(surf, rect)


def dibujar_activos(pantalla, estado):
    tablero_global, _, sub_forzado = estado
    jugables = [sub_forzado] if sub_forzado != -1 and tablero_global[sub_forzado] == 0 \
               else [i for i, v in enumerate(tablero_global) if v == 0]
    for sub in jugables:
        bc, br = sub % 3, sub // 3
        ox = MARGEN + bc * CELDA_GRANDE + RELLENO
        oy = MARGEN + br * CELDA_GRANDE + RELLENO
        lado = CELDA_CHICA * 3
        pygame.draw.rect(pantalla, COLOR_ACTIVO, (ox - 3, oy - 3, lado + 6, lado + 6), 4)


def clic_a_jugada(mx, my):
    bc = (mx - MARGEN) // CELDA_GRANDE
    br = (my - MARGEN) // CELDA_GRANDE
    if bc not in range(3) or br not in range(3):
        return None
    ox = MARGEN + bc * CELDA_GRANDE + RELLENO
    oy = MARGEN + br * CELDA_GRANDE + RELLENO
    total = CELDA_CHICA * 3
    if not (ox <= mx < ox + total and oy <= my < oy + total):
        return None
    col = (mx - ox) // CELDA_CHICA
    fila = (my - oy) // CELDA_CHICA
    return (br * 3 + bc, fila * 3 + col)


def main():
    pygame.init()
    pygame.freetype.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Gato Ultimate")

    fuente       = pygame.freetype.SysFont("monospace", 36, bold=True)
    fuente_chica = pygame.freetype.SysFont("monospace", 20)
    reloj        = pygame.time.Clock()

    juego = UltimateGato()
    estado, turno = juego.inicializa()
    humano = 1
    ia = jugador_negamax_profundo(2)
    espera_ia = 1000
    tiempo_ia = None

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
                    and not juego.terminal(estado) and turno == humano):
                jugada = clic_a_jugada(*evento.pos)
                if jugada and jugada in juego.jugadas_legales(estado, turno):
                    estado = juego.transicion(estado, jugada, turno)
                    turno = -turno
                    tiempo_ia = pygame.time.get_ticks()

        if not juego.terminal(estado) and turno != humano:
            ahora = pygame.time.get_ticks()
            if tiempo_ia is None:
                tiempo_ia = ahora
            if ahora - tiempo_ia >= espera_ia:
                estado = juego.transicion(estado, ia(juego, estado, turno), turno)
                turno = -turno
                tiempo_ia = None

        pantalla.fill(FONDO)
        dibujar_cuadricula(pantalla, MARGEN, MARGEN, CELDA_GRANDE, 6, LINEA_GRANDE)
        if not juego.terminal(estado):
            dibujar_activos(pantalla, estado)

        for br in range(3):
            for bc in range(3):
                ox = MARGEN + bc * CELDA_GRANDE + RELLENO
                oy = MARGEN + br * CELDA_GRANDE + RELLENO
                sub = 3 * br + bc
                dibujar_cuadricula(pantalla, ox, oy, CELDA_CHICA, 3, LINEA_CHICA)
                dibujar_fichas(pantalla, fuente, fuente_chica, ox, oy, CELDA_CHICA, sub, estado[1][sub])

        dibujar_estado(pantalla, fuente_chica, juego, estado, turno)
        pygame.display.flip()
        reloj.tick(60)


if __name__ == "__main__":
    main()