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


def starting_player():
    """
        Determine the starting player, taking into account player 1's winning strategy.
    """
    # These are losing positions for player 1. Player 2 plays first.
    if n == m and n % 3 == 2:
        return 2
    elif n > m and m % 3 == 1:
        return 2
    elif n < m and n % 3 == 1:
        return 2
    # If none of the above, player 1 plays first, because he has a winning position.
    return 1


def random_movement_choice():
    """
        Randomly choose between the two possible movements.
    """
    a = random.choice([1, 2])
    if a == 1:
        b = 2
    else:
        b = 1
    return n - a, m - b


def player_1_winning_strategy():
    """
        Player 1's winning strategy.
    """
    # if only one possible movement, choose it
    if n == 1:
        return n - 1, m - 2
    elif m == 1:
        return n - 2, m - 1
    # else choose the movement that leads to a winning position.
    elif n == m:
        return random_movement_choice()
    elif n > m:
        if m % 3 == 0:
            return n - 1, m - 2
        elif m % 3 == 1:
            return random_movement_choice()
        elif m % 3 == 2:
            return n - 2, m - 1
    elif n < m:
        if n % 3 == 0:
            return n - 2, m - 1
        elif n % 3 == 1:
            return random_movement_choice()
        elif n % 3 == 2:
            return n - 1, m - 2


def player_2_strategy():
    """
        Player 2's strategy.
    """
    # if only one possible movement, choose it
    if n == 1:
        return n - 1, m - 2
    elif m == 1:
        return n - 2, m - 1
    # else choose randomly.
    return random_movement_choice()


def start_game():
    """
        Method that starts the game.
    """
    global n, m, player
    while True:
        if n == 0 or m == 0 or (n == 1 and m == 1):
            break  # the player that cannot move wins

        if player == 1:
            n, m = player_1_winning_strategy()
            player = 2

        else:  # player == 2
            n, m = player_2_strategy()
            player = 1


def initialize_strategy_table():
    """
        Create header and first column of the strategy table.
    """
    strategy_array = [[''] + [f'{x}' for x in range(n + 1)]]  # first row
    for y in range(m + 1):
        row = [f'{y}']
        row += ['' for _ in range(n + 1)]
        strategy_array.append(row)  # add row to the strategy table
    strategy_array = np.array(strategy_array)
    return strategy_array


def fill_strategy_table(strategy_array):
    """
        Fill the strategy table with 'W' and 'L' using the winning strategy.
    """
    # We start from y=1 and x=1 because the first row and column are the headers.
    for y in range(1, m + 2):
        for x in range(1, n + 2):
            if y == 1 or x == 1:  # (1,x) or (y,1)
                strategy_array[y, x] = 'W'
            elif y == 2 and x == 2:  # (2,2)
                strategy_array[y, x] = 'W'
            elif x == 2 or y == 2:  # (y,2) or (2,x)
                strategy_array[y, x] = 'L'
            elif y >= 3 and x >= 3:
                if strategy_array[y - 1, x - 2] == 'L' or strategy_array[y - 2, x - 1] == 'L':
                    strategy_array[y, x] = 'W'
                else:
                    strategy_array[y, x] = 'L'


def create_strategy_table():
    """
        Create the strategy table.
    """
    # Create the strategy table
    strategy_array = initialize_strategy_table()

    # fill the strategy table
    fill_strategy_table(strategy_array)
    file_name = 'thema_3_strategy_table.csv'

    # save the strategy table as a csv file
    try:
        np.savetxt(file_name, strategy_array, delimiter=',', fmt='%s')
        print(f'Strategy table created successfully in {file_name}!')
    except:
        print('Error while saving the strategy table!')


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
