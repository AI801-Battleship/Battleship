import random
import copy

class MonteCarloAI:
    def __init__(self, simulations=100):
        self.simulations = simulations
    
    def simulate_game(self, board, previous_info):
        board_copy = copy.deepcopy(board)
        previous_info_copy = copy.deepcopy(previous_info)
        counter = 0

        while self.check_ships_remaining(board_copy):
            # Use heuristic to generate a guess
            guess = self.heuristic_guess(previous_info_copy)
            row, col = self.convert_to_RC(guess)
            
            # Check for hits
            if board_copy[row][col] != '.':     
                ship_hit = board_copy[row][col]
                board_copy[row][col] = '.'  
                sink = True

                # See if ship was sunk
                for r in range(len(board_copy)):
                    if any(board_copy[r][c] == ship_hit for c in range(len(board_copy))):
                        sink = False
                        break
                if sink:
                    previous_info_copy[guess] = ['sunk', ship_hit]
                else:
                    previous_info_copy[guess] = ['hit', ship_hit]
            else:
                previous_info_copy[guess] = ['miss', None]
            counter += 1
        
        return counter

    # Find a random guess to test against
    def random_guess(self, board, previous_info):
        size = len(board)
        unexplored = [(row, col) for row in range(size) for col in range(size) if f"{chr(row + ord('A'))}{col + 1}" not in previous_info]
        if unexplored:
            return f"{chr(unexplored[0][0] + ord('A'))}{unexplored[0][1] + 1}"
        else:
            while True:
                row = random.randint(0, size - 1)
                col = random.randint(0, size - 1)
                coordinate = f"{chr(row + ord('A'))}{col + 1}"
                if coordinate not in previous_info:
                    return coordinate

    # Use heuristic to generate a guess
    def heuristic_guess(self, previous_info):
        size = len(previous_info)
        most_likely = [f"{chr(r + ord('A'))}{c + 1}" for r in range(size) for c in range(size)]
        middle = size // 2
        most_likely.sort(key=lambda x: abs(ord(x[0]) - ord('A') - middle) + abs(int(x[1:]) - middle))
        return most_likely[0]

    def convert_to_RC(self, coordinate):
        row = ord(coordinate[0]) - ord('A')
        col = int(coordinate[1:]) - 1
        return row, col

    def check_ships_remaining(self, board):
        for row in board:
            if any(cell != '.' for cell in row):
                return True
        return False

    def choose_move(self, previous_info, board_size):
        best_move = None
        best_result = float('inf')
        
        # Check random guess against heuristic guess and return better move based on simulations
        for _ in range(self.simulations):
            board_copy = [['.' for _ in range(board_size)] for _ in range(board_size)]
            move = self.random_guess(board_copy, previous_info)
            result = self.simulate_game(board_copy, previous_info)
            if result < best_result:
                best_result = result
                best_move = move
        
        return best_move
