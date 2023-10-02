#!/bin/python3.9
from Be import *
from copy import copy
import random
import time


should_close=True

class StartWindow(BWindow):
    def __init__(self):
        BWindow.__init__(
            self,
            BRect(100, 100, 250, 250),
            "Match It",
            B_TITLED_WINDOW_LOOK,
            B_NORMAL_WINDOW_FEEL,
            B_NOT_RESIZABLE | B_QUIT_ON_WINDOW_CLOSE,
        )
        START_MSG = int32(b"StBt")
        self.events = {START_MSG: self.start}
        self.panel = BView(self.Bounds(), "panel", 8, 20000000)
        self.label = BStringView(BRect(40, 30, 200, 50), "label", "Match It")
        font=be_plain_font
        font.SetSize(font.Size()+5)
        self.label.SetFont(font)
        self.start_button = BButton(
            BRect(40, 90, 100, 50), "start_button", "Start", BMessage(START_MSG)
        )
        self.panel.AddChild(self.label, None)
        self.panel.AddChild(self.start_button, None)
        self.AddChild(self.panel, None)
        self.Show()

    def MessageReceived(self, msg):
        if msg.what in self.events:
            self.events[msg.what](msg)
        else:
            BWindow.MessageReceived(self, msg)
    

    def start(self, msg):
        global should_close
        print("Started!")
        should_close=False
        setupwindow=SetupWindow()
        self.Quit()

class SetupWindow(BWindow):
    def __init__(self):
        BWindow.__init__(
            self,
            BRect(100, 100, 450, 250),
            "Setup",
            B_TITLED_WINDOW_LOOK,
            B_NORMAL_WINDOW_FEEL,
            B_NOT_RESIZABLE | B_QUIT_ON_WINDOW_CLOSE,
        )
        OK_MSG = int32(b"OkBt")
        self.events = {OK_MSG: self.ok}
        self.panel = BView(self.Bounds(), "panel", 8, 20000000)
        self.input_1 = BTextControl(
            BRect(10, 10, 330, 20), "input 1", "Name Of Player 1", "player1", BMessage(OK_MSG)
        )
        self.input_2 = BTextControl(
            BRect(10, 60, 330, 20), "input 2", "Name Of Player 2", "player2", BMessage(OK_MSG)
        )
        self.ok_button = BButton(
            BRect(120, 100, 210, 50), "ok_button", "Ok", BMessage(OK_MSG)
        )
        self.panel.AddChild(self.input_1, None)
        self.panel.AddChild(self.input_2, None)
        self.panel.AddChild(self.ok_button, None)
        self.AddChild(self.panel, None)
        self.Show()

    def MessageReceived(self, msg):
        if msg.what in self.events:
            self.events[msg.what](msg)
        else:
            BWindow.MessageReceived(self, msg)
    

    def ok(self, msg):
        global should_close
        print("Started!")
        should_close=False
        player1=self.input_1.Text()
        player2=self.input_2.Text()
        mainwindow=MainWindow(player1,player2)
        self.Quit()

class MainWindow(BWindow):
    def __init__(self,player1,player2):
        BWindow.__init__(
            self,
            BRect(100, 100, 700, 700),
            "Match It",
            B_TITLED_WINDOW_LOOK,
            B_NORMAL_WINDOW_FEEL,
            B_NOT_RESIZABLE | B_QUIT_ON_WINDOW_CLOSE,
        )
        OK_MSG = int32(b"OkBt")
        self.events = {x: self.ok for x in range(24)}
        self.panel = BView(self.Bounds(), "panel", 8, 20000000)
        self.player1=[player1,0]
        self.player2=[player2,0]
        self.prev = None
        self.prevprev=None
        self.first = True
        self.player1_turn = True
        self.symbols = ['!','!','@','@','#','#','{','{','$','$','%','%','^','^','&','&','*','*','~','~','?','?','[','[']
        random.shuffle(self.symbols)
        self.buttons=[]
        i=0
        for x in range(6):
            for y in range(4):
                self.buttons.append(BButton(BRect(10+(100*x),10+(100*y),90+(100*x),90+(100*y)), f'button_{x}_{y}', '', BMessage(i)))
                self.panel.AddChild(self.buttons[-1],None)
                i+=1
        font=be_plain_font
        font.SetSize(be_plain_font.Size()+10)
        self.label_1 = BStringView(BRect(200, 450, 450, 490), "label 1", "Player1 Turn")
        self.label_1.SetFont(font)
        self.panel.AddChild(self.label_1, None)
        self.label_2 = BStringView(BRect(200, 550, 450, 570), "label 2", f"{self.player1[0]}: {self.player1[1]}{' '*30}{self.player2[0]}: {self.player2[1]}")
        self.panel.AddChild(self.label_2, None)
        self.AddChild(self.panel, None)
        self.Show()

    def MessageReceived(self, msg):
        if msg.what in self.events:
            self.events[msg.what](msg)
        else:
            BWindow.MessageReceived(self, msg)
            
    

    def ok(self, msg):
        print(msg,msg.what)
        i=msg.what
        self.buttons[i].SetLabel(self.symbols[i])
        print('first',self.first,'\nprevprev',self.prevprev,'\nprev',self.prev,'\ni',i,'\nsymbols[i]',self.symbols[i])
        
        if self.first:
            if self.prevprev is not None:
                self.buttons[self.prevprev].SetLabel('')
            if self.prev  is not None:
                self.buttons[self.prev].SetLabel('')
            self.prevprev=self.prev
            self.prev=i
            
        elif self.prev != i:
            
            if self.symbols[self.prev] == self.symbols[i]: # correct match
                self.buttons[self.prev].SetEnabled(False)
                self.buttons[i].SetEnabled(False)
                if self.player1_turn:
                    self.player1[1] += 1
                else:
                    self.player2[1] += 1
            
            print([not x.IsEnabled() for x in self.buttons])
            if all([not x.IsEnabled() for x in self.buttons]):
                if self.player1[1] > self.player2[1]:
                    title='Congratulations!'
                    text = f'{self.player1[0]} Won!'
                elif self.player1[1] < self.player2[1]:
                    title='Congratulations!'
                    text = f'{self.player2[0]} Won!'
                else:
                    title='Good Game!'
                    text = f'{self.player1[0]} Drew With {self.player2[0]}!'
                print(title)
                print(text)
                b=BAlert(title,text,'Ok',None,None)
                b.Go()
                self.Quit()
            self.player1_turn = not self.player1_turn
            self.prevprev=self.prev
            self.prev=i
            person=self.player1[0] if self.player1_turn else self.player2[0]
            self.label_1.SetText(f'{person} Turn')
            self.label_2.SetText(f"{self.player1[0]}: {self.player1[1]}{' '*30}{self.player2[0]}: {self.player2[1]}")
            
        self.first = not self.first
        for i, x in enumerate(self.buttons):
            if not x.IsEnabled():
                x.SetLabel(self.symbols[i])
        


class MatchIt(BApplication):
    def __init__(self):
        BApplication.__init__(self, "application/x-matchit")
        startwindow = StartWindow()
    def QuitRequested(self):
        global should_close
        rtn = should_close
        if not should_close:
            should_close=True
        return rtn


def main():
    a = MatchIt()
    a.Run()


if __name__ == "__main__":
    main()
