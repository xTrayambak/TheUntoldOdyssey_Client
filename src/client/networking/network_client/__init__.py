#!/usr/bin/env python3
from src.log import log, warn
from src.client.settingsreader import getSetting

from panda3d.core import QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter
from direct.task import Task

class NetworkClient:
    def __init__(self, instance):
        self.connectingTo = "???"

        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

        self.instance = instance

    def poll(self, task):
        if self.instance.state != self.instance.states_enum.INGAME:
            return Task.done

        
            
        return Task.cont

    def connect(self, timeout: int = 8000):
        ip_address = getSetting("networking", "proxy")[0]["ip"]
        port = getSetting("networking", "proxy")[0]["port"]

        log(f"Connecting to [{ip_address}:{port}]", "Worker/Connection")

        self.connectingTo = f"{ip_address}:{port}"
        self.instance.spawnNewTask("networkclient-poll", self.poll)
        self.instance.change_state(5)

        self.connection = self.cManager.openTCPClientConnection(ip_address, port, timeout)

        if self.connection:
            log(f"We connected to the servers! Yaaaayyy! (good ending) [server=({ip_address}:{port})]")
            self.cReader.addConnection(self.connection)
            self.instance.change_state(3)
        else:
            self.instance.change_state(3)
            warn(f"We failed to connect to the server! (bad ending) [server=({ip_address}:{port})]")