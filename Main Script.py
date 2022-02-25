from psychopy import visual, gui #We import the necessary libraries for the experiment
from Functions import *


bgColor = "grey" #We set up the background for the experiment
expWin = visual.Window(size=(1366,768),color=bgColor,units="pix")

expDlg = gui.Dlg(title= "Operation Span Task") #We collect the necessary data from
expDlg.addText("Participant Info") #participant
expDlg.addField("Participant ID: ")
PData = expDlg.show() #If after the information is obtained the "OK" button is not pressed
print(PData)
if not expDlg.OK: #the screen will be closed
    expWin.close()
    
Operation_Span_Task(PData, expWin).Run()
  
expWin.close()