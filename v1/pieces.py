# Implementations of the Piece class for each chess piece
from piece import Piece
import pygame

class Pawn(Piece):

    def __init__(self, color, pos, game):
        super().__init__(color, pos, game)
        self.icons = [ "♟", "♙"]
        self.name = "pawn"
        
    def get_legal_moves(self, ignore_check=False) -> list:
        (i,j) = self.pos
        moves = []
        
        # White pawn
        if self.color == "white":
            
            # If not going off the board
            if j - 1 >= 0:
                
                # If there is no piece in front of it
                if self.game.pieces[i][j - 1] == None:
                    moves.append((i, j - 1))
                    # If it hasn't moved yet, it can move two spaces
                    if j == 6 and self.game.pieces[i][j - 2] == None:
                        moves.append((i, j - 2))
                
                # If can capture to the left
                if i - 1 >= 0 and self.game.pieces[i - 1][j - 1] != None and self.game.pieces[i - 1][j - 1].color != self.color:
                    moves.append((i - 1, j - 1))
                    
                # If can capture to the right
                if i + 1 < 8 and self.game.pieces[i + 1][j - 1] != None and self.game.pieces[i + 1][j - 1].color != self.color:
                    moves.append((i + 1, j - 1))
                    
        # Black pawn
        else:
            
            # If not going off the board
            if j + 1 < 8:
                
                # If there is no piece in front of it
                if self.game.pieces[i][j + 1] == None:
                    moves.append((i, j + 1))
                    # If it hasn't moved yet, it can move two spaces
                    if j == 1 and self.game.pieces[i][j + 2] == None:
                        moves.append((i, j + 2))
                
                # If can capture to the left
                if i - 1 >= 0 and self.game.pieces[i - 1][j + 1] != None and self.game.pieces[i - 1][j + 1].color != self.color:
                    moves.append((i - 1, j + 1))
                    
                # If can capture to the right
                if i + 1 < 8 and self.game.pieces[i + 1][j + 1] != None and self.game.pieces[i + 1][j + 1].color != self.color:
                    moves.append((i + 1, j + 1))
                    
        # TODO: en passant

        if not ignore_check:            
            moves = self.remove_check_moves(moves)
                
        return moves           

class Rook(Piece):
    
    def __init__(self, color, pos, game):
        super().__init__(color, pos, game)
        self.icons = [ "♜", "♖"]
        self.name = "rook"

    def get_legal_moves(self, ignore_check=False) -> list:
        (i,j) = self.pos
        moves = []
        
        # Check all squares to the left
        temp_i = i
        while temp_i - 1 >= 0:
            temp_i -= 1
            if self.game.pieces[temp_i][j] == None:
                moves.append((temp_i, j))
            else:
                if self.game.pieces[temp_i][j].color != self.color:
                    moves.append((temp_i, j))
                break
            
        # Check all squares to the right
        temp_i = i
        while temp_i + 1 <= 7:
            temp_i += 1
            if self.game.pieces[temp_i][j] == None:
                moves.append((temp_i, j))
            else:
                if self.game.pieces[temp_i][j].color != self.color:
                    moves.append((temp_i, j))
                break
            
        # Check all squares above
        temp_j = j
        while temp_j - 1 >= 0:
            temp_j -= 1
            if self.game.pieces[i][temp_j] == None:
                moves.append((i, temp_j))
            else:
                if self.game.pieces[i][temp_j].color != self.color:
                    moves.append((i, temp_j))
                break
            
        # Check all squares below
        temp_j = j
        while temp_j + 1 <= 7:
            temp_j += 1
            if self.game.pieces[i][temp_j] == None:
                moves.append((i, temp_j))
            else:
                if self.game.pieces[i][temp_j].color != self.color:
                    moves.append((i, temp_j))
                break
            
        
        # TODO: check if king is in  check
        if not ignore_check:
            moves = self.remove_check_moves(moves)
        return moves

