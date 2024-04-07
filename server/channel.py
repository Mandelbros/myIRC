import socket

class Channel:
    def __init__(self,admin) :
        self.users = [admin]
        self.channel_admin = [admin]