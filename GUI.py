import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from GameList import Game, games_data
import random

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
    
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop() if not self.is_empty() else None
    
    def peek(self):
        return self.items[-1] if not self.is_empty() else None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)

class GameShopGUI:
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

        self.queue = Queue()
        self.total_customers = 25
        self.your_position = 3

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
        """Show the game information"""
        queue_window.destroy()
        game_info_window = tk.Toplevel(self.master)
        game_info_window.title("Welcome to Game Shop")
        width = game_info_window.winfo_screenwidth()
        height = game_info_window.winfo_screenheight()
        game_info_window.geometry(f"{width}x{height}")

        # Create a frame to contain the game information and filter selection box
        frame = tk.Frame(game_info_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        frame.grid_rowconfigure(0, weight = 1)
        frame.grid_columnconfigure(2, weight = 1)
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

        def UpdateScroll(event):
            """Update the scroll bar after resizing """
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        inner_frame.bind("<Configure>",UpdateScroll)

        # Add column headers
        headers = ["Title", "Price", "Review Score", "Genre", "ESRB Rating"]
        for idx, header in enumerate(headers):
            header_label = tk.Label(inner_frame, text=header, font=("Helvetica", 14))
            header_label.grid(row=0, column=idx, padx=10)

        def add_to_cart(game_data):
            """Add a new game to the cart"""
            self.cart.push(game_data)
            self.last_added_genre = game_data['genre'] 
            self.update_cart_display()
            self.update_recommended_games()

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

            add_to_cart_button = tk.Button(inner_frame, text="Add to Cart", bg=BLUE, command=lambda gd=game_data: add_to_cart(gd))
            add_to_cart_button.grid(row=idx, column=5, padx=10, pady=(10, 0))


        canvas.configure(scrollregion=canvas.bbox("all"))

        # Add the canvas to the window using grid 
        canvas.grid(row=0, column=2, rowspan=2, sticky="nsew")

        # Add padding to the bottom for better spacing
        tk.Label(inner_frame, text="", font=("Helvetica", 14)).grid(row=len(sorted_games_data) + 1, column=0, pady=(10, 20))

        # Bind the inner frame to the canvas
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        Bottom_frame = tk.Frame(game_info_window)
        Bottom_frame.pack(side = tk.BOTTOM, anchor= 'w', padx=10, pady=10)
         
        #Keep track of game last added to cart
        self.last_added_genre = None
        

         # Create the Remove from Cart button
        #self.remove_from_cart_button = tk.Button(Bottom_frame, text="Remove from Cart", bg="red", fg="white", command=self.remove_selected_from_cart)
        #self.remove_from_cart_button.pack(pady=10)
       
        # Games you may like Listbox
        self.recommended_listbox = tk.Listbox(Bottom_frame, height=10, width=50)
        self.recommended_listbox.insert(0, "Games you may also like:")
        self.recommended_listbox.pack(side=tk.LEFT, padx=5, pady =15)  
        self.update_recommended_games()

     
        # Initialize the cart Listbox for displaying and selecting cart items
        self.cart_listbox = tk.Listbox(Bottom_frame, height=10, width=50)
        self.cart_listbox.pack(side=tk.LEFT, padx=25)  

        self.total_cost_label = tk.Label(Bottom_frame, text="Total Cost: $0.00")
        self.total_cost_label.pack(pady=10)  # Adjust padding as needed
        
         # Create the Remove from Cart button
        self.remove_from_cart_button = tk.Button(Bottom_frame, text="Remove from Cart", bg="red", fg="white", command=self.remove_selected_from_cart)
        self.remove_from_cart_button.pack(pady=10)
    
    def update_cart_display(self):
        """Convert stack to list to display cart items"""
        cart_list = []
        total_cost = 0  # Initialize total cost
        
        while not self.cart.is_empty():
            item = self.cart.pop()
            cart_list.append(item)
            self.temp_cart.push(item)
            total_cost += item['price']  # Add item's price to total cost

        # Update Listbox
        self.cart_listbox.delete(0, tk.END)
        for item in reversed(cart_list):  # Reverse to maintain order
            self.cart_listbox.insert(tk.END, f"{item['title']} - ${item['price']}")

        # Transfer items back to the original cart
        while not self.temp_cart.is_empty():
            self.cart.push(self.temp_cart.pop())

        # Update the total cost display
        # Ensure you have initialized this label somewhere in your GUI setup
        # For example: self.total_cost_label = tk.Label(your_window, text="Total Cost: $0.00")
        # And added it to the layout: self.total_cost_label.pack()
        self.total_cost_label.config(text=f"Total Cost: ${total_cost:.2f}")

    def remove_selected_from_cart(self):
        """Remove selected games from cart"""
        selection = self.cart_listbox.curselection()
        if selection:
            selected_index = selection[0]
            selected_game = self.cart.items[selected_index]

            # Remove the selected item
            self.cart.items.pop(selected_index)

            # Update the last added genre if the removed game was the last one added
            if selected_game['genre'] == self.last_added_genre:
                self.last_added_genre = None

            self.update_cart_display()
            self.update_recommended_games()
        else:
            messagebox.showinfo("Selection Error", "Please select an item to remove.")

    def update_recommended_games(self):
        """Update the recommended games based on the last added genre"""
        if self.last_added_genre:
            # Filter games with the same genre as the last added game
            recommended_games = [game for game in games_data if game['genre'] == self.last_added_genre]
            
            # Ensure there are recommended games
            if recommended_games:
                # Randomly select a game from the recommended list
                recommended_game = random.choice(recommended_games)
                
                # Clear and update the recommended games Listbox
                self.recommended_listbox.delete(0, tk.END)
                self.recommended_listbox.insert(tk.END, "Games you may also like:")
                self.recommended_listbox.insert(tk.END, recommended_game['title'])
            else:
                # If no recommended games found, display a message
                self.recommended_listbox.delete(0, tk.END)
                self.recommended_listbox.insert(tk.END, "No recommended games found")
        else:
            # If no game has been added to the cart, display a message
            self.recommended_listbox.delete(0, tk.END)
            self.recommended_listbox.insert(tk.END, "Add a game to your cart to see recommendations")
    
    def calculate_total_cost(self):
        """ Calculate the total cost of items in the cart"""
        total_cost = 0
        temp_stack = Stack()  # Temporary stack to hold items while calculating total cost

        # Pop items from the cart to calculate total cost and store them temporarily
        while not self.cart.is_empty():
            item = self.cart.pop()
            total_cost += item['price']  # Assuming each item is a dictionary with a 'price' key
            temp_stack.push(item)
        
        # Push items back into the cart from the temporary stack
        while not temp_stack.is_empty():
            self.cart.push(temp_stack.pop())
        
        return total_cost

if __name__ == "__main__":
    root = tk.Tk()
    app = GameShopGUI(root)
    root.mainloop()