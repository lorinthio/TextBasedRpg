from threading import Thread
import Serialization
import socket

class Server:
    
    def __init__(self, host, port):
        self.clients = []
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
            Thread(target = self.listenToClient, args= (client, address)).start()
            
    def listenToClient(self, client, address):
        print "Got Client Connection"
        size = 1024
        while True:
            try:
                data = Serialization.deserialize(client.recv(size))
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    print "Recieved {}".format(data)
                    client.send(Serialization.serialize(data))
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False
        
    def handleClientConnection(self, client):
        return
        
class ClientConnection:
    
    def __init__(self, ID):
        self.ID = ID
        
        
def main():
    server = Server('', 8123).listen()
    print "Server Closed..."
    print "Hit enter to close this window"
    raw_input()
    
main()