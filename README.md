## myIRC

myIRC is a simple IRC client built with Python and Tkinter. It allows you to connect to an IRC server, join channels, and send and receive messages.

```
myIRC/
│
├── client_controller.py
├── main_window.py
├── channel_window.py
├── server_interface.py
└── main.py
```

- client_controller.py: This file contains the `ClientController` class, which is the main controller for the application. It manages the creation and interaction of the other classes, handles communication between them, and controls the overall flow of the application.

- main_window.py: This file contains the `MainWindow` class, which represents the primary user interface of the application. It displays server messages and user interactions.

- channel_window.py: This file contains the `ChannelWindow` class, which represents the user interface for a channel. It allows the user to send and receive messages in the channel.

- server_interface.py: This file contains the `ServerInterface` class, which handles the connection to the IRC server. It sends and receives messages to and from the server.

- main.py: This is the entry point of the application. It creates an instance of the `ClientController` and starts the application.

## How to Run

To run the application, simply execute the main.py script:

```
python main.py
```

## Features
- Connect to an IRC server
- Join multiple channels
- Send and receive messages
- Handle user commands

## Future Improvements
- Add support for private messages
- Add error handling for server disconnections
- Improve the user interface