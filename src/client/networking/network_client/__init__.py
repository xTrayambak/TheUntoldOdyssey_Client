#!/usr/bin/env python3
from src.log import log, warn
from src.client.shared import DisconnectStatusCodes
from src.client.settingsreader import getSetting
from src.client.util.conversion import *
from src.client.game import Game
from src.client.game.entity import Entity
from src.client.util.conversion import encode, decode

from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from direct.distributed.PyDatagram import PyDatagram

class NetworkClient:
    def __init__(self, instance):
        self.connectingTo = "???"

        self.instance = instance
        self.connection = None
        self.client_id = 0

        self.last_packet_ms = 0

        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

    def connect(self, addr: str, port: int):
        log(f"Connecting to [{addr}:{port}]", "Worker/Network")
        
        self.connectingTo = f"{addr}:{port}"
        self.instance.change_state(5)
        self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(f"Connecting to {self.connectingTo}")
        try:
            log(f"Attempting to connect to ({addr}:{port})", "Worker/Network")
            async def __inner_conntask(task):
                await task.pause(.5)
                self.connection = self.cManager.openTCPClientConnection(addr, port, 256)
                if self.connection is None:
                    self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(f"Failed to establish connection; the servers are likely down.")
                    return
                self.cReader.addConnection(self.connection)
                self.instance.change_state(3)
                return task.done
            self.instance.spawnNewTask('__inner_conntask', __inner_conntask)
            self.poll()
            log(f"Connected to ({addr}:{port})", "Worker/Network")
        except Exception as exc:
            warn(f"An error occured whilst connecting to the server: {exc}", "Worker/NetworkClient/Exception")
            self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(f"Internal exception: {exc}")
            
    def _send(self, data):
        """
        Send data to the server.
        """
        datagram = PyDatagram(encode(data))
        self.cWriter.send(datagram, self.connection)

    def send(self, data):
        def __inner():
            self._send(data)
        
        res = self.pcall(__inner)
        if res != None:
            self.instance.change_state(5)
            self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(f"Internal Exception whilst Sending Packet:\n{res}")

    def pcall(self, func):
        """
        Run something in a protected call, just if you think it can raise an error.
        """
        try:
            return func()
        except Exception as exc:
            warn(f"Protected call caught an error: {exc}", "Worker/ProtectedRunner")
            return exc

    def on_packet_receive(self, packet):
        """
        Receive data from the server.
        """
        log(packet)

    def keep_alive_task(self):
        """
        Make sure the server doesn't think we disconnected.
        """
        self.send(
            {
                "type": "keep-alive"
            }
        )

    def disconnect(self, reason:str = 'unknown'):
        self.send(
            {
                "type": "disconnect",
                "reason": reason
            }
        )
        self.cManager.closeConnection(self.connection)

    def _poll(self, task):
        self.last_packet_ms += 0.5 + self.instance.clock.getDt()
        self.keep_alive_task()

        return task.cont

    def poll(self):
        self.instance.spawnNewTask('poll-network', self._poll)