from colorama import Fore, Style
from game import Game
import random

COMMANDS = ["quit", "help", "new", "print", "resign", "hint"]
COMMAND_DESC = {
    "quit": "Close the program.",
    "help": "Show this help text.",
    "new": "Start a new game.",
    "print": "Print the board.",
    "resign": "Resign the game.",
    "hint": "Get the 3 best moves for the current position based on ♞.eef's evaluation.",
}


def help_text():
    COMMANDS.sort()

    text = "\n"

    # To move text
    text += f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}To Make a Move{Style.RESET_ALL}\n"
    text += "  Type the move you want to make in PGN notation (e.g. e4, Nxd5).\n\n"
    text += "--------\n\n"

    # Add commands
    for command in COMMANDS:
        text += f"{Fore.LIGHTGREEN_EX}{command}{Style.RESET_ALL}:\n  {COMMAND_DESC[command]}\n\n"

    # Get rid of last newline
    text = text[:-1]

    return text


def handle_command(command, game, args: list):
    match command:
        case "quit":
            exit()
        case "help":
            print(help_text())
        case "new":
            inp = input(
                "Choose whether you want to play as white, black, or random. (w/b/r): "
            )

            while inp not in ["w", "b", "r"]:
                inp = input("Please enter either 'w', 'b', or 'r': ")

            game = Game()

            if inp == "r":
                game.viewAsWhite = random.choice([True, False])
            else:
                game.viewAsWhite = inp == "w"

            print(game)
        case "print":
            if game is None:
                print(
                    f"{Fore.LIGHTRED_EX}No game is in progress. Type 'new' to create a new game.{Style.RESET_ALL}"
                )
            else:
                print(game)
        case _:
            print("Not implemented yet.")

    return game


def __main__(*args, **kwargs):
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Welcome to Eef's Chess Engine (♞.eef)!")
    print(f"{Style.NORMAL}Type 'quit' to quit at any time.")
    print("Type 'help' for a list of commands.")
    print("To get started, type 'new' to start a new game.")
    print(Style.RESET_ALL)
    game = None

    while True:
        # Get input
        inp = input(f"{Fore.LIGHTGREEN_EX}♞.eef> {Style.RESET_ALL}")
        tokens = inp.split()
        
        if len(tokens) == 0:
            continue

        # Check commands
        if tokens[0] in COMMANDS:
            game = handle_command(inp, game, tokens[1:])
            continue

        # Check if game exists
        if game is None:
            print(
                f"{Fore.LIGHTRED_EX}No game is in progress. Type 'new' to create a new game.{Style.RESET_ALL}"
            )
            continue

        # Make move
        move_res = game.move_str(inp)

        # Print board if move was valid
        if move_res:
            print(game)


# Run main function
if __name__ == "__main__":
    __main__()
