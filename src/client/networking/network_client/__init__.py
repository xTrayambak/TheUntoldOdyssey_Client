from src.client.log import log

import socket
import threading

BUFFER_SIZE = 2048

RESULT_HEARTBEAT_FAILURE = 0
RESULT_HEARTBEAT_SUCCESS = 1

def createThread(function, args = ()):
    thr = threading.Thread(target = function, args = args)
    return thr

class NetworkClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

        self.connectingTo = "???"
        log("Network client initialized.")

    def connect(self, address, port, instance):
        """
        Connect to a TCP server, and start the network packet exchange "heartbeat".

        NetworkClient.connect -> NetworkClient.start_heartbeat -> NetworkClient._start_heartbeat <THREADED>
                              -> socket.connect [args=address, port]    
        """
        self.connectingTo = address + ":" +str(port)
        instance.change_state(5)
        log("Connecting to <{}:{}>, locating host, this may take a few seconds.".format(address, port), "Worker/NetworkClient")
        self.socket.connect((address, port))
        self.running = True
        return self.start_heartbeat()

    def start_heartbeat(self):
        thread = createThread(self._start_heartbeat)
        log("Starting network server-to-client node TCP connection heartbeat.", "Worker/Thread-{}".format(3))
        thread.start()

    def _start_heartbeat(self):
        while self.running:
            result = self.heartbeat()
            if result == RESULT_HEARTBEAT_FAILURE: 
                break

    def heartbeat(self):
        data = self.socket.recv(BUFFER_SIZE)

        if data is None:
            return RESULT_HEARTBEAT_FAILURE
        
        return RESULT_HEARTBEAT_SUCCESS
        
    def send(self, data):
        self.socket.send(data)