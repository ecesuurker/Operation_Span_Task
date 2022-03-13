from psychopy import visual, gui #We import the necessary libraries for the experiment
from Functions import *
import webbrowser

bgColor = "white" #We set up the background for the experiment
expWin = visual.Window(size=(1366,768),color=bgColor,units="pix")
#expWin = visual.Window(size=(1920,1080), color=bgcolor, units='pix')

expDlg = gui.Dlg(title= "Operation Span Task") #We collect the necessary data from
expDlg.addText("Katılımcı Bilgisi") #participant
expDlg.addField("Katılımcı Numarası: ")
PData = expDlg.show() #If after the information is obtained the "OK" button is not pressed
print(PData)
if not expDlg.OK: #the screen will be closed
    expWin.close()
    
Operation_Span_Task(PData[0], expWin).Run()
  
expWin.close()

webbrowser.open('https://forms.gle/MXoC2H7NuXyM8ni86')