# exercise 6.13

import random

import numpy as np
from Bio import SeqIO


def read_fasta_seq(file):
    """
        Read the fasta file and return the len of the sequence.
    """
    seq = SeqIO.parse(open(file), 'fasta')
    for fasta in seq:
        return len(str(fasta.seq))


def initialize_strategy_table():
    """
        Create header and first column of the strategy table.
        We always create a square table with the max length of the two sequences,
        because it helps us find the strategy table.
    """
    if n > m:
        x = n
    else:
        x = m
    strategy_array = [[''] + [f'{i}' for i in range(x + 1)]]  # first row
    for y in range(x + 1):
        row = [f'{y}']
        row += ['' for _ in range(x + 1)]
        strategy_array.append(row)  # add row to the strategy table
    strategy_array = np.array(strategy_array)
    return strategy_array, x


def fill_upper_triangular_table(M, N, strategy_array):
    """
        Fill the upper triangular table with the losing positions, starting from the first L position.
        Each time we find an L position, we fill the winning positions in the same row, column and diagonal,
        and we also save the symmetric L position coordinates in a dictionary (L_symmetric_idx).
    """

    def fill_winning_positions():
        """
            Fill the winning positions of the upper triangular table for the current L position.
        """
        if row in L_in_row_idx.keys() and not L_in_row_idx[row]:
            L_in_row_idx[row] = True
            for c in range(col + 1, N + 2):
                strategy_array[row, c] = 'W'
        if col in L_in_col_idx.keys() and not L_in_col_idx[col]:
            L_in_col_idx[col] = True
            for r in range(row + 1, M + 2):
                strategy_array[r, col] = 'W'
        if (row, col) in L_in_diag_idx.keys() and not L_in_diag_idx[(row, col)]:
            L_in_diag_idx[(row, col)] = True
            r = row + 1
            c = col + 1
            while r < M + 2 and c < N + 2:
                strategy_array[r, c] = 'W'
                r += 1
                c += 1

    strategy_array[1, 1] = 'L'  # (1,1) is the first L position
    L_in_row_idx = {1: False}
    L_in_col_idx = {1: False}
    L_in_diag_idx = {(1, 1): False}
    L_symmetric_idx = {1: 1}  # row : col
    row = 1
    col = 1
    while True:
        fill_winning_positions()
        if col < M + 2 and row < N + 2 and col not in L_symmetric_idx.keys():
            L_symmetric_idx[col] = row
        row += 1
        if row > M + 1:  # if we have reached the last row, break.
            break
        try:
            col = list(strategy_array[row])[row + 1:].index('') + row + 1
            if row in L_symmetric_idx.keys():
                row += 1
                col = list(strategy_array[row])[row + 1:].index('') + row + 1
        except:  # if '' not in current row, continue.
            continue
        strategy_array[row, col] = 'L'
        if row not in L_in_row_idx.keys():
            L_in_row_idx[row] = False
        if col not in L_in_col_idx.keys():
            L_in_col_idx[col] = False
        if (row, col) not in L_in_diag_idx.keys():
            L_in_diag_idx[(row, col)] = False
    return L_symmetric_idx


def fill_lower_triangular_table(M, N, L_symmetric_idx, strategy_array):
    """
        Fill the lower triangular table with the winning positions, starting from the second L position
        (the first L position is already filled).
    """
    L_symmetric_idx.pop(1)  # remove the first L position because it is already filled.
    for row in L_symmetric_idx:
        col = L_symmetric_idx[row]
        strategy_array[row, col] = 'L'
        for c in range(col + 1, N + 2):
            strategy_array[row, c] = 'W'
        for r in range(row + 1, M + 2):
            strategy_array[r, col] = 'W'
        r = row + 1
        c = col + 1
        while r < M + 2 and c < N + 2:
            strategy_array[r, c] = 'W'
            r += 1
            c += 1


def fill_strategy_table(strategy_array, N, M):
    """
        Fill the strategy table with 'W' and 'L' using the winning strategy.
    """
    L_symmetric_idx = fill_upper_triangular_table(M, N, strategy_array)
    fill_lower_triangular_table(M, N, L_symmetric_idx, strategy_array)


def create_strategy_table():
    """
        Create the strategy table.
    """
    # Create the strategy table
    strategy_array, x = initialize_strategy_table()

    # fill the strategy table
    fill_strategy_table(strategy_array, x, x)
    strategy_array = strategy_array[0:m + 2, 0:n + 2]  # keep the m+2 first rows and n+2 first columns
    file_name = 'thema_2_strategy_table.csv'

    # save the strategy table as a csv file
    try:
        np.savetxt(file_name, strategy_array, delimiter=',', fmt='%s')
        print(f'Strategy table created successfully in {file_name}!')
    except:
        print('Error while saving the strategy table!')


