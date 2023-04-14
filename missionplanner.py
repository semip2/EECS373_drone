import socket 

import clr

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Drawing import Point
from System.Windows import Forms

# GUI window
class CommandBox(Forms.Form):
    def __init__(self):
        self.Text = "Command Box!"
        self.Width = 350
        self.Height = 350

        self.start_button = Forms.Button()
        self.start_button.Text = 'Start Bluetooth'
        self.start_button.Location = Point(20, 20)
        self.start_button.Height = 25
        self.start_button.Width = 80
        self.start_button.Click += self.start_click
        
        self.panic_button = Forms.Button()
        self.panic_button.Text = 'Panic!'
        self.panic_button.Location = Point(230, 20)
        self.panic_button.Height = 25
        self.panic_button.Width = 80
        self.panic_button.Click += self.panic_click

        self.CancelButton = self.panic_button

        self.Controls.Add(self.start_button)
        self.Controls.Add(self.panic_button)

    def start_click(self, sender, event):
        run()

    def panic_click(self, sender, event):
        panic()

def run():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost',50000)) 

    flying = False

    while 1: 
        data = s.recv(105)
        print("Data recieved:", data)
        if not flying: 
            if(data.find(b'O') != -1): 
                print("Taking off")
                Script.ChangeMode('AltHold')
                MAV.doARM(True)
                Script.Sleep(5000)
                Script.SendRC(3,1500, True)
                #Script.SendRC(3, 1500 + Script.GetParam('THR_DZ'), True)
                Script.Sleep(2000)
                Script.SendRC(3, 1500, True)  
                Script.Sleep(2000)          
                flying = True
        elif flying: 
            if(data.find(b'O') != -1): 
                print("Landing")
                Script.ChangeMode('Land')
                flying = False
                Script.Sleep(5000)
                break
            elif(data[0] == b'C'): 
                print("Centering")
                Script.ChangeMode('AltHold')
                #Script.SendRC(3, 1500, True) #neutral throttle
                Script.SendRC(1, 1500, True)
                Script.SendRC(2, 1500, True)
                Script.SendRC(3, 1500, True)
                #Script.SendRC(1, 1500, True) #level roll
                #Script.SendRC(2, 1500, True) #level pitch
                #Script.Sleep(2000)
            elif(data[0] == b'L'): 
                print("Moving left")
                #Script.SendRC(8, 1700, True) #manual mode
                #Script.SendRC(2, 1500, True) #level pitch
                #Script.SendRC(3, 1500, True) #neutral throttle
                #Script.SendRC(1, 2000, True) #roll left
                Script.SendRC(1, 1600, True)
                Script.SendRC(2, 1500, True)
                Script.SendRC(3, 1500, True)
                #Script.Sleep(2000)
            elif(data[0] == b'R'): 
                print("Moving right")
                #Script.SendRC(8, 1700, True) #manual mode
                Script.SendRC(2, 1500, True) #level pitch
                Script.SendRC(3, 1500, True) #neutral throttle
                Script.SendRC(1, 1000, True) #roll right
                #Script.Sleep(2000)
            elif(data[0] == b'U'): 
                print("Moving up")
                #Script.SendRC(8, 1700, True) #manual mode
                Script.SendRC(1, 1500, True) #level roll            
                Script.SendRC(3, 1500, True) #neutral throttle
                Script.SendRC(2, 1000, True) #pitch up
                #Script.Sleep(2000)
            elif(data[0] == b'D'): 
                print("Moving down")
                #Script.SendRC(8, 1700, True) #manual mode
                Script.SendRC(1, 1500, True) #level roll            
                Script.SendRC(3, 1500, True) #neutral throttle
                Script.SendRC(2, 1600, True) #pitch down
                #Script.Sleep(2000)

    print("Closing bluetooth & Ending")
    s.close()

def panic(): 
    MAV.doARM(False)

def main():
    for channel in range(1, 9):
        Script.SendRC(channel, 1500, True)

    form = CommandBox()
    Forms.Application.Run(form)

main()