class Knight(Piece):
        
    def __init__(self, color, pos, game):
        super().__init__(color, pos, game)
        self.icons = [ "♞", "♘"]
        self.name = "knight"

    def get_legal_moves(self, ignore_check=False) -> list:
        (i,j) = self.pos
        moves = []
        
        # Up two, left one
        if i - 1 >= 0 and j - 2 >= 0:
            if self.game.pieces[i - 1][j - 2] == None or self.game.pieces[i - 1][j - 2].color != self.color:
                moves.append((i - 1, j - 2))
                
        # Up two, right one
        if i + 1 <= 7 and j - 2 >= 0:
            if self.game.pieces[i + 1][j - 2] == None or self.game.pieces[i + 1][j - 2].color != self.color:
                moves.append((i + 1, j - 2))
                
        # Up one, left two
        if i - 2 >= 0 and j - 1 >= 0:
            if self.game.pieces[i - 2][j - 1] == None or self.game.pieces[i - 2][j - 1].color != self.color:
                moves.append((i - 2, j - 1))
                
        # Up one, right two
        if i + 2 <= 7 and j - 1 >= 0:
            if self.game.pieces[i + 2][j - 1] == None or self.game.pieces[i + 2][j - 1].color != self.color:
                moves.append((i + 2, j - 1))
                
        # Down two, left one
        if i - 1 >= 0 and j + 2 <= 7:
            if self.game.pieces[i - 1][j + 2] == None or self.game.pieces[i - 1][j + 2].color != self.color:
                moves.append((i - 1, j + 2))
                
        # Down two, right one
        if i + 1 <= 7 and j + 2 <= 7:
            if self.game.pieces[i + 1][j + 2] == None or self.game.pieces[i + 1][j + 2].color != self.color:
                moves.append((i + 1, j + 2))
                
        # Down one, left two
        if i - 2 >= 0 and j + 1 <= 7:
            if self.game.pieces[i - 2][j + 1] == None or self.game.pieces[i - 2][j + 1].color != self.color:
                moves.append((i - 2, j + 1))
                
        # Down one, right two
        if i + 2 <= 7 and j + 1 <= 7:
            if self.game.pieces[i + 2][j + 1] == None or self.game.pieces[i + 2][j + 1].color != self.color:
                moves.append((i + 2, j + 1))
                
        
        # TODO: check if king is in  check
        if not ignore_check:
            moves = self.remove_check_moves(moves)
        return moves

class Bishop(Piece):

    def __init__(self, color, pos, game):
        super().__init__(color, pos, game)
        self.icons = [ "♝", "♗"]
        self.name = "bishop"

    def get_legal_moves(self, ignore_check=False) -> list:
        (i,j) = self.pos
        moves = []
        
        # Up left
        temp_i = i
        temp_j = j
        while temp_i - 1 >= 0 and temp_j - 1 >= 0:
            temp_i -= 1
            temp_j -= 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        # Up right
        temp_i = i
        temp_j = j
        while temp_i + 1 <= 7 and temp_j - 1 >= 0:
            temp_i += 1
            temp_j -= 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        # Down left
        temp_i = i
        temp_j = j
        while temp_i - 1 >= 0 and temp_j + 1 <= 7:
            temp_i -= 1
            temp_j += 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        # Down right
        temp_i = i
        temp_j = j
        while temp_i + 1 <= 7 and temp_j + 1 <= 7:
            temp_i += 1
            temp_j += 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        
        # TODO: check if king is in  check
        if not ignore_check:
            moves = self.remove_check_moves(moves)
        return moves

