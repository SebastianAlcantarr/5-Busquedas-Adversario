import pygame
import pygame.freetype
import sys

# --- Configuración ---
WIDTH, HEIGHT = 620, 670
MARGIN = 20
BIG_CELL = 185       # tamaño celda del tablero grande
SMALL_CELL = 55      # tamaño celda de cada sub-tablero
PADDING = 7          # espacio interno entre borde de celda grande y sub-tablero

BG_COLOR      = 16, 122, 19
BIG_LINE_COLOR   = (0, 0,0)
SMALL_LINE_COLOR = (0, 0,0)
X_COLOR       = (255, 255,255)
O_COLOR       = (255, 255,255)
TEXT_COLOR    = (200, 200, 200)

big_board = [
    [
        [[1, 2, 0], [0, 1, 0], [0, 0, 2]],
        [[0, 0, 1], [2, 0, 0], [0, 1, 0]],
        [[0, 0, 0], [0, 2, 0], [1, 0, 0]],
    ],
    [
        [[2, 0, 0], [0, 1, 2], [0, 0, 1]],
        [[1, 0, 2], [0, 1, 0], [2, 0, 1]],
        [[0, 1, 0], [0, 0, 2], [1, 0, 0]],
    ],
    [
        [[0, 0, 2], [1, 0, 0], [0, 2, 1]],
        [[1, 0, 0], [0, 2, 1], [0, 0, 0]],
        [[2, 1, 0], [0, 0, 1], [2, 0, 0]],
    ],
]

def draw_grid(screen, ox, oy, cell_size, line_width, color):
    total = cell_size * 3
    for i in range(1, 3):
        x = ox + i * cell_size
        pygame.draw.line(screen, color, (x, oy), (x, oy + total), line_width)
    for i in range(1, 3):
        y = oy + i * cell_size
        pygame.draw.line(screen, color, (ox, y), (ox + total, y), line_width)

def draw_pieces(screen, font, ox, oy, cell_size, sub_board):
    for row in range(3):
        for col in range(3):
            val = sub_board[row][col]
            cx = ox + col * cell_size + cell_size // 2
            cy = oy + row * cell_size + cell_size // 2
            if val == 1:
                surf, rect = font.render("X", X_COLOR)
                rect.center = (cx, cy)
                screen.blit(surf, rect)
            elif val == 2:
                surf, rect = font.render("O", O_COLOR)
                rect.center = (cx, cy)
                screen.blit(surf, rect)

def draw_status(screen, small_font):
    surf, rect = small_font.render("Turno de: X  |  Jugar en: sub-tablero 5", TEXT_COLOR)
    rect.topleft = (MARGIN, HEIGHT - 38)
    screen.blit(surf, rect)

def main():
    pygame.init()
    pygame.freetype.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ultimate Tic Tac Toe - Visual")

    piece_font = pygame.freetype.SysFont("monospace", 36, bold=True)
    small_font  = pygame.freetype.SysFont("monospace", 20)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BG_COLOR)

        # Tablero grande
        draw_grid(screen, MARGIN, MARGIN, BIG_CELL, 6, BIG_LINE_COLOR)

        # Sub-tableros dentro de cada celda
        for br in range(3):
            for bc in range(3):
                ox = MARGIN + bc * BIG_CELL + PADDING
                oy = MARGIN + br * BIG_CELL + PADDING
                draw_grid(screen, ox, oy, SMALL_CELL, 3, SMALL_LINE_COLOR)
                draw_pieces(screen, piece_font, ox, oy, SMALL_CELL, big_board[br][bc])

        draw_status(screen, small_font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()