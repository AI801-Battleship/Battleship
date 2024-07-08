import tkinter as tk
import random
from functools import partial  # Import functools.partial

from legend import Legend  # Assuming this is your custom Legend class


class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship Game")

        self.board_size = 10
        self.cell_size = 30

        self.player_board = []
        self.opponent_board = []

        self.current_turn = "Player"

        self.create_board("Opponent", 0, "lightcoral")
        self.create_board("Player", self.board_size * self.cell_size + 60, "lightblue")

        self.ships = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
        self.current_ship_index = 0  # Index to track the current ship being placed
        self.current_ship = self.ships[self.current_ship_index]

        # Lists to store locations of player and enemy ships
        self.player_ships = [[False]*self.board_size for _ in range(self.board_size)]
        self.enemy_ships = [[False]*self.board_size for _ in range(self.board_size)]
        self.enemy_ship_count = 17
        self.player_ship_count = 17

        # Store ships' remaining hits
        self.player_ship_hits = {}
        self.enemy_ship_hits = {}
        # Entry widget for inputting coordinates
        self.coordinate_entry = tk.Entry(root)
        self.coordinate_entry.grid(row=self.board_size + 1, column=0, columnspan=self.board_size, pady=10, sticky=tk.W)

        # Add direction button so user knows which way ship will be placed
        self.ship_direction = 'horizontal'
        self.direction_button = tk.Button(root, text='Current Direction: ' + self.ship_direction, command=self.change_direction)
        self.direction_button.grid(row=self.board_size + 1, column=self.board_size, pady=10)

        # Button for placing ships
        self.place_ship_button = tk.Button(root, text="Place Ship: "+self.current_ship, command=self.place_ship_from_entry)
        self.place_ship_button.grid(row=self.board_size + 1, column=self.board_size + 1, pady=10)

        # Button for firing shots
        self.fire_shot_button = tk.Button(root, text="Fire Shot", command=self.fire_shot_from_entry)
        self.fire_shot_button.grid(row=self.board_size + 1, column=self.board_size + 2, pady=10)

        # Message bar to display game messages
        self.message_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.message_bar.grid(row=self.board_size + 2, column=0, columnspan=self.board_size + 3, padx=5, pady=10, sticky=tk.W+tk.E)




        # Game Phase (False = placement phase, true = gameplay phase)
        self.game_phase = False
        
        
        self.legend = Legend(self.root, x_offset=2)

    def create_board(self, label, x_offset, color):
        board_frame = tk.Frame(self.root, bg=color)
        board_frame.grid(row=0, column=x_offset // self.cell_size, padx=10, pady=10)
        tk.Label(board_frame, text=label, bg=color).grid(row=0, columnspan=self.board_size + 1)

        for col in range(self.board_size):
            tk.Label(board_frame, text=str(col + 1), bg=color).grid(row=1, column=col + 1)

        for row in range(self.board_size):
            tk.Label(board_frame, text=chr(65 + row), bg=color).grid(row=row + 2, column=0)
            row_cells = []
            for col in range(self.board_size):
                cell_frame = tk.Frame(board_frame, width=self.cell_size, height=self.cell_size, bg=color,
                                     highlightbackground="black", highlightthickness=1)
                cell_frame.grid_propagate(False)
                cell_frame.grid(row=row + 2, column=col + 1)

                canvas = tk.Canvas(cell_frame, width=self.cell_size, height=self.cell_size, bg=color)
                canvas.pack()
                dot_radius = 2
                canvas.create_oval(
                    (self.cell_size - dot_radius) / 2, (self.cell_size - dot_radius) / 2,
                    (self.cell_size + dot_radius) / 2, (self.cell_size + dot_radius) / 2,
                    fill="white"
                )

                row_cells.append(canvas)
            if label == "Player":
                self.player_board.append(row_cells)
            else:
                self.opponent_board.append(row_cells)

    def get_ship_size(self, ship_name):
        # Returns the size of the ship based on its name
        ship_sizes = {
            "Carrier": 5,
            "Battleship": 4,
            "Cruiser": 3,
            "Submarine": 3,
            "Destroyer": 2
        }
        return ship_sizes.get(ship_name, 0)
    
    def place_ship_from_entry(self):
        coordinate = self.coordinate_entry.get().upper()  # Get coordinate from entry and convert to uppercase

        if len(coordinate) < 2 or not coordinate[0].isalpha() or not coordinate[1:].isdigit():
            # Invalid coordinate format, handle error (e.g., show message)
            self.update_message("Invalid coordinate format. Please enter a valid coordinate (e.g., A1).")
            return

        row = ord(coordinate[0]) - ord('A')
        col = int(coordinate[1:]) - 1

        if self.current_ship_index is not None:
            ship_size = self.get_ship_size(self.current_ship)
            if self.can_place_ship(row, col, ship_size):
                self.place_ship(row, col, ship_size)
            else:
                self.update_message(f"Cannot place {self.current_ship} at {coordinate}. Try again.")
        else:
            self.update_message("All ships placed. Cannot place more ships.")

    def can_place_ship(self, row, col, ship_size, is_player=True):
        # Check if the ship can be placed without overlapping or going out of bounds
        board = self.player_ships if is_player else self.enemy_ships
        if self.current_ship_index is not None:
            if self.ship_direction == "horizontal":
                if col + ship_size > self.board_size:
                    return False
                return all(not board[row][col + i] for i in range(ship_size))
            else:  # vertical
                if row + ship_size > self.board_size:
                    return False
                return all(not board[row + i][col] for i in range(ship_size))
        return False

    def place_ship(self, row, col, ship_size):
        # Place the ship on the player's board
        if self.ship_direction == "horizontal":
            for i in range(ship_size):
                self.player_board[row][col + i].create_rectangle(0, 0, self.cell_size, self.cell_size, fill="gray")
                self.player_ships[row][col + i] = self.current_ship
        else:  # vertical
            for i in range(ship_size):
                self.player_board[row + i][col].create_rectangle(0, 0, self.cell_size, self.cell_size, fill="gray")
                self.player_ships[row + i][col] = self.current_ship
        self.player_ship_hits[self.current_ship] = ship_size
        self.cycle_ship()

    def cycle_ship(self):
        # Cycle through ships in self.ships
        if self.current_ship_index < len(self.ships) - 1:
            self.current_ship_index += 1
            self.current_ship = self.ships[self.current_ship_index]
            self.place_ship_button.config(text='Place Ship: ' + self.current_ship)
        else:
            self.current_ship_index = None
            self.update_message("All ships placed!")
            self.game_phase = True

    def change_direction(self):
        self.ship_direction = "vertical" if self.ship_direction == "horizontal" else "horizontal"
        self.direction_button.config(text='Current Direction: ' + self.ship_direction)

    def place_enemy_ships(self):
        for ship_name in self.ships:
            ship_size = self.get_ship_size(ship_name)
            placed = False
            while not placed:
                row = random.randint(0, self.board_size - 1)
                col = random.randint(0, self.board_size - 1)
                self.ship_direction = random.choice(["horizontal", "vertical"])
                if self.can_place_ship(row, col, ship_size, is_player=False):
                    if self.ship_direction == "horizontal" and col + ship_size <= self.board_size:
                        for i in range(ship_size):
                            self.enemy_ships[row][col + i] = ship_name
                    elif self.ship_direction == "vertical" and row + ship_size <= self.board_size:
                        for i in range(ship_size):
                            self.enemy_ships[row + i][col] = ship_name
                    self.enemy_ship_hits[ship_name] = ship_size
                    placed = True

    def fire_shot_from_entry(self):
        coordinate = self.coordinate_entry.get().upper()  # Get coordinate from entry and convert to uppercase

        if len(coordinate) < 2 or not coordinate[0].isalpha() or not coordinate[1:].isdigit():
            # Invalid coordinate format, handle error (e.g., show message)
            self.update_message("Invalid coordinate format. Please enter a valid coordinate (e.g., A1).")
            return

        row = ord(coordinate[0]) - ord('A')
        col = int(coordinate[1:]) - 1

        if self.game_phase:
            self.fire_shot(row, col)
        else:
            self.update_message("Gameplay phase has not started yet.")

    def fire_shot(self, row, col):
        self.update_message('')
        if self.current_turn == "Player":
            if self.enemy_ships[row][col]:
                self.opponent_board[row][col].create_rectangle(0, 0, self.cell_size, self.cell_size, fill="red")
                self.current_ship_label.config(text=f"{self.current_turn} hit on {self.get_board_label(row, col)}")
                self.enemy_ship_count -= 1

                self.enemy_ship_hits[self.enemy_ships[row][col]] -= 1
                if self.enemy_ship_hits[self.enemy_ships[row][col]] == 0:
                    self.sink_ship(self.enemy_ships[row][col], self.opponent_board, self.enemy_ships)

                if self.enemy_ship_count == 0:
                    self.display_winner("Player")
            else:
                self.opponent_board[row][col].create_rectangle(0, 0, self.cell_size, self.cell_size, fill="white")
                self.current_ship_label.config(text=f"{self.current_turn} miss on {self.get_board_label(row, col)}")
                self.switch_turn()

        else:
            if self.player_ships[row][col]:
                self.player_board[row][col].create_rectangle(0, 0, self.cell_size, self.cell_size, fill="red")
                self.current_ship_label.config(text=f"{self.current_turn} hit on {self.get_board_label(row, col)}")
                self.player_ship_count -= 1

                self.player_ship_hits[self.player_ships[row][col]] -= 1
                if self.player_ship_hits[self.player_ships[row][col]] == 0:
                    self.sink_ship(self.player_ships[row][col], self.player_board, self.player_ships)

                if self.player_ship_count == 0:
                    self.display_winner("Opponent")
            else:
                self.player_board[row][col].create_rectangle(0, 0, self.cell_size, self.cell_size, fill="white")
                self.current_ship_label.config(text=f"{self.current_turn} miss on {self.get_board_label(row, col)}")
                self.switch_turn()

    def sink_ship(self, ship_id, board, ships):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if ships[row][col] == ship_id:
                    board[row][col].create_rectangle(0, 0, self.cell_size, self.cell_size, fill="blue")
        self.update_message(ship_id + ' sunk!')

    def get_board_label(self, row, col):
        label_row = chr(65 + row)
        label_col = str(col + 1)
        return f"{label_row}{label_col}"
        
    def switch_turn(self):
        self.current_turn = "Opponent" if self.current_turn == "Player" else "Player"
        self.legend.update_turn(self.current_turn)
        if self.current_turn == "Opponent":
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            self.fire_shot(row, col)

    def display_winner(self, winner):
        self.game_phase = None
        winner_label = tk.Label(self.root, text=f"{winner} wins!", font=("Helvetica", 24), fg="green")
        winner_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def update_message(self, message):
        self.message_bar.config(text=message)


if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()
