from server_interface import ServerInterface
from main_window import MainWindow
from channel_window import ChannelWindow

class ClientController:
    def __init__(self):
        self.main_window = None
        self.server_interface = None
        self.channel_windows = {}
        self.user_nick = ""
        self.VALID_COMMANDS = {"PASS", "NICK", "USER","OPER", "MODE","SERVICE","QUIT","SQUIT","JOIN","PART","TOPIC","NAMES","LIST","INVITE","KICK","PRIVMSG","NOTICE","MOTD","LUSERS","VERSION","STATS","LINKS","TIME","CONNECT","TRACE","ADMIN","INFO","SERVLIST","SQUERY","WHO","WHOIS","WHOWAS","KILL","PING","PONG","ERROR"}

    def start(self):
        # Create the main window
        self.main_window = MainWindow(self)
        self.main_window.show()

    def connect_to_server(self, server, port, nickname):
        # Create the server interface
        self.server_interface = ServerInterface(server, port, nickname, self.handle_server_message)
        try: 
            self.server_interface.connect(nickname, nickname, nickname)
            self.user_nick = nickname
        except Exception as e:
            self.main_window.display_message("Connection Error: ", str(e))

    def join_channel(self, channel):
        # Create a new channel window
        self.channel_windows[channel] = ChannelWindow(self, channel)
        self.send_message("JOIN "+ channel)
        self.channel_windows[channel].show()

    def handle_user_input(self, input, channel=None):
        if self.server_interface is None:       # send error message back
            return
        
        # Check if the input is a command
        if input.startswith("/"):
            self.handle_user_command(input)
        else:
            self.send_message(input, channel)

    def handle_user_command(self, command):
        # Split the command into the command name and arguments
        parts = command[1:].split(" ")
        command_name = parts[0]
        command_args = parts[1:]

        if command_name not in self.VALID_COMMANDS:
            self.main_window.display_message("Invalid command: " + command)
            return 
        self.send_message(command_name + " " + command_args)

    def send_message(self, message, channel=None):
        # Send a message to the server or a specific channel
        if channel:
            message = ("PRIVMSG {} :{}".format(channel, message))
      
        self.server_interface.send_message(message)

    def handle_server_message(self, line):
        if 'PRIVMSG #' in line:
            # Parse the line to determine its type and content
            sender, channel, message = self.parse_channel_message(line)
            self.channel_windows[channel].display_message(message, sender)
            # self.send_message(message, channel)
        elif 'PING' in line:
            ping_message = line.split(":", 1)[1] 
            self.server_interface.send_message(f"PONG :{ping_message}")
        else:
            message_type, content = self.parse_server_message(line)
            self.main_window.display_message(content)

    def parse_server_message(self, line):
            return 'server', line               #TO DO
    
    def parse_channel_message(self, line):
        # Channel messages contain 'PRIVMSG #'
        if 'PRIVMSG ' in line:
            parts = line.split('PRIVMSG ', 1)
            sender = parts[0].split('!')[0][1:]
            channel_message = parts[1].split(' :', 1)
            channel = channel_message[0]
            message = channel_message[1]
            return sender, channel, message
        else:
            return 'server', line