from psychopy import visual, event, core, gui
import random, csv, keyboard
import os

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
        part_fileName = "data/OSTdata_" + str(ParticipantNumber) +".csv" #The responses of each
        part_file = open(part_fileName, "w", newline="") #participant will be also
        self.partData = csv.DictWriter(part_file, fieldnames=field) #recorded to a separate
        self.partData.writeheader()                                #file
        
    def Instructions(self, fileName):
        """
        A function that reads instructions from a specified file and displays them on the
        screen.
        """
        inst = open(fileName, "r", encoding="utf8") 
        lines = ""
        for line in inst:
            line = line.strip()
            lines += line + "\n"
            
        sent = visual.TextStim(win = self.expWind, color=txtColor, text=lines, height=30,
                               wrapWidth=1000)
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
        math["math_q"] = m[0].strip()
        math["expected"] = m[1].strip().replace('"','')
        question = visual.TextStim(win = self.expWind, color=txtColor, text=m[0], 
                                   height=30, pos=(0,0))
        self.isi.start(3)
        question.draw()
        self.expWind.flip()
        self.isi.complete()
        true = visual.TextStim(win = self.expWind, color=txtColor, text="Doğru", 
                               pos=(-300, 0), height=30)
        false = visual.TextStim(win = self.expWind, color=txtColor, text="Yanlış", 
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
        self.Instructions("N-OST_Instructions.txt")
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
                stm = stm + imgNames[a].replace(".jpg",";")
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
            while not dataInput.OK:
                dataInput = gui.Dlg(title="")
                dataInput.addField()
                inp = dataInput.show()
            data["answers"] = inp[0]
            self.OSTdata.writerow(data)
            self.partData.writerow(data)
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
        self.Instructions("L-OST_Instructions.txt")
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
                stm = stm + words[a] + ";"
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
            while not dataInput.OK:
                dataInput = gui.Dlg(title="")
                dataInput.addField()
                inp = dataInput.show()
            data["answers"] = inp[0]
            self.OSTdata.writerow(data)
            self.partData.writerow(data)
        return p
    
    def Break(self, trialNum):
        """
        A function that waits between the trials so that participant can take a 5
        minute break
        """
        Break = visual.TextStim(win = self.expWind, color=txtColor, 
                                text= str(trialNum) + ". bölüm sona erdi. Eğer ara vermek istiyorsanız lütfen şimdi verin. Devam etmek istediğinizde 'space' tuşuna basınız.",  
                                   height=30, pos=(0,0), wrapWidth=1000)
        Break.draw()
        self.expWind.flip()
        event.waitKeys(keyList=["space"])
        return
    
    def Test_Trial(self):
        """
        A function that presents the participant with test stimuli to help them learn
        the task.
        """
        test = visual.TextStim(win = self.expWind, color=txtColor, 
                                text="Deneyi daha anlaşılır kılmak için şimdi size bir deneme gösterilecektir. Şimdi size bir kelime ve matematik sorusu gösterilecektir. Matematik sorusu ekrandan kaybolduktan sonra, sorunun doğru çözülüp çözülmediğini belirtmeniz istenecektir. Sonrasında ise ortaya çıkan ekrana gördüğünüz kelimeyi yazmanız istenecektir. Hazır olduğunuzda 'space' tuşuna basarak denemeyi başlatabilirsiniz.",  
                                   height=30, pos=(0,0), wrapWidth=1000)
        test.draw()
        self.expWind.flip()
        event.waitKeys(keyList=["space"])
        self.isi.start(.5)
        self.fixation.draw()
        self.expWind.flip()
        self.isi.complete()
        test = visual.TextStim(win = self.expWind, color=txtColor, text="Bilkent",  
                               height=30, pos=(0,0))
        self.isi.start(1)
        test.draw()
        self.expWind.flip()
        self.isi.complete()
        test = visual.TextStim(win = self.expWind, color=txtColor, 
                               text="(5 + 2) x 3 = 21",  height=30, pos=(0,0))
        self.isi.start(3)
        test.draw()
        self.expWind.flip()
        self.isi.complete()
        true = visual.TextStim(win = self.expWind, color=txtColor, text="Doğru", 
                               pos=(-300, 0), height=30)
        false = visual.TextStim(win = self.expWind, color=txtColor, text="Yanlış", 
                               pos=(300, 0), height=30)
        true.draw()
        false.draw()
        self.expWind.flip()
        event.waitKeys(keyList=["a","l"])
        testInput = gui.Dlg(title="")
        testInput.addField()
        output = testInput.show()
        if testInput.OK:
            dlg = gui.Dlg("Deneme")
            dlg.addText("Harika! Denemeyi bitirdiniz. Denemeyi bir daha yapmak ister misiniz?")
            dlg.addField("", choices=["Hayır","Evet"])
            t = dlg.show()
            print(t)
            if t[0] == "Evet":
                return self.Test_Trial()
            else:
                return
        else:
            while not testInput.OK:
                testInput = gui.Dlg(title="")
                testInput.addField()
                output = testInput.show()
            
    def Run(self):
        """
        A function that runs the experiment. It arranges the running order of the 
        functions.
        """
        self.Instructions("General_Instructions.txt")
        self.Test_Trial()
        direc = os.path.realpath(__file__).replace("Functions.py","N-OST_Images")
        trialTypes = ["N-OST","TurkishDaily", "EnglishDaily", "TurkishAcademic", "EnglishAcademic"]
        random.shuffle(trialTypes)
        mathNum = 0
        for trial in trialTypes:
            if trial == "N-OST":
                mathNum = self.NonLinguistic_OST("N-OST_Stimuli.txt", direc, p=mathNum)
                if trialTypes.index(trial) != (len(trialTypes) - 1):
                    self.Break(int(trialTypes.index(trial)) + 1)
            else:
                s = trial + ".txt"
                mathNum = self.Linguistic_OST(s, trial, mathNum)
                if trialTypes.index(trial) != (len(trialTypes) - 1):
                    self.Break(int(trialTypes.index(trial)) + 1) 
        end = visual.TextStim(win = self.expWind, color=txtColor, 
                                text="Deney sona erdi. Katıldığınız için teşekkür ederiz. Araştırmacıya deneyin bittiğini haber verebilirsiniz. \n Çıkmak için 'space' tuşuna basınız.",  
                                   height=30, pos=(0,0), wrapWidth=1000)
        end.draw()
        self.expWind.flip()
        event.waitKeys(keyList=["space"])