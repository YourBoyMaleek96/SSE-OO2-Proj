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
        """Show the game info page and allows you to add games to cart"""
        game_info_window = tk.Toplevel(parent)
        game_info_window.title("Welcome to  Game Shop")
        width = game_info_window.winfo_screenwidth()
        height = game_info_window.winfo_screenheight()
        game_info_window.geometry(f"{width}x{height}")

        # Create a frame to contain the game information
        frame = tk.Frame(game_info_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Add padding

        # Create a Canvas widget for scrolling
        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar for the canvas
        v_scroll = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        v_scroll.pack(side=tk.RIGHT, fill="y")

        # Configure canvas to use scrollbar
        canvas.configure(yscrollcommand=v_scroll.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Create labels for column headers
        title_header_label = tk.Label(inner_frame, text="Title", font=("Helvetica", 14))
        title_header_label.grid(row=0, column=0, padx=10)
        price_header_label = tk.Label(inner_frame, text="Price", font=("Helvetica", 14))
        price_header_label.grid(row=0, column=1, padx=10)
        esrb_header_label = tk.Label(inner_frame, text="ESRB Rating", font=("Helvetica", 14))
        esrb_header_label.grid(row=0, column=2, padx=10)
        genre_header_label = tk.Label(inner_frame, text="Genre", font=("Helvetica", 14))
        genre_header_label.grid(row=0, column=3, padx=10)

        # Insert game data with buttons
        for idx, game_data in enumerate(games_data, start=1):
            game = Game(**game_data)

            # Display game title
            title_label = tk.Label(inner_frame, text=game.title, font=("Helvetica", 14), anchor="center")
            title_label.grid(row=idx * 2, column=0, pady=(10, 0))

            # Display game price
            price_label = tk.Label(inner_frame, text=f"${game.price}", font=("Helvetica", 14), anchor="center")
            price_label.grid(row=idx * 2, column=1, pady=(10, 0))

            # Display game ESRB rating
            esrb_label = tk.Label(inner_frame, text=game.esrb_rating, font=("Helvetica", 14), anchor="center")
            esrb_label.grid(row=idx * 2, column=2, pady=(10, 0))

            # Display game genre
            genre_label = tk.Label(inner_frame, text=game.genre, font=("Helvetica", 14), anchor="center")
            genre_label.grid(row=idx * 2, column=3, pady=(10, 0))

            # Add spacing between each game entry
            tk.Label(inner_frame, text="", font=("Helvetica", 14)).grid(row=idx * 2 + 1, columnspan=4)

           # Add to Cart button
            add_to_cart_button = tk.Button(inner_frame, text="Add to Cart" , bg = BLUE, command=lambda g=game: self.add_to_cart(g))
            add_to_cart_button.grid(row=idx * 2, column=4, pady=(10, 0))

        # Bind the inner frame to the canvas
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Add the canvas to the window
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add padding to the bottom for better spacing
        tk.Label(inner_frame, text="", font=("Helvetica", 14)).grid(row=len(games_data) * 2 + 2, columnspan=6, pady=(10, 0))




    

if __name__ == "__main__":
    root = tk.Tk()
    app = GameShopGUI(root)
    root.mainloop()