#!/usr/bin/env python3
from src.log import log
from src.client.settingsreader import getSetting
from src.client.networking.network_client.listener import GameActionListener

import threading
from PodSixNet.Connection import connection

class NetworkClient:
    def __init__(self):
        self.connectingTo = "???"
        self.connection = None
        self.gameActionListener = GameActionListener()
        
    def connect(self, instance, address=getSetting("networking", "proxy")[0]["ip"], port=getSetting("networking", "proxy")[0]["port"]):
        """
        Connect to a TCP server, and start the network packet exchange "heartbeat".

        NetworkClient.connect -> NetworkClient.start_heartbeat -> NetworkClient._start_heartbeat <THREADED>
                              -> socket.connect [args=address, port]    
        """
        self.connectingTo = address + ":" +str(port)
        instance.change_state(5)

        log("Connecting to <{}:{}>, locating host, this may take a few seconds.".format(address, port), "Worker/NetworkClient")
        try:
            self.gameActionListener.Connect((address, port))
            self.gameActionListener.Send({"action": "authenticate", "username": "xTrayambak", "password": "joe"})
        except Exception as e:
            log(str(e), "Error/NetworkClient")
            instance.workspace.getComponent("ui", "connecting_screen_status").setText("An error occured whilst connecting to the servers.\n\n"+str(e))

    def send(self, data):
        self.gameActionListener.Send(data)

    def run(self, instance):
        instance.taskMgr.add("network_pump", self.connection.Pump)