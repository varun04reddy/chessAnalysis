import chess
import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 400, 400
DIMENSION = 8  # chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations
IMAGES = {}


def load_images():
    piece_names = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
    for piece in piece_names:
        for color in ['black', 'white']:
            IMAGES[color + piece] = pygame.transform.scale(pygame.image.load(f"images/{color}{piece}.png"), (SQ_SIZE, SQ_SIZE))


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = chess.Board()
    load_images()  # only do this once
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()

def draw_game_state(screen, gs):
    draw_board(screen) 
    draw_pieces(screen, gs)  

def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, gs):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = gs.piece_at(chess.square(c, 7 - r)) 
            if piece:
                piece_color = 'white' if piece.color == chess.WHITE else 'black'
                piece_type = piece.piece_type
                piece_name = ''
                if piece_type == chess.PAWN:
                    piece_name = 'pawn'
                elif piece_type == chess.KNIGHT:
                    piece_name = 'knight'
                elif piece_type == chess.BISHOP:
                    piece_name = 'bishop'
                elif piece_type == chess.ROOK:
                    piece_name = 'rook'
                elif piece_type == chess.QUEEN:
                    piece_name = 'queen'
                elif piece_type == chess.KING:
                    piece_name = 'king'
                screen.blit(IMAGES[piece_color + piece_name], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
