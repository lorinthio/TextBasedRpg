from threading import Thread
from Client import ClientConnection
from Database import DatabaseService
from PacketHandler import ServerPacketHandler
import Common.Serialization as Serialization
import socket

class Server:
    
    def __init__(self, host, port):
        self.clients = []
        self.dbService = DatabaseService()
        self.packetHandler = ServerPacketHandler(self, self.dbService)
        self.currentID = 0
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        if(host == ""):
            host = "localhost"
        print "Server started on, {} on port {}".format(host, port)
        
    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            Thread(target = self.handleClientConnection, args= (client, address)).start()
        
    def handleClientConnection(self, client, address):
        self.currentID = self.currentID + 1
        print "Got Client Connection, ID: " + str(self.currentID)
        self.clients.append(ClientConnection(self.packetHandler, client, address, self.currentID))
        
if __name__ == "__main__":
    server = Server('', 8123).listen()
    print "Server Closed..."
    print "Hit enter to close this window"
    raw_input()