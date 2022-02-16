#!/usr/bin/env python3
from src.log import log, warn
from src.client.shared import DisconnectStatusCodes
from src.client.settingsreader import getSetting
from src.client.util.conversion import *

from panda3d.core import QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, NetDatagram
from direct.task import Task
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

class NetworkClient:
    def __init__(self, instance):
        self.connectingTo = "???"

        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

        self.instance = instance
        self.connection = None

    def send(self, data: list) -> PyDatagram:
        for value in data:
            dataType = type(value)
            datagram = PyDatagram()

            if dataType == int:
                datagram.addUint8(value)
            else:
                datagram.addString(str(value))
        
        self.cWriter.send(datagram, self.connection)
        return datagram

    def on_packet_receive(self, packet):
        data = PyDatagramIterator(packet)
        
        strings = encodedToDecoded(data.getString())

        if strings['type'] == "disconnect":
            self.disconnect()
            self.instance.workspace.getComponent("ui", "connecting_screen_backbtn").show()
            if strings[1] in DisconnectStatusCodes:
                self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(DisconnectStatusCodes[strings['extra']])
            else:
                self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(strings['extra'])

    def disconnect(self):
        self.instance.workspace.clear()
        self.instance.change_state(5)

    def poll(self, task):
        if self.instance.state != self.instance.states_enum.INGAME and self.instance.state != self.instance.states_enum.SETTINGS:
            #self.instance.change_state(1)
            log(f"Player has quit the game! Disconnecting from server... [state={self.instance.state}]")
            return Task.done

        if self.cReader.dataAvailable():
            datagram = NetDatagram()
            if self.cReader.getData(datagram):
                self.on_packet_receive(datagram)

        self.send(
            [encode(
                "position",
                (0, 0, 0)
            )]
        )

        return Task.cont

    def connect(self, timeout: int = 8000):
        ip_address = getSetting("networking", "proxy")[0]["ip"]
        port = getSetting("networking", "proxy")[0]["port"]

        log(f"Connecting to [{ip_address}:{port}]", "Worker/Connection")

        self.connectingTo = f"{ip_address}:{port}"

        self.instance.change_state(5)
    
        async def taskCon(task):
            await task.pause(1)
            self.connection = self.cManager.openTCPClientConnection(ip_address, port, timeout)

            if self.connection:
                log(f"We connected to the servers! Yaaaayyy! (good ending) [server=({ip_address}:{port})]", "Worker/Networking")
                self.cReader.addConnection(self.connection)
                self.instance.change_state(3)

                log("Sending client version to the server.", "Worker/Networking")
                # send the version/brand of the client we're using.
                self.send(
                    [
                        encode(
                            "client_brand",
                            self.instance.version
                        )
                    ]
                )

                # send the authentication data to the server.
                self.send(
                    [
                        encode(
                            "authentication",
                            "xTrayambak"
                        )
                    ]
                )
                self.instance.spawnNewTask("networkclient-poll", self.poll)
                return task.done
            else:
                self.instance.change_state(5)
                self.instance.workspace.getComponent("ui", "connecting_screen_backbtn").show()
                try:
                    self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(DisconnectStatusCodes['disconnect-unabletoconnect'])
                except:
                    self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText('disconnect-unabletoconnect')
                warn(f"We failed to connect to the server! (bad ending) [server=({ip_address}:{port})]", "Worker/Networking")
                return task.done

        self.instance.spawnNewTask("taskCon", taskCon)