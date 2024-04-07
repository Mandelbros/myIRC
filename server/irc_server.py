import socket
import threading
from channel import Channel
class Server:

    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users={}
        self.channels={}

    def send_all (self, message, origin=None):
        for user, connection in self.users.items():
            if user != origin:
                connection.sendall(message.encode('utf-8'))

    def start_server(self):
    
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f'Servidor IRC iniciado en {self.host}:{self.port}')

        while True:
            connection, address = self.server.accept()
            print(f'Nuevo cliente conectado desde {address}')
            cliente_thread = threading.Thread(target= self.handle_client, args=(connection, address))
            cliente_thread.start()
    
    def handle_client(self,connection):
        user_name=None
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                try:
                    data_decoded = data.decode('utf-8')
                except UnicodeDecodeError:
                    print("Error de codificación, ignorando datos")
                    continue
                
                print(f'Mensaje recibido: {data_decoded}')

                # Analizar mensaje IRC
                parts = data_decoded.strip().split(' ')
                command = parts[0]

                if command == "NICK" :
                    user_name = parts[1]
                    self.users[user_name] = connection
                elif command == "QUIT":
                    if user_name:
                        del self.users[user_name]
                        connection.close()
                    break
                elif command == "PRIVMSG":
                    destinatario = parts[1]
                    mensaje = ' '.join(parts[2:])
                    usuario_origen = user_name
                    mensaje_enviar = f':{usuario_origen}!{usuario_origen}@{self.host} PRIVMSG {destinatario} :{mensaje}'
                    self.send_all(mensaje_enviar, user_name)
                else:
                    mensaje_error = f':{self.host} 421 {user_name} :Unknown command\n'
                    connection.sendall(mensaje_error.encode('utf-8'))

            except Exception as e:
                print(f"Error al procesar el mensaje: {e}")
                break