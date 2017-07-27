from Tkinter import *
from Commands import enterChatVar
from Common.WindowHelpers import setupGrid, centerWindow, makeNotification
from Common.Utils import PacketTypes
import cPickle as pickle
import socket
import Common.Serialization as Serialization

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
        self.email = StringVar()
        self.activeFrame = None
        
    def createLoginWindow(self):
        if self.activeFrame:
            self.activeFrame.destroy()
        width = 250
        height = 70
        
        frame = Frame(self.master)
        setupGrid(self.master, 2, 3)
        frame.grid(row=0, column=0, rowspan=3, columnspan=2)
        self.activeFrame = frame
        setupGrid(frame, 2, 3)
        self.master.title("Login")
        self.master.minsize(width, height)
        self.master.maxsize(width, height)
        
        Label(frame, text="Username : ").grid(row=0, column=0)
        Label(frame, text="Password : ").grid(row=1, column=0)
        Entry(frame, textvariable=self.username).grid(row=0, column=1)
        Entry(frame, textvariable=self.password, show="*").grid(row=1, column=1)
        Button(frame, command=self.attemptLogin, text="Login").grid(row=2, column=0)
        Button(frame, command=self.createAccountCreationWindow, text="Register").grid(row=2, column=1)
        centerWindow(self.master, width, height)
        
    def createAccountCreationWindow(self):
        if self.activeFrame:
            self.activeFrame.destroy()
        width = 250
        height = 90
        
        frame = Frame(self.master)
        setupGrid(self.master, 2, 4)
        frame.grid(row=0, column=0, rowspan=4, columnspan=2)
        self.activeFrame = frame
        
        self.master.title("Register")
        Label(frame, text="Email : ").grid(row=0, column=0)
        Label(frame, text="Username : ").grid(row=1, column=0)
        Label(frame, text="Password : ").grid(row=2, column=0)
        Entry(frame, textvariable=self.email).grid(row=0, column=1)
        Entry(frame, textvariable=self.username).grid(row=1, column=1)
        Entry(frame, textvariable=self.password, show="*").grid(row=2, column=1)
        Button(frame, command=self.attemptCreate, text="Create").grid(row=3, column=0)
        Button(frame, command=self.createLoginWindow, text="Cancel").grid(row=3, column=1) 
        centerWindow(self.master, width, height)       
        
        
    def attemptLogin(self):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.loginServerAddress, 8123))
            try:
                packet = Serialization.pack(PacketTypes.LOGIN, {"username": self.username.get(), "password": self.password.get()})
                conn.send(packet)
                data = conn.recv(1024)
                if data:
                    data = Serialization.deserialize(data)
                    messageType = data["message"]
                    if(messageType == PacketTypes.LOGIN_SUCCESS):
                        self.showLoginSuccess()
                    elif(messageType == PacketTypes.LOGIN_FAILURE):
                        self.showLoginFailure()
            except:
                conn.close()
        except:
            self.failedConnection()        
      
    def showLoginSuccess(self):
        top = makeNotification("Login Success!")
        Message(top, text="You have successfully logged in!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()
        
    def showLoginFailure(self):
        top = makeNotification("Login Failure!")
        Message(top, text="Invalid username/password", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()
                
    def failedConnection(self):
        top = makeNotification("Connection Failed!")
        Message(top, text="There was no response from the server", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()
        
    def attemptCreate(self):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.loginServerAddress, 8123))
            try:
                packet = Serialization.pack(PacketTypes.ACCOUNT_CREATE, {"username": self.username.get(), "password": self.password.get(), "email": self.email.get()})
                conn.send(packet)
                data = conn.recv(1024)
                if data:
                    data = Serialization.deserialize(data)
                    messageType = data["message"]
                    if(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_ACCOUNT_EXISTS):
                        self.showErrorAccountExists()
                    elif(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_EMAIL_EXISTS):
                        self.showErrorEmailExists()
                    elif(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_USERNAME_EXISTS):
                        self.showErrorUsernameExists()
                    elif(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_PASSWORD):
                        self.showErrorInvalidPassword()
                    elif(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_USERNAME):
                        self.showErrorInvalidUsername()
                    elif(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_EMAIL):
                        self.showErrorInvalidEmail()                        
                    elif(messageType == PacketTypes.ACCOUNT_CREATE_SUCCESS):
                        self.showAccountCreateSuccess()
            finally:
                conn.close()
        except:
            self.failedConnection()
            
    def showErrorAccountExists(self):
        top = makeNotification("Error!")
        Message(top, text="Account exists with your username or email!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()
        
    def showErrorEmailExists(self):
        top = makeNotification("Error!")
        Message(top, text="Account exists with that email!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()   
        
    def showErrorUsernameExists(self):
        top = makeNotification("Error!")
        Message(top, text="Account exists with that username!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack() 
        
    def showErrorInvalidPassword(self):
        top = makeNotification("Error!")
        Message(top, text="Your password must contain a number!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack() 
        
    def showErrorInvalidEmail(self):
        top = makeNotification("Error!")
        Message(top, text="Please enter a valid email!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()     
        
    def showErrorInvalidUsername(self):
        top = makeNotification("Error!")
        Message(top, text="Your username must be 7-20 characters long!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack() 
        
    def showAccountCreateSuccess(self):
        top = makeNotification("Account Creation Success!")
        Message(top, text="You account was created successfully!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()  

def start():
    win = LoginWindow()
    win.mainloop()

    #win = GameWindow()
    #win.mainloop()
    