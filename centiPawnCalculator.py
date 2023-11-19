import chess
import chess.engine
import chess.pgn
from datetime import datetime
import pandas as pd
from tqdm import tqdm
import logging

# Set up logging
logging.basicConfig(filename='chess_analysis.log', level=logging.INFO)

def initialize_engine(engine_path):
    return chess.engine.SimpleEngine.popen_uci(engine_path)

def read_games_from_pgn(file_path):
    with open(file_path) as file:
        return [game for game in chess.pgn.read_game(file) if game is not None]

def evaluate_position(board, engine, limit):
    try:
        info = engine.analyse(board, limit)
        return info['score'].white().score(mate_score=1000)
    except Exception as e:
        logging.error(f"Error evaluating position: {e}")
        return None

def calculate_centipawn_loss(game, engine, limit):
    board = game.board()
    evaluations = [evaluate_position(board, engine, limit)]

    for move in game.mainline_moves():
        board.push(move)
        evaluations.append(evaluate_position(board, engine, limit))

    return [max(min(eval, 1000), -1000) for eval in evaluations if eval is not None]

def calculate_average_loss(evaluations):
    centipawn_loss_list = []
    for i in range(1, len(evaluations)):
        loss = evaluations[i - 1] - evaluations[i] if i % 2 != 0 else evaluations[i] - evaluations[i - 1]
        centipawn_loss_list.append(max(loss, 0))
    return round(sum(centipawn_loss_list) / len(centipawn_loss_list)) if centipawn_loss_list else 0

def create_game_dataframe(game, evaluations, depth):
    game_data = {
        "Date": datetime.strptime(game.headers["Date"], "%Y.%m.%d"),
        "Event Name": game.headers["Event"],
        "Event Rounds": game.headers["EventRounds"],
        "Round": game.headers["Round"],
        "Moves": len(game.mainline_moves()),
        "White Av CP Loss": calculate_average_loss(evaluations[::2]),
        "Black Av CP Loss": calculate_average_loss(evaluations[1::2]),
        "Evaluations List": evaluations,
        "PGN": game.accept(chess.pgn.StringExporter(headers=True, variations=True, comments=True)),
        "Analysis Depth": depth,
        "White Name": game.headers["White"],
        "Black Name": game.headers["Black"],
        "Result": game.headers["Result"],
        "White ELO": game.headers.get("WhiteElo", ""),
        "Black ELO": game.headers.get("BlackElo", "")
    }
    return pd.DataFrame([game_data])

def main():
    start_time = datetime.now()

    engine_path = 'varun/Documents/chess/engine/stockfish/15/bin/stockfish'
    pgn_file_path = 'db.pgn'
    analysis_depth = 20
    time_limit = 999
    limit = chess.engine.Limit(time=time_limit, depth=analysis_depth)

    engine = initialize_engine(engine_path)
    games = read_games_from_pgn(pgn_file_path)
    final_df = pd.DataFrame()

    for game in tqdm(games):
        try:
            evaluations = calculate_centipawn_loss(game, engine, limit)
            game_df = create_game_dataframe(game, evaluations, analysis_depth)
            final_df = pd.concat([final_df, game_df])
        except Exception as e:
            logging.error(f"Error processing game: {e}")

    final_df.to_pickle('chess_analysis_results.pkl')
    engine.quit()

    finish_time = datetime.now()
    logging.info(f'Analysis completed! Duration: {finish_time - start_time}')

if __name__ == "__main__":
    main()
