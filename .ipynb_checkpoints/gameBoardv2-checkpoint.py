import tkinter as tk
import random
from functools import partial  # Import functools.partial

class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship Game")
        # Initial Board Setup
        self.boardSize = 10
        self.cellSize = 30
        self.player_1 = self.createBoard("Player 1", 0, "lightcoral")
        self.player_2 = self.createBoard("Player 2", self.boardSize * self.cellSize + 60, "lightblue")

        # Game Information
        self.gamePhase = "Placement"
        self.current_player = random.choice(["Player 1", "Player 2"])
        self.current_placement_direction = 'Horizontal'
        self.current_ship = "Carrier"  # Start with the Carrier
        
        # Ship Information - Dictionary containing lists which will hold ship locations
        self.player1_ships ={
            "Carrier": [],
            "Battleship": [],
            "Cruiser": [],
            "Submarine": [],
            "Destroyer": []
        }
        self.player2_ships ={
            "Carrier": [],
            "Battleship": [],
            "Cruiser": [],
            "Submarine": [],
            "Destroyer": []
        }
        
        # Input Box and Button for ship placement
        self.coordinate_entry = tk.Entry(self.root)
        self.coordinate_entry.grid(row=self.boardSize + 3, column=0)

        place_ship_button = tk.Button(self.root, text="Place Ship", command=self.place_ship_from_entry)
        place_ship_button.grid(row=self.boardSize + 3, column=1)

        # Message Box
        self.message_box = tk.Label(self.root, text="Placeholder")
        self.message_box.grid(row=self.boardSize + 5, column=0)

    # Board creation, currently unchanged from previous iteration
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
                rowCells.append(canvas)
        return rowCells

    def place_ship_from_entry(self):
        coordinate = self.coordinate_entry.get().upper()  # Get coordinate from entry and convert to uppercase

        if len(coordinate) < 2 or not coordinate[0].isalpha() or not coordinate[1:].isdigit():
            # Invalid coordinate format, handle error (e.g., show message)
            self.message_box.config(text="Invalid coordinate format. Please enter a valid coordinate (e.g., A1).")
            return

        row = ord(coordinate[0]) - ord('A')
        col = int(coordinate[1:]) - 1
        
        if self.isValidPlacement(row, col):
            self.placeShip(row, col)
            self.message_box.config(text=f"Placed {self.current_ship} at {coordinate}.")
            self.next_ship_to_place()  # Move to the next ship
        else:
            self.message_box.config(text=f"Cannot place {self.current_ship} at {coordinate}. Try again.")

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

    def isValidPlacement(self, row, col):
        ship_size = self.get_ship_size(self.current_ship)
        
        # Set variables for placement based on current player
        if self.current_player == "Player 1":
            ships = self.player1_ships
        else:
            ships = self.player2_ships
        
        # Horizontal orientation:
        if self.current_placement_direction == "Horizontal":
            # Out of Bounds check
            if (row < 0 or row >= self.boardSize or col < 0 or col + ship_size > self.boardSize):
                return False
            # Check for overlap with existing ships
            for i in range(ship_size):
                if ships[self.current_ship] and (row, col + i) in ships[self.current_ship]:
                    return False
        # Vertical orientation:
        elif self.current_placement_direction == "Vertical":
            # Out of bounds check
            if (row < 0 or row + ship_size > self.boardSize or col < 0 or col >= self.boardSize):
                return False
            # Check for overlap with existing ships
            for i in range(ship_size):
                if ships[self.current_ship] and (row + i, col) in ships[self.current_ship]:
                    return False
        
        return True

    def placeShip(self, row, col):
        # Place the ship on the board and record its positions
        ship_size = self.get_ship_size(self.current_ship)
        
        if self.current_player == "Player 1":
            board = self.player_1
            ships = self.player1_ships
        else:
            board = self.player_2
            ships = self.player2_ships
        
        if self.current_placement_direction == "Horizontal":
            for i in range(ship_size):
                board[row][col + i].create_rectangle(0, 0, self.cellSize, self.cellSize, fill="black")
                ships[current_ship].append((row, col + i))
        elif self.current_placement_direction == "Vertical":
            for i in range(ship_size):
                board[row + i][col].create_rectangle(0, 0, self.cellSize, self.cellSize, fill="black")
                ships[current_ship].append((row + i, col))

    def next_ship_to_place(self):
        # Cycle to the next ship to be placed
        ships_to_place = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
        current_index = ships_to_place.index(self.current_ship)
        next_index = (current_index + 1) % len(ships_to_place)
        self.current_ship = ships_to_place[next_index]

if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()
