import random
from random_ai import random_ai

def exploratory_local_search_ai(previous_info, board_size):
    
    def convert_to_RC(coordinate):
        row = ord(coordinate[0]) - ord('A')
        col = int(coordinate[1:]) - 1
        return row, col
    
    # Create a set to keep track of all sunk ship names
    sunk_ships = set()
    
    # Iterate through previous_info to find all sunk ships
    for coord, (status, ship_name) in previous_info.items():
        if status == 'sunk':
            sunk_ships.add(ship_name)
    
    # Create List containing all hits on ships that are not yet sunk from the previous information
    unsunk_hits = []
    for coord, (status, ship_name) in previous_info.items():
        if status == 'hit':
            # Check if the ship associated with the hit is not in sunk_ships
            if ship_name not in sunk_ships:
                unsunk_hits.append(coord)
    
    # If no known unsunk ships, default to random search behavior
    if len(unsunk_hits) == 0:
        return random_ai(previous_info, board_size)
    
    else:
        # Pick first element of unsunk_hits
        first_hit_row, first_hit_col = convert_to_RC(unsunk_hits[0])

        # Iterate through the rest of unsunk_hits starting from index 1
        for hit_coord in unsunk_hits[1:]:
            hit_row, hit_col = convert_to_RC(hit_coord)
            status, ship_name = previous_info[hit_coord]

            # Check if the ship of the hit is the same as the first hit
            if ship_name == previous_info[unsunk_hits[0]][1]:
                second_hit_row, second_hit_col = hit_row, hit_col
                
                # Determine the orientation based on the relationship between hits
                if first_hit_row == second_hit_row:
                    orientation = 'horizontal'
                else:
                    orientation = 'vertical'
                
                # Make guesses based on the determined direction
                while True:
                    if orientation == 'horizontal':
                        direction_chosen = random.choice([(0, -1), (0, 1)])  # Left or Right
                    else:
                        direction_chosen = random.choice([(-1, 0), (1, 0)])  # Up or Down
                    # Calculate new coordinates
                    new_row = first_hit_row + direction_chosen[0]
                    new_col = first_hit_col + direction_chosen[1]
                    new_guess = chr(new_row + ord('A')) + str(new_col + 1)
                    
                    # Keep going in the chosen direction until a free space is found
                    while new_guess in previous_info:
                        new_row += direction_chosen[0]
                        new_col += direction_chosen[1]
                        new_guess = chr(new_row + ord('A')) + str(new_col + 1)
                    
                    # Check if new coordinates are within board boundaries
                    if 0 <= new_row < board_size and 0 <= new_col < board_size: 
                        return new_guess
                    else:
                        break
        
        # If all directions from unsunk hits are invalid, choose a random direction
        while True:
            direction_chosen = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
            new_row = first_hit_row + direction_chosen[0]
            new_col = first_hit_col + direction_chosen[1]
            new_guess = chr(new_row + ord('A')) + str(new_col + 1)
            while new_guess in previous_info:
                new_row += direction_chosen[0]
                new_col += direction_chosen[1]
                new_guess = chr(new_row + ord('A')) + str(new_col + 1)
            # Ensure the new guess is within board boundaries and hasn't been guessed before
            if 0 <= new_row < board_size and 0 <= new_col < board_size and new_guess not in previous_info:
                return new_guess
