#!/usr/bin/env python3
from src.log import log
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

    def connect(self):
        ip_address = getSetting("networking", "proxy")["ip"]
        port = getSetting("networking", "proxy")["port"]

        log(f"Connecting to [{ip_address}:{port}]", "Worker/Connection")

        self.instance.spawnNewTask(self.poll, "networkclient-poll")
        self.instance.change_state(5)