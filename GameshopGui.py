import customtkinter as ctk

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

class GameShopGUI:
    def __init__(self, master):
        self.master = master
        master.title("GameShop")
        master.geometry("400x200")  # Set window size

        self.queue = Queue()
        self.total_customers = 25
        self.your_position = 10

        # Create banner label
        self.banner_label = ctk.CTkLabel(master, text="GameShop", bg_color=BLUE, fg_color=BLUE, text_color="white", font=("Helvetica", 24))
        self.banner_label.pack(fill=ctk.X)

        # Create access button
        self.access_button = ctk.CTkButton(master, text="Access Website", fg_color=BLUE, text_color="white", font=("Helvetica", 12), command=self.access_website)
        self.access_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def access_website(self):
        # Hide the main window
        self.master.withdraw()

        # Create a new window for the queue updates
        queue_window = ctk.CTk()
        queue_window.title("GameShop")
        queue_window.geometry("400x200")

        # Function to update the queue label
        def update_queue_label():
            if self.your_position > 2:
                self.your_position -= 1
                self.total_customers += 1
                queue_label.configure(text=f"You are {self.your_position}/{self.total_customers}. There are {self.your_position - 1} people in front of you.")
                queue_window.after(3000, update_queue_label)
            elif self.your_position == 2:
                queue_label.configure(text=f"You are {self.your_position}/{self.total_customers}. There are {self.your_position - 1} people in front of you.")
                queue_window.after(3000, show_you_are_in)
            else:
                queue_label.configure(text="You are in!")
                queue_window.after(3000, close_window)

        # Create label to display queue status
        queue_label = ctk.CTkLabel(queue_window, text=f"You are {self.your_position}/{self.total_customers}. There are {self.your_position - 1} people in front of you.", font=("Helvetica", 12))
        queue_label.pack(pady=10)

        # Start updating the queue label
        update_queue_label()

        # Function to show "You're in!" page
        def show_you_are_in():
            queue_window.destroy()
            in_window = ctk.CTk()
            in_window.title("You're In")
            in_window.geometry("200x100")
            in_label = ctk.CTkLabel(in_window, text="You're in!", font=("Helvetica", 18))
            in_label.pack(expand=True)
            in_window.mainloop()

        # Function to close the queue window and show the main window again
        def close_window():
            queue_window.destroy()
            self.master.deiconify()

if __name__ == "__main__":
    app = ctk.CTk()
    GameShopGUI(app)
    app.mainloop()
