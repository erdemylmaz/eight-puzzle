import random
import copy

# i will use heuristicts, (wrong count)
# a* algorithm

# goal state:
# 1 2 3
# 4 5 6
# 7 8 

def main():
    initial_board = { "board": [[1,3,5], [4,2, None], [7,8,6]]}
    # initial_board = create_board()
    current_board = initial_board

    print("initial board: ")
    print("heuristic: ", find_heuristic(current_board["board"]))
    print_board(current_board["board"])
    print(" SOLVING... ")

    is_solved = False

    active_boards = []
    controlled_boards = []

    counter = 0

    while not is_solved:
        print("\n\nstep: ", counter)
        counter += 1
        
        if counter == 1:
            current_board["parent_nodes"] = []
        
        current_possibilities = find_possibilities(current_board["board"])

        for possibility in current_possibilities:
            possibility["parent_nodes"] = []
            possibility["parent_nodes"] += current_board["parent_nodes"] + [{"board": current_board["board"], "possibility_action": possibility["possibility_action"]}]

        active_boards += current_possibilities

        least_heuristic = 100

        for active_board in active_boards:
            if active_board["heuristic"] < least_heuristic and active_board["board"] not in controlled_boards:
                least_heuristic = active_board["heuristic"]
                current_board = active_board

        active_boards.remove(current_board)

        if current_board["heuristic"] == 0:
            is_solved = True
            
        controlled_boards.append(current_board)

        print(" ")
        print("least heuristic: ", least_heuristic)
        print("current board: ")
        print_board(current_board["board"])

    if is_solved:
        print("Found in ", counter, " steps")
        print("\n\nSolution: ")
        step = 0
        for board_index, board in enumerate(current_board["parent_nodes"]):
            step += 1
            print()
            print("-" * len(board["possibility_action"]))
            print(" # Step: ", step)
            
            try:
                next_board = current_board["parent_nodes"][board_index + 1]["board"]
            except IndexError:
                next_board = current_board["board"]


            print(board["possibility_action"])
            print("-" * len(board["possibility_action"]))
            print_board(board["board"])
            print("\n- to - \n") 
            print_board(next_board)
            print()

        print("Problem Solved...")


def find_empty(board):
    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if not col:
                return row_index, col_index

def update_board(board, moving_row, moving_col, new_row, new_col):
    copied_board = copy.deepcopy(board)
    copied_board[new_row][new_col] = copied_board[moving_row][moving_col]
    copied_board[moving_row][moving_col] = None

    return copied_board

def find_possibilities(board):
    empty_row, empty_col = find_empty(board)

    # empty up neighbor to down
    # empty down neighbor to up
    # empty left neighbor to right
    # empty right neighbor to left

    # there is max 4 possibility for each board,

    possibilities = []

    for neighbor in ["up", "down", "left", "right"]:
        is_possible = True
        neighbor_row = empty_row
        neighbor_col = empty_col

        if neighbor == "up":
            neighbor_row = empty_row - 1

            if neighbor_row < 0:
                is_possible = False
        elif neighbor == "down":
            neighbor_row = empty_row + 1

            if neighbor_row > 2:
                is_possible = False
        elif neighbor == "left":
            neighbor_col = empty_col - 1

            if neighbor_col < 0:
                is_possible = False
        elif neighbor == "right":
            neighbor_col = empty_col + 1

            if neighbor_col > 2:
                is_possible = False

        if is_possible:
            possible_board = update_board(board, neighbor_row, neighbor_col, empty_row, empty_col)
            changing_number = board[neighbor_row][neighbor_col]
            action_name = ""
            if neighbor == "up":
                action_name = "down"
            elif neighbor == "down":
                action_name = "up"
            elif neighbor == "left":
                action_name = "right"
            elif neighbor == "right":
                action_name = "left"

            action = f"move {changing_number} to {action_name}"

            possible = {
                        "board": possible_board,
                        "heuristic": find_heuristic(possible_board),
                        "possibility_action": action
                    }

            possibilities.append(possible)

    return possibilities


def find_heuristic(board):
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, None]]
    total_heuristic = 0

    for row_index, row in enumerate(board):
        for col_index, number in enumerate(row):
             if number:
                col_heuristic = 0

                col_correct_row = (number - 1) // 3
                col_correct_col = (number - 1) % 3

                distance_row = abs(col_correct_row - row_index)
                distance_col = abs(col_correct_col - col_index)

                col_heuristic = distance_row + distance_col

                total_heuristic += col_heuristic


    return total_heuristic


def print_board(board, end = "\n"):
    for row in board:
        for col in row:
            if col:
                print(col, end=" ")
            else:
                print(" ", end=" ")

        print("")

def create_board():
    used_numbers = []

    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]

    for i in range(8):
        random_number = random.randint(1, 8)

        while random_number in used_numbers:
            random_number = random.randint(1, 8)

        used_numbers.append(random_number)

        random_row = random.randint(0, 2)
        random_col = random.randint(0, 2)

        while board[random_row][random_col]:
            random_row = random.randint(0, 2)
            random_col = random.randint(0, 2)

        board[random_row][random_col] = random_number
            
    board = {
            "board": board,
            }

    return board

if __name__ == "__main__":
    main()
    
    


