# Abstract class for a chess piece

class Piece:

    def __init__(self, color, pos, game):
        self.color = color
        self.pos = pos
        self.game = game
        self.icons = None

    def get_legal_moves(self) -> list:
        pass
