import Tkinter
import tkMessageBox

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        #self.entry = Tkinter.Entry(self)
        #self.entry.grid(column=1,row=0,sticky='EW')

        packetList = Tkinter.Listbox(self,width=100,selectmode="single")
        packetList.grid(column=0,row=1)

        #packetList.insert(0,"aaa")
        #packetList.insert(1,"bbb")
        #print "this:"
        #print packetList.get(1)

        startButton = Tkinter.Button(self,text="Start",command=self.startCapture())
        startButton.grid(column=0,row=0)

        stopButton = Tkinter.Button(self,text="Stop",command=self.stopCapture())
        stopButton.grid(colum=1,row=0)


        #does something when you resize the window
        #self.grid_columnconfigure(0,weight=1)

        #determines whether the window is resizeable in x and y coordinates
        self.resizable(True,False)

    def startCapture(self):
    def stopCapture(self):


def GUI():
    app = simpleapp_tk(None)
    app.title('my application')
    app.mainloop()

if __name__ == "__main__":
    GUI()