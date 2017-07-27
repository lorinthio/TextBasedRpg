import Common.Serialization as Serialization
from Common.Utils import PacketTypes, getConfig

class ClientConnection:
    
    def __init__(self, packetHandler, client, address, ID):
        self.packetHandler = packetHandler
        self.dataSize = getConfig().PacketSize
        self.client = client
        self.address = address
        self.ID = ID
        self.loop()
        
    def loop(self):
        while self.client:
            try:
                data = Serialization.deserialize(self.client.recv(self.dataSize))
                self.packetHandler.handlePacket(data, self)
            except:
                self.client.close()
                print "Client Disconnected"
                self.client = None
            
    def send(self, message, data):
        packet = Serialization.pack(message, data)
        self.client.send(packet)        