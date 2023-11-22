from colorama import Fore, Back, Style

BLACK_TEXT = ["♟", "♞", "♝", "♜", "♛", "♚"]
WHITE_TEXT = ["♙", "♘", "♗", "♖", "♕", "♔"]
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Game:
    """Represents a game of chess. This includes the board, the pieces, the moves, and the PGN tags."""
    
    # Below are some helpful tips for understanding how the board is represented.
    # Also see https://www.chessprogramming.org/Main_Page for more information.
    
    # This represents the board as 12 bitboards (64 bits each) (LSB is a1, MSB is h8, row/rank-major order)
    # Each bitboard represents a piece type for a side (e.g. black pawns, white knights, etc.)
    # The bitboard is 1 if the piece is there and 0 if it is not
    
    # Bitboards are also used to represent moves and available squares
    # For example, if the white pawns bitboard is 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000010
    # then the white pawn on a2 can move to b2 by using a XOR operation with the move bitboard:
    # 0b00000000_00000000_00000000_00000000_00000000_00000000_00000010_00000010.
    # This is because XORing a bitboard with itself will result in 0, and XORing a bitboard with 0 will result in the bitboard.
    # Essentially a 1 in the move bitboard will either add or remove a piece from the board depending on if it is a 1 or 0 in the pieces bitboard.
    
    # Other bitboard operations can be used to get available squares for a piece.
    # TODO: implement

    def __init__(self, *args):
        """Initializes the game. This can be done in 3 ways:
        - No arguments: Initializes the game to the default starting position
        - One argument: Initializes the game to the given game
        - Two arguments: Initializes the game to the given FEN or PGN

        Raises:
            ValueError: If the number of arguments is not 0, 1, or 2. Or if the arguments are invalid.
        """

        # Default board
        if len(args) == 0:
            self.reset()

        # Copy board
        elif len(args) == 1:
            self.copy(args[0])

        # Load FEN or PGN based on arg 0
        elif len(args) == 2:
            if args[0].lower() == "fen":
                self.load_fen(args[1])
            elif args[0].lower() == "pgn":
                self.load_pgn(args[1])
            else:
                raise ValueError("Invalid argument")

    def reset(self):
        """Resets the board to the default starting position."""

        self.isWhiteTurn = True
        self.viewAsWhite = True

        # Bitboards (64 bits each) (LSB is a1, MSB is h8, row/rank-major order)
        self.black_pawns = (
            0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self.black_knights = (
            0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self.black_bishops = (
            0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self.black_rooks = (
            0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self.black_queens = (
            0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )
        self.black_king = (
            0b00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        )

        self.white_pawns = (
            0b_00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000
        )
        self.white_knights = (
            0b_00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010
        )
        self.white_bishops = (
            0b_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100
        )
        self.white_rooks = (
            0b_00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001
        )
        self.white_queens = (
            0b_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000
        )
        self.white_king = (
            0b_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000
        )

        # Castling rights
        self.white_kingside_castle = True
        self.white_queenside_castle = True
        self.black_kingside_castle = True
        self.black_queenside_castle = True

        # En passant target square
        self.en_passant_target = None

        # Halfmove clock
        self.halfmove_clock = 0

        # Fullmove number
        self.fullmove_number = 1

        # Move list
        self.moves = []

        # PGN tags
        self.tags = {}

    def copy(self, other: "Game"):
        """Copies the given Game into this Game.

        Args:
            other (Game): Game to copy

        Raises:
            TypeError: If the input is not a Game
            ValueError: If the input Game is not valid
        """

        # Validate input
        if not isinstance(other, Game):
            raise TypeError("Input must be a Game")

        if not other.validate_state():
            raise ValueError("Input Game is not valid")

        # Copy attributes
        self.isWhiteTurn = other.isWhiteTurn
        self.viewAsWhite = other.viewAsWhite

        self.black_pawns = other.black_pawns
        self.black_knights = other.black_knights
        self.black_bishops = other.black_bishops
        self.black_rooks = other.black_rooks
        self.black_queens = other.black_queens
        self.black_king = other.black_king

        self.white_pawns = other.white_pawns
        self.white_knights = other.white_knights
        self.white_bishops = other.white_bishops
        self.white_rooks = other.white_rooks
        self.white_queens = other.white_queens
        self.white_king = other.white_king

        self.white_kingside_castle = other.white_kingside_castle
        self.white_queenside_castle = other.white_queenside_castle
        self.black_kingside_castle = other.black_kingside_castle
        self.black_queenside_castle = other.black_queenside_castle

        self.en_passant_target = other.en_passant_target

        self.halfmove_clock = other.halfmove_clock
        self.fullmove_number = other.fullmove_number

        self.moves = other.moves.copy()
        self.tags = other.tags.copy()

    def __eq__(self, other: "Game") -> bool:
        return False  # TODO: implement

    # def __repr__(self) -> str:
    # pass # TODO: implement

    def __str__(self) -> str:
        """Returns a string representation of the board.
        This has styling for the terminal.
        It has the ranks and files labeled.
        It has the pieces represented by unicode characters (e.g. ♙, ♘, ♗, ♖, ♕, ♔).

        Returns:
            str: String representation of the board
        """

        # Go through each bitboard and assemble a string representation of the board
        board = Style.BRIGHT

        i_range = range(7, -1, -1) if self.viewAsWhite else range(8)
        j_range = range(8) if self.viewAsWhite else range(7, -1, -1)

        # Go through all ranks from 8 to 1
        for i in i_range:
            board += str(i + 1) + " "

            # Go through all files on the current rank
            for j in j_range:
                # Get the bit at the current position
                bit = 1 << (j + i * 8)

                # TODO: custom colors?
                board += Back.LIGHTGREEN_EX if (i + j) % 2 == 0 else Back.WHITE
                board += Fore.BLACK

                if self.black_pawns & bit:
                    board += BLACK_TEXT[0]
                elif self.black_knights & bit:
                    board += BLACK_TEXT[1]
                elif self.black_bishops & bit:
                    board += BLACK_TEXT[2]
                elif self.black_rooks & bit:
                    board += BLACK_TEXT[3]
                elif self.black_queens & bit:
                    board += BLACK_TEXT[4]
                elif self.black_king & bit:
                    board += BLACK_TEXT[5]
                elif self.white_pawns & bit:
                    board += WHITE_TEXT[0]
                elif self.white_knights & bit:
                    board += WHITE_TEXT[1]
                elif self.white_bishops & bit:
                    board += WHITE_TEXT[2]
                elif self.white_rooks & bit:
                    board += WHITE_TEXT[3]
                elif self.white_queens & bit:
                    board += WHITE_TEXT[4]
                elif self.white_king & bit:
                    board += WHITE_TEXT[5]
                else:
                    board += " "

                # Spacing
                board += " " + Back.RESET + Fore.RESET

            board += "\n"

        board += "  a b c d e f g h" if self.viewAsWhite else "  h g f e d c b a"

        return board

    def move_str(self, move_str: str):
        """Makes a move on the board based on the given PGN move string.

        Args:
            move_str (str): PGN move string to make (e.g. "Nf3", "Bxe5", "O-O", "O-O-O", "Nxd4", "Nxd4+", "Nxd4#")
        """

        # TODO: validate string lengths

        # This takes a PGN move string and makes the move

        # This parses a PGN move string from back to front
        # This is easier since the back is more consistent
        # than the front in terms of position in the string.
        # From the back it will always be (if they exist):
        #   - Check/Checkmate
        #   - Promotion
        #   - Position to move to
        #   - Takes
        #   - Deciding position (rank, file, or both)
        #       (if there are two pieces that can move to the same square)
        #   - Piece type

        move = self.parse_pgn_move(move_str)

        if move in ["O-O", "O-O-O"]:
            # TODO: self.castle(move)
            return

        print(move)

        # TODO: Get location of piece that is moving

        # TODO: Get location of piece that is being taken

        # TODO: Move the piece

    def move(
        self,
        from_pos: str,
        to_pos: str,
        piece: str,
        takes: bool,
        promotion: str = None,
        check: bool = False,
        checkmate: bool = False,
    ):
        """Makes a move on the board based on the given parameters.

        Args:
            from_pos (str): Position to move from (e.g. "a1", "b2", "c3")
            to_pos (str): Position to move to (e.g. "a1", "b2", "c3")
            piece (str): Type of piece to move (e.g. "N", "B", "R", "Q", "K", "a-h")
            takes (bool): Whether the move is a take or not
            promotion (str, optional): Type of piece to promote to. Defaults to None.
            check (bool, optional): Whether the move is a check. Defaults to False.
            checkmate (bool, optional): Whether the move is a checkmate. Defaults to False.
        """

        # Get move bits from positions
        move = self.two_pos_to_bit(from_pos, to_pos)

        # XOR the bitboard with the move number to move the piece
        if self.isWhiteTurn:
            match piece:
                case "N":
                    self.white_knights ^= move
                case "B":
                    self.white_bishops ^= move
                case "R":
                    self.white_rooks ^= move
                case "Q":
                    self.white_queens ^= move
                case "K":
                    self.white_king ^= move
                case "O-O":  # Kingside Castling
                    king_move = self.two_pos_to_bit("e1", "g1")
                    rook_move = self.two_pos_to_bit("h1", "f1")

                    self.white_king ^= king_move
                    self.white_rooks ^= rook_move

                    self.white_kingside_castle = False
                    self.white_queenside_castle = False
                case "O-O-O":  # Queenside Castling
                    king_move = self.two_pos_to_bit("e1", "c1")
                    rook_move = self.two_pos_to_bit("a1", "d1")

                    self.white_king ^= king_move
                    self.white_rooks ^= rook_move

                    self.white_kingside_castle = False
                    self.white_queenside_castle = False
                case _:
                    self.white_pawns ^= move
        else:
            match piece:
                case "N":
                    self.black_knights ^= move
                case "B":
                    self.black_bishops ^= move
                case "R":
                    self.black_rooks ^= move
                case "Q":
                    self.black_queens ^= move
                case "K":
                    self.black_king ^= move
                case "O-O":  # Kingside Castling
                    king_move = self.two_pos_to_bit("e8", "g8")
                    rook_move = self.two_pos_to_bit("h8", "f8")

                    self.black_king ^= king_move
                    self.black_rooks ^= rook_move

                    self.black_kingside_castle = False
                    self.black_queenside_castle = False
                case "O-O-O":  # Queenside Castling
                    king_move = self.two_pos_to_bit("e8", "c8")
                    rook_move = self.two_pos_to_bit("a8", "d8")

                    self.black_king ^= king_move
                    self.black_rooks ^= rook_move

                    self.black_kingside_castle = False
                    self.black_queenside_castle = False
                case _:
                    self.black_pawns ^= move

        # Switch the turn
        self.isWhiteTurn = not self.isWhiteTurn

        # Increase the turn number
        if self.isWhiteTurn:
            self.fullmove_number += 1

    def pos_to_bit(self, pos: str) -> int:
        """Converts a position to a bitboard.

        Args:
            pos (str): Position to convert (e.g. "a1", "b2", "c3")

        Returns:
            int: Bitboard of the position (e.g. a2 -> 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000010)
        """

        file = pos[0]
        rank = int(pos[1]) - 1

        file_num = ["a", "b", "c", "d", "e", "f", "g", "h"].index(file.lower())
        return 1 << (file_num + rank * 8)

    def bit_to_pos(self, bit: int) -> [str]:
        """Converts a bitboard to a list of positions.

        Args:
            bit (int): Bitboard to convert

        Returns:
            [str]: List of positions (e.g. ["a1", "b2", "c3"])
        """
        pass  # TODO: implement

    def two_pos_to_bit(self, pos1: str, pos2: str) -> int:
        """Converts two positions to a bitboard.

        Args:
            pos1 (str): Board position 1
            pos2 (str): Board position 2

        Returns:
            int: Bitboard of the two positions (e.g. (a1, a2) -> 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000011)
        """
        return self.pos_to_bit(pos1) ^ self.pos_to_bit(pos2)

    def load_fen(self, fen: str):
        """Loads the game from a FEN.

        Args:
            fen (str): FEN to load
        """

        # Set everything to 0
        self.black_pawns = 0
        self.black_knights = 0
        self.black_bishops = 0
        self.black_rooks = 0
        self.black_queens = 0
        self.black_king = 0

        self.white_pawns = 0
        self.white_knights = 0
        self.white_bishops = 0
        self.white_rooks = 0
        self.white_queens = 0
        self.white_king = 0

        # Split the FEN into its components
        fen_split = fen.split(" ")
        (
            piece_positions,
            active_color,
            castling_availability,
            en_passant_target,
            halfmove_clock,
            fullmove_number,
        ) = fen_split

        # Get piece positions
        piece_positions = piece_positions.split("/")
        for rank in range(8):  # TODO: validate that there are 8 ranks in the FEN
            file = 1
            for item in piece_positions[rank]:
                if item.isnumeric():
                    file += int(item)
                    continue
                else:
                    # Add the piece type
                    bit = self.pos_to_bit(
                        ["a", "b", "c", "d", "e", "f", "g", "h"][file - 1]
                        + str(8 - rank)
                    )
                    match item:
                        # Lowercase letters are black pieces
                        case "p":
                            self.black_pawns |= bit
                        case "n":
                            self.black_knights |= bit
                        case "b":
                            self.black_bishops |= bit
                        case "r":
                            self.black_rooks |= bit
                        case "q":
                            self.black_queens |= bit
                        case "k":
                            self.black_king |= bit

                        # Capital letters are white pieces
                        case "P":
                            self.white_pawns |= bit
                        case "N":
                            self.white_knights |= bit
                        case "B":
                            self.white_bishops |= bit
                        case "R":
                            self.white_rooks |= bit
                        case "Q":
                            self.white_queens |= bit
                        case "K":
                            self.white_king |= bit

                    file += 1

        # Get the active color
        self.isWhiteTurn = active_color == "w"

        # TODO: implement

    def load_pgn(self, pgn: str):
        """Loads the game from a PGN.

        Args:
            pgn (str): PGN to load
        """
        pass  # TODO: implement

    def parse_pgn_move(self, move_str: str) -> dict | str:
        """Parses a PGN move string into a dictionary of its components.

        Args:
            move_str (str): Move string to parse

        Returns:
            dict|str: Dictionary of the move's components or a string if the move is a resignation or castling
        """

        # --- Check for resignation --- #
        if move_str in ["1-0", "0-1", "1/2-1/2"]:
            return move_str

        # Check castling
        if move_str in ["O-O", "O-O-O"]:
            return move_str

        # To lowercase
        move_str = move_str.lower()

        # --- Check/Checkmate --- #
        check = False
        checkmate = False
        if move_str[-1] in ["+", "#"]:
            check_str = move_str[-1]
            move_str = move_str[:-1]

            check = check_str == "+"
            checkmate = check_str == "#"

            # If there is still a + or #, then it's invalid
            if "+" in move_str or "#" in move_str:
                print("Invalid move: Bad +/#")
                return None

        # If there is a + or # not at the end, then it's invalid
        elif move_str in ["+", "#"]:
            print("Invalid move: Bad +/#")
            return None

        # --- Promotion --- #
        promotion = None
        if move_str[-2] == "=":
            promotion = move_str[-1]
            move_str = move_str[:-2]

            # Validate promotion
            if promotion not in ["n", "b", "r", "q"]:
                print("Invalid move: Bad promotion")
                return None

        # If there is still a =, then it's invalid
        elif "=" in move_str:
            print("Invalid move: Bad promotion")
            return None

        # --- Position to move to --- #
        move_to = move_str[-2:]
        move_str = move_str[:-2]

        # Validate position to move to
        if len(move_to) != 2:
            print("Invalid move: Bad position to move to")
            return None
        if not self.validate_is_pos(move_to):
            print("Invalid move: Bad position to move to")
            return None

        # If move_str is empty now, then it's a pawn move (without a deciding position or takes)
        if len(move_str) == 0:
            piece = move_to[0]
            return {
                "piece": piece,
                "deciding_pos": None,
                "takes": False,
                "move_to": move_to,
                "promotion": promotion,
                "check": check,
                "checkmate": checkmate,
            }

        # --- Takes --- #
        takes = move_str[-1] == "x"
        if takes:
            move_str = move_str[:-1]

            # If there is still an x, then it's invalid
            if "x" in move_str:
                print("Invalid move: Bad take")
                return None

        # --- Deciding position --- #
        deciding_pos = None

        # Deciding position if there is more than 1 character left
        if len(move_str) > 1:
            deciding_pos = move_str[1:]
            move_str = move_str[0]

            # Check if it is a file or rank
            if (
                len(deciding_pos) == 1
                and not self.validate_is_file(deciding_pos)
                and not self.validate_is_rank(deciding_pos)
            ):
                print("Invalid move: Bad deciding position")
                return None

            # Check if it is a board position
            if not self.validate_is_pos(deciding_pos):
                print("Invalid move: Bad deciding position")
                return None

        # --- Piece type --- #
        piece = move_str

        print(piece)

        # Validate piece type
        if piece not in [
            "n",
            "b",
            "r",
            "q",
            "k",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
        ]:
            print("Invalid move: Bad piece type")
            return None

        # Return the parsed move
        return {
            "piece": piece,
            "deciding_pos": deciding_pos,
            "takes": takes,
            "move_to": move_to,
            "promotion": promotion,
            "check": check,
            "checkmate": checkmate,
        }

    def is_check(self) -> bool:
        """Checks if the current side is in check.

        Returns:
            bool: Whether the current side is in check or not
        """
        pass

    def is_checkmate(self) -> bool:
        """Checks if the current side is in checkmate.

        Returns:
            bool: Whether the current side is in checkmate or not
        """
        pass

    def is_stalemate(self) -> bool:
        """Checks if the current side is in stalemate.

        Returns:
            bool: Whether the current side is in stalemate or not
        """
        pass

    def validate_state(self) -> bool:
        """Validates the current state of the board. This includes:
        - Making sure there is only one king per side
        - Making sure there are no pawns on the first or last ranks
        - Making sure the kings are not in check if it is their turn
        - Making sure the kings are not in checkmate if it is their turn
        - Making sure the kings are not in stalemate if it is their turn

        Returns:
            bool: _description_
        """

        # TODO: figure out if game complete is valid
        return True

    def validate_is_pos(self, pos: str) -> bool:
        """Validates the given string is a valid board position.

        Args:
            pos (str): Position to validate

        Returns:
            bool: Whether the position is valid or not
        """

        # Check length
        if len(pos) != 2:
            return False

        # Check if it is a board position
        [file, rank] = pos
        if not self.validate_is_file(file) or not self.validate_is_rank(rank):
            return False

        # If it passes all checks, then it is a valid position
        return True

    def validate_is_rank(self, rank: str) -> bool:
        """Validates whether the given string is a valid rank.

        Args:
            rank (str): Rank to validate

        Returns:
            bool: Whether the rank is valid or not
        """

        # Check length
        if len(rank) != 1:
            return False

        # Check if it is a rank
        if rank not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            return False

        # If it passes all checks, then it is a valid rank
        return True

    def validate_is_file(self, file: str) -> bool:
        """Validates whether the given string is a valid file.

        Args:
            file (str): File to validate

        Returns:
            bool: Whether the file is valid or not
        """

        # Check length
        if len(file) != 1:
            return False

        # Check if it is a file
        if file not in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            return False

        # If it passes all checks, then it is a valid file
        return True
