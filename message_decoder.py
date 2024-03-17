# message_decoder.py

class MessageDecoder:
    def __init__(self, irc_client):
        self.irc_client = irc_client

    def process_message(self, message):
        if "PING" in message:
            ping_message = message.split(":", 1)[1]
            self.irc_client.socket.send(f"PONG :{ping_message}\r\n".encode('utf-8'))
        elif "322 {self.irc_client.nickname}" in message:
            parts = message.split()
            channel_index = parts.index("322 {myusername}") + 2
            channel_name = parts[channel_index]
            num_people = parts[channel_index + 1]
            print(f"Channel: {channel_name}, People: {num_people}")

            # Add your message processing logic here
        return message
    