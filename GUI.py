import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from GameList import Game, games_data

# Constant for color theme
BLUE = "#1f6aa5"
DARK = "gray14"
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.size += 1

    def dequeue(self):
        if not self.head:
            return None
        value = self.head.value
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self.size -= 1
        return value

class GameShopGUI:
    def __init__(self, master):
        self.master = master
        master.title("GameShop")
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry(f"{width}x{height}")

        self.queue = Queue()
        self.total_customers = 25
        self.your_position = 2

        # Create banner label spanning across the top
        self.banner_label = tk.Label(master, text="Welcome to GameShop", bg=BLUE, fg="white", font=("Helvetica", 24))
        self.banner_label.pack(fill=tk.X)

        # Create access button
        self.access_button = tk.Button(master, text="Access Website", bg=BLUE, fg="white", font=("Helvetica", 12), command=self.access_website)
        self.access_button.pack(pady=50)

    def access_website(self):
        """This function is used to start queue"""
        self.master.withdraw()

        # Create a new window for the queue updates
        queue_window = tk.Toplevel(self.master)
        queue_window.title("GameShop")
        width = queue_window.winfo_screenwidth()
        height = queue_window.winfo_screenheight()
        queue_window.geometry(f"{width}x{height}")

        def update_queue_label():
            """This function is used to update the queue and keep track of position"""
            if self.your_position > 2:
                self.your_position -= 1
                queue_label.config(text=f"You are {self.your_position}/{self.total_customers}. There are {self.your_position - 1} people in front of you.")
                queue_window.after(2000, update_queue_label)  # Re-schedule the update
            else:
                self.show_game_info_page(queue_window)

        # Create label to display queue status spanning across the top
        queue_label = tk.Label(queue_window, text=f"You are {self.your_position}/{self.total_customers}. There are {self.your_position - 1} people in front of you.", font=("Helvetica", 12), bg=BLUE, fg="white")
        queue_label.pack(fill=tk.X, pady=(50, 0))

        # Start updating the queue label and countdown
        update_queue_label()

    def sort_games(self, criterion="title", descending=False):
        """Sorts the list of games based on a given criterion."""
        if criterion == "title":
            sorted_games = sorted(games_data, key=lambda x: x[criterion], reverse=descending)
        elif criterion in ["price", "review"]:
            sorted_games = sorted(games_data, key=lambda x: float(x[criterion]), reverse=descending)
        else:
            sorted_games = games_data
        return sorted_games

    def show_game_info_page(self, queue_window):
        queue_window.destroy()
        game_info_window = tk.Toplevel(self.master)
        game_info_window.title("Welcome to Game Shop")
        width = game_info_window.winfo_screenwidth()
        height = game_info_window.winfo_screenheight()
        game_info_window.geometry(f"{width}x{height}")

        # Create a frame to contain the game information and filter selection box
        frame = tk.Frame(game_info_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Add filter selection box on the left
        filter_label = tk.Label(frame, text="Filter by:", font=("Helvetica", 12))
        filter_label.grid(row=0, column=0, padx=(0, 5), sticky="e")
        filter_options = [
            "Alphabetically: A-Z",
            "Alphabetically: Z-A",
            "Price: High to Low",
            "Price: Low to High",
            "Review: High to Low",
            "Review: Low to High"
        ]
        filter_combobox = ttk.Combobox(frame, values=filter_options, state="readonly", width=20)
        filter_combobox.current(0)  # Select the first option by default
        filter_combobox.grid(row=0, column=1, padx=(0, 10), sticky="w")

        # Create a Canvas widget for scrolling
        canvas = tk.Canvas(frame)
        canvas.grid(row=0, column=2, rowspan=2, sticky="nsew")

        # Create a scrollbar for the canvas
        v_scroll = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        v_scroll.grid(row=0, column=3, rowspan=2, sticky="ns")

        # Configure canvas to use scrollbar
        canvas.configure(yscrollcommand=v_scroll.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Add column headers
        headers = ["Title", "Price", "Review Score", "Genre", "ESRB Rating"]
        for idx, header in enumerate(headers):
            header_label = tk.Label(inner_frame, text=header, font=("Helvetica", 14))
            header_label.grid(row=0, column=idx, padx=10)

        # Display sorted game data
        sorted_games_data = self.sort_games("title", False)
        for idx, game_data in enumerate(sorted_games_data, start=1):
            game = Game(**game_data)

            # Display Game Title, Price, Review Score, Genre, and ESRB Rating
            tk.Label(inner_frame, text=game.title, font=("Helvetica", 14), anchor="center").grid(row=idx, column=0, pady=(10, 0), sticky= "nsew")
            tk.Label(inner_frame, text=f"${game.price}", font=("Helvetica", 14), anchor="center").grid(row=idx, column=1, pady=(10, 0), sticky= "nsew")
            tk.Label(inner_frame, text=f"{game.review} / 5", font=("Helvetica", 14), anchor="center").grid(row=idx, column=2, pady=(10, 0), sticky= "nsew")
            tk.Label(inner_frame, text=game.genre, font=("Helvetica", 14), anchor="center").grid(row=idx, column=3, pady=(10, 0), sticky= "nsew")
            tk.Label(inner_frame, text=game.esrb_rating, font=("Helvetica", 14), anchor="center").grid(row=idx, column=4, pady=(10, 0), sticky= "nsew")
        
            # Add to Cart button
            add_to_cart_button = tk.Button(inner_frame, text="Add to Cart", bg="blue")
            add_to_cart_button.grid(row=idx, column=5, padx=10, pady=(10, 0))
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Bind the inner frame to the canvas
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # Stretch game info 
        frame.columnfigure(2, weight = 1) 
        frame.rowconfigure(0, weight = 1)


if __name__ == "__main__":
    root = tk.Tk()
    app = GameShopGUI(root)
    root.mainloop()