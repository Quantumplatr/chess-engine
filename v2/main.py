from game import Game

game = Game()

# game.viewAsWhite = False

# game.load_fen("rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")

while True:
    print(game)

    # Get input
    move = input("Enter move: ")

    # Check quit
    if move == "quit":
        break

    # Check if move is valid
    # TODO: implement

    # Make move
    game.move_str(move)
