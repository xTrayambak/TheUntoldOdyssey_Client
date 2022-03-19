from src.client.networking.packet import Packet

class KeepAlivePacket(Packet):
    def __init__(self, data: list = None):
        if data is None:
            data = []

        data.append("keep-alive")
        super().__init__(data)

class DisconnectPacket(Packet):
    def __init__(self, data: list = None):
        if data is None:
            data = []
            
        data.append("disconnect")
        super().__init__(data)

class AuthenticationPacket(Packet):
    def __init__(self, token: str, data: list = None):
        if data is None:
            data = []
            
        data.append(token)
        super().__init__(data)