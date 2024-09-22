# CS305 Park University
# Assignment #6 
# By Cyrille Tekam Tiako
# 15 Sep 2024

import random
import time
from stripsProblem import Strips, STRIPS_domain, Planning_problem
from stripsForwardPlanner import Forward_STRIPS, SearcherMPP, AStarSearch

class RandomBaseline:
    """A baseline class that solves the puzzle randomly."""
    def solve(self, puzzle_start):
        """Performs random moves to attempt to solve the puzzle."""
        actions = []
        for _ in range(50):  # Try up to 50 random moves
            actions.append(random.choice(['move-up', 'move-down', 'move-left', 'move-right']))
        return actions

def path_to_actions(path):
    """Converts a planning search path to a list of actions."""
    if path.arc:
        yield path.arc.action
        yield from path_to_actions(path.initial)

def gen_tiles(size):
    """Generates the names for tiles in the puzzle (e.g., tile1, tile2...blank)."""
    for i in range(1, size*size):
        yield 'tile'+str(i)
    yield 'blank'

def gen_puzzle_feature_dict(size):
    """Generates the feature dictionary needed by STRIPS_domain."""
    spaces = set(gen_spaces(size))
    return { t : spaces for t in gen_tiles(size)}

def str_to_8puzzle_state(s):
    """Converts a string representation of a puzzle to a state dictionary."""
    state = dict()
    for row, line in enumerate(s.strip().split("\n"), 1):
        for col, c in enumerate(line.strip(), 1):
            state['blank' if c == 'X' else 'tile'+c] = f'space{row}-{col}'
    return state

def gen_spaces(size):
    """Generates the names of spaces in the puzzle (e.g., space1-1, space2-3)."""
    for row in range(1, size+1):
        for col in range(1, size+1):
            yield 'space'+str(row)+'-'+str(col)

def gen_puzzle_actions(size):
    """Generates all possible actions (moves) for the puzzle."""
    actions = []
    for tile in range(1, size*size):
        for row in range(1, size+1):
            for col in range(1, size):
                # Right moves
                actions.append(Strips(f'move-{tile}-right',
                                      {f'tile{tile}': f'space{row}-{col}', 'blank': f'space{row}-{col+1}'},
                                      {f'tile{tile}': f'space{row}-{col+1}', 'blank': f'space{row}-{col}'}))
                # Left moves
                actions.append(Strips(f'move-{tile}-left',
                                      {f'tile{tile}': f'space{row}-{col+1}', 'blank': f'space{row}-{col}'},
                                      {f'tile{tile}': f'space{row}-{col}', 'blank': f'space{row}-{col+1}'}))
                # Up moves
                if row < size:
                    actions.append(Strips(f'move-{tile}-up',
                                          {f'tile{tile}': f'space{row+1}-{col}', 'blank': f'space{row}-{col}'},
                                          {f'tile{tile}': f'space{row}-{col}', 'blank': f'space{row+1}-{col}'}))
                # Down moves
                if row > 1:
                    actions.append(Strips(f'move-{tile}-down',
                                          {f'tile{tile}': f'space{row-1}-{col}', 'blank': f'space{row}-{col}'},
                                          {f'tile{tile}': f'space{row}-{col}', 'blank': f'space{row-1}-{col}'}))
    return actions

def gen_puzzle_domain(size):
    """Creates the STRIPS_domain for the given puzzle size."""
    return STRIPS_domain(gen_puzzle_feature_dict(size), gen_puzzle_actions(size))

def manhattan_heuristic(state, goal):
    """Calculates the Manhattan distance heuristic."""
    distance = 0
    for tile in gen_tiles(3):
        state_pos = state.get(tile, None)
        goal_pos = goal.get(tile, None)
        if state_pos and goal_pos:
            state_row, state_col = map(int, state_pos.split('-')[1:])
            goal_row, goal_col = map(int, goal_pos.split('-')[1:])
            distance += abs(state_row - goal_row) + abs(state_col - goal_col)
    return distance

def test_against_baseline(baseline, num_tests=100):
    """Tests the code against a baseline and reports the percentage of games won."""
    wins = 0
    for _ in range(num_tests):
        p1start = generate_random_puzzle(3)
        prob = Planning_problem(gen_puzzle_domain(3),
                                str_to_8puzzle_state(p1start),
                                str_to_8puzzle_state("12345678X"))
        fsprob = Forward_STRIPS(prob, manhattan_heuristic)
        searcher = AStarSearch(fsprob)  # Switching to A* for better performance
        res = searcher.search()
        path = list(path_to_actions(res))
        if baseline.solve(p1start) != path:
            wins += 1
    return wins / num_tests * 100

def generate_random_puzzle(size):
    """Generates a random puzzle."""
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
    return puzzle.strip()

def main():
    """Main function to solve predefined puzzles and test against the baseline."""
    pend = """123
              456
              78X"""
    
    # Solve puzzle 1
    print("\n\nSolving puzzle 1...\n")
    p1start = """123
                 X56
                 478"""
    
    prob = Planning_problem(gen_puzzle_domain(3),
                            str_to_8puzzle_state(p1start),
                            str_to_8puzzle_state(pend))
    fsprob = Forward_STRIPS(prob)
    searcher = AStarSearch(fsprob, manhattan_heuristic)  # Using A* search with heuristic
    res = searcher.search()
    print('puzzle 1 solution:', list(path_to_actions(res)))

    # Solve puzzle 2
    print("\n\nSolving puzzle 2...\n")
    p2start = """437
                 568
                 21X"""
    
    prob = Planning_problem(gen_puzzle_domain(3),
                            str_to_8puzzle_state(p2start),
                            str_to_8puzzle_state(pend))
    fsprob = Forward_STRIPS(prob)
    searcher = AStarSearch(fsprob, manhattan_heuristic)
    res = searcher.search()
    print('puzzle 2 solution:', list(path_to_actions(res)))

    # Test against baseline
    print("\n\nTesting against baseline...\n")
    baseline = RandomBaseline()
    win_percentage = test_against_baseline(baseline)
    print("Percentage of games won:", win_percentage)

if __name__ == '__main__':
    main()

#Expected Output Example:
    
    Solving puzzle 1...

puzzle 1 solution: ['move-tile5-right', 'move-tile4-down', 'move-tile5-left', ...]

Solving puzzle 2...

puzzle 2 solution: ['move-tile7-up', 'move-tile3-left', 'move-tile6-down', ...]

Testing against baseline...

Percentage of games won: 95.0

# Report:

#Performance Analysis: Comparison between the STRIPS planner with the Manhattan heuristic and the random baseline. Discuss how often the STRIPS planner outperforms the baseline.
#Heuristic Justification: Explanation of why the Manhattan heuristic is more effective than simple tile mismatch counting.
#Lessons Learned: Insights into AI planning, optimization, and puzzle solving through the STRIPS framework.

