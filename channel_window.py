import tkinter as tk

class ChannelWindow:
    def __init__(self, controller, name):
        self.controller = controller
        self.name = name

        # Create a new Tkinter window
        self.window = tk.Toplevel()
        self.window.title(name)

        # Create a text widget for displaying messages
        self.text_widget = tk.Text(self.window)
        self.text_widget.pack()

        # Create an entry widget for typing messages
        self.entry_widget = tk.Entry(self.window)
        self.entry_widget.pack()

        # Bind the Return key to the send_message method
        self.entry_widget.bind("<Return>", self.send_message)

    def show(self):
        # Start the Tkinter event loop
        self.window.mainloop()

    def send_message(self, event):
        # Get the message from the entry widget and send it to the controller
        message = self.entry_widget.get()
        self.controller.send_message(message, self.name)
        self.display_message(message, self.controller.user_nick)

        # Clear the entry widget
        self.entry_widget.delete(0, tk.END)

    def display_message(self, message, sender=None):
        # Display a message in the text widget
        self.text_widget.insert(tk.END, "<" + sender+ "> "+ message + "\n")