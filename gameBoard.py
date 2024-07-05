import tkinter as tk
import random
from functools import partial  # Import functools.partial

from legend import Legend


class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship Game")

        self.boardSize = 10
        self.cellSize = 30

        self.playerBoard = []
        self.opponentBoard = []

        self.current_turn = "Player"

        self.createBoard("Opponent", 0, "lightcoral")
        self.createBoard("Player", self.boardSize * self.cellSize + 60, "lightblue")

        self.ships = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
        self.current_ship_index = 0  # Index to track the current ship being placed
        self.current_ship = self.ships[self.current_ship_index]
        self.current_ship_label = tk.Label(root, text='Currently Placing: ' + self.current_ship)
        self.current_ship_label.grid(row=self.boardSize + 2, column=0, columnspan=self.boardSize + 1, pady=10)

        # Lists to store locations of player and enemy ships
        self.player_ships = [[False]*self.boardSize for _ in range(self.boardSize)]
        self.enemy_ships = [[False]*self.boardSize for _ in range(self.boardSize)]
        self.enemy_ship_count = 17
        self.player_ship_count = 17

        # Store ships' remaining hits
        self.player_ship_hits = {}
        self.enemy_ship_hits = {}

        # Place enemy ships - currently just set to randomly place them
        self.place_enemy_ships()

        # Add direction button so user knows which way ship will be placed
        self.ship_direction = 'horizontal'
        self.direction_button = tk.Button(root, text='Current Direction: ' + self.ship_direction, command=self.change_direction)
        self.direction_button.grid(row=self.boardSize + 2, column=self.boardSize + 2, pady=10)

        # Add label when a ship is sunk
        self.ship_sunk_label = tk.Label(root, text='')
        self.ship_sunk_label.grid(row=self.boardSize + 2, column=1, columnspan=4, pady=10)

        # Game Phase (False = placement phase, true = gameplay phase)
        self.gamePhase = False
        
        
        self.legend = Legend(self.root, x_offset=2)

    def createBoard(self, label, xOffset, color):
        boardFrame = tk.Frame(self.root, bg=color)
        boardFrame.grid(row=0, column=xOffset // self.cellSize, padx=10, pady=10)
        tk.Label(boardFrame, text=label, bg=color).grid(row=0, columnspan=self.boardSize + 1)

        for col in range(self.boardSize):
            tk.Label(boardFrame, text=str(col + 1), bg=color).grid(row=1, column=col + 1)

        for row in range(self.boardSize):
            tk.Label(boardFrame, text=chr(65 + row), bg=color).grid(row=row + 2, column=0)
            rowCells = []
            for col in range(self.boardSize):
                cellFrame = tk.Frame(boardFrame, width=self.cellSize, height=self.cellSize, bg=color,
                                     highlightbackground="black", highlightthickness=1)
                cellFrame.grid_propagate(False)
                cellFrame.grid(row=row + 2, column=col + 1)

                canvas = tk.Canvas(cellFrame, width=self.cellSize, height=self.cellSize, bg=color)
                canvas.pack()
                dotRadius = 2
                canvas.create_oval(
                    (self.cellSize - dotRadius) / 2, (self.cellSize - dotRadius) / 2,
                    (self.cellSize + dotRadius) / 2, (self.cellSize + dotRadius) / 2,
                    fill="white"
                )

                # Use functools.partial to bind the event with specific row, col, and board label
                canvas.bind("<Button-1>", partial(self.cellClicked, row, col, label))
                rowCells.append(canvas)
            if label == "Player":
                self.playerBoard.append(rowCells)
            else:
                self.opponentBoard.append(rowCells)

    def cellClicked(self, row, col, board_label, event):
        if self.gamePhase == False:
            # Placement phase logic
            if board_label == "Player":
                ship_size = self.get_ship_size(self.current_ship)
                if self.can_place_ship(row, col, ship_size):
                    self.place_ship(row, col, ship_size)
        else:
            # Gameplay phase logic
            if board_label == "Opponent":
                # Handle firing shots at opponent's board
                self.fire_shot(row, col)

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

    def can_place_ship(self, row, col, ship_size, is_player=True):
        # Check if the ship can be placed without overlapping or going out of bounds
        board = self.player_ships if is_player else self.enemy_ships
        if self.current_ship_index is not None:
            if self.ship_direction == "horizontal":
                if col + ship_size > self.boardSize:
                    return False
                return all(not board[row][col + i] for i in range(ship_size))
            else:  # vertical
                if row + ship_size > self.boardSize:
                    return False
                return all(not board[row + i][col] for i in range(ship_size))
        return False

    def place_ship(self, row, col, ship_size):
        # Place the ship on the player's board
        if self.ship_direction == "horizontal":
            for i in range(ship_size):
                self.playerBoard[row][col + i].create_rectangle(0, 0, self.cellSize, self.cellSize, fill="gray")
                self.player_ships[row][col + i] = self.current_ship
        else:  # vertical
            for i in range(ship_size):
                self.playerBoard[row + i][col].create_rectangle(0, 0, self.cellSize, self.cellSize, fill="gray")
                self.player_ships[row + i][col] = self.current_ship
        self.player_ship_hits[self.current_ship] = ship_size
        self.cycle_ship()

    def cycle_ship(self):
        # Cycle through ships in self.ships
        if self.current_ship_index < len(self.ships) - 1:
            self.current_ship_index += 1
            self.current_ship = self.ships[self.current_ship_index]
            self.current_ship_label.config(text='Currently Placing: ' + self.current_ship)
        else:
            self.current_ship_index = None
            self.current_ship_label.config(text="All Ships Placed!")
            self.gamePhase = True

    def change_direction(self):
        self.ship_direction = "vertical" if self.ship_direction == "horizontal" else "horizontal"
        self.direction_button.config(text='Current Direction: ' + self.ship_direction)

    def place_enemy_ships(self):
        for ship_name in self.ships:
            ship_size = self.get_ship_size(ship_name)
            placed = False
            while not placed:
                row = random.randint(0, self.boardSize - 1)
                col = random.randint(0, self.boardSize - 1)
                self.ship_direction = random.choice(["horizontal", "vertical"])
                if self.can_place_ship(row, col, ship_size, is_player=False):
                    if self.ship_direction == "horizontal" and col + ship_size <= self.boardSize:
                        for i in range(ship_size):
                            self.enemy_ships[row][col + i] = ship_name
                    elif self.ship_direction == "vertical" and row + ship_size <= self.boardSize:
                        for i in range(ship_size):
                            self.enemy_ships[row + i][col] = ship_name
                    self.enemy_ship_hits[ship_name] = ship_size
                    placed = True


    def fire_shot(self, row, col):
        self.ship_sunk_label.config(text='')
        if self.current_turn == "Player":
            if self.enemy_ships[row][col]:
                self.opponentBoard[row][col].create_rectangle(0, 0, self.cellSize, self.cellSize, fill="red")
                # self.enemy_ships[row][col] = False  # Mark the ship as hit (assuming ships can't be hit twice)
                self.current_ship_label.config(text=f"{self.current_turn} hit on {self.getBoardLabel(row, col)}")
                # Decrease opponent's ship count
                self.enemy_ship_count -= 1

                # Check if ship was sunk
                self.enemy_ship_hits[self.enemy_ships[row][col]] -= 1
                if self.enemy_ship_hits[self.enemy_ships[row][col]] == 0:
                    self.sink_ship(self.enemy_ships[row][col], self.opponentBoard, self.enemy_ships)

                # Check if opponent has no ships left
                if self.enemy_ship_count == 0:
                    self.display_winner("Player")
            else:
                self.opponentBoard[row][col].create_rectangle(0, 0, self.cellSize, self.cellSize, fill="white")
                self.current_ship_label.config(text=f"{self.current_turn} miss on {self.getBoardLabel(row, col)}")
                self.switch_turn()

        else:
            if self.player_ships[row][col]:
                self.playerBoard[row][col].create_rectangle(0, 0, self.cellSize, self.cellSize, fill="red")
                self.player_ships[row][col] = False  # Mark the ship as hit (assuming ships can't be hit twice)
                self.current_ship_label.config(text=f"{self.current_turn} hit on {self.getBoardLabel(row, col)}")
                # Decrease player's ship count
                self.player_ship_count -= 1

                # Check if player has no ships left
                if self.player_ship_count == 0:
                    self.display_winner("Opponent")
            else:
                self.playerBoard[row][col].create_rectangle(0, 0, self.cellSize, self.cellSize, fill="white")
                self.current_ship_label.config(text=f"{self.current_turn} miss on {self.getBoardLabel(row, col)}")
                self.switch_turn()

    def sink_ship(self, ship_id, board, ships):
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if ships[row][col] == ship_id:
                    board[row][col].create_rectangle(0, 0, self.cellSize, self.cellSize, fill="blue")
        self.ship_sunk_label.config(text=ship_id + ' sunk!')

    def getBoardLabel(self, row, col):
        label_row = chr(65 + row)
        label_col = str(col + 1)
        return f"{label_row}{label_col}"
        
    def switch_turn(self):
        self.current_turn = "Opponent" if self.current_turn == "Player" else "Player"
        self.legend.update_turn(self.current_turn)
        if self.current_turn == "Opponent":
            #Placeholder ai Logic
            row = random.randint(0, self.boardSize - 1)
            col = random.randint(0, self.boardSize - 1)
            self.fire_shot(row, col)
    def display_winner(self, winner):
        # Disable further gameplay
        self.gamePhase = None

        # Display winner message
        winner_label = tk.Label(self.root, text=f"{winner} wins!", font=("Helvetica", 24), fg="green")
        winner_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()
