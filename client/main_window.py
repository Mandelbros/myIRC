import tkinter as tk
from tkinter import simpledialog
import json 
from datetime import datetime
import os

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
        self.options_menu.add_command(label="Send Notice", command=self.send_notice_dialog)
        self.options_menu.add_command(label="Send Message", command=self.send_message_dialog)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.window.config(menu=self.menu_bar)

        # Create a scrollbar
        # Create a text widget for displaying messages
        self.server_messages = tk.Text(self.window)
        self.server_messages.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.server_messages.tag_configure('red', foreground='red')
        self.server_messages.tag_configure('timestamp', foreground='blue')


        self.scrollbar = tk.Scrollbar(self.server_messages)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.server_messages.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.server_messages.yview)

        # Create an entry widget for typing messages
        self.user_input = tk.Entry(self.window)
        self.user_input.pack(side=tk.BOTTOM, fill=tk.X)
        self.user_input.bind("<Return>", self.send_message)
        
        # Bind the window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def show(self):
        # Start the Tkinter event loop
        self.window.mainloop()

    def connect_to_server_dialog(self): 
        # Load the connection info from the config file
        try:
            with open('./client/config.json', 'r') as f:
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

        # Create a Checkbox for SSL connection
        use_ssl = tk.BooleanVar()
        ssl_checkbox = tk.Checkbutton(dialog, text="Use SSL", variable=use_ssl)
        ssl_checkbox.pack(side=tk.TOP)

        # Create a connect button
        connect_button = tk.Button(dialog, text="Connect", command=lambda: [
            self.save_config(server_entry.get(), port_entry.get(), nickname_entry.get()), 
            self.controller.connect_to_server(server_entry.get(), int(port_entry.get()), nickname_entry.get(), use_ssl.get()), 
            dialog.destroy()
        ])
        connect_button.pack(side=tk.TOP)

        # Make the dialog modal
        dialog.grab_set()

    def join_channel_dialog(self):
        channel_name = simpledialog.askstring("Join Channel", "Enter channel name:")
        if channel_name:
            self.controller.join_channel(channel_name)
            # self.controller.chat_windows[channel_name] = ChatWindow(self.controller, channel_name)

    def send_notice_dialog(self):
        # Create a new Toplevel window
        dialog = tk.Toplevel(self.window)
        dialog.title("Notice")
        dialog.geometry("300x150")

        # Create labels and entry fields for target and message
        tk.Label(dialog, text="Target:").pack(side=tk.TOP)
        target_entry = tk.Entry(dialog, width=40)
        target_entry.pack(side=tk.TOP)

        tk.Label(dialog, text="Message:").pack(side=tk.TOP)
        message_entry = tk.Entry(dialog, width=40)
        message_entry.pack(side=tk.TOP)

        # Set the default values of the entry fields to the loaded notice info
        target_entry.insert(0, '')
        message_entry.insert(0, '')

        # Create a send button
        send_button = tk.Button(dialog, text="Send", command=lambda: [self.controller.send_notice(message_entry.get(), target_entry.get()), dialog.destroy()])
        send_button.pack(side=tk.TOP)

        # Make the dialog modal
        dialog.grab_set()

    def send_message_dialog(self):
        # Create a new Toplevel window
        dialog = tk.Toplevel(self.window)
        dialog.title("Message")
        dialog.geometry("350x150")

        # Create labels and entry fields for target and message
        tk.Label(dialog, text="Target:").pack(side=tk.TOP)
        target_entry = tk.Entry(dialog, width=40)
        target_entry.pack(side=tk.TOP)

        tk.Label(dialog, text="Message:").pack(side=tk.TOP)
        message_entry = tk.Entry(dialog, width=40)
        message_entry.pack(side=tk.TOP)

        # Set the default values of the entry fields to the loaded notice info
        target_entry.insert(0, '')
        message_entry.insert(0, '')

        # Create a send button
        send_button = tk.Button(dialog, text="Send", command=lambda: [self.controller.send_message(message_entry.get(), target_entry.get()), dialog.destroy()])
        send_button.pack(side=tk.TOP)

        # Make the dialog modal
        dialog.grab_set()

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
        current_time = datetime.now().strftime('%H:%M:%S')
        # Prepend the timestamp to the message
        current_time = "[{}]* ".format(current_time)
        self.server_messages.insert(tk.END, current_time, 'timestamp')

        if message.startswith("NOTICE from"):
            user = message.split(":", 1)[0] + ":"
            msg = message.split(":", 1)[1]
            self.server_messages.insert(tk.END, user, 'red')
            self.server_messages.insert(tk.END, msg + "\n")
        else:
            self.server_messages.insert(tk.END, message + "\n")
        self.server_messages.see(tk.END)

    def on_close(self):
        # Stop the application
        self.controller.stop()  # replace with your method to stop the application

        # Destroy the window
        self.window.destroy()