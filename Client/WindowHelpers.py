def setupGrid(frame, width, height):
    frame.grid()  
    for x in range(width):
        frame.columnconfigure(x, weight=1) 
    for y in range(height):
        frame.rowconfigure(y, weight=1)  