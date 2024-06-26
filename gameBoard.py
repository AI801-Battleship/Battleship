import tkinter as tk

class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship Game")
        
        self.boardSize = 10
        self.cellSize = 30

        self.playerBoard = []
        self.opponentBoard = []

        self.createBoard("Opponent", 0, "lightcoral")
        self.createBoard("Player", self.boardSize * self.cellSize + 60, "lightblue")

    def createBoard(self, label, xOffset, color):
        boardFrame = tk.Frame(self.root, bg = color)
        boardFrame.grid(row = 0, column = xOffset // self.cellSize, padx = 10, pady = 10)
        tk.Label(boardFrame, text = label, bg = color).grid(row = 0, columnspan = self.boardSize + 1)

        for col in range(self.boardSize):
            tk.Label(boardFrame, text=str(col + 1), bg = color).grid(row = 1, column = col + 1)

        for row in range(self.boardSize):
            tk.Label(boardFrame, text = chr(65 + row), bg = color).grid(row = row + 2, column = 0)
            rowCells = []
            for col in range(self.boardSize):
                cellFrame = tk.Frame(boardFrame, width = self.cellSize, height = self.cellSize, bg = color, highlightbackground = "black", highlightthickness = 1)
                cellFrame.grid_propagate(False)
                cellFrame.grid(row = row + 2, column = col + 1)
                
                canvas = tk.Canvas(cellFrame, width = self.cellSize, height = self.cellSize, bg = color)
                canvas.pack()
                dotRadius = 2
                canvas.create_oval(
                    (self.cellSize - dotRadius) / 2, (self.cellSize - dotRadius) / 2,
                    (self.cellSize + dotRadius) / 2, (self.cellSize + dotRadius) / 2,
                    fill = "white"
                )
                
                canvas.bind("<Button-1>", lambda event, r = row, c = col: self.cellClicked(r, c, boardFrame))
                rowCells.append(canvas)
            if label == "Player":
                self.playerBoard.append(rowCells)
            else:
                self.opponentBoard.append(rowCells)

    def cellClicked(self, row, col, board):
        cell = board.grid_slaves(row = row + 2, column = col + 1)[0]
        canvas = cell.winfo_children()[0]
        canvas.create_rectangle(0, 0, self.cellSize, self.cellSize, fill = "red")
        cell.unbind("<Button-1>")

if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()
