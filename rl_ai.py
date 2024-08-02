import random
import numpy as np
import matplotlib.pyplot as plt
import itertools
from collections import deque


class BattleshipEnvImproved:
    def __init__(self, board_size=10):
        self.board_size = board_size
        self.ship_sizes = {
            "Carrier": 5,
            "Battleship": 4,
            "Cruiser": 3,
            "Submarine": 3,
            "Destroyer": 2
        }
        self.reset()

    def reset(self):
        self.board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.place_ships()
        self.previous_info = {}
        self.counter = 0
        return self.get_state()

    def place_ships(self):
        for ship_name, ship_size in self.ship_sizes.items():
            placed = False
            while not placed:
                is_horizontal = random.choice([True, False])
                if is_horizontal:
                    row = random.randint(0, self.board_size - 1)
                    col = random.randint(0, self.board_size - ship_size)
                    if all(self.board[row][col+i] == '.' for i in range(ship_size)):
                        for i in range(ship_size):
                            self.board[row][col+i] = ship_name
                        placed = True
                else:
                    row = random.randint(0, self.board_size - ship_size)
                    col = random.randint(0, self.board_size - 1)
                    if all(self.board[row+i][col] == '.' for i in range(ship_size)):
                        for i in range(ship_size):
                            self.board[row+i][col] = ship_name
                        placed = True

    def get_state(self):
        flat_board = [cell for row in self.board for cell in row]
        hit_count = sum(cell == 'H' for row in self.board for cell in row)
        miss_count = sum(cell == 'M' for row in self.board for cell in row)
        remaining_ships = [size for ship, size in self.ship_sizes.items() if any(ship in row for row in self.board)]
        state = tuple(flat_board + [hit_count, miss_count] + remaining_ships)
        return state

    def convert_to_RC(self, coordinate):
        row = ord(coordinate[0]) - ord('A')
        col = int(coordinate[1:]) - 1
        return row, col

    def step(self, action):
        row, col = action
        if self.board[row][col] != '.' and self.board[row][col] != 'H' and self.board[row][col] != 'M':     
            ship_hit = self.board[row][col]
            self.board[row][col] = 'H'  
            sink = True
            for r in range(self.board_size):
                if any(self.board[r][c] == ship_hit for c in range(self.board_size)):
                    sink = False
                    break
            if sink:
                reward = 10 + self.ship_sizes[ship_hit] * 2  # Larger reward for sinking bigger ships
                self.previous_info[(row, col)] = ['sunk', ship_hit]
            else:
                reward = 5 + self.ship_sizes[ship_hit]  # Reward proportional to the ship size hit
                self.previous_info[(row, col)] = ['hit', ship_hit]
        else:
            reward = -5  # Penalty for a miss
            self.board[row][col] = 'M'  # Mark the cell as miss
            self.previous_info[(row, col)] = ['miss', None]
        self.counter += 1

        # Check for adjacent hits and near misses
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row + i < self.board_size and 0 <= col + j < self.board_size:
                    if self.board[row + i][col + j] == 'H':
                        reward += 3  # Small reward for hitting near another hit

        done = not any(cell != '.' and cell != 'H' and cell != 'M' for row in self.board for cell in row)
        return self.get_state(), reward, done, {}

    def render(self):
        for row in self.board:
            print(' '.join(row))
        print()

