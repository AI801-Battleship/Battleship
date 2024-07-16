import random

def random_ai(previous_info, board_size):
    # Generate random row and column until a unique guess is found
    while True:
        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)
        guess = chr(row + ord('A')) + str(col + 1)  # Convert to 'A1', 'B2', etc.
        
        # Check if the guess is not in previous_info keys
        if guess not in previous_info.keys():
            return guess