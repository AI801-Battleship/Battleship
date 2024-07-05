import tkinter as tk


class Legend:
    def __init__(self, root, x_offset, y_offset=0):
        self.root = root
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.create_legend()

    def create_legend(self):
        legend_frame = tk.Frame(self.root, bg="white", width=300, height=200)
        legend_frame.grid(row=self.y_offset, column=self.x_offset, padx=10, pady=10, sticky='n')
        # legend_frame.grid_propagate(False)

        tk.Label(legend_frame, text="Legend", bg="white", font=('Arial', 12, 'bold')).grid(row=0, column=0,
                                                                                           columnspan=2, pady=5)

        legend_items = [
            ("Ship", "black"),
            ("Hit", "red"),
            ("Miss", "white")
        ]

        for i, (text, color) in enumerate(legend_items, start=1):
            color_box = tk.Canvas(legend_frame, width=20, height=20, bg=color)
            color_box.grid(row=i, column=0, padx=5, pady=5)
            tk.Label(legend_frame, text=text, bg="white").grid(row=i, column=1, padx=5, pady=5)

            self.turn_label = tk.Label(legend_frame, text="Turn: Player", bg="white", font=('Arial', 12))
            self.turn_label.grid(row=len(legend_items) + 1, column=0, columnspan=2, pady=10)

    def update_turn(self, turn):
        self.turn_label.config(text="Turn: " + turn)
