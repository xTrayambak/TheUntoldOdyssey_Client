#!/usr/bin/env python3
from src.log import log, warn
from src.client.shared import DisconnectStatusCodes
from src.client.settingsreader import getSetting
from src.client.util.conversion import *
from src.client.game import Game
from src.client.game.entity import Entity

from panda3d.core import QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, NetDatagram
from direct.task import Task
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

import ast
import time

class NetworkClient:
    def __init__(self, instance):
        self.connectingTo = "???"

        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

        self.instance = instance
        self.connection = None
        self.client_id = 0

        self.last_packet_ms = 0

    def send(self, data: list) -> PyDatagram:
        for value in data:
            dataType = type(value)
            datagram = PyDatagram()

            if dataType == int:
                datagram.addUint8(value)
            else:
                datagram.addString(str(value))

        datagram.addString(str(self.client_id))
        self.cWriter.send(datagram, self.connection)
        return datagram

    def on_packet_receive(self, packet):
        self.last_packet_ms = 0
        data = PyDatagramIterator(packet)
        
        strings = encodedToDecoded(data.getString())

        if strings['type'] == "disconnect":
            log("We have been disconnected from the server! (reason={})".format(strings["extra"]))
            self.disconnect()
            self.instance.workspace.getComponent("ui", "connecting_screen_backbtn").show()
            if strings['extra'] in DisconnectStatusCodes:
                self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(DisconnectStatusCodes[strings['extra']])
            else:
                self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(strings['extra'])
        elif strings['type'] == "new_entity":
            attributes = strings['extra'].split("#")
            name = attributes[0]
            position = ast.literal_eval(attributes[1])

            self.instance.game.add_new_entity(
                Entity(
                    name,
                    position
                )
            )
            
            log("A new entity has spawned!")
        elif strings['type'] == "client_secret_id":
            log("The server has assigned us an ID!")
            self.client_id = int(strings['extra'])
        elif strings['type'] == 'entity_list':
            log("Entity data has been received from the server!", sender = "Worker/ClientToServer")
            for entity in strings['extra'].split("++"):
                data = entity.split("#")
                name = data[0]
                pos = ast.literal_eval(data[1]) 

                log(f"New entity spawning! [{name}#{pos}]")

                self.instance.game.entityManager.add_entity(
                    Entity(
                        name, pos
                    )
                )

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
                str(self.instance.player.entity.getPos())+"|"+str(self.client_id)
            )]
        )

        self.last_packet_ms += 0.1

        if int(self.last_packet_ms) > 500:
            warn("We have not received a single packet in 500 ms! Is the server unresponsive? Disconnecting!", "Worker/NetworkSanity")

            self.disconnect()
            if 'disconnect-timeout' in DisconnectStatusCodes:
                self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText(DisconnectStatusCodes['disconnect-timeout'])
            else:
                self.instance.workspace.getComponent("ui", "connecting_screen_status").node().setText("disconnect-timeout")
            return task.done

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

                self.instance.game = Game()

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

                log("Asking server for entity data...")
                self.send(
                    [encode(
                        "entities_get",
                        []
                    )]
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