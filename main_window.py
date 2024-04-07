import tkinter as tk
from tkinter import simpledialog
import json
from channel_window import ChannelWindow

class MainWindow:
    def __init__(self, controller):
        self.controller = controller

        # Create a new Tkinter window
        self.window = tk.Tk()
        self.window.title("myIRC")

        # Set the initial size of the window
        self.window.geometry("800x600")

        # Create a menu bar
        self.menu_bar = tk.Menu(self.window)
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.options_menu.add_command(label="Connect", command=self.connect_to_server_dialog)
        self.options_menu.add_command(label="Join Channel", command=self.join_channel_dialog)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.window.config(menu=self.menu_bar)

        # Create a scrollbar
        # Create a text widget for displaying messages
        self.server_messages = tk.Text(self.window)
        self.server_messages.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.scrollbar = tk.Scrollbar(self.server_messages)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.server_messages.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.server_messages.yview)

        # Create an entry widget for typing messages
        self.user_input = tk.Entry(self.window)
        self.user_input.pack(side=tk.BOTTOM, fill=tk.X)
        self.user_input.bind("<Return>", self.send_message)

    def show(self):
        # Start the Tkinter event loop
        self.window.mainloop()

    def connect_to_server_dialog(self):
         # Load the connection info from the config file
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {'server': '', 'port': '', 'nickname': ''}

        # Create a new Toplevel window
        dialog = tk.Toplevel(self.window)
        dialog.title("Connect")
        dialog.geometry("300x200")

        # Create labels and entry fields for server, port, and nickname
        tk.Label(dialog, text="Server:").pack(side=tk.TOP)
        server_entry = tk.Entry(dialog)
        server_entry.pack(side=tk.TOP)

        tk.Label(dialog, text="Port:").pack(side=tk.TOP)
        port_entry = tk.Entry(dialog)
        port_entry.pack(side=tk.TOP)

        tk.Label(dialog, text="Nickname:").pack(side=tk.TOP)
        nickname_entry = tk.Entry(dialog)
        nickname_entry.pack(side=tk.TOP)

        # Set the default values of the entry fields to the loaded connection info
        server_entry.insert(0, config['server'])
        port_entry.insert(0, config['port'])
        nickname_entry.insert(0, config['nickname'])

        # Create a connect button
        connect_button = tk.Button(dialog, text="Connect", command=lambda: [self.save_config(server_entry.get(), port_entry.get(), nickname_entry.get()), self.controller.connect_to_server(server_entry.get(), int(port_entry.get()), nickname_entry.get()), dialog.destroy()])
        connect_button.pack(side=tk.TOP)

        # Make the dialog modal
        dialog.grab_set()

    def join_channel_dialog(self):
        channel_name = simpledialog.askstring("Join Channel", "Enter channel name:")
        if channel_name:
            self.controller.join_channel(channel_name)
            self.controller.channel_windows[channel_name] = ChannelWindow(self.controller, channel_name)

    def save_config(self, server, port, nickname):
        # Save the connection info to a JSON file
        with open('config.json', 'w') as f:
            json.dump({'server': server, 'port': port, 'nickname': nickname}, f)

    def send_message(self, event):
        # Get the message from the entry widget
        message = self.user_input.get()

        # Send the message to the controller
        self.controller.handle_user_input(message)

        # Clear the entry widget
        self.user_input.delete(0, tk.END)

    def display_message(self, message):
        # Display a message in the text widget
        self.server_messages.insert(tk.END, message + "\n")
 