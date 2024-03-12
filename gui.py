import tkinter as tk
from tkinter import messagebox 
from config import Config

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("IRC Client")
        self.geometry("800x600")
        self.irc_client = None
        self.app_config = Config()  # Cambia 'self.config' a 'self.app_config'

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Connect", command=self.connect)
        menubar.add_cascade(label="Options", menu=filemenu)
        self.config(menu=menubar)

    def connect(self):
        ConnectDialog(self, self.app_config)  # Cambia 'self.config' a 'self.app_config'

class ConnectDialog(tk.Toplevel):
    def __init__(self, parent, app_config):
        super().__init__(parent)
        self.title("Connect")
        self.geometry("300x200")
        self.app_config = app_config

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

        self.connect_button = tk.Button(self, text="Connect", command=self.connect)
        self.connect_button.pack(side=tk.TOP)
        self.bind('<Return>', lambda event: self.connect()) 
        self.grab_set()  # Hace que esta ventana sea modal

    def connect(self):
        server = self.server_entry.get()
        port = int(self.port_entry.get())
        nickname = self.nickname_entry.get()

        self.app_config.set('Connection', 'server', server)  # Cambia 'self.config.set' a 'self.app_config.set'
        self.app_config.set('Connection', 'port', str(port))  # Cambia 'self.config.set' a 'self.app_config.set'
        self.app_config.set('Connection', 'nickname', nickname)  # Cambia 'self.config.set' a 'self.app_config.set'

        # Aquí puedes crear una instancia de IRCClient y conectarla
        # Necesitarás modificar esta parte para hacer algo útil con la conexión
        print(f"Connecting to {server}:{port} as {nickname}...")
        self.destroy() 
