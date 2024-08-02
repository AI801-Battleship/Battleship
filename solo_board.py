# Function: Used for model training
# Input: ai_model = used for decision making on firing shots
#        board_size = parameters of the board that need to be passed through - only needed if we are altering the board for alternative game modes.
# Output: returns number of strikes needed to win the game.
import random
from random_ai import random_ai
from exploratory_local_search_ai import exploratory_local_search_ai
from probabilistic_ai import probabilistic_ai
from monte_carlo_ai import MonteCarloAI
import matplotlib.pyplot as plt
import numpy as np



def play_solo_board(ai_model, board_size=10):
    ship_sizes = {
        "Carrier": 5,
        "Battleship": 4,
        "Cruiser": 3,
        "Submarine": 3,
        "Destroyer": 2
        }
    #Initialize empty board.
    board = [['.' for _ in range(board_size)] for _ in range(board_size)]

    # Randomly place ships.
    for ship_name, ship_size in ship_sizes.items():
        placed = False
        while not placed:
            is_horizontal = random.choice([True, False])
            if is_horizontal:
                # Generate random starting position for a horizontal ship
                row = random.randint(0, board_size - 1)
                col = random.randint(0, board_size - ship_size - 1)
                
                # Check if the positions are valid (no overlap)
                if all(board[row][col+i] == '.' for i in range(ship_size)):
                    # Place the ship on the board
                    for i in range(ship_size):
                        board[row][col+i] = ship_name
                    placed = True
            else:
                row = random.randint(0, board_size - ship_size - 1)
                col = random.randint(0, board_size - 1)
                # Check if the positions are valid (no overlap)
                if all(board[row+i][col] == '.' for i in range(ship_size)):
                    # Place the ship on the board
                    for i in range(ship_size):
                        board[row+i][col] = ship_name
                    placed = True
    
    #Prior Information used for models
        #Hold array of all previous guesses
    previous_info = {}
    
    #Function to convert guess into row, col
    def convert_to_RC(coordinate):
        row = ord(coordinate[0]) - ord('A')
        col = int(coordinate[1:]) - 1
        return row, col
    
    # Check if there are still ships remaining on the board
    def check_ships_remaining(board):
        for row in board:
            if any(cell != '.' for cell in row):
                return True
        return False
    
    # Counter used for final output of this function
    counter = 0
    
    #Actually playing
    while check_ships_remaining(board):
        #Input information to the ai_model which returns a coordinate to guess
        #Assume the model has mechanism of checking a repeat move
        guess = ai_model(previous_info, board_size=10)
        row,col = convert_to_RC(guess)
        if board[row][col] != '.':     
            ship_hit = board[row][col]
            # Change the board
            board[row][col] = '.'  
            #sink
            sink = True
            for r in range(board_size):
                if any(board[r][c] == ship_hit for c in range(board_size)):
                    sink = False
                    break
            if sink:
                previous_info[guess] = ['sunk', ship_hit]
            else:
                previous_info[guess] = ['hit', ship_hit]
        else:
            # Miss
            previous_info[guess] = ['miss', None]
        counter += 1
    return counter

results = []

monte_carlo_ai_model = MonteCarloAI(simulations=100)

# Run the function 100 times
for _ in range(100):
    result = play_solo_board(monte_carlo_ai_model.choose_move)
    results.append(result)
average_result = np.mean(results)

# Line plot with circles for each result
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(results) + 1), results, marker='o', linestyle='None', color='b', label='Results')
plt.plot([1, len(results)], [average_result, average_result], linestyle='--', color='r', label=f'Average: {average_result:.2f}')
plt.xlabel('Game Number')
plt.ylabel('Number of Strikes to Win')
plt.title('Random AI results from 100 games')
plt.grid(True)
plt.ylim(0, 120)  # Adjust as needed based on your data range
plt.xlim(0, 101)  # Start x-axis at 1 to match the game number
plt.legend()
plt.show()