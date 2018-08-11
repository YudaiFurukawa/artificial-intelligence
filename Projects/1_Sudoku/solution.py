from utils import *
#https://github.com/vxy10/AIND-Sudoku/blob/master/solution.py

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    # print('naked_twin')
    twins = [box for box in values.keys() if len(values[box]) == 2]
    twins = [[box1,box2] for box1 in twins for box2 in peers[box1] if set(values[box1])==set(values[box2])]

    # print(twins)
    for i in range(len(twins)):
        box1 = twins[i][0]
        box2 = twins[i][1]
        # find common peers
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        peers_common = peers1 & peers2
        # delete the digit in the twins from common peers
        for peers_box in peers_common:
            # print(len(values[peers_common]))
            if len(values[peers_box])>2:
                for rm_val in values[box1]:
                    values = assign_value(values, peers_box, values[peers_box].replace(rm_val,''))

                # print(values)
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    solved_values = [box for box in values.keys() if len(values[box])==1]
    for box in solved_values:
        digit = values[box]
        # print(values[box])
    # print(peers)
        for peer in peers[box]:
            # print(peer)
            values[peer] = values[peer].replace(digit,'')
    # print('elimination')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:
        # print(len(unit))
        for digit in '123456789':
            tmp = [box for box in unit if digit in values[box]]
            # print(tmp)
            if len(tmp) == 1:
                values[tmp[0]]= digit
    # print('onlychoice')
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    values = reduce_puzzle(values)
    # print('search')
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)

    return values


if __name__ == "__main__":
    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid = values2grid({"C5": "23456    789", "C7": "2345678", "I7": "1", "I1": "2345678", "B7": "2345678", "B4": "345678", "C8": "3456789", "I6": "23678", "F7": "58", "A4": "34568", "A3": "7", "B9": "124578", "I8": "345678", "G7": "2345678", "H2": "12345678", "A8": "345689", "B1": "2345689", "E8": "1", "C9": "124578", "E9": "3", "G8": "345678", "B5": "23456789", "F6": "37", "H9": "24578", "C4": "345678", "A1": "2345689", "G2": "12345678", "F5": "37", "G9": "24578", "I2": "2345678", "H4": "345678", "A9": "2458", "D1": "36", "B3": "1234569", "D4": "1", "H8": "345678", "F9": "6", "B6": "236789", "D6": "5", "F3": "24", "E2": "567", "I5": "2345678", "H3": "1234569", "D8": "2", "G6": "1236789", "D2": "9", "G5": "23456789", "G3": "1234569", "A7": "234568", "E1": "567", "H7": "2345678", "C6": "236789", "D9": "47", "E5": "678", "B8": "3456789", "A5": "1", "E3": "56", "B2": "1234568", "D7": "47", "G4": "345678", "F2": "24", "G1": "23456789", "E7": "9", "A6": "23689", "A2": "234568", "E4": "2", "I4": "345678", "D3": "8", "C1": "2345689", "E6": "4", "I3": "23456", "H6": "1236789", "F4": "9", "H5": "23456789", "F1": "1", "F8": "58", "I9": "9", "C3": "1234569", "D5": "36", "H1": "23456789", "C2": "1234568"})
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
