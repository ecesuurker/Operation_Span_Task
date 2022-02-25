from psychopy import visual, event
from tkinter import *

expWin = visual.Window(size=(1366,768),color="grey",units="pix")

textBox = Entry(text="Placeholder text")
textBox.draw()
expWin.flip()
event.waitKeys(keyList=["space"])
print(data)

expWin.close()


