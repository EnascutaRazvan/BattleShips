import numpy as np

number_of_rows = int(input("Enter the number of rows: "))
number_of_cols = int(input("Enter the number of cols: "))
size_of_ship = int(input("Enter the size of ship: "))

A = np.zeros((number_of_rows, number_of_cols), dtype=np.int32)
A_hidden = np.zeros((number_of_rows, number_of_cols), dtype=np.int32)
B = np.zeros((number_of_rows, number_of_cols), dtype=np.int32)
B_hidden = np.zeros((number_of_rows, number_of_cols), dtype=np.int32)


def set_start_positions(player_board):
    start_pos = input("Start position: ").split(' ')
    print(start_pos)
    row = int(start_pos[0])
    col = int(start_pos[1])
    player_board[row][col] = -1
    for size in range(0, size_of_ship - 1):
        col += 1
        player_board[row][col] = -1


def check_attacked_position(player_board_hidden, row, col):
    if player_board_hidden[row][col] == 1:
        return True
    else:
        return False


def attack(player_board_hidden, player_board):
    correct_attack = False
    while not correct_attack:
        move = input("Attack: ").split(' ')
        if len(move) == 2:
            row = int(move[0])
            col = int(move[1])
            if row < number_of_rows and col < number_of_cols and not check_attacked_position(player_board_hidden, row,
                                                                                             col):
                correct_attack = True
                if player_board[row][col] == -1:
                    print("Hit!")
                    player_board_hidden[row][col] = 1
                else:
                    print("Miss!")
                    player_board_hidden[row][col] = 1
            else:
                if row >= number_of_rows or col >= number_of_cols:
                    print("Wrong move!")
                elif check_attacked_position(player_board_hidden, row, col):
                    print("You already attacked this position!")
        else:
            print("Wrong move!")
            correct_attack = False



def check_if_ship_is_sunk(player_board_hidden, player_board, player):
    parts_of_ship = 0
    for row in range(0, number_of_rows):
        for col in range(0, number_of_cols):
            if player_board_hidden[row][col] == 1 and player_board[row][col] == -1 and parts_of_ship < size_of_ship:
                parts_of_ship += 1
    if parts_of_ship == size_of_ship:
        print("Player " + player + " won!")
        return True
    return False


winner = False
firstA = True
firstB = True
turn_playerA = True
turn_playerB = False
while not winner:
    if turn_playerA and not winner:
        if firstA:
            set_start_positions(player_board=A)
            firstA = False
        else:
            attack(player_board_hidden=B_hidden, player_board=B)
            print(B_hidden, "\n")
            winner = check_if_ship_is_sunk(player_board_hidden=B_hidden, player_board=B, player="A")
    turn_playerA = False
    turn_playerB = True

    if turn_playerB and not winner:
        if firstB:
            set_start_positions(player_board=B)
            firstB = False
        else:
            attack(player_board_hidden=A_hidden, player_board=A)
            print(A_hidden, "\n")
            winner = check_if_ship_is_sunk(player_board_hidden=A_hidden, player_board=A, player="B")

        turn_playerA = True
        turn_playerB = False
