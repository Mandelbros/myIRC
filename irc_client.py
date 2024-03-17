import socket

class IRCClient:
    def __init__(self, server, port, nickname):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channels = []

    def connect(self):
        self.socket.connect((self.server, self.port))
        self.socket.send(f"NICK {self.nickname}\r\n".encode('utf-8'))
        self.socket.send(f"USER {self.nickname} 0 * :{self.nickname}\r\n".encode('utf-8'))

    def send_command(self, command):
        self.socket.send((command + "\r\n").encode('utf-8'))

    def get_channels_names(self):                   #  del?
        self.socket.send("LIST\r\n".encode('utf-8'))
    
    def join_channel(self, channel_name):
        # Send a JOIN command to the server
        self.send_command(f"JOIN {channel_name}")

    def disconnect(self):
        self.socket.close()