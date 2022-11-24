# Coursework 02 ~ Phoebe Pinney
# Dodge

### imports
try:
    import Tkinter
except:
    import tkinter as Tkinter

from tkinter import Tk, messagebox, Entry, PhotoImage, Label, Button, Text
import time, random
from threading import Timer
###

### Initial set up values
width=1000
height=700
back_colour='pale green'
moving_speed = 8
###

class main(object): # main class (holds entire game)
    def __init__(self):
        # initialize tkinter window parameters
        self.root = Tk()
        self.root.title(" Dodge ")
        self.root.geometry("1000x700")
        self.root.resizable(0, 0)
        self.root.configure(bg=back_colour)

        self.__initImages() # call to initialise the game images

    def __initImages(self):
        self.images = {
            'startBtnImg': PhotoImage(file="start.png"),
            'scoresBtnImg': PhotoImage(file="scores.png"),
            'quitBtnImg': PhotoImage(file="quit.png"),
            'againBtnImg' : PhotoImage(file="again.png"),
            'title': PhotoImage(file="title.png"),
            'chickenright': PhotoImage(file="chickenright.png"),
            'xmasCR' : PhotoImage(file="xmasCR.png"),
            'chickenleft' : PhotoImage(file="chickenleft.png"),
            'xmasCL' : PhotoImage(file="xmasCL.png"),
            'egg' : PhotoImage(file="egg.png"),
            'fire' : PhotoImage(file="fire.png"),
            'bossKeyScreenImg' : PhotoImage(file="bosskeyscreen.png")
        }

        self.__initWidgets() # call to initialise the game widgets

    def __initWidgets(self):
        # initialize widgets for start screen
        self.startBtn = Button(self.root, image=self.images['startBtnImg'], bd=4,highlightbackground='black', highlightthickness= 5, bg='white', width="305", height="77", command =self.__initGameOnce)
        self.quitBtn = Button(self.root, image=self.images['quitBtnImg'], bd=4,highlightbackground='black', highlightthickness= 5, bg='white', width="305", height="77", command =self.root.quit)
        self.scoresBtn = Button(self.root, image=self.images['scoresBtnImg'], bd=4,highlightbackground='black', highlightthickness= 5, bg='white', width="641", height="77", command=self.showScoreboard)
        self.titleLabel = Label(highlightthickness=0,image=self.images['title'], bd=0)
        self.scoreboardLabel = Label(highlightthickness=0,image=self.images['scoresBtnImg'], bd=0, bg=back_colour)

        # initialize widgets for the game
        self.gameCanvas = Tkinter.Canvas(width=width, height=height, background=back_colour)

        # key binds for the game control
        self.root.bind('<Left>', self.left)
        self.root.bind('<Right>', self.right)
        self.root.bind('<Up>', self.up)
        self.root.bind('<Down>', self.down)
        self.root.bind('<Escape>', self.escape)
        self.root.bind('p', self.pause)
        self.root.bind('b', self.bosskey)
        self.root.bind('x', self.xpress)
        self.root.bind('m', self.mpress)
        self.root.bind('a', self.apress)
        self.root.bind('s', self.spress)

        # call to display the start menu
        self.__initStartMenu()

    def __initStartMenu(self):
        # initial values to set
        self.scoreboardreset = False
        self.gameRunning = False
        self.startmenu = True

        # place pre-initialised widgets
        self.startBtn.place(x=347, y=310)
        self.scoresBtn.place(x=179, y=420)
        self.quitBtn.place(x=347, y=530)
        self.titleLabel.place(x=210, y=50)

        # creation of other start screen widgets
        self.xmaschicken = Label(image=self.images['xmasCL'], bg=back_colour)
        self.xmaschicken.place(x=60, y=580)
        self.secret = Label(anchor='center',bg=back_colour,text="Can you activate the\nsecret christmas mode?",font=('times 12 bold'),fg='white')
        self.secret.place(x=25, y=545)
        self.text="Catch the egg and dodge the fire!"
        self.words = Label(anchor='center',bg=back_colour,text=self.text,font=('times 30 bold'),fg='green')
        self.words.place(x=206, y=240)
        self.green = True
        if self.startmenu == True:
            self.flashtext() # makes text flash between black and green

        # execute the game
        self.root.mainloop()

    def flashtext(self):
        if self.startmenu == True:
            if self.green == True:
                self.words.configure(fg='black')
                self.green = False
            elif self.green == False:
                self.words.configure(fg='green')
                self.green = True
            self.root.after(300,self.flashtext) # uses after to create a pause

    def showScoreboard(self): # displays the scoreboard
        # destroys start screen widgets and sets some values
        self.scoreboardreset = True
        self.titleLabel.destroy()
        self.startBtn.destroy()
        self.quitBtn.destroy()
        self.scoresBtn.destroy()
        self.words.destroy()
        self.secret.destroy()
        self.xmaschicken.destroy()
        self.startmenu = False

        self.scoreboardLabel.place(x=179,y=50)

        # read in the scoreboard values saved in the text file
        scores = open('Scores.txt', 'r')
        self.scorevalues = []
        for line in scores:
            try:
                score, name = line.split()
                score = int(score)
                self.scorevalues.append((score, name))
            except:
                pass

        self.scorevalues.sort(key=lambda s: s[0], reverse = True) # sort values in decending order

        # creates some scoreboard screen widgets
        self.top5 = Label(anchor='center',bg=back_colour,text="TOP 5 SCORES:",font=('cooper 50 bold'),fg='black')
        self.top5.place(x=230, y=145)
        self.eggimage1 = Label(image=self.images['egg'], bg=back_colour)
        self.eggimage2 = Label(image=self.images['egg'], bg=back_colour)
        self.eggimage1.place(x=180,y=150)
        self.eggimage2.place(x=770, y=150)
        self.chickenOnBtn = Label(image=self.images['chickenright'], bg=back_colour)
        self.chickenOnBtn.place(x=815, y=513)
        self.backBtn = Button(self.root, text="BACK", fg='black', font=("cooper 20 bold"), bd=4,highlightbackground='black', highlightthickness= 5, bg='white', width="4", height="1", command =self.reset)
        self.backBtn.place(x=800, y=600)

        # sets scoreboard top 5 positions
        try:
            self.one = self.scorevalues[0]
        except:
            self.one = ["EMPTY"," "]
        try:
            self.two = self.scorevalues[1]
        except:
            self.two = ["EMPTY"," "]
        try:
            self.three = self.scorevalues[2]
        except:
            self.three = ["EMPTY"," "]
        try:
            self.four = self.scorevalues[3]
        except:
            self.four = ["EMPTY"," "]
        try:
            self.five = self.scorevalues[4]
        except:
            self.five = ["EMPTY"," "]

        # creates scoreboard
        self.place1Text = ("1: " + str(self.one[0]) + "    " + self.one[1])
        self.place2Text = ("2: " + str(self.two[0]) + "    " + self.two[1])
        self.place3Text = ("3: " + str(self.three[0]) + "    " + self.three[1])
        self.place4Text = ("4: " + str(self.four[0]) + "    " + self.four[1])
        self.place5Text = ("5: " + str(self.five[0]) + "    " + self.five[1])
        self.scoreboardText = (self.place1Text + "\n" + self.place2Text + "\n" + self.place3Text + "\n" + self.place4Text + "\n" + self.place5Text)
        self.scoreboardTextLbl = Label(justify='left',bg=back_colour,text=self.scoreboardText,font=('cooper 45 bold'),fg='white')
        self.scoreboardTextLbl.place(x=200,y=250)

        scores.close() # close text file

    def __initGameOnce(self):
        # removes start screen widgets
        self.titleLabel.destroy()
        self.startBtn.destroy()
        self.quitBtn.destroy()
        self.scoresBtn.destroy()
        self.words.destroy()
        self.secret.destroy()
        self.xmaschicken.destroy()
        self.startmenu = False

        # instantiate game canvas
        self.gameCanvas.pack()

        self.__initGame()

    def left(self, event): # left arrow
        coords = self.gameCanvas.coords(self.player)
        self.gameCanvas.delete("player")
        if self.xmas == True:
            self.player=self.gameCanvas.create_image(coords, image=self.images['xmasCL'], tag="player")
        else:
            self.player=self.gameCanvas.create_image(coords, image=self.images['chickenleft'], tag="player")
        self.x=-self.moving_speed
        self.y=0
        return

    def right(self, event): # right arrow
        coords1 = self.gameCanvas.coords(self.player)
        if self.xmas == True:
            self.gameCanvas.delete("player")
            self.player=self.gameCanvas.create_image(coords1, image=self.images['xmasCR'], tag="player")
        else:
            self.gameCanvas.delete("player")
            self.player=self.gameCanvas.create_image(coords1, image=self.images['chickenright'], tag="player")
        self.x=self.moving_speed
        self.y=0
        return

    def up(self, event): # up arrow
        self.x=0
        self.y=-self.moving_speed
        return

    def down(self, event): # down arrow
        self.x=0
        self.y=self.moving_speed
        return

    def escape(self, event): # escape button
        self.timerLoop.stop()
        self.windowOpen = False
        self.root.destroy()

    def pause(self, event): # pause feature
        if self.unbind == False:
            if self.paused == True:
                self.timerLoop.start()
                self.paused = False
            else:
                self.timerLoop.stop()
                self.paused = True

    def bosskey(self, event): # bosskey
        if self.unbind == False:
            if self.bossKeyScreenUp == True:
                self.bossKeyScreen.destroy()
                self.timerLoop.start()
                self.bossKeyScreenUp = False
            else:
                self.bossKeyScreen = Tkinter.Label(highlightthickness=0,image=self.images['bossKeyScreenImg'], bd=0)
                self.bossKeyScreen.place(x=0,y=0)
                self.timerLoop.stop()
                self.bossKeyScreenUp = True

    def xpress(self,event): # x for xmas
        if self.unbind == False:
            self.xpressed = True

    def mpress(self,event): # m in xmas
        if self.unbind == False:
            self.mpressed = True

    def apress(self,event): # a in xmas
        if self.unbind == False:
            self.apressed = True

    def spress(self,event): # s in xmas (cheat code unlocked)
        if self.unbind == False:
            self.spressed = True
            if self.xpressed == True and self.mpressed == True and self.apressed == True:
                self.xmas = True
                self.xmastime()

    def __initGame(self):
        # sets some initial game values
        self.windowOpen = True
        self.score = 0
        self.x=moving_speed
        self.y=0
        self.roadmap=[(0,0)]
        self.target=None # player's target
        self.score=0 # score starts at 0
        self.danger=[] # list of obstacles
        self.moving_speed=moving_speed

        # place some game widgets
        self.scoreboardLabel = Tkinter.Label(self.root, font=('cooper 15 bold'), bg=back_colour, fg='white', text="Score : {}".format(self.score))
        self.scoreboardLabel.place(x=455,y=10)
        self.player=self.gameCanvas.create_image(400, 400, image=self.images['chickenright'], tag="player")
        self.reminder = Tkinter.Label(self.root, bg=back_colour, font=('cooper 10'), fg='green', text="Reminder: you speed up each time you score a point and GAME OVER if you go off the screen!")
        self.reminder.place(x=200, y=680)
        self.infotext = Tkinter.Label(self.root, justify='left', bg=back_colour, font=('cooper 10'), fg='green', text="Press:\nEsc -> EXIT\nP -> Pause\nB -> Boss Key")
        self.infotext.place(x=12,y=8)

        # creates grid for obstacles
        self.grid = []
        for row in range(20):
            for col in range(10):
                self.grid.append([row, col])
        for each in self.grid:
            each[0] = each[0]*50
            each[1] = each[1]*72

        self.gameStarting() # call to begin game moving

    def gameStarting(self):
        # sets some initial values
        self.unbind = False
        self.gameRunning = True
        self.paused = False
        self.bossKeyScreenUp = False
        self.xpressed = False
        self.mpressed = False
        self.apressed = False
        self.spressed = False
        self.xmas = False

        # what to do if user closes the game window
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        # creates a repeating loop while game is playing
        self.timerLoop = RepeatTimer(0.09, self.looping)
        self.timerLoop.start()

    def close_window(self): # when window closed
        self.gameRunning = False
        self.windowOpen = False
        self.timerLoop.stop()
        self.root.destroy()

    def xmastime(self): # when cheat code unlocked
        self.xmasMsg = Label(anchor='center',bg=back_colour,text="CHRISTMAS MODE!!",font=('times 15 bold'),fg='red')
        self.xmasMsg.place(x=785, y=11)
        eggcoords = self.gameCanvas.coords(self.target)
        self.gameCanvas.delete("target")
        egg = PhotoImage(file="xmasegg.png")
        label2 = Label(image=egg)
        label2.image = egg
        self.target=self.gameCanvas.create_image(eggcoords, image=egg, tag="target")

    def looping(self): # updates game every loop
        self.re_update()
        # checks if window still open
        if self.windowOpen == False:
            self.close_window


    def moving(self): # makes the player character move
        self.gameCanvas.move(self.player,self.x,self.y)
        x,y=self.gameCanvas.coords(self.player)
        if x<=0 or y<=0:
            self.x=0
            self.y=0
            self.gameOver()
        elif height<=y or width<=x:
            self.x=0
            self.y=0
            self.gameOver()
        try:
            for each in self.danger:
                x1,y1=self.gameCanvas.coords(each)
                if len(self.gameCanvas.find_overlapping(x1,y1,x1+15,y1+15))!=1:
                    self.gameOver()
        except:
            pass
        return

    def gameOver(self): # when the player goes outside of the game window or hits fire - GAME OVER
        self.unbind = True
        self.gameOverMsg = Tkinter.Label(self.root, bg=back_colour, text="GAME OVER!",font=('cooper 60 bold'),fg='red')
        self.gameOverMsg.place(x=230, y=250)
        self.gameRunning=False
        self.timerLoop.stop()
        self.nameLbl = Label(anchor='center',bg=back_colour,text="Name: ",font=('cooper 30 bold'),fg='black')
        self.nameLbl.place(x=300, y=400)
        self.nameTxtBox = Entry(self.root, width=10, font=('cooper 20'), bd=4, justify='center')
        self.nameTxtBox.place(x=460, y=400)


        self.againBtn = Tkinter.Button(self.root, image=self.images['againBtnImg'], bd=4,highlightbackground='black', highlightthickness= 5, bg='white', width="510", height="77", command =self.saveScore)
        self.againBtn.place(x=247, y=500)
        return

    def saveScore(self): # saves player final score and name to text file
        self.name=self.nameTxtBox.get()
        scores = open('Scores.txt', 'a')
        scores.write(str(self.score))
        scores.write(" ")
        if self.name != "":
            scores.write(self.name)
        else:
            scores.write("?")
        scores.write("\n")
        scores.close()
        self.reset()

    def find(self): # has target been hit by the player?
        if self.target==None: # creates a target if one not already there
            x=random.randint(30,width-30)
            y=random.randint(30,height-30)
            if self.xmas == True:
                egg = PhotoImage(file="xmasegg.png")
            else:
                egg = PhotoImage(file="egg.png")
            label2 = Label(image=egg)
            label2.image = egg
            self.target=self.gameCanvas.create_image(x,y, image=egg, tag="target")

        if self.target: # checks for collision
            x1,y1=self.gameCanvas.coords(self.target)
            if len(self.gameCanvas.find_overlapping(x1,y1,x1+20,y1+20))!=1:
                self.gameCanvas.delete("target")
                self.target=None
                self.update_scoreboard()
                self.scoreboardLabel['text']="Score : {}".format(self.score)
        return

    def dodge(self): # creates objects the player must avoid
        fire = PhotoImage(file="fire.png")
        label3 = Label(image=fire)
        label3.image = fire
        novalidpos = True
        while novalidpos == True: # until random position for fire isnt already full
            pos=random.randint(0,201)
            if self.grid[pos] != "FULL":
                x = self.grid[pos][0]
                y = self.grid[pos][1]
                self.danger.append(self.gameCanvas.create_image(x,y, image=fire, tag="danger"))
                self.grid[pos] = "FULL"
                novalidpos = False

    def update_scoreboard(self): # updates scoreboard
        self.score=self.score+1
        self.dodge()
        self.moving_speed= (self.moving_speed)+1
        return

    def re_update(self): # updates game
        self.moving()
        self.find()

    def reset(self): # resets values when game state changes
        if self.scoreboardreset==True: # if resetting from scoreboard screen
            self.top5.destroy()
            self.eggimage1.destroy()
            self.eggimage2.destroy()
            self.backBtn.destroy()
            self.scoreboardTextLbl.destroy()
            self.chickenOnBtn.destroy()
        else: # if resetting from gameplay
            self.nameTxtBox.destroy()
            self.reminder.destroy()
            self.nameLbl.destroy()
            self.againBtn.destroy()
            self.gameOverMsg.destroy()
            self.infotext.destroy()
            self.gameCanvas.destroy()
            self.scoreboardLabel.destroy()
            try:
                self.xmasMsg.destroy()
            except:
                pass

        self.__initImages() # reinitialises whole game (to start screen)

class RepeatTimer(object): # timer object class

    def __init__(self, interval, function, *args):
        self.thread = None
        self.interval = interval
        self.function = function
        self.args = args
        self.isRunning = False

    def _handleFunction(self):
        self.isRunning = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.isRunning:
            self.thread = Timer(self.interval, self._handleFunction)
            self.thread.start()
            self.isRunning = True

    def stop(self):
            self.thread.cancel()
            self.isRunning = False


main = main() # creates main object
