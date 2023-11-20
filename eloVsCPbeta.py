import chess
import chess.pgn
import chess.engine
import pandas as pd
import matplotlib.pyplot as plt
import os

def evaluate_game(game, engine, player_name):
    board = game.board()
    centipawn_losses = []

    for move in game.mainline_moves():
        board.push(move)
        if board.turn == chess.WHITE and game.headers['White'] == player_name or \
           board.turn == chess.BLACK and game.headers['Black'] == player_name:
            info = engine.analyse(board, chess.engine.Limit(depth=20))
            score = info['score'].pov(board.turn).score(mate_score=1000)
            best_move = engine.play(board, chess.engine.Limit(depth=20)).move
            board.pop()
            best_score = engine.analyse(board, chess.engine.Limit(depth=20))['score'].pov(board.turn).score(mate_score=1000)
            centipawn_loss = abs(score - best_score)
            centipawn_losses.append(centipawn_loss)
            board.push(move)

    return centipawn_losses

def process_games(pgn_file_path, engine_path, player_name):
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    game_data = {'Date': [], 'ELO': [], 'ACPL': []}

    with open(pgn_file_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None or (game.headers['White'] != player_name and game.headers['Black'] != player_name):
                continue

            elo = int(game.headers['WhiteElo']) if game.headers['White'] == player_name else int(game.headers['BlackElo'])
            centipawn_losses = evaluate_game(game, engine, player_name)
            acpl = sum(centipawn_losses) / len(centipawn_losses) if centipawn_losses else 0
            
            game_data['Date'].append(game.headers['Date'])
            game_data['ELO'].append(elo)
            game_data['ACPL'].append(acpl)

    engine.quit()
    return pd.DataFrame(game_data)

def plot_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('ELO', color=color)
    ax1.plot(df['Date'], df['ELO'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('ACPL', color=color)  
    ax2.plot(df['Date'], df['ACPL'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  
    plt.show()

def main():
    pgn_file_path = '/varun/documents/chess/chessDB/user38Data/player_games.pgn'
    engine_path = 'varun/Documents/chess/engine/stockfish/15/bin/stockfish'
    player_name = 'Player38'

    df = process_games(pgn_file_path, engine_path, player_name)
    plot_data(df)

if __name__ == "__main__":
    main()
