import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from GameList import Game, games_data, GameGraph,get_games
import random
from Sort import merge_sort, quick_sort, selection_sort, bubble_sort, insertion_sort, heap_sort

# Constants for color theme
BLUE = "#1f6aa5"
DARK = "gray14"

#Node Class
class Node:
    #Initialization
    def __init__(self, value):
        self.value = value
        self.next = None

#Queue Class
class Queue:
    #Initialization
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    #Enters item into queue
    def enqueue(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.size += 1

    #Removes item from queue
    def dequeue(self):
        if not self.head:
            return None
        value = self.head.value
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self.size -= 1
        return value

#Stack Class
class Stack:
    #Initialization
    def __init__(self):
        self.items = []
    
    #Push item into stack
    def push(self, item):
        self.items.append(item)
    
    #Pops item out of stack
    def pop(self):
        return self.items.pop() if not self.is_empty() else None
    
    #Peeks next item in stack
    def peek(self):
        return self.items[-1] if not self.is_empty() else None
    
    #Check if stack is empty
    def is_empty(self):
        return len(self.items) == 0
    
    #Returns size of stack
    def size(self):
        return len(self.items)

#Binary Search Tree Node Class
class BSTNode:
    #Initialization
    def __init__(self, genre):
        self.genre = genre
        self.games = []
        self.left = None
        self.right = None

#Binary Search Tree Class
class BinarySearchTree:
    #Initialization
    def __init__(self):
        self.root = None

    #Insert item into tree
    def insert(self, game):
        if self.root is None:
            self.root = BSTNode(game.genre)
            self.root.games.append(game)
        else:
            self._insert_recursive(self.root, game)

    #Recursively inserts item
    def _insert_recursive(self, node, game):
        if game.genre < node.genre:
            if node.left is None:
                node.left = BSTNode(game.genre)
                node.left.games.append(game)
            else:
                self._insert_recursive(node.left, game)
        elif game.genre > node.genre:
            if node.right is None:
                node.right = BSTNode(game.genre)
                node.right.games.append(game)
            else:
                self._insert_recursive(node.right, game)
        else:
            node.games.append(game)

    #Tree traversal
    def in_order_traversal(self):
        games_by_genre = []
        self._in_order_recursive(self.root, games_by_genre)
        return games_by_genre

    #Recursive tree traversal
    def _in_order_recursive(self, node, games_by_genre):
        if node is not None:
            self._in_order_recursive(node.left, games_by_genre)
            games_by_genre.append((node.genre, node.games))
            self._in_order_recursive(node.right, games_by_genre)

#GUI Class
class GameShopGUI:
    #Initialization
    def __init__(self, master):
        self.master = master
        master.title("GameShop")
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry(f"{width}x{height}")
        self.cart = Stack()
        self.temp_cart = Stack()
        self.cart_display = None
        self.cart_listbox = None
        self.game_graph = None
        self.queue = Queue()
        self.total_customers = 25
        self.your_position = random.randint(3, 23)
        self.games_data = games_data

        self.banner_label = tk.Label(master, text="Welcome to GameShop", bg=BLUE, fg="white", font=("Helvetica", 24))
        self.banner_label.pack(fill=tk.X)

        self.access_button = tk.Button(master, text="Access Website", bg=BLUE, fg="white", font=("Helvetica", 12), command=self.access_website)
        self.access_button.pack(pady=50)

    #Start of program and queue
    def access_website(self):
        self.master.withdraw()
        self.game_graph = GameGraph(get_games())
        queue_window = tk.Toplevel(self.master)
        queue_window.title("GameShop")
        width = queue_window.winfo_screenwidth()
        height = queue_window.winfo_screenheight()
        queue_window.geometry(f"{width}x{height}")

        #Updates queue
        def update_queue_label():
            if self.your_position > 2:
                self.your_position -= 1
                queue_label.config(text=f"You are {self.your_position}/{self.total_customers}. There are {self.your_position - 1} people in front of you.")
                queue_window.after(2000, update_queue_label)
            else:
                self.show_game_info_page(queue_window)

        queue_label = tk.Label(queue_window, text=f"You are {self.your_position}/{self.total_customers}. There are {self.your_position - 1} people in front of you.", font=("Helvetica", 12), bg=BLUE, fg="white")
        queue_label.pack(fill=tk.X, pady=(50, 0))

        update_queue_label()

    #Adds game to checkout cart
    def add_to_cart(self, game_data):
        self.cart.push(game_data)
        self.last_added_genre = game_data['genre'] 
        self.update_cart_display()
        self.update_recommended_games()

    #Game sorting function
    def sort_games(self, sort_criteria, order="ascending"):
        """Sorts the list of games based on a given criterion."""
        games = self.games_data

        if sort_criteria == 'title':
            key_func = lambda game: game[sort_criteria]
            if order == "ascending":
                sorted_games = merge_sort(games, key=key_func)
            else:
                sorted_games = quick_sort(games, key=key_func)

        elif sort_criteria == 'price':
            key_func = lambda game: game[sort_criteria]
            if order == "ascending":
                sorted_games = insertion_sort(games, key=key_func)
            else:
                sorted_games = heap_sort(games, key=key_func)

        elif sort_criteria == 'review':
            key_func = lambda game: game[sort_criteria]
            if order == "ascending":
                sorted_games = bubble_sort(games, key=key_func)
            else:
                sorted_games = selection_sort(games, key=key_func)

        return sorted_games

    #Function to display games list on screen
    def display_games(self, sorted_games_data):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        headers = ["Title", "Price", "Review Score", "Genre", "ESRB Rating"]
        for idx, header in enumerate(headers):
            header_label = tk.Label(self.inner_frame, text=header, font=("Helvetica", 14))
            header_label.grid(row=0, column=idx, padx=10)

        for idx, game_data in enumerate(sorted_games_data, start=1):
            game = Game(**game_data)

            tk.Label(self.inner_frame, text=game.title, font=("Helvetica", 14)).grid(row=idx, column=0, pady=(10, 0))
            tk.Label(self.inner_frame, text=f"${game.price}", font=("Helvetica", 14)).grid(row=idx, column=1, pady=(10, 0))
            tk.Label(self.inner_frame, text=f"{game.review} / 5", font=("Helvetica", 14)).grid(row=idx, column=2, pady=(10, 0))
            tk.Label(self.inner_frame, text=game.genre, font=("Helvetica", 14)).grid(row=idx, column=3, pady=(10, 0))
            tk.Label(self.inner_frame, text=game.esrb_rating, font=("Helvetica", 14)).grid(row=idx, column=4, pady=(10, 0))

            add_to_cart_button = tk.Button(self.inner_frame, text="Add to Cart", bg=BLUE, command=lambda gd=game_data: self.add_to_cart(gd))
            add_to_cart_button.grid(row=idx, column=5, padx=10, pady=(10, 0))

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    #Gets selected filter from dropdown menu
    def on_filter_selection(self, event):
        selected_option = event.widget.get()

        option_mapping = {
            "Alphabetically: A-Z": ("title", "ascending"),
            "Alphabetically: Z-A": ("title", "descending"),
            "Price: High to Low": ("price", "descending"),
            "Price: Low to High": ("price", "ascending"),
            "Review: High to Low": ("review", "descending"),
            "Review: Low to High": ("review", "ascending"),
            "Genre: Alphabetically": ("genre", "ascending")
        }

        if selected_option in option_mapping:
            sort_criteria, order = option_mapping[selected_option]
            if sort_criteria == 'genre':
                sorted_games_data = self.sort_games_by_genre()
            else:
                sorted_games_data = self.sort_games(sort_criteria, order)
            self.display_games(sorted_games_data)

    #Binary search tree sort by genre
    def sort_games_by_genre(self):
        bst = BinarySearchTree()
        for game_data in self.games_data:
            bst.insert(Game(**game_data))

        sorted_genres_games = bst.in_order_traversal()
        sorted_games_data = []
        for genre, games in sorted_genres_games:
            sorted_games_data.extend([game.__dict__ for game in games])
        return sorted_games_data

    #Displays main shop page
    def show_game_info_page(self, queue_window):
        queue_window.destroy()
        game_info_window = tk.Toplevel(self.master)
        game_info_window.title("Welcome to Game Shop")
        width = game_info_window.winfo_screenwidth()
        height = game_info_window.winfo_screenheight()
        game_info_window.geometry(f"{width}x{height}")

        self.frame = tk.Frame(game_info_window)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight = 1)
        self.frame.grid_columnconfigure(2, weight = 1)
        filter_label = tk.Label(self.frame, text="Filter by:", font=("Helvetica", 12))
        filter_label.grid(row=0, column=0, padx=(0, 5), sticky="e")
        filter_options = [
            "Alphabetically: A-Z",
            "Alphabetically: Z-A",
            "Price: High to Low",
            "Price: Low to High",
            "Review: High to Low",
            "Review: Low to High",
            "Genre: Alphabetically"
        ]
        filter_combobox = ttk.Combobox(self.frame, values=filter_options, state="readonly", width=20)
        filter_combobox.current(0)
        filter_combobox.grid(row=0, column=1, padx=(0, 10), sticky="w")
        filter_combobox.bind("<<ComboboxSelected>>", self.on_filter_selection)

        self.canvas = tk.Canvas(self.frame)
        self.canvas.grid(row=0, column=2, rowspan=2, sticky="nsew")

        v_scroll = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        v_scroll.grid(row=0, column=3, rowspan=2, sticky="ns")

        self.canvas.configure(yscrollcommand=v_scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        #Dynamic scroll bar for game list
        def UpdateScroll(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.inner_frame.bind("<Configure>",UpdateScroll)

        headers = ["Title", "Price", "Review Score", "Genre", "ESRB Rating"]
        for idx, header in enumerate(headers):
            header_label = tk.Label(self.inner_frame, text=header, font=("Helvetica", 14))
            header_label.grid(row=0, column=idx, padx=10)

        sorted_games_data = self.sort_games("title", "ascending")
        for idx, game_data in enumerate(sorted_games_data, start=1):
            game = Game(**game_data)

            tk.Label(self.inner_frame, text=game.title, font=("Helvetica", 14), anchor="center").grid(row=idx, column=0, pady=(10, 0), sticky= "nsew")
            tk.Label(self.inner_frame, text=f"${game.price}", font=("Helvetica", 14), anchor="center").grid(row=idx, column=1, pady=(10, 0), sticky= "nsew")
            tk.Label(self.inner_frame, text=f"{game.review} / 5", font=("Helvetica", 14), anchor="center").grid(row=idx, column=2, pady=(10, 0), sticky= "nsew")
            tk.Label(self.inner_frame, text=game.genre, font=("Helvetica", 14), anchor="center").grid(row=idx, column=3, pady=(10, 0), sticky= "nsew")
            tk.Label(self.inner_frame, text=game.esrb_rating, font=("Helvetica", 14), anchor="center").grid(row=idx, column=4, pady=(10, 0), sticky= "nsew")

            add_to_cart_button = tk.Button(self.inner_frame, text="Add to Cart", bg=BLUE, command=lambda gd=game_data: self.add_to_cart(gd))
            add_to_cart_button.grid(row=idx, column=5, padx=10, pady=(10, 0))

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.grid(row=0, column=2, rowspan=2, sticky="nsew")

        tk.Label(self.inner_frame, text="", font=("Helvetica", 14)).grid(row=len(sorted_games_data) + 1, column=0, pady=(10, 20))

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        Bottom_frame = tk.Frame(game_info_window)
        Bottom_frame.pack(side = tk.BOTTOM, anchor= 'w', padx=10, pady=10)

        self.last_added_genre = None

        self.recommended_listbox = tk.Listbox(Bottom_frame, height=10, width=50)
        self.recommended_listbox.insert(0, "Games you may also like:")
        self.recommended_listbox.pack(side=tk.LEFT, padx=5, pady =15)  
        self.update_recommended_games()

        self.cart_listbox = tk.Listbox(Bottom_frame, height=10, width=50)
        self.cart_listbox.pack(side=tk.LEFT, padx=25)  

        self.total_cost_label = tk.Label(Bottom_frame, text="Total Cost: $0.00")
        self.total_cost_label.pack(pady=10)

        self.remove_from_cart_button = tk.Button(Bottom_frame, text="Remove from Cart", bg="red", fg="white", command=self.remove_selected_from_cart)
        self.remove_from_cart_button.pack(pady=10)
    
    #Updates cart when game is added or removed
    def update_cart_display(self):
        cart_list = []
        total_cost = 0
        
        while not self.cart.is_empty():
            item = self.cart.pop()
            cart_list.append(item)
            self.temp_cart.push(item)
            total_cost += item['price']

        self.cart_listbox.delete(0, tk.END)
        for item in reversed(cart_list):
            self.cart_listbox.insert(tk.END, f"{item['title']} - ${item['price']}")

        while not self.temp_cart.is_empty():
            self.cart.push(self.temp_cart.pop())

        self.total_cost_label.config(text=f"Total Cost: ${total_cost:.2f}")

    #Removes items from cart and stack
    def remove_selected_from_cart(self):
        selection = self.cart_listbox.curselection()
        if selection:
            selected_index = selection[0]
            selected_game = self.cart.items[selected_index]

            self.cart.items.pop(selected_index)

            if selected_game['genre'] == self.last_added_genre:
                self.last_added_genre = None

            self.update_cart_display()
            self.update_recommended_games()
        else:
            messagebox.showinfo("Selection Error", "Please select an item to remove.")

    #Game recommedation system
    def update_recommended_games(self):
        """Update the recommended games based on the last added genre"""
        self.recommended_listbox.delete(0, tk.END)
        selected_game = self.cart.peek()
        if self.last_added_genre:
            recommended_games = [game for game in games_data if game['genre'] == self.last_added_genre]

            recommended_games = [game for game in recommended_games if game not in self.cart.items]

            if recommended_games:
                recommended_game = random.choice(recommended_games)
                
                self.recommended_listbox.delete(0, tk.END)
                self.recommended_listbox.insert(tk.END, "Games you may also like:")
                self.recommended_listbox.insert(tk.END, recommended_game['title'])
            else:
                self.recommended_listbox.delete(0, tk.END)
                self.recommended_listbox.insert(tk.END, "No recommended games found")
        else:
            self.recommended_listbox.delete(0, tk.END)
            self.recommended_listbox.insert(tk.END, "Add a game to your cart to see recommendations")
    
    #Calculates cost of items in cart (Stack manipulation)
    def calculate_total_cost(self):
        total_cost = 0
        temp_stack = Stack()

        while not self.cart.is_empty():
            item = self.cart.pop()
            total_cost += item['price']
            temp_stack.push(item)
        
        while not temp_stack.is_empty():
            self.cart.push(temp_stack.pop())
        
        return total_cost

#Main method
if __name__ == "__main__":
    root = tk.Tk()
    app = GameShopGUI(root)
    root.mainloop()