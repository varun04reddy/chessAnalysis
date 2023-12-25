import chess
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 550, 400  
SCOREBOARD_WIDTH = 150  
DIMENSION = 8  
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30  
IMAGES = {}
HIGHLIGHT_COLOR = pygame.Color('yellow')

white_wins = 0
black_wins = 0

reset_button = {
    "x": WIDTH // 2 - 100,
    "y": HEIGHT // 2 + 50,
    "width": 200,
    "height": 50,
    "text": "Play Again"
}


def load_images():
    piece_names = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
    for piece in piece_names:
        for color in ['black', 'white']:
            IMAGES[color + piece] = pygame.transform.scale(pygame.image.load(f"images/{color}{piece}.png"), (SQ_SIZE, SQ_SIZE))

def main():
    global white_wins, black_wins
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    gs = chess.Board()
    load_images()  
    running = True
    sq_selected = () 
    player_clicks = []  # Keeps track of player clicks [(6, 4), (4, 4)]
    game_over = False

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sq_selected == (row, col): 
                        sq_selected = () 
                        player_clicks = []  
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)  
                    if len(player_clicks) == 2:  
                        move = chess.Move.from_uci(chess.square_name(chess.square(player_clicks[0][1], 7 - player_clicks[0][0])) + chess.square_name(chess.square(player_clicks[1][1], 7 - player_clicks[1][0])))
                        if move in list(gs.legal_moves):
                            gs.push(move)
                            if gs.is_checkmate():
                                game_over = True
                                if gs.turn: 
                                    black_wins += 1
                                else:
                                    white_wins += 1
                        sq_selected = ()  # Reset user clicks
                        player_clicks = []

        draw_game_state(screen, gs)
        if sq_selected and not game_over:
            highlight_moves(screen, gs, list(gs.legal_moves), sq_selected)

        if game_over:
           show_endgame_screen(screen, gs.turn)
           for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    if reset_button["x"] <= location[0] <= reset_button["x"] + reset_button["width"] and reset_button["y"] <= location[1] <= reset_button["y"] + reset_button["height"]:
                        # Reset the game
                        gs = chess.Board()
                        game_over = False
                        sq_selected = ()
                        player_clicks = []

        pygame.display.flip()
        clock.tick(MAX_FPS)




def draw_game_state(screen, gs):
    draw_board(screen) 
    draw_pieces(screen, gs)
    draw_scoreboard(screen)  

def draw_scoreboard(screen):
    pygame.draw.rect(screen, pygame.Color("white"), (WIDTH - SCOREBOARD_WIDTH, 0, SCOREBOARD_WIDTH, HEIGHT))
    font = pygame.font.SysFont("Arial", 24)
    text_color = pygame.Color("Black")

    # Display the scores
    white_score_text = font.render(f"Black Wins: {black_wins}", True, text_color)
    black_score_text = font.render(f"White Wins: {white_wins}", True, text_color)

    screen.blit(white_score_text, (WIDTH - SCOREBOARD_WIDTH + 10, 20))
    screen.blit(black_score_text, (WIDTH - SCOREBOARD_WIDTH + 10, 350))


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


def highlight_moves(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.piece_at(chess.square(c, 7 - r)) is not None:  
            s = pygame.Surface((SQ_SIZE, SQ_SIZE)) 
            s.set_alpha(100)  
            s.fill(HIGHLIGHT_COLOR)
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))  
            
            for move in valid_moves:
                if move.from_square == chess.square(c, 7 - r):
                    end_row, end_col = 7 - chess.square_rank(move.to_square), chess.square_file(move.to_square)
                    screen.blit(s, (end_col * SQ_SIZE, end_row * SQ_SIZE))

def show_endgame_screen(screen, winner):
    font = pygame.font.SysFont("Arial", 32)
    reset_font = pygame.font.SysFont("Arial", 24)
    text_color = pygame.Color("Black")

    # Display the winner
    if winner:
        text = font.render("Black wins!", True, text_color)
    else:
        text = font.render("White wins!", True, text_color)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    # Draw the reset button
    pygame.draw.rect(screen, pygame.Color("black"), (reset_button["x"], reset_button["y"], reset_button["width"], reset_button["height"]))
    reset_text = reset_font.render(reset_button["text"], True, "white")
    screen.blit(reset_text, (reset_button["x"] + reset_button["width"] // 2 - reset_text.get_width() // 2, reset_button["y"] + reset_button["height"] // 2 - reset_text.get_height() // 2))

    pygame.display.flip()


if __name__ == "__main__":
    main()
