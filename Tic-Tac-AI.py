"""
Author: Kartikay Chiranjeev Gupta
Last Date of Modification: 2/7/2021
"""

elements = ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ']
winning_combos = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]
user_move = []
comp_move = []
SIGN = {1: ' X ', -1: ' O '}
bypass = False  # Used when user want to start first.


def is_Winning(moves):
    """
    Checks if the player is winning.
    :param moves: list of moves belonging to user or computer.
    :return: True if anyone is winning, false otherwise.
    """
    for combo in winning_combos:
        if combo[0] in moves and combo[1] in moves and combo[2] in moves:
            return True
    return False


def avail_Moves():
    """
    Returns a set containing all available move on board.
    :return: set of available moves.
    """
    a, b, c = set(user_move), set(comp_move), {1, 2, 3, 4, 5, 6, 7, 8, 9}
    return c - a.union(b)


def is_Draw():
    """
    Checks if the games are draw.
    :return: True if the game is draw, false otherwise.
    """
    if avail_Moves() == set() and not is_Winning(user_move) and not is_Winning(comp_move):
        return True
    return False


def print_Board(elements_):
    """
    Prints the 'X' and 'O' in proper game format.
    :param elements_: List of 'X' and 'O'
    :return: None
    """
    elements_ = iter(elements_)
    for i in range(3):
        for j in range(3):
            if j != 2:
                print(next(elements_), end='|')
            else:
                print(next(elements_))
        if i != 2:
            print('---|---|---')


def Choose_sign():
    """
    Ask user to choose either X or O
    :return: None
    """
    while True:
        _choice = input('Choose Sign [ X / O ]: ')
        if _choice == 'x' or _choice == 'X':
            SIGN[1], SIGN[-1] = ' X ', ' O '
            break
        elif _choice == 'o' or _choice == 'O':
            SIGN[-1], SIGN[1] = ' X ', ' O '
            break
        else:
            print('Enter a valid choice!')
            continue


def Take_input():
    """
    Takes a valid input from user.
    :return: int between 1 and 9 as per entered by user.
    """
    position = input("Select position: ")
    invalid = True
    while invalid:
        try:
            position = int(position)
            if 1 <= position <= 9 and position not in user_move and position not in comp_move:
                invalid = False
                user_move.append(position)
                elements[position - 1] = SIGN[1]
                return position
            else:
                print("Invalid position entered!")
                position = input('Enter a valid position: ')
                continue
        except ValueError:
            print('Invalid character entered!')
            position = input('Enter a valid character: ')
            continue


def Mini_max(player):
    """
    Minimax is a type of backtracking algorithm. The Minimax algorithm finds an optimal move in game.
    Minimax algorithm takes into consideration that the opponent is also playing optimally,
    which makes it useful for two-player games like Tic-tac-toe.
    :param player: 1 if the algorithm runs for user, else -1 for computer.
    :return: list of best move and score
    """
    best = [None, 1] if player == 1 else [None, -1]

    if is_Winning(user_move):
        return [None, -1]
    elif is_Winning(comp_move):
        return [None, 1]
    elif is_Draw():
        return [None, 0]

    for move in avail_Moves():
        user_move.append(move) if player == 1 else comp_move.append(move)
        _, score = Mini_max(-player)
        if player == 1:
            user_move.pop()
            if score < best[1]:  # Minimizing
                best = [move, score]
        else:
            comp_move.pop()
            if score > best[1]:  # Maximizing
                best = [move, score]
    return best


def Compute_move(_func_):
    """
    Return a move [from 1-9] using the selected hardness function
    :param _func_: list of functions
    :return: move from available move.
    """
    move, _ = _func_()
    print('Computer chose: ', move)
    elements[move - 1] = SIGN[-1]
    comp_move.append(move)
    return move


def Easy_mode():
    """
    Uses Random choice function, hence easy to beat.
    :return: Random value from available moves.
    """
    move = list(avail_Moves())[0]
    elements[move - 1] = SIGN[-1]
    comp_move.append(move)
    return [move, None]


def God_mode():
    """
    Uses Mini_max function, hence it is impossible to beat this mode.
    :return:Mini_max function with computer player set as argument.
    """
    return Mini_max(-1)


def Choose_hardness():
    """
    Ask User to select hardness mode.
    :return: None
    """
    diff_funcs = [Easy_mode, God_mode]
    while True:
        choice_ = int(input('Select hardness:\n1.)Easy Mode\n2.)God Mode\n'))
        if choice_ == 1 or choice_ == 2 or choice_ == 3:
            break
        print('Invalid input!')
    return diff_funcs[choice_ - 1]


if __name__ == '__main__':
    func_ = Choose_hardness()
    Choose_sign()
    choice = input('Like to start first ? [ y / n ]: ')
    print_Board(elements)
    if choice == 'y' or choice == 'Y':
        bypass = True
    while True:
        if bypass:
            Take_input()
            if is_Winning(user_move):
                print_Board(elements)
                print('YOU WON!')
                break
            elif is_Draw():
                print_Board(elements)
                print('!!DRAW!!')
                break
        Compute_move(func_)
        print_Board(elements)
        bypass = True
        if is_Winning(comp_move):
            print_Board(elements)
            print('YOU LOSE!')
            break
        elif is_Draw():
            print_Board(elements)
            print('!!DRAW!!')
            break
        continue
