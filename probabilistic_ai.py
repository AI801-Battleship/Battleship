import numpy as np
import random

def convert_to_RC(coordinate):
    row = ord(coordinate[0]) - ord('A')
    col = int(coordinate[1:]) - 1
    return row, col

def probabilistic_ai(previous_info, board_size=10):
    if 'heatmap' not in previous_info:
        previous_info['heatmap'] = np.ones((board_size, board_size))
    
    heatmap = previous_info['heatmap']

    # Reduce the probability of already guessed cells to zero
    for guess, result in previous_info.items():
        if isinstance(result, list):
            row, col = convert_to_RC(guess)
            heatmap[row][col] = 0
    
    # Update heatmap based on hits and adjacent cells
    for guess, result in previous_info.items():
        if isinstance(result, list) and result[0] == 'hit':
            row, col = convert_to_RC(guess)
            for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
                if 0 <= r < board_size and 0 <= c < board_size:
                    if heatmap[r][c] != 0:
                        heatmap[r][c] += 1
    
    # Make the heatmap a probability distribution
    total = np.sum(heatmap)
    if total > 0:
        heatmap /= total

    # Pick the cell with the highest probability
    max_prob = np.max(heatmap)
    best_guesses = np.argwhere(heatmap == max_prob)
    row, col = random.choice(best_guesses)

    # Convert row, col to coordinate
    guess = chr(row + ord('A')) + str(col + 1)
    return guess
