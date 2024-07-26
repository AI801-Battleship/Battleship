import numpy as np
import random

def convert_to_RC(coordinate):
    row = ord(coordinate[0]) - ord('A')
    col = int(coordinate[1:]) - 1
    return row, col

def convert_to_coordinate(row, col):
    return chr(row + ord('A')) + str(col + 1)

def probabilistic_ai(previous_info, board_size=10):
    # List of available ships with their sizes
    ship_sizes = {
        "Carrier": 5,
        "Battleship": 4,
        "Cruiser": 3,
        "Submarine": 3,
        "Destroyer": 2
    }
    
    available_ships = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
    
    # Initialize hits list
    hits = []
    
    # Process hits and sunk ships
    for coord, result in previous_info.items():
        if isinstance(result, list):
            if result[0] == 'sunk' and result[1] in available_ships:
                available_ships.remove(result[1])
                # Remove all hits associated with this sunk ship
                hits = [(rc, ship) for rc, ship in hits if ship != result[1]]
            elif result[0] == 'hit':
                hits.append((convert_to_RC(coord), result[1]))

    # Determine the maximum ship size remaining in available ships
    if available_ships:
        max_length = max(ship_sizes[ship] for ship in available_ships)
    else:
        max_length = 0  # No ships remaining
    
    # Initialize heatmap for potential guesses
    probability_board = np.zeros((board_size, board_size))
    
    # Process hits to calculate probabilities
    for (hit_row, hit_col), ship_hits in hits:
        # Check in each direction: Up, Down, Left, Right
        for delta_row, delta_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            direction_length = 0
            probe_row, probe_col = hit_row, hit_col
            
            # Check availability of spaces in each direction
            while True:
                probe_row += delta_row
                probe_col += delta_col
                
                # Ensure probe is within bounds
                if not (0 <= probe_row < board_size and 0 <= probe_col < board_size):
                    break
                
                guess = convert_to_coordinate(probe_row, probe_col)
                
                if (probe_row, probe_col) in [(r, c) for (r, c), _ in hits]:
                    direction_length += 1
                elif guess in previous_info:
                    if previous_info[guess][0] == 'miss':
                        break
                else:
                    direction_length += 1
                    probability_board[probe_row, probe_col] += direction_length
                    break

    # If there are hits, use the probability board to select a target
    if np.any(probability_board):
        max_prob = np.max(probability_board)
        best_guesses = np.argwhere(probability_board == max_prob)
        selected_row, selected_col = random.choice(best_guesses)
        return convert_to_coordinate(selected_row, selected_col)
    
    # If no hit, unsunk ships, search for the best positions to place the largest remaining ship
    for row in range(board_size):
        for col in range(board_size):
            # Check horizontal placement
            if col + max_length <= board_size:
                valid = True
                for k in range(max_length):
                    guess = convert_to_coordinate(row, col + k)
                    if guess in previous_info:
                        valid = False
                        break
                if valid:
                    for k in range(max_length):
                        probability_board[row, col + k] += 1
            
            # Check vertical placement
            if row + max_length <= board_size:
                valid = True
                for k in range(max_length):
                    guess = convert_to_coordinate(row + k, col)
                    if guess in previous_info:
                        valid = False
                        break
                if valid:
                    for k in range(max_length):
                        probability_board[row + k, col] += 1

    # Select the cell with the highest probability
    max_prob = np.max(probability_board)
    best_guesses = np.argwhere(probability_board == max_prob)
    selected_row, selected_col = random.choice(best_guesses)
    return convert_to_coordinate(selected_row, selected_col)
