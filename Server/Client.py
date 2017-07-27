import Common.Serialization as Serialization
from Common.Utils import PacketTypes

class ClientConnection:
    
    def __init__(self, packetHandler, client, address, ID):
        self.packetHandler = packetHandler
        self.dataSize = 1024
        self.client = client
        self.address = address
        self.ID = ID
        self.loop()
        
    def loop(self):
        while True:
            try:
                data = Serialization.deserialize(self.client.recv(self.dataSize))
                self.packetHandler.handlePacket(data, self)
            except:
                self.client.close()
                return False
            
    def send(self, message, data):
        packet = Serialization.pack(message, data)
        self.client.send(packet)        