def starting_player():
    """
        Determine the starting player, taking into account player 1's winning strategy.
        If n == m (square table), player 1 starts because he can possibly win in the first move (diagonal move).
        Else (rectangular table), player 2 starts.
    """
    if n == m:
        return 1
    else:
        return 2


def random_movement_choice(number):
    value = random.choice([1, 2, 3])
    if value == 1:
        return n - number, m
    elif value == 2:
        return n, m - number
    else:
        return n - number, m - number


def player_1_winning_strategy(number):
    """
        Player 1's winning strategy.
    """

    def horizontal_or_vertical_move():
        if random.uniform(0, 1) < 0.5:
            return n - number, m  # horizontal move
        else:
            return n, m - number  # vertical move

    def diagonal_or_vertical_move():
        if random.uniform(0, 1) < 0.5:
            return n - number, m - number  # diagonal move
        else:
            return n, m - number  # vertical move

    def diagonal_or_horizontal_move():
        if random.uniform(0, 1) < 0.5:
            return n - number, m - number  # diagonal move
        else:
            return n - number, m  # horizontal move

    if n == m:  # square table
        if n - number == 0:  # diagonal move if n == m == number
            return 0, 0
        else:  # random choice (horizontal or vertical move)
            return horizontal_or_vertical_move()
    else:  # rectangular table
        if n - number < 0:  # if number is bigger than n, we can only make a vertical move
            return n, m - number
        elif m - number < 0:  # if number is bigger than m, we can only make a horizontal move
            return n - number, m
        elif n - number != m and m - number != n:  # if we can make any move without creating a square table
            return random_movement_choice(number)  # random choice (horizontal, vertical or diagonal move)
        else:  # if we can make a move and create a square table
            if n - number != 0 and n - number == m:  # upper triangular table, diagonal or vertical move
                return diagonal_or_vertical_move()
            elif m - number != 0 and m - number == n:  # lower triangular table, diagonal or horizontal move
                return diagonal_or_horizontal_move()
            elif n - number == 0:  # lower triangular table
                return n, m - number  # vertical move, creating a square table
            else:  # m - number == 0, upper triangular table
                return n - number, m  # horizontal move, creating a square table


def player_2_strategy(number):
    """
        Player 2's strategy.
    """
    if n - number < 0:  # if number is bigger than n, player 2 can only make a vertical move
        return n, m - number
    elif m - number < 0:  # if number is bigger than m, player 2 can only make a horizontal move
        return n - number, m
    return random_movement_choice(number)  # random choice (horizontal, vertical or diagonal move)


def start_game():
    """
        Method that starts the game.
    """
    global n, m, player
    while True:
        if n == 0 and m == 0:  # the player that cannot move loses.
            if player == 1:
                player = 2  # player 2 wins
            else:
                player = 1  # player 1 wins
            break
        number = random.randint(1, max(n, m))
        if player == 1:
            n, m = player_1_winning_strategy(number)
            player = 2

        else:  # player == 2
            n, m = player_2_strategy(number)
            player = 1


if __name__ == '__main__':
    paths = ['../auxiliary2023/brain_medium_sequence.fa', '../auxiliary2023/brain_small_sequence.fa',
             '../auxiliary2023/brain_very_small_sequence.fa', '../auxiliary2023/liver_medium_sequence.fa',
             '../auxiliary2023/liver_small_sequence.fa', '../auxiliary2023/liver_very_small_sequence.fa',
             '../auxiliary2023/muscle_medium_sequence.fa', '../auxiliary2023/muscle_small_sequence.fa',
             '../auxiliary2023/muscle_very_small_sequence.fa']

    seq1 = paths.pop(random.choice([0, len(paths) - 1]))
    n = read_fasta_seq(seq1)  # n is the length of the first sequence
    seq2 = paths.pop(random.choice([0, len(paths) - 1]))
    m = read_fasta_seq(seq2)  # m is the length of the second sequence

    print(f'\nThe first sequence consists of {n} nucleotides.')
    print(f'The second sequence consists of {m} nucleotides.\n')

    choice = input('Do you want to create a strategy table? (y/n): ')
    while choice != 'y' and choice != 'n':
        choice = input('Please enter y or n: ')
    if choice == 'y':
        create_strategy_table()

    # Determine the starting player
    player = starting_player()

    # The game begins
    start_game()
    print(f'\nGame over!\nThe winner is player {player}!')
