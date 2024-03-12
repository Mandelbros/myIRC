import tkinter as tk
from tkinter import messagebox 

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("IRC Client")
        self.geometry("800x600")
        self.irc_client = None

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Connect", command=self.connect)
        menubar.add_cascade(label="Options", menu=filemenu)
        self.config(menu=menubar)
    def connect(self):
        ConnectDialog(self)

class ConnectDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Connect")
        self.geometry("300x200")

        tk.Label(self, text="Server:").pack()
        self.server_entry = tk.Entry(self)
        self.server_entry.pack()

        tk.Label(self, text="Port:").pack()
        self.port_entry = tk.Entry(self)
        self.port_entry.pack()

        tk.Label(self, text="Nickname:").pack()
        self.nickname_entry = tk.Entry(self)
        self.nickname_entry.pack()

        self.connect_button = tk.Button(self, text="Connect", command=self.connect)
        self.connect_button.pack()

        self.grab_set()  # Hace que esta ventana sea modal

    def connect(self):
        server = self.server_entry.get()
        port = int(self.port_entry.get())
        nickname = self.nickname_entry.get()

        # Aquí puedes crear una instancia de IRCClient y conectarla
        # Necesitarás modificar esta parte para hacer algo útil con la conexión
        print(f"Connecting to {server}:{port} as {nickname}...")

