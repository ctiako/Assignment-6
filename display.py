# CS305 Park University
# Assignment #6 
# By Cyrille Tekam Tiako
# 15 Sep 2024

from stripsProblem import Strips, STRIPS_domain, Planning_problem
from stripsForwardPlanner import Forward_STRIPS, SearcherMPP
import time
import random

def path_to_actions(path):
    """converts an AIPython planning search path to a list of actions"""
    if path.arc:
        yield path.arc.action
        yield from path_to_actions(path.initial)

def gen_tiles(size):
    """generates the names for tiles in the slide-puzzle search
       space in the format tileX where X is the number on the
       tile. 'blank' is also generated for the absent tile."""
    for i in range(1, size*size):
        yield 'tile'+str(i)
    yield 'blank'

def gen_puzzle_feature_dict(size):
    """generates the feature dictionary needed by STRIPS_domain"""
    spaces = set(gen_spaces(size))
    return { t : spaces for t in gen_tiles(size)}

def str_to_8puzzle_state(s):
    """converts a 3x3 string in to an 8puzzle search state.
       Whitespace is trimmed off of each line and X stands in
       for the blank space (no number tile)."""
    row = 0
    state = dict()
    for line in s.strip().split("\n"):
        row += 1
        col = 0
        line = line.strip()
        for c in line:
            col += 1
            state['blank' if c=='X' else 'tile'+c] = \
                          'space'+str(row)+'-'+str(col)
    return state

def gen_spaces(size):
    """generates names of the spaces on the slide puzzle. These
       names represent 2-d coordinates on the square puzzle and
       have the format spaceX-Y where X is the row and Y is the
       column. """
    for row in range(1, size+1):
        for col in range(1, size+1):
            yield 'space'+str(row)+'-'+str(col)

def gen_puzzle_actions(size):
    #right moves
    for tile in range(1, size*size):
        for row in range(1,size+1):
            for col in range(1,size):
                yield Strips('move-'+str(tile)+'-right',
                             {'tile'+str(tile):
                              'space'+str(row)+'-'+str(col),
                             'blank':
                             'space'+str(row)+'-'+str(col+1)},
                             {'tile'+str(tile):
                              'space'+str(row)+'-'+str(col+1),
                             'blank':
                             'space'+str(row)+'-'+str(col)})
    #left moves
    for tile in range(1, size*size):
        for row in range(1,size+1):
            for col in range(2,size+1):
                yield Strips('move-'+str(tile)+'-left',
                             {'tile'+str(tile):
                              'space'+str(row)+'-'+str(col),
                             'blank':
                             'space'+str(row)+'-'+str(col-1)},
                             {'tile'+str(tile):
                              'space'+str(row)+'-'+str(col-1),
                             'blank':
                             'space'+str(row)+'-'+str(col)})
    #down moves
    for tile in range(1, size*size):
        for row in range(2,size+1):
            for col in range(1,size+1):
                yield Strips('move-'+str(tile)+'-down',
                             {'tile'+str(tile):
                              'space'+str(row)+'-'+str(col),
                             'blank':
                             'space'+str(row-1)+'-'+str(col)},
                             {'tile'+str(tile):
                              'space'+str(row-1)+'-'+str(col),
                             'blank':
                             'space'+str(row)+'-'+str(col)})
    #up moves
    for tile in range(1, size*size):
        for row in range(1,size):
            for col in range(1,size+1):
                yield Strips('move-'+str(tile)+'-up',
                             {'tile'+str(tile):
                              'space'+str(row)+'-'+str(col),
                             'blank':
                             'space'+str(row+1)+'-'+str(col)},
                             {'tile'+str(tile):
                              'space'+str(row+1)+'-'+str(col),
                             'blank':
                             'space'+str(row)+'-'+str(col)})

def gen_puzzle_domain(size):
    """creates the STRIPS_domain for the given slide-puzzle size"""
    return STRIPS_domain(gen_puzzle_feature_dict(size),
                         gen_puzzle_actions(size))

def puzzle_heuristic(state, goal):
    """counts how many tiles are in their proper place and subtracts
       that from the maximum number of tiles."""
    count = 0
    for tile in gen_tiles(3):
        if state.get(tile, None) == goal.get(tile, None):
            count += 1
    return 9 - count

def test_against_baseline(baseline, num_tests=100):
    """tests the code against a baseline opponent and reports the
       percentage of games won."""
    wins = 0
    for _ in range(num_tests):
        p1start = generate_random_puzzle(3)
        prob = Planning_problem(gen_puzzle_domain(3),
                            str_to_8puzzle_state(p1start),
                            str_to_8puzzle_state("12345678X"))
        fsprob = Forward_STRIPS(prob, puzzle_heuristic)
        searcher = SearcherMPP(fsprob)
        res = searcher.search()
        path = path_to_actions(res)
        if baseline.solve(p1start) != path:
            wins += 1
    return wins / num_tests * 100

def generate_random_puzzle(size):
    """generates a random puzzle of the given size."""
    tiles = list(gen_tiles(size))
    random.shuffle(tiles)
    puzzle = ""
    for row in range(1, size+1):
        for col in range(1, size+1):
            tile = tiles.pop(0)
            if tile == 'blank':
                puzzle += "X"
            else:
                puzzle += tile[4:]
        puzzle += "\n"
    return puzzle[:-1]

def main():
    pend = """123
              456
              78X"""

    print("\n\nSolving puzzle 1...\n")
    p1start = """123
                 X56
                 478"""

    prob = Planning_problem(gen_puzzle_domain(3),
                        str_to_8puzzle_state(p1start),
                        str_to_8puzzle_state(pend))
    fsprob = Forward_STRIPS(prob)
    searcher = SearcherMPP(fsprob, puzzle_heuristic)
    res = searcher.search()
    print('puzzle 1 solution:', list(path_to_actions(res)))

    print("\n\nSolving puzzle 2...\n")
    p2start = """437
                 568
                 21X"""

    prob = Planning_problem(gen_puzzle_domain(3),
                        str_to_8puzzle_state(p2start),
                        str_to_8puzzle_state(pend))
    fsprob = Forward_STRIPS(prob)
    searcher = SearcherMPP(fsprob, puzzle_heuristic)
    res = searcher.search()
    print('puzzle 2 solution:', list(path_to_actions(res)))

    print("\n\nSolving puzzle 2 with heuristic...\n")
    prob = Planning_problem(gen_puzzle_domain(3),
                        str_to_8puzzle_state(p2start),
                        str_to_8puzzle_state(pend))
    fsprob = Forward_STRIPS(prob, puzzle_heuristic)
    searcher = SearcherMPP(fsprob)
    res = searcher.search()
    print('puzzle 2 solution:', list(path_to_actions(res)))

    print("\n\nTesting against baseline...\n")
    baseline = RandomBaseline()
    print("Percentage of games won:", test_against_baseline(baseline))

if __name__ == '__main__':
  main()
