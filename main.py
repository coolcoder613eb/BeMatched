#!/bin/python3.9
from Be import *
from copy import copy


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
        self.start_msg = BMessage(START_MSG)
        self.panel = BView(self.Bounds(), "panel", 8, 20000000)
        self.label = BStringView(BRect(40, 30, 200, 50), "label", "Match It")
        font=be_plain_font
        font.SetSize(font.Size()+5)
        self.label.SetFont(font)
        self.start_button = BButton(
            BRect(40, 90, 100, 50), "start_button", "Start", self.start_msg
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
        self.ok_msg = BMessage(OK_MSG)
        self.panel = BView(self.Bounds(), "panel", 8, 20000000)
        #self.label_1 = BStringView(BRect(50, 10, 150, 30), "label 1", "Name Of Player 1")
        self.input_1 = BTextControl(BRect(50, 10, 250, 20), "input 1", "Name Of Player 1","player1",self.ok_msg)
        #be_plain_font.SetSize(be_plain_font.Size()-5)
        #self.input_1.SetFont(be_plain_font)
        self.ok_button = BButton(
            BRect(40, 90, 100, 50), "ok_button", "Ok", self.ok_msg
        )
        self.panel.AddChild(self.input_1, None)
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
        self.Quit()

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
