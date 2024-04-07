import socket
import threading

class ServerInterface:
    def __init__(self, server, port, nickname, message_callback):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiving_thread = None
        self.message_callback = message_callback

    def connect(self, nickname, username, realname):
        # Connect to the server
        self.socket.connect((self.server, self.port))

        # Send the NICK and USER commands
        self.send_message("NICK {}".format(nickname))
        self.send_message("USER {} 0 * :{}".format(username, realname))
        
        # Start the receiving thread
        self.receiving_thread = threading.Thread(target=self.fetch_server_messages)
        self.receiving_thread.start()

    def send_message(self, message):
        # Send a message to the server
        self.socket.send((message + "\r\n").encode('utf-8'))

    def fetch_server_messages(self):
        buffer = ""
        while True:
            raw_data = self.socket.recv(2048)
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
                self.message_callback(line)
    
    def disconnect(self):
        # Disconnect from the server
        self.socket.close()