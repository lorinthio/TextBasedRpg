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
        username = data["username"]
        password = data["password"]
        
        account = self.database.getAccount(username)
        if account:
            if username == account[1] and password == account[2]:
                client.send(PacketTypes.LOGIN_SUCCESS, None)
            else:
                client.send(PacketTypes.LOGIN_FAILURE, None)
        else:
            client.send(PacketTypes.LOGIN_FAILURE, None)
        
        