import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.channels = {}
        self.users = {}

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor IRC iniciado en {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Nueva conexión de {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        user_name = None
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                try:
                    data_decoded = data.decode('utf-8')
                except UnicodeDecodeError:
                    print("Error de codificación, ignorando datos")
                    continue

                parts = data_decoded.strip().split(' ')
                command = parts[0]

                if command == "NICK":
                    user_name = parts[1]
                    self.users[user_name] = client_socket
                elif command == "JOIN":
                    channel_name = parts[1]
                    if channel_name not in self.channels:
                        self.channels[channel_name] = []
                    self.channels[channel_name].append(user_name)
                elif command == "PRIVMSG":
                    channel_name = parts[1]
                    message = ' '.join(parts[2:])
                    if channel_name in self.channels:
                        for user in self.channels[channel_name]:
                            if user != user_name:
                                self.users[user].sendall(f"{user_name}: {message}\n".encode())
                elif command == "QUIT":
                    if user_name:
                        for channel in self.channels.values():
                            if user_name in channel:
                                channel.remove(user_name)
                        del self.users[user_name]
                        client_socket.close()
                    break
            except Exception as e:
                print(f"Error al procesar el mensaje: {e}")
                break

if __name__ == "__main__":
    server = Server("192.168.57.100", 6667)
    server.start()