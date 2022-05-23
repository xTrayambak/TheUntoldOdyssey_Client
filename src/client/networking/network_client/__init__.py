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

        self.authenticated = False

        self.last_packet_ms = 0

        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

    def tuo_network_protocol(self):
        """
        The TUO networking/multiplayer protocol.
        (since the server is proprietary, I'm just giving an easy way to replicate it ;D)

        Connect >>
            C -> S: Send authentication token
            S -> C: Send authentication result >>
                If 0:
                    S -> C: Send player list of entities
                    S -> C: Send player inventory data
                    S -> C: Send last position ([0, 0, 0] if player is new)
                    S -> C: Send environment data (weather, wind speed)
                    C -> S (LOOP): Send player position data, inventory manipulation data >>
                        S (SANITIZE): Check if it's actually valid data (player didn't move a billion metres away, or randomly get an item they never had in their inventory) >>
                            If Suspicious:
                                S -> C: Revert changes and request apology packet from client (meaning, client sends data synced with server.)
                                C -> S: Give apology packet and revert changes client side
                            Else:
                                S -> GAME_STORAGE: Keep in temporary data bank till a save event is triggered.
                    S -> C (LOOP): Validate all player data, send keep-alive packets.
                    C -> S (LOOP): Accept all server data, send keep-alive packets.
                If 1:
                    Go to disconnect screen with error, as server kicked us.
        Disconnect [SERVER-INTENDED] >>
            S -> C: Send disconnect packet with 'reason' ID (check src.client.shared.DisconnectStatusCodes)
            S [P3D_NETWORK]: Terminate connection.
        Disconnect [CLIENT-INTENDED] >>
            C -> S: Send a 'disconnect' packet, server immediately terminates connection.
            C&S [P3D_NETWORK]: Terminate connection.
        Disconnect [CLIENT-CRASH] >>
            S [KEEPALIVE]: Notice something is off within 1000 updates, indicating force disconnect.
            S [P3D_NETWORK]: Terminate connection.
        """
        # Send authentication data
        self.send({'auth_token': self.instance.token})

    def connect(self, addr: str, port: int):
        log(f"Connecting to [{addr}:{port}]", "Worker/Network")
        
        self.connectingTo = f"{addr}:{port}"
        self.instance.change_state(5)
        self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(f"Connecting to the server...")
        try:
            log(f"Attempting to connect to ({addr}:{port})", "Worker/Network")
            self.connection = self.cManager.openTCPClientConnection(addr, port, 256)
            if self.connection is None:
                self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(f"Failed to establish connection; the servers are likely down.")
                return
            self.cReader.addConnection(self.connection)
            self.tuo_network_protocol()
            self.instance.change_state(3)
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
        if not self.authenticated: return # we do not want authentication packets mixed up with keep-alive ones.
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
        
        if self.connection is not None:
            self.cManager.closeConnection(self.connection)

    def _poll(self, task):
        #log(f"VALUE={self.instance.getState()} | TYPE={type(self.instance.getState())}")
        #log(f"VALUE={self.instance.getSharedData().GameStates.INGAME} | TYPE={type(self.instance.getSharedData().GameStates.INGAME)}")
        if self.instance.getState() != self.instance.getSharedData().GameStates.INGAME:
            # since we are not a spooky multi-billion dollar corp, we won't connect your pc to our servers when it isn't needed.
            # you're welcome :)
            log("We are no longer on the in-game state, disconnecting.", "Worker/NetworkClient")
            return task.done

        

        self.last_packet_ms += 0.5

        if self.last_packet_ms > 1000: # 1000 ms
            warn("The server has not sent any packet in 2000 ms, indicating a disconnect.", "Worker/DisconnectDetector")
            self.instance.change_state(self.instance.getSharedData().GameStates.CONNECTING)

            self.instance.workspace.getComponent('ui', 'connecting_screen_status').node().setText("Response from server timed out. Please check your internet connection.\nContact your ISP if the problem persists.")
        self.keep_alive_task()

        return task.cont

    def poll(self):
        self.instance.spawnNewTask('poll-network', self._poll)