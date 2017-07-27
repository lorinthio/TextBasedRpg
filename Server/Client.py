import Serialization
from Utils import PacketTypes

class ClientConnection:
    
    def __init__(self, client, address, ID):
        self.dataSize = 1024
        self.client = client
        self.address = address
        self.ID = ID
        self.loop()
        
    def loop(self):
        while True:
            try:
                data = Serialization.deserialize(self.client.recv(self.dataSize))
                msg = data["message"]
                dat = data["data"]
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    print "Message : " + str(msg)
                    print "Recieved {}".format(dat)
                    self.send(PacketTypes.LOGIN_FAILURE, {})
                else:
                    raise error('Client disconnected')
            except:
                self.client.close()
                return False
            
    def send(self, message, data):
        packet = Serialization.pack(message, data)
        self.client.send(packet)        