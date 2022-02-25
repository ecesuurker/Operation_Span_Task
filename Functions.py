from psychopy import visual, event, core, gui
import random, csv, keyboard

txtColor = "black" #We determine the text color

class Operation_Span_Task():
    
    def __init__(self, ParticipantNumber, experimentWindow): #We 
        self.pNum = ParticipantNumber #initialize the variables that we will use
        self.expWind = experimentWindow #throughout
        self.fixation = visual.ShapeStim(experimentWindow, 
            vertices=((0, -15), (0, 15), (0,0), (-15,0), (15, 0)), lineWidth=5, pos=[0,0],
            closeShape=False,
            lineColor="black") #The fixation cross that will be used in the experiment
        self.isi = core.StaticPeriod() #The function that we will use for timing of the
                                        #experiment
        filename = "OSTdata.csv" #Appending the participant file we already have
        file = open(filename, "a", newline="",encoding="utf8")
        field = ["ID", "trial_name", "block_number", "stimuli", "answers"]
        self.OSTdata = csv.DictWriter(file, fieldnames=field)
        math = open("mathQuestions.txt", "r") #Inputting math questions and randomizing
        self.mathQ = math.readlines()
        random.shuffle(self.mathQ)
        mFile = open("Mathdata.csv", "a", newline="") #Appending the data file we have
        mfield = ["ID", "math_q", "expected", "key_press"] #for math questions
        self.mathData = csv.DictWriter(mFile, fieldnames=mfield)
        self.blocknumbers = [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
        
    def Instructions(self, fileName):
        """
        A function that reads instructions from a specified file and displays them on the
        screen.
        """
        inst = open(fileName, "r") 
        lines = ""
        for line in inst:
            line = line.strip()
            lines += line + "\n"
            
        sent = visual.TextStim(win = self.expWind, color=txtColor, text=lines, height=30)
        sent.draw()
        self.expWind.flip()
        event.waitKeys(keyList=["space"]) #The instructions appear on the screen until the
        inst.close() #"enter" key is pressed
        return
        
    def MathQuestions(self, p):
        """
        A function that displays predefined math questions for 3 seconds and obtains an
        answer from the participant regarding truth of the solution to math question. This
        function also writes the math questions and the obtained answers to a file with 
        participant ID to be later used for sanity check.
        """
        math = {}
        math["ID"] = self.pNum
        m = self.mathQ[p].split(",")
        math["math_q"] = m[0]
        math["expected"] = m[1]
        question = visual.TextStim(win = self.expWind, color=txtColor, text=m[0], 
                                   height=30, pos=(0,0))
        self.isi.start(3)
        question.draw()
        self.expWind.flip()
        self.isi.complete()
        true = visual.TextStim(win = self.expWind, color=txtColor, text="True", 
                               pos=(-300, 0), height=30)
        false = visual.TextStim(win = self.expWind, color=txtColor, text="False", 
                               pos=(300, 0), height=30)
        true.draw()
        false.draw()
        self.expWind.flip()
        event.waitKeys(keyList=["a","l"])
        math["key_press"] = keyboard.read_key()
        self.mathData.writerow(math)
        return
        
    def NonLinguistic_OST(self, stimuliFile, directory, p=0):
        """
        A function that displays predetermined images in a random order in 12 blocks that
        have stimuli ranging from 2 to 5. After presenting each image, the function calls
        MathQuestions function to display math questions. After each block, a dialogue 
        box is presented to participants that they have write the name of the images in 
        the order they were presented to them. The function writes the answers given by
        the participant, name of the stimuli, participant ID to a data file.
        """
        stimuli = open(stimuliFile, "r")
        imgNames = []
        for name in stimuli:
            name = name.strip().lower() + ".jpg"
            imgNames.append(name)
        random.shuffle(imgNames)
        random.shuffle(self.blocknumbers)
        a = 0
        for block in self.blocknumbers:
            self.isi.start(.5)
            self.fixation.draw()
            self.expWind.flip()
            self.isi.complete()
            data = {}
            data["ID"] = self.pNum
            data["trial_name"] = "N-OST"
            data["block_number"] = block
            stm = ""
            for i in range(block):
                stm = stm + imgNames[a]
                img = directory + "\\" + imgNames[a]
                i = visual.ImageStim(self.expWind, pos=(0,0), size=[300,300], image=img)
                self.isi.start(1)
                i.draw()
                self.expWind.flip()
                self.isi.complete()
                self.MathQuestions(p)
                p += 1
                a += 1
            data["stimuli"] = stm
            dataInput = gui.Dlg(title="")
            dataInput.addField()
            inp = dataInput.show()
            data["answers"] = inp[0]
            self.OSTdata.writerow(data)
        return p
            
    def Linguistic_OST(self, stimuliFile, trialType, p=0):
        """
        A function that displays predetermined words in a random order in 12 blocks that
        have stimuli ranging from 2 to 5. After presenting each word, the function calls
        MathQuestions function to display math questions. After each block, a dialogue 
        box is presented to participants that they have write the words in the order they
        were presented to them. The function writes the answers given by the participant,
        name of the stimuli, participant ID to a data file.
        """
        stimuli = open(stimuliFile, "r",encoding="utf8")
        words = []
        for word in stimuli:
            word = word.strip()
            words.append(word)
        random.shuffle(words)
        random.shuffle(self.blocknumbers)
        a = 0
        for block in self.blocknumbers:
            self.isi.start(.5)
            self.fixation.draw()
            self.expWind.flip()
            self.isi.complete()
            data = {}
            data["ID"] = self.pNum
            data["trial_name"] = "L-OST:" + trialType
            data["block_number"] = block
            stm = ""
            for i in range(block):
                stm = stm + words[a]
                w = visual.TextStim(win = self.expWind, color=txtColor, text=words[a], 
                               pos=(0, 0), height=30)
                self.isi.start(1)
                w.draw()
                self.expWind.flip()
                self.isi.complete()
                self.MathQuestions(p)
                p += 1
                a += 1
            data["stimuli"] = stm
            dataInput = gui.Dlg(title="")
            dataInput.addField()
            inp = dataInput.show()
            data["answers"] = inp[0]
            self.OSTdata.writerow(data)
        return p
    
    def Run(self):
        """
        A function that runs the experiment. It arranges the running order of the 
        functions.
        """
        self.Instructions("Instructions.txt")
        direc = r"C:\Users\ece-s\OneDrive\Masaüstü\Senior Project\Operation Span Task\N-OST_Images"
        trialTypes = ["N-OST","TurkishDaily", "EnglishDaily", "TurkishAcademic", "EnglishAcademic"]
        random.shuffle(trialTypes)
        mathNum = 0
        for trial in trialTypes:
            if trial == "N-OST":
                mathNum = self.NonLinguistic_OST("N-OST_Stimuli.txt", direc, p=mathNum)
#            else:
#                s = trial + ".txt"
#                mathNum = self.Linguistic_OST(s, trial, mathNum)