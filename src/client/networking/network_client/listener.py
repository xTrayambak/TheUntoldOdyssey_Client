from src.client.log import log

from PodSixNet.Connection import ConnectionListener

class GameActionListener(ConnectionListener):
    def __init__(self):
        self.events = {
            "connect_init": [],
            "connect": [],
            "player_chat": [],
            "networkerror": []
        }

    def hook(self, func, event):
        self.events[event].append(func)

    def Network(self, data):
        log(f"Received data from server <{data}>", "Worker/GameActionListener")
        
        for func in self.events["connect_init"]:
            func(data)

    def Network_ClientConnected(self, data):
        log(f"Connected to the server, server has sent data. [{data}]")

        for func in self.events["connect"]:
            func(data)

    def Network_PlayerChat(self, data):
        log(f"<{data['username']}>: {data['message']}", "Worker/Chat")

        for func in self.events["player_chat"]:
            func(data)
    
    def Network_Error(self, data):
        log(f"Server has experienced an error and has sent it to the client. [{data}]")

        for func in self.events["networkerror"]:
            func(data)