# Abstract class for a chess piece

class Piece:

    def __init__(self, color, pos, game):
        self.color = color
        self.pos = pos
        self.game = game
        self.icons = None

    def get_legal_moves(self, ignore_check=False) -> list:
        pass
    
    def remove_check_moves(self, moves) -> list:
        # Remove moves that would put the king in check
        for move in moves:
            if self.game.would_be_check(self, move):
                moves.remove(move)
        return moves
