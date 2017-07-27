from Common.Utils import PacketTypes

class ServerPacketHandler:
    
    def __init__(self, Server, Database):
        self.server = Server
        self.database = Database
    
    def handlePacket(self, packet, client):
        msg = packet["message"]
        data = packet["data"]
        
        if(msg == PacketTypes.LOGIN):
            handleLogin(data, client)
            
    def handleLogin(self, data, client):
        self.database
        
        