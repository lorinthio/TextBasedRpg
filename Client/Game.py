from Tkinter import *
from Commands import enterChatVar
from Common.WindowHelpers import setupGrid
from Objects import Player
from Client import ClientConnection
import Common.Serialization as Serialization

class GameWindow(Frame):
    
    def __init__(self, player, master=None):
        self.player = player
        Frame.__init__(self, master)
        setupGrid(self.master, 6, 8)
        self.setupVariables()
        self.setupWindow()
        self.setupChatFrame()
        self.setupCharacterFrame()
        self.entryBar()
        self.setupKeyBindings()
        self.connect()

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
        
    def connect(self):
        self.client = ClientConnection()
        self.client.connect()
        self.master.protocol("WM_DELETE_WINDOW", self.disconnect)
        
    def disconnect(self):
        self.client.disconnect()
        self.master.destroy()

def start(player):
    win = GameWindow(player)
    win.mainloop()
    