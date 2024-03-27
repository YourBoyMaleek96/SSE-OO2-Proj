import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from GameList import Game, games_data

# Constant for color theme
BLUE = "#1f6aa5"

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
import tkinter as tk
from tkinter import ttk, messagebox
from GameList import Game, games_data

# Constant for color theme
BLUE = "#1f6aa5"

class GameShopGUI:
    def __init__(self, master):
        self.master = master
        master.title("GameShop")
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry(f"{width}x{height}")

        self.queue = Queue()
        self.total_customers = 25
        self.your_position = 10

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
                queue_label.config(text="Welcome to GameShop")
                self.show_game_info_page(queue_window)

        # Create label to display queue status spanning across the top
        queue_label = tk.Label(queue_window, text=f"You are {self.your_position}/{self.total_customers}. There are {self.your_position - 1} people in front of you.", font=("Helvetica", 12), bg=BLUE, fg="white")
        queue_label.pack(fill=tk.X, pady=(50, 0))

        # Start updating the queue label and countdown
        update_queue_label()

    def show_game_info_page(self, parent):
        # Create a new window for displaying game information
        game_info_window = tk.Toplevel(parent)
        game_info_window.title("Game Information")
        width = game_info_window.winfo_screenwidth()
        height = game_info_window.winfo_screenheight()
        game_info_window.geometry(f"{width}x{height}")

        # Create a frame to contain the Treeview
        frame = tk.Frame(game_info_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a Treeview widget for displaying the game information
        tree = ttk.Treeview(frame, columns=("Title", "Price", "Review", "Genre", "ESRB Rating", "Add to Cart"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        # Define column headings
        tree.heading("Title", text="Title", command=lambda: self.sort_column(tree, "Title"))
        tree.heading("Price", text="Price", command=lambda: self.sort_column(tree, "Price"))
        tree.heading("Review", text="Review", command=lambda: self.sort_column(tree, "Review"))
        tree.heading("Genre", text="Genre", command=lambda: self.sort_column(tree, "Genre"))
        tree.heading("ESRB Rating", text="ESRB Rating", command=lambda: self.sort_column(tree, "ESRB Rating"))
        tree.heading("Add to Cart", text="Add to Cart")

        # Insert game data into the Treeview with add to cart buttons
        for game_data in games_data:
            game = Game(**game_data)
            tree.insert("", "end", values=(game.title, game.price, game.review, game.genre, game.esrb_rating, ""),
                        tags=game.title)
            button = tk.Button(game_info_window, text="Add", command=lambda game=game: self.add_to_cart(game))
            tree.set(tree.tag_has(game.title), "Add to Cart", button)

        # Create a label to display welcome message
        welcome_label = tk.Label(game_info_window, text="Welcome to GameShop", font=("Helvetica", 24), bg=BLUE, fg="white")
        welcome_label.pack(fill=tk.X, pady=(50, 0))



if __name__ == "__main__":
    root = tk.Tk()
    app = GameShopGUI(root)
    root.mainloop()