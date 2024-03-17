import tkinter as tk
from tkinter import messagebox, Listbox, PanedWindow, Text
from config import Config
from irc_client import IRCClient
from message_decoder import MessageDecoder
import threading
import tkinter.simpledialog as simpledialog
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("IRC Client")
        self.geometry("800x600")
        self.irc_client = None
        self.app_config = Config()
        self.channel_windows = {}

        self.menu_bar = tk.Menu(self)
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.options_menu.add_command(label="Connect", command=self.connect_button)
        self.options_menu.add_command(label="Join Channel", command=self.join_channel_dialog)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.config(menu=self.menu_bar)

        self.paned_window = PanedWindow(self)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        self.channels_list = Listbox(self.paned_window)
        self.paned_window.add(self.channels_list)

        self.server_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.server_frame)

        self.server_messages = Text(self.server_frame)
        self.server_messages.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add a scrollbar to the server_messages Text widget
        self.scrollbar = tk.Scrollbar(self.server_messages)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.server_messages.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.server_messages.yview)

        # Add an Entry widget for user input
        self.user_input = tk.Entry(self.server_frame)
        self.user_input.pack(side=tk.BOTTOM, fill=tk.X)
        self.user_input.bind('<Return>', self.send_user_message)

    def connect_button(self):
        ConnectDialog(self, self.app_config,self)
    
    def join_channel_dialog(self):
        channel_name = simpledialog.askstring("Join Channel", "Enter channel name:")
        if channel_name:
            self.irc_client.join_channel(channel_name)
            self.channel_windows[channel_name] = ChannelWindow(self.irc_client, channel_name)
    
    def connect_to_server(self, server, port, nickname):
        self.server_messages.insert(tk.END, f"* Connecting to {server} ({port})\n")
        self.server_messages.see(tk.END)

        self.irc_client = IRCClient(server, port, nickname)
        self.message_decoder = MessageDecoder(self.irc_client)

        self.irc_client.connect()

        self.message_loop_thread = threading.Thread(target=self.fetch_server_messages, daemon=True)
        self.message_loop_thread.start()
        self.server_messages_thread = threading.Thread(target=self.update_server_messages, daemon=True)
        self.server_messages_thread.start()

        # self.irc_client.send_command("LIST")  

    def fetch_server_messages(self):
        buffer = ""
        while True:
            raw_data = self.irc_client.socket.recv(2048)
            start = 0
            while start < len(raw_data):
                try:
                    # Try to decode a chunk of data
                    chunk = raw_data[start:start+1024].decode('utf-8')
                    buffer += chunk
                    start += 1024
                except UnicodeDecodeError:
                    # If a UnicodeDecodeError occurs, skip to the next chunk
                    start += 1024

            while "\r\n" in buffer:
                line, buffer = buffer.split("\r\n", 1)
                processed_line = self.message_decoder.process_message(line)
                yield processed_line

    def update_server_messages(self):
        for message in self.fetch_server_messages():
            if message is None:
                continue
            if message.startswith(":") and "PRIVMSG" in message:            # spliting bug?
                parts = message.split()
                channel_name = parts[2]
                if channel_name in self.channel_windows:
                    self.channel_windows[channel_name].add_message(message)
            else:
                self.server_messages.insert(tk.END, message + "\n")
                self.server_messages.see(tk.END)

    def send_user_message(self, event):
        message = self.user_input.get()
        self.server_messages.tag_config("red", foreground="red")
        self.server_messages.insert(tk.END, "me: ", "red")
        self.server_messages.insert(tk.END, message + "\n")
        self.server_messages.see(tk.END)
        # self.irc_client.send_command(message)         # caught user msg and process it
        self.user_input.delete(0, tk.END)

class ConnectDialog(tk.Toplevel):
    def __init__(self, parent, app_config, main_window):
        super().__init__(parent)
        self.title("Connect")
        self.geometry("300x200")
        self.app_config = app_config
        self.main_window = main_window

        tk.Label(self, text="Server:").pack(side=tk.TOP)
        self.server_entry = tk.Entry(self)
        self.server_entry.insert(0, app_config.get('Connection', 'server', ''))
        self.server_entry.pack(side=tk.TOP)

        tk.Label(self, text="Port:").pack(side=tk.TOP)
        self.port_entry = tk.Entry(self)
        self.port_entry.insert(0, app_config.get('Connection', 'port', ''))
        self.port_entry.pack(side=tk.TOP)

        tk.Label(self, text="Nickname:").pack(side=tk.TOP)
        self.nickname_entry = tk.Entry(self)
        self.nickname_entry.insert(0, app_config.get('Connection', 'nickname', ''))
        self.nickname_entry.pack(side=tk.TOP)

        self.connect_button = tk.Button(self, text="Connect", command=self.gather_data)
        self.connect_button.pack(side=tk.TOP)
        self.bind('<Return>', lambda event: self.connect()) 
        self.grab_set()  # Hace que esta ventana sea modal

    def gather_data(self):
        server = self.server_entry.get()
        port = int(self.port_entry.get())
        nickname = self.nickname_entry.get()

        self.app_config.set('Connection', 'server', server)
        self.app_config.set('Connection', 'port', str(port))
        self.app_config.set('Connection', 'nickname', nickname)

        self.main_window.connect_to_server(server, port, nickname)
        self.destroy()

class ChannelWindow(tk.Toplevel):
    def __init__(self, irc_client, channel_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.irc_client = irc_client
        self.channel_name = channel_name

        self.title(channel_name)

        self.server_messages = tk.Text(self)
        self.server_messages.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.scrollbar = tk.Scrollbar(self.server_messages)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.server_messages.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.server_messages.yview)

        self.user_input = tk.Entry(self)
        self.user_input.pack(side=tk.BOTTOM, fill=tk.X)
        self.user_input.bind('<Return>', self.send_user_message)

    def send_user_message(self, event):
        message = self.user_input.get()
        self.server_messages.tag_config("red", foreground="red")
        self.server_messages.insert(tk.END, "me: ", "red")
        self.server_messages.insert(tk.END, message + "\n")
        self.server_messages.see(tk.END)
        self.irc_client.send_command(f"PRIVMSG {self.channel_name} :{message}")
        self.user_input.delete(0, tk.END)

    def add_message(self, message):
        self.server_messages.insert(tk.END, message + "\n")
        self.server_messages.see(tk.END)