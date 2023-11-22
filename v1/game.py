# Class representing a game of chess

from piece import Piece
from pieces import *

class Game:
    
    def __init__(self, game=None):
        
        if game is not None:
            self.turn = game.turn
            self.pieces = [[None for i in range(8)] for j in range(8)]
            for i in range(8):
                for j in range(8):
                    piece = game.pieces[i][j]
                    if piece is not None:
                        if piece.name == "pawn":
                            self.pieces[i][j] = Pawn(piece.color, piece.pos, self)
                        elif piece.name == "rook":
                            self.pieces[i][j] = Rook(piece.color, piece.pos, self)
                        elif piece.name == "knight":
                            self.pieces[i][j] = Knight(piece.color, piece.pos, self)
                        elif piece.name == "bishop":
                            self.pieces[i][j] = Bishop(piece.color, piece.pos, self)
                        elif piece.name == "queen":
                            self.pieces[i][j] = Queen(piece.color, piece.pos, self)
                        elif piece.name == "king":
                            self.pieces[i][j] = King(piece.color, piece.pos, self)
                            
            self.result = game.result
            return
        
        self.turn = "white"
        self.pieces = [[None for i in range(8)] for j in range(8)]
        self.result = None
        
        # Initialize the board
        self.pieces[0][0] = Rook("black", (0, 0), self)
        self.pieces[1][0] = Knight("black", (1, 0), self)
        self.pieces[2][0] = Bishop("black", (2, 0), self)
        self.pieces[3][0] = Queen("black", (3, 0), self)
        self.pieces[4][0] = King("black", (4, 0), self)
        self.pieces[5][0] = Bishop("black", (5, 0), self)
        self.pieces[6][0] = Knight("black", (6, 0), self)
        self.pieces[7][0] = Rook("black", (7, 0), self)
        self.pieces[0][7] = Rook("white", (0, 7), self)
        self.pieces[1][7] = Knight("white", (1, 7), self)
        self.pieces[2][7] = Bishop("white", (2, 7), self)
        self.pieces[3][7] = Queen("white", (3, 7), self)
        self.pieces[4][7] = King("white", (4, 7), self)
        self.pieces[5][7] = Bishop("white", (5, 7), self)
        self.pieces[6][7] = Knight("white", (6, 7), self)
        self.pieces[7][7] = Rook("white", (7, 7), self)
        
        for i in range(8):
            self.pieces[i][1] = Pawn("black", (i, 1), self)
            self.pieces[i][6] = Pawn("white", (i, 6), self)
        
        
    def get_piece(self, pos) -> Piece:
        (i,j) = pos
        return self.pieces[i][j]
    
    def is_checkmate(self) -> bool:
        # If the current player has no legal moves and the king is in check, it is checkmate
        return not self.has_legal_moves() and self.is_in_check(self.turn)
    
    def is_stalemate(self) -> bool:
        # If the current player has no legal moves and the king is not in check, it is stalemate
        return not self.has_legal_moves() and not self.is_in_check(self.turn)
    
    def move_piece(self, pos1, pos2, ignore_check=False):
        # Get the piece
        piece = self.get_piece(pos1)
        
        # Make sure the piece is not empty
        if piece is None:
            return
        
        # Make sure the move is legal
        if pos2 not in piece.get_legal_moves(ignore_check=ignore_check):
            return
        
        # Move the piece
        piece.pos = pos2
        self.pieces[pos1[0]][pos1[1]] = None
        self.pieces[pos2[0]][pos2[1]] = piece
        
        # TODO: Check for promotion
        
        # Check for checkmate
        if not ignore_check and self.is_checkmate():
            self.result = "1-0" if self.turn == "white" else "0-1"
            
        # Check for stalemate
        if not ignore_check and self.is_stalemate():
            self.result = "1/2-1/2"
        
        # Change the turn
        self.turn = "black" if self.turn == "white" else "white"
        
    def has_legal_moves(self) -> bool:
        for i in range(8):
            for j in range(8):
                piece = self.get_piece((i,j))
                if piece is not None and piece.color == self.turn:
                    if len(piece.get_legal_moves()) > 0:
                        return True
                    
    def is_in_check(self, color) -> bool:
        # In check if the king is in the list of legal moves of any of the opponent's pieces
        
        # Find the king
        king = None
        for i in range(8):
            for j in range(8):
                piece = self.get_piece((i,j))
                if piece is not None and piece.color == color and piece.name == "king":
                    king = piece
                    break
                
        # Check if the king is in the list of legal moves of any of the opponent's pieces
        for i in range(8):
            for j in range(8):
                piece = self.get_piece((i,j))
                if piece is not None and color != self.turn and king.pos in piece.get_legal_moves(ignore_check=True):
                    return True
                    
        return False
    
    def would_be_check(self, piece, moving_to):
        game_copy = Game(self)
        game_copy.move_piece(piece.pos, moving_to, ignore_check=True)
        return game_copy.is_in_check(self.turn)
        
        
    