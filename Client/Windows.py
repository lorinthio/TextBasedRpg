from Tkinter import *
from Commands import enterChatVar
from WindowHelpers import setupGrid

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
        self.createWindow()
        
        
    def setupVariables(self):
        self.username = StringVar()
        self.password = StringVar()
        
    def createWindow(self):
        self.master.grid()
        setupGrid(self.master, 2, 3)
        self.master.title("Login")
        self.master.minsize(250, 70)
        self.master.maxsize(250, 70)
        
        Label(self.master, text="Username : ").grid(row=0, column=0)
        Label(self.master, text="Password : ").grid(row=1, column=0)
        Entry(self.master, textvariable=self.username).grid(row=0, column=1)
        Entry(self.master, textvariable=self.password, show="*").grid(row=1, column=1)
        Button(self.master, text="Login").grid(row=2, column=0)

def setupWindow():
    win = LoginWindow()
    win.mainloop()
    
    return
    win = GameWindow()
    win.mainloop()
    