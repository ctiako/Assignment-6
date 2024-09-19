# CS305 Park University
# Assignment #6 
# By Cyrille Tekam Tiako
# 15 Sep 2024

from stripsProblem import Strips, STRIPS_domain, Planning_problem
from stripsForwardPlanner import Forward_STRIPS, SearcherMPP
import time

#######################
# Helper Functions:
#
# The functions below were created to help you complete the
# planning tasks. You will need to complete the implementation
# of other functions below.

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
        for row in range(1,size):
            for col in range(1,size+1):
                yield Strips('move-'+str(tile)+'-down',
                             {'tile'+str(tile):
                              'space'+str(row)+'-'+str(col),
                             'blank':
                             'space'+str(row+1)+'-'+str(col)},
                             {'tile'+str(tile):
                              'space'+str(row+1)+'-'+str(col),
                             'blank':
                             'space'+str(row)+'-'+str(col)})
    #up moves
    for tile in range(1, size*size):
        for row in range(2,size+1):
            for col in range(1,size+1):
                yield Strips('move-'+str(tile)+'-up',
                             {'tile'+str(tile):
                              'space'+str(row)+'-'+str(col),
                             'blank':
                             'space'+str(row-1)+'-'+str(col)},
                             {'tile'+str(tile):
                              'space'+str(row-1)+'-'+str(col),
                             'blank':
                             'space'+str(row)+'-'+str(col)})

def gen_puzzle_domain(size):
    """creates the STRIPS_domain for the given slide-puzzle size"""
    return STRIPS_domain(gen_puzzle_actions(size), gen_puzzle_feature_dict(size))

def puzzle_heuristic(state, goal):
    """counts how many tiles are in their proper place and
       subtracts that from the maximum number of tiles"""
    return sum(1 for tile in gen_tiles(3) if state[tile] == goal[tile])

def main():
    # 5.
    # TODO: Your solution should quickly find the simple
    # solution to this puzzle. You can probably see what
    # it is yourself. Ensure this is working properly
    # when you finish all of the code but the heuristic.
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
    searcher = SearcherMPP(fsprob)
    res = searcher.search()
    print('puzzle 1 solution:', list(path_to_actions(res)))

    # 6.
    # TODO: next run the code below and note that it will take a
    # long time (more than 10 seconds, probably) to solve this
    # more complex puzzle!
    p2start = """437
                 568
                 21X"""

    print("\n\nSolving puzzle 2...\n")
    start_time = time.perf_counter()
    prob = Planning_problem(gen_puzzle_domain(3),
                        str_to_8puzzle_state(p2start),
                        str_to_8puzzle_state(pend))
    fsprob = Forward_STRIPS(prob)
    searcher = SearcherMPP(fsprob)
    res = searcher.search()
    print('puzzle 2 solution:', list(path_to_actions(res)))
    end_time = time.perf_counter()
    print("Time:", end_time - start_time, "seconds")

    # 7.
    # TODO: Once you have implemented the heuristic, this
    # should work properly and should converge on the same
    # solution much more quickly. If you follow the
    # advice given, it should be at least 10x as fast on
    # this example.
    print("\n\nSolving puzzle 2 with heuristic...\n")
    start_time = time.perf_counter()
    prob = Planning_problem(gen_puzzle_domain(3),
                        str_to_8puzzle_state(p2start),
                        str_to_8puzzle_state(pend))
    fsprob = Forward_STRIPS(prob, puzzle_heuristic)
    searcher = SearcherMPP(fsprob)
    res = searcher.search()
    print('puzzle 2 solution:', list(path_to_actions(res)))
    end_time = time.perf_counter()
    print("Time:", end_time - start_time, "seconds")

    # If you wish to play with more examples, you can use the
    # 8-puzzle generator below:
    # https://murhafsousli.github.io/8puzzle/#/

if __name__ == '__main__':
  main()