class Queen(Piece):

    def __init__(self, color, pos, game):
        super().__init__(color, pos, game)
        self.icons = [ "♛", "♕"]
        self.name = "queen"

    def get_legal_moves(self, ignore_check=False) -> list:
        (i,j) = self.pos
        moves = []
        
        # Up left
        temp_i = i
        temp_j = j
        while temp_i - 1 >= 0 and temp_j - 1 >= 0:
            temp_i -= 1
            temp_j -= 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        # Up right
        temp_i = i
        temp_j = j
        while temp_i + 1 <= 7 and temp_j - 1 >= 0:
            temp_i += 1
            temp_j -= 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        # Down left
        temp_i = i
        temp_j = j
        while temp_i - 1 >= 0 and temp_j + 1 <= 7:
            temp_i -= 1
            temp_j += 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        # Down right
        temp_i = i
        temp_j = j
        while temp_i + 1 <= 7 and temp_j + 1 <= 7:
            temp_i += 1
            temp_j += 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        # Up
        temp_i = i
        temp_j = j
        while temp_j - 1 >= 0:
            temp_j -= 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        # Down
        temp_i = i
        temp_j = j
        while temp_j + 1 <= 7:
            temp_j += 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        # Left
        temp_i = i
        temp_j = j
        while temp_i - 1 >= 0:
            temp_i -= 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        # Right
        temp_i = i
        temp_j = j
        while temp_i + 1 <= 7:
            temp_i += 1
            if self.game.pieces[temp_i][temp_j] == None:
                moves.append((temp_i, temp_j))
            else:
                if self.game.pieces[temp_i][temp_j].color != self.color:
                    moves.append((temp_i, temp_j))
                break
            
        
        # TODO: check if king is in  check
        if not ignore_check: 
           moves = self.remove_check_moves(moves)
        return moves
    
class King(Piece):

    def __init__(self, color, pos, game):
        super().__init__(color, pos, game)
        self.icons = [ "♚", "♔"]
        self.name = "king"

    def get_legal_moves(self, ignore_check=False) -> list:
        (i,j) = self.pos
        moves = []
        
        # Up left
        if i - 1 >= 0 and j - 1 >= 0:
            if self.game.pieces[i - 1][j - 1] == None:
                moves.append((i - 1, j - 1))
            else:
                if self.game.pieces[i - 1][j - 1].color != self.color:
                    moves.append((i - 1, j - 1))
            
        # Up
        if j - 1 >= 0:
            if self.game.pieces[i][j - 1] == None:
                moves.append((i, j - 1))
            else:
                if self.game.pieces[i][j - 1].color != self.color:
                    moves.append((i, j - 1))
            
        # Up right
        if i + 1 <= 7 and j - 1 >= 0:
            if self.game.pieces[i + 1][j - 1] == None:
                moves.append((i + 1, j - 1))
            else:
                if self.game.pieces[i + 1][j - 1].color != self.color:
                    moves.append((i + 1, j - 1))
            
        # Left
        if i - 1 >= 0:
            if self.game.pieces[i - 1][j] == None:
                moves.append((i - 1, j))
            else:
                if self.game.pieces[i - 1][j].color != self.color:
                    moves.append((i - 1, j))
            
        # Right
        if i + 1 <= 7:
            if self.game.pieces[i + 1][j] == None:
                moves.append((i + 1, j))
            else:
                if self.game.pieces[i + 1][j].color != self.color:
                    moves.append((i + 1, j))
            
        # Down left
        if i - 1 >= 0 and j + 1 <= 7:
            if self.game.pieces[i - 1][j + 1] == None:
                moves.append((i - 1, j + 1))
            else:
                if self.game.pieces[i - 1][j + 1].color != self.color:
                    moves.append((i - 1, j + 1))

        # Down
        if j + 1 <= 7:
            if self.game.pieces[i][j + 1] == None:
                moves.append((i, j + 1))
            else:
                if self.game.pieces[i][j + 1].color != self.color:
                    moves.append((i, j + 1))
            
        # Down right
        if i + 1 <= 7 and j + 1 <= 7:
            if self.game.pieces[i + 1][j + 1] == None:
                moves.append((i + 1, j + 1))
            else:
                if self.game.pieces[i + 1][j + 1].color != self.color:
                    moves.append((i + 1, j + 1))
            
        # Castling
        # TODO: implement
        
        
        # TODO: check if king is in  check
        if not ignore_check:
            moves = self.remove_check_moves(moves)
        return moves