
"""Author: Ali Sartaz Khan
   Main program for Battleship
   Creates a board.  Right now, the code hard-codes the board in one
   arrangement: a standard one, using 5 standard ship types. The User and the
   Computer take turns in attacking eachother's board. The first side to get all
   their ships sunk loses.
"""
import random
import time
import os
from battleship     import *

from standard_ships import *


def assemble_ships_player(player_A_board):
    player_A_board.print()
    print("State your rotation value and coordinates in the following format: val x y")

    try:
        battleship = input("Battleship: ").split()
        player_A_board.add_ship(Battleship(int(battleship[0])), (int(battleship[1]), int(battleship[2])))
        player_A_board.print()

        cruiser = input("Cruiser: ").split()
        player_A_board.add_ship(Cruiser(int(cruiser[0])), (int(cruiser[1]), int(cruiser[2])))
        player_A_board.print()

        carrier = input("Aircraft Carrier: ").split()
        player_A_board.add_ship(Carrier(int(carrier[0])), (int(carrier[1]), int(carrier[2])))
        player_A_board.print()

        submarine = input("Submarine: ").split()
        player_A_board.add_ship(Submarine(int(submarine[0])), (int(submarine[1]), int(submarine[2])))
        player_A_board.print()

        destroyer = input("Destroyer: ").split()
        player_A_board.add_ship(Destroyer(int(destroyer[0])), (int(destroyer[1]), int(destroyer[2])))
        player_A_board.print()
    except:
        print("You are overlapping the ships. Restart this program and try again!")
        os._exit(0)

    player_A_ships = [Battleship(int(battleship[0])),
                      Cruiser(int(cruiser[0])),
                      Carrier(int(carrier[0])),
                      Submarine(int(submarine[0])),
                      Destroyer(int(destroyer[0]))]

    return player_A_ships

def assemble_opponent_ships(opponent_A_board):
    opponent_A_ships = [Battleship(3),
                        Cruiser(0),
                        Carrier(0),
                        Submarine(0),
                        Destroyer(3)]

    opponent_A_board.add_ship(opponent_A_ships[0], (1, 5))
    opponent_A_board.add_ship(opponent_A_ships[1], (1, 2))
    opponent_A_board.add_ship(opponent_A_ships[2], (4, 5))
    opponent_A_board.add_ship(opponent_A_ships[3], (5, 8))
    opponent_A_board.add_ship(opponent_A_ships[4], (9, 2))
    return opponent_A_ships

def player_move(opponent_board):
    while True:
        move = input("What is the next move? Move format must be: x y\n")
        move = move.split()
        print()

        if len(move) != 2:
            print("Invalid move.  Move format must be: x y")
            input("Press ENTER to continue")
            continue

        try:
            x = int(move[0])
            y = int(move[1])
        except:
            print("Invalid move.  Move format must be: x y")
            input("Press ENTER to continue")
            continue

        if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
            print("Invalid move.  The range of valid moves is 0 through {} (inclusive)".format(SIZE))
            input("Press ENTER to continue")
            continue

        if opponent_board.has_been_used((x, y)):
            print("Invalid move.  The location {},{} has already been used.".format(x, y))
            input("Press ENTER to continue")
            continue
        break


    move_result = opponent_board.attempt_move((x, y))
    if move_result is not None:
        print("RESULT: " + move_result)
        print()


def opponent_move(player_A_board):
    while True:
        x = random.randint(0, SIZE-1)
        y = random.randint(0, SIZE-1)
        if player_A_board.has_been_used((x, y)):
            continue
        break

    move_result = player_A_board.attempt_move((x, y))
    print("RESULT: " + move_result)
    print()


def main():
    global SIZE
    SIZE = 10
    player_A_board = Board(SIZE)
    opponent_A_board = Board(SIZE)
    player_A_ships = assemble_ships_player(player_A_board)
    opponent_ships = assemble_opponent_ships(opponent_A_board)
    print("\n\n\nWelcome to Battleship!")
    print()
    print("This is the target side of the game")
    print()


    # ------------------ GAME LOOP -------------------------
    i = 0
    move_result = None
    while True:
        if move_result is not None:
            print()
            print()
            print()
        if i % 2 == 0:
            player_move(opponent_A_board)
            print("Ship list: Opponent")
            print("----------")
            for s in opponent_ships:
                s.print()
            print()
            if all_sunk(opponent_ships):
                print("You win!")
                break
        else:
            print("Computer's turn...")
            opponent_move(player_A_board)
            player_A_board.print()
            print()

            print("Ship list: Player")
            print("----------")
            for s in player_A_ships:
                s.print()
            print()
            t_end = time.time() + 4
            while time.time() < t_end:
                continue
            if all_sunk(player_A_ships):
                print("Computer Wins!")
                break

        i+=1

    print("\n\n\n *** GAME OVER ***")
    print()
    print("Your Board:")
    player_A_board.print()
    print("\n)
    print("Opponent's Board:")
    opponent_A_board.print()


def all_sunk(ships):
    for s in ships:
        if not s.is_sunk():
            return False
    return True



if __name__ == "__main__":
    main()


