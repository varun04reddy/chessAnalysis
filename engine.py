import chess
import chess.engine


engine = chess.engine.SimpleEngine.popen_uci("C:\\Users\\varun\\UVA CS\\personal projects\\chess\\chessAnalysis\\stockfish\\stockfish-windows-x86-64-avx2.exe")

print("hello world")



class Engine:

    
    def __init__(self, engine_path):
        self.engine_path = engine_path
        self.engine = None

    def start_engine(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)

    def make_move(self, board):
        if not board.is_game_over():
            result = self.engine.play(board, chess.engine.Limit(time=0.1))
            return result.move
        return None

    def close_engine(self):
        if self.engine:
            self.engine.quit()
