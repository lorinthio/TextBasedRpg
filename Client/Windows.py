from Tkinter import *
from Commands import enterChatVar
from WindowHelpers import setupGrid
from Utils import PacketTypes
import cPickle as pickle
import socket
import Serialization

class GameWindow(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        setupGrid(self.master, 6, 8)
        self.setupVariables()
        self.setupWindow()
        self.setupChatFrame()
        self.setupCharacterFrame()
        self.entryBar()
        self.setupKeyBindings()

    def setupVariables(self):
        self.entryVar = StringVar()
        self.chatText = None


    def setupWindow(self):
        self.master.title("Text Based Adventure")
        self.master.maxsize(1000, 800)
        self.master.minsize(600,400)
        self.master["bg"] = "white"
        
    def setupCharacterFrame(self):
        frame = Frame(self.master)
        frame.grid(row=0, column=0, rowspan=6, columnspan=2, sticky=W+E+S+N)
        
        Label(frame, text="Character", font=("Helvetica", 16), justify=LEFT, anchor=W).pack()
        
    def setupChatFrame(self):
        frame = Frame(self.master, bg="black")
        setupGrid(frame, 4, 6)
        frame.grid(row=0, column=2, rowspan=6, columnspan=4, sticky=W+E+S+N)
        chatText = Text(frame, wrap=WORD)
        chatText.grid(row=0, column=0, rowspan=6, columnspan=4, sticky=W+E+S+N)
        scrollbar = Scrollbar(frame, command=chatText.yview)
        chatText['yscrollcommand'] = scrollbar.set
        self.chatText = chatText
        
    def setupKeyBindings(self):
        self.master.bind('<Return>', 
                    lambda event:
                         enterChatVar(self.chatText, self.entryVar))
        
    def entryBar(self):
        Entry(self.master, textvariable=self.entryVar).grid(row=5, column=2, rowspan=1, columnspan=6, sticky=W+E+S)

class LoginWindow(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.setupVariables()
        self.createLoginWindow()
        self.loginServerAddress = "localhost" # Change this when releasing
        
    def setupVariables(self):
        self.username = StringVar()
        self.password = StringVar()
        
    def createLoginWindow(self):
        width = 250
        height = 70
        
        frame = Frame(self.master)
        setupGrid(self.master, 2, 3)
        frame.grid(row=0, column=0, rowspan=3, columnspan=2)
        setupGrid(frame, 2, 3)
        self.master.title("Login")
        self.master.minsize(width, height)
        self.master.maxsize(width, height)
        
        Label(self.master, text="Username : ").grid(row=0, column=0)
        Label(self.master, text="Password : ").grid(row=1, column=0)
        Entry(self.master, textvariable=self.username).grid(row=0, column=1)
        Entry(self.master, textvariable=self.password, show="*").grid(row=1, column=1)
        Button(self.master, command=self.attemptLogin, text="Login").grid(row=2, column=0)
        
        self.centerWindow(self.master, width, height)
        
    def createAccountCreationWindow(self):
        frame = Frame(self.master)
        setupGrid(self.master, 2, 4)
        
    def attemptLogin(self):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.loginServerAddress, 8123))
            try:
                packet = Serialization.pack("LOGIN", {"username": self.username.get(), "password": self.password.get()})
                conn.send(packet)
                data = conn.recv(1024)
                if data:
                    data = Serialization.deserialize(data)
                    messageType = data["message"]
                    print str(data)
                    if(messageType == PacketTypes.LOGIN_SUCCESS):
                        self.showSuccess()
                    elif(messageType == PacketTypes.LOGIN_FAILURE):
                        self.showFailure()
            except:
                conn.close()
        except:
            self.failedConnection()
                
    def makeNotification(self, title):
        top = Toplevel()
        top.title(title)
        
        w = 300
        h = 60
        
        self.centerWindow(top, w, h)
        
        return top
    
    def centerWindow(self, window, width, height):
        window.minsize(width, height)
        window.maxsize(width, height)
    
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws/2) - (width/2)
        y = (hs/2) - (height/2)        
    
        window.geometry("{}x{}+{}+{}".format(width, height, x, y))        
                
    def showSuccess(self):
        top = self.makeNotification("Login Success!")
        Message(top, text="You have successfully logged in!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()
        
    def showFailure(self):
        top = self.makeNotification("Login Failure!")
        Message(top, text="Invalid username/password", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()
                
    def failedConnection(self):
        top = self.makeNotification("Connection Failed!")
        Message(top, text="There was no response from the server", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()

def start():
    win = LoginWindow()
    win.mainloop()

    #win = GameWindow()
    #win.mainloop()
    