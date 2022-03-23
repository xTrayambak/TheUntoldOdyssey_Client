#!/usr/bin/env python3
from src.log import log, warn
from src.client.shared import DisconnectStatusCodes
from src.client.settingsreader import getSetting
from src.client.util.conversion import *
from src.client.game import Game
from src.client.game.entity import Entity

import pydatanet

import ast
import time
import threading

from multiprocessing.pool import ThreadPool

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
        self.instance.change_state(5)
        self.server = pydatanet.Client()
        try:
            self.server.connect(addr, port, autoPoll=False)
            def heartbeat(task): 
                self.server._heartbeat() 
                return task.cont
                
            self.instance.spawnNewTask('heartbeat-internal-pydatanet', heartbeat)
            self.instance.change_state(3)
        except Exception as exc:
            self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(f"Internal exception: {exc}")
        
        self.server.hook_tcp_recv(self.on_packet_receive)


    def send(self, data):
        """
        Send data to the server.
        """
        self.server.send(data)

    def on_packet_receive(self, packet):
        """
        Receive data from the server.
        """
        print(packet)

    def keep_alive_task(self):
        """
        Make sure the server doesn't think we disconnected.
        """
        self.send("keep-alive")

    def _poll(self):
        self.keep_alive_task()

    def poll(self):
        self.instance.spawnNewTask('poll-network', self._poll)