class QLearningAgentImproved:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, epsilon_decay=0.995):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.visited = set()

    def choose_action(self, state):
        state_key = state
        if random.uniform(0, 1) < self.epsilon:
            action = (random.randint(0, 9), random.randint(0, 9))
            while action in self.visited:
                action = (random.randint(0, 9), random.randint(0, 9))
            return action
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros((10, 10))
        valid_actions = [(i, j) for i in range(10) for j in range(10) if (i, j) not in self.visited]
        if not valid_actions:
            return (random.randint(0, 9), random.randint(0, 9))
        best_action = max(valid_actions, key=lambda x: self.q_table[state_key][x[0], x[1]])
        return best_action

    def update_q_table(self, state, action, reward, next_state):
        state_key = state
        next_state_key = next_state
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros((10, 10))
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros((10, 10))
        best_next_action = max([(i, j) for i in range(10) for j in range(10)], key=lambda x: self.q_table[next_state_key][x[0], x[1]])
        td_target = reward + self.gamma * self.q_table[next_state_key][best_next_action[0], best_next_action[1]]
        td_error = td_target - self.q_table[state_key][action[0], action[1]]
        self.q_table[state_key][action[0], action[1]] += self.alpha * td_error

    def decay_epsilon(self):
        self.epsilon = max(0.01, self.epsilon * self.epsilon_decay)

def train_agent(env, agent, episodes=100, batch_size=10):
    experience_replay = deque(maxlen=10000)
    for episode in range(episodes):
        state = env.reset()
        agent.visited = set()
        done = False
        while not done:
            action = agent.choose_action(state)
            agent.visited.add(action)
            next_state, reward, done, _ = env.step(action)
            experience_replay.append((state, action, reward, next_state))
            if len(experience_replay) >= batch_size:
                minibatch = random.sample(experience_replay, batch_size)
                for s, a, r, ns in minibatch:
                    agent.update_q_table(s, a, r, ns)
            state = next_state
        agent.decay_epsilon()

env = BattleshipEnvImproved()
agent = QLearningAgentImproved()
train_agent(env, agent)

# Test the trained agent
results = []
for _ in range(100):
    state = env.reset()
    agent.visited = set()
    done = False
    while not done:
        action = agent.choose_action(state)
        agent.visited.add(action)
        state, _, done, _ = env.step(action)
    results.append(env.counter)
average_result = np.mean(results)

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(results) + 1), results, marker='o', linestyle='None', color='b', label='Results')
plt.plot([1, len(results)], [average_result, average_result], linestyle='--', color='r', label=f'Average: {average_result:.2f}')
plt.xlabel('Game Number')
plt.ylabel('Number of Strikes to Win')
plt.title('Improved Q-Learning AI Results from 100 Games')
plt.grid(True)
plt.ylim(0, 120)
plt.xlim(0, 101)
plt.legend()
plt.show()




# def grid_search(env, param_grid, episodes=100):
#     best_params = None
#     best_result = float('inf')
#     results = []

#     for params in param_grid:
#         alpha, gamma, epsilon, epsilon_decay = params
#         agent = QLearningAgentImproved(alpha=alpha, gamma=gamma, epsilon=epsilon, epsilon_decay=epsilon_decay)
#         train_agent(env, agent, episodes=episodes)
        
#         trial_results = []
#         for _ in range(20):  # Reduce the number of test games to speed up
#             state = env.reset()
#             agent.visited = set()
#             done = False
#             while not done:
#                 action = agent.choose_action(state)
#                 agent.visited.add(action)
#                 state, _, done, _ = env.step(action)
#             trial_results.append(env.counter)
        
#         average_result = np.mean(trial_results)
#         results.append((params, average_result))
        
#         if average_result < best_result:
#             best_result = average_result
#             best_params = params

#         print(f"Tested params: {params}, Average result: {average_result:.2f}")

#     print(f"Best parameters: {best_params} with average result: {best_result:.2f}")
#     return best_params, results

# param_grid = list(itertools.product(
#     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], 
#     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], 
#     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],  
#     [0.995]  
# ))

# best_params, results = grid_search(env, param_grid, episodes=100)

# plt.figure(figsize=(10, 6))
# params_str = [f"{p}" for p, _ in results]
# average_results = [res for _, res in results]
# plt.barh(params_str, average_results, color='skyblue')
# plt.xlabel('Average Number of Strikes to Win')
# plt.ylabel('Parameters')
# plt.title('Grid Search Results for Improved Q-Learning AI')
# plt.show()
