import random
import numpy as np
    # Essentially two phases of this algorithm - searching phase and killing phase.
    # In searching phase, we have not yet found any ships / the last found ship was already sunk.
    # For each spot on the board, we need to find how many ships can fit given the prior information in that spot. We will multiply each by a constant 1.1. (subject to change
    # To prevent reselects, any ship hit or sunk information will change the probability to zero. 
    
    #Ship information - will need to be dynamically updated as ships are sunk.

def pdf_ai(previous_info, board_size):
    # Define list of lists to represent board probabilities.
    # Start each as temporarily equal for every spot on the board. This will change as we do other calculations.
    probability_board = np.full((board_size, board_size), 1.0 / (board_size**2))
    
    # Ship information - will need to be dynamically updated as ships are sunk.
    ship_sizes = {
        "Carrier": 5,
        "Battleship": 4,
        "Cruiser": 3,
        "Submarine": 3,
        "Destroyer": 2
    }
    
    # List of available ships to be dynamically updated as ships are sunk.
    available_ships = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]

    # Function to convert coordinate to row, col format
    def convert_to_RC(coordinate):
        row = ord(coordinate[0]) - ord('A')
        col = int(coordinate[1:]) - 1
        return row, col
    
    # Iterate through previous_info to update probability_board
    for coord, (status, ship_name) in previous_info.items():
        row, col = convert_to_RC(coord)
        
        # Change probability to zero for any hits or sunk for that coord
        if status == 'hit' or status == 'sunk':
            probability_board[row, col] = 0
        
        # Remove sunk ship from available ships
        if status == 'sunk' and ship_name in available_ships:
            available_ships.remove(ship_name)

    # Determine the maximum ship size remaining in available ships
    max_length = max(ship_sizes[ship] for ship in available_ships)

    # Iterate through and adjust probabilities based on potential ship placements
    for row in range(board_size):
        for col in range(board_size):
            value = probability_board[row, col]
            
            # Skip zero probability cells
            if value == 0:
                continue

            # Define directions: Up, Down, Left, Right
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            # Counter to track how many ships (of max_length) can fit in each direction
            counter = 0
            
            # Check each direction
            for direction in directions:
                delta_row, delta_col = direction
                probe_row, probe_col = row, col
                
                # Iterate up to max_length in current direction
                for _ in range(max_length):
                    probe_row += delta_row
                    probe_col += delta_col
                    
                    # Check if probe cell is out of bounds or probability is zero
                    if (probe_row < 0 or probe_row >= board_size or
                        probe_col < 0 or probe_col >= board_size or
                        probability_board[probe_row, probe_col] == 0):
                        break
                    
                    # Increment counter for current direction
                    counter += 1
            
            # Adjust probability_board for the current cell
            probability_board[row, col] *= (1.1 ** counter)
    
    # Normalize probability_board to ensure sum of probabilities is 1
    total_probability = np.sum(probability_board)
    probability_board /= total_probability
    
    # Find the cell with the highest probability
    max_prob = np.max(probability_board)
    max_indices = np.argwhere(probability_board == max_prob)
    selected_index = random.choice(max_indices)
    selected_cell = chr(selected_index[0] + ord('A')) + str(selected_index[1] + 1)
    print(selected_cell)
    
    return selected_cell

# # Example usage:
# test_info = {
#     'A1': ('hit', 'Carrier'),
#     'D4': ('sunk', 'Carrier'),
#     'E5': ('hit', 'Submarine')
# }
# print(pdf_ai(test_info, 10))