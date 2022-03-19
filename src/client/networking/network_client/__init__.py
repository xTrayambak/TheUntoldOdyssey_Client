#!/usr/bin/env python3
from src.log import log, warn
from src.client.shared import DisconnectStatusCodes
from src.client.settingsreader import getSetting
from src.client.util.conversion import *
from src.client.game import Game
from src.client.game.entity import Entity
from src.client.networking.encoding import encode_object, decode_object
from src.client.networking.packets import *

import enet

import ast
import time
import threading

class NetworkClient:
    def __init__(self, instance):
        self.connectingTo = "???"

        self.instance = instance
        self.connection = None
        self.client_id = 0

        self.last_packet_ms = 0

    def connect(self, addr: str, port: int):
        log(f"Connecting to [{addr}:{port}]", "Worker/Network")
        
        self.connectingTo = f"{addr}:{port}"
        self.server = enet.Host(None, 1, 0, 0, 0)
        self.connection = self.server.connect(enet.Address(bytes(addr.encode('utf-8')), port), 1)
        
        log("Connection established! Now spawning tasks...", "Worker/Network")
        threading.Thread(target=self.poll, args=())

    def send(self, data):
        """
        Send data to the server.
        """
        pass

    def on_packet_receive(self, packet):
        """
        Receive data from the server.
        """
        pass

    def keep_alive_task(self):
        """
        Make sure the server doesn't think we disconnected.
        """
        self.send(
            KeepAlivePacket()
        )

    def _poll(self):
        event = self.server.service(1000)

        if event.type == enet.EVENT_TYPE_CONNECT:
            log("The server is now allowing us to send/receive packets properly.", "Worker/Network")
        elif event.type == enet.EVENT_TYPE_DISCONNECT:
            log("The server has disconnected us!", "Worker/Network")
            return -1
        elif event.type == enet.EVENT_TYPE_RECEIVE:
            log("Packet received!", "Worker/Network")
            self.on_packet_receive(event.packet.data)
        
        return 1

    def poll(self):
        while True:
            r = self._poll()
            if r == -1: break