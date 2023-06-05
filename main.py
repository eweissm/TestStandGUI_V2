# Test Stand GUI V2
# Date: 05/29/2023
# By: Eric Weissman
# Description: This code generates a GUI for the test stand controls. At the moment, this GUI offers both manual controls
# and automatic controls which can be toggled between.

# TODO:
#  add wire feed controls
#  allow for g-code entries for automatic controls


# import used packages
import serial
import time
import tkinter


# Define buttons commands----------------------------------------------------------------------------------------------
def buttonCommand_setActuatorSelectionLeft(): #set manual controls to actuate only the left actuators
    global ActuatorSelection_state
    ActuatorSelection_state = 0
    ActuatorSelectionLabel.set("Left")
    ser.write(bytes('LE', 'UTF-8'))  # left Signal
    print(bytes('LE', 'UTF-8'))


def buttonCommand_setActuatorSelectionRight():  #set manual controls to actuate only the right actuators
    global ActuatorSelection_state
    ActuatorSelection_state = 1
    ActuatorSelectionLabel.set("Right")
    ser.write(bytes('RE', 'UTF-8'))  # right Signal
    print(bytes('RE', 'UTF-8'))

def buttonCommand_setActuatorSelectionBoth():  #set manual controls to actuate both side of actuators
    global ActuatorSelection_state
    ActuatorSelection_state = 2
    ActuatorSelectionLabel.set("Both")
    ser.write(bytes('BE', 'UTF-8'))  # both Signal
    print(bytes('BE', 'UTF-8'))

def buttonCommand_toggleAutomatedControls(): #toggles between manual and automated controls
    global Automated_Controls_state

    # if we are in automated controls --> set to manual--> else set controls to automatic
    if Automated_Controls_state == 1:
        Automated_Controls_state = 0
        varLabel.set("Automated Controls: Off ")
        ser.write(bytes('ME', 'UTF-8')) #Manual Signal
        print(bytes('ME', 'UTF-8'))
    else:
        Automated_Controls_state = 1
        varLabel.set("Automated Controls: On ")
        ser.write(bytes('AE', 'UTF-8')) #Automated Signal
        print(bytes('AE', 'UTF-8'))

def buttonCommand_updateTargetHeight(): #Reads the txt entry and sends to serial message arduino to update target height
    global TargetHeight
    TargetHeight = TargetHeightEntry.get()
    ser.write(bytes('V'+str(int(TargetHeight))+'E', 'UTF-8'))
    print(bytes('V'+str(int(TargetHeight))+'E', 'UTF-8'))


def buttonCommand_moveUp():  # manual control for moving up
    ser.write(bytes('UE', 'UTF-8'))  # up Signal
    print(bytes('UE', 'UTF-8'))


def buttonCommand_moveDown():  # manual control for moving down
    ser.write(bytes('DE', 'UTF-8'))  # down Signal
    print(bytes('DE', 'UTF-8'))

def buttonCommand_FeedWireForward():  # manual control for feeding the wire forward
    ser.write(bytes('FE', 'UTF-8'))   # wire forward signal
    print(bytes('FE', 'UTF-8'))

def buttonCommand_FeedWireBackward():  #manual control for feeding the wire backward
    ser.write(bytes('KE', 'UTF-8'))   # wire backward signal
    print(bytes('KE', 'UTF-8'))

def buttonCommand_STOP(): # manual control for stopping wire feed
    ser.write(bytes('JE','UTF-8')) # wire stop signal
    print(bytes('JE','UTF-8'))

def buttonCommand_updateTargetSpeed(): #Reads the txt entry and sends to serial message arduino to update target speed
    global TargetSpeed
    TargetSpeed = TargetSpeedEntry.get()
    TargetSpeed = float(TargetSpeed)/0.0177
    ser.write(bytes('S'+str(int(TargetSpeed))+'E', 'UTF-8'))
    print(bytes('S'+str(int(TargetSpeed))+'E', 'UTF-8'))

def buttonCommand_updateAutoOnOff(): # Toggles between manual and automated control of wire feed speed
    global Automated_Controls_stateWF

    # if we are in automated controls --> set to manual--> else set controls to automatic
    if Automated_Controls_stateWF == 1:
        Automated_Controls_stateWF = 0
        varLabel1.set("Automated Wire Feed Controls: Off ")
        ser.write(bytes('NE', 'UTF-8'))  # Manual Signal
        print(bytes('NE', 'UTF-8'))
    else:
        Automated_Controls_stateWF = 1
        varLabel1.set("Automated Wire Feed Controls: On ")
        ser.write(bytes('GE', 'UTF-8'))  # Automated Signal
        print(bytes('GE', 'UTF-8'))
def buttonCommand_RotateCW(): # manual control for rotating platform clockwise
    global RotateDirectionState
    RotateDirectionState = 1
    RotateDirection.set("Clockwise")
    ser.write(bytes('ZE', 'UTF-8'))   # Rotate platform clockwise signal
    print(bytes('ZE', 'UTF-8'))

def buttonCommand_RotateCCW(): # manual control for rotating platform counterclockwise
    global RotateDirectionState
    RotateDirectionState = 0
    RotateDirection.set("Counter-Clockwise")
    ser.write(bytes('XE', 'UTF-8'))   # Rotate platform clockwise signal
    print(bytes('XE', 'UTF-8'))

def buttonCommand_Rotate(): # manual control for rotating platform clockwise
    global TargetAngle
    TargetAngle = TargetAngleEntry.get()

    ser.write(bytes('C'+str(int(TargetAngle))+'E', 'UTF-8'))
    print(bytes('C'+str(int(TargetAngle))+'E', 'UTF-8'))

def buttonCommand_updateAutoRPOnOff(): # Toggles between manual and automated control of rotating platform speed
    global Automated_Controls_stateRP

    # if we are in automated controls --> set to manual--> else set controls to automatic
    if Automated_Controls_stateRP == 1:
        Automated_Controls_stateRP = 0
        AutoRPLabel.set("Automated Rotating Platform Controls: Off ")
        ser.write(bytes('OE', 'UTF-8'))  # Manual Signal
        print(bytes('OE', 'UTF-8'))
    else:
        Automated_Controls_stateRP = 1
        AutoRPLabel.set("Automated Rotating Platform Controls: On ")
        ser.write(bytes('PE', 'UTF-8'))  # Automated Signal
        print(bytes('PE', 'UTF-8'))

def buttonCommand_updateTargetAngleSpeed(): #Reads the txt entry and sends to serial message arduino to update target speed
    global TargetAngleSpeed
    TargetAngleSpeed = TargetAngleSpeedEntry.get()

    ser.write(bytes('I'+str(int(TargetAngleSpeed))+'E', 'UTF-8'))
    print(bytes('I'+str(int(TargetAngleSpeed))+'E', 'UTF-8'))

# declare the automated controls to default at 0 (manual controls)
Automated_Controls_state = 0
Automated_Controls_stateWF = 0
Automated_Controls_stateRP = 0

# Actuator default selection is both
ActuatorSelection_state = 2

# Platform Rotation Direction default is counterclockwise
RotateDirectionState = 0

# Set up Serial Communication with Arduino------------------------------------------------------------------------------
ser = serial.Serial('com3', 9600,writeTimeout=1)  # create Serial Object
time.sleep(3)  # delay 3 seconds to allow serial com to get established


# Build GUI-------------------------------------------------------------------------------------------------------------
tkTop = tkinter.Tk()  # Create GUI Box
tkTop.geometry('1200x1080')  # size of GUI
tkTop.title("Test Stand Controller")  # title in top left of window

Title = tkinter.Label(tkTop,text='Test Stand Controls', font=("Courier", 14, 'bold')).grid(row=0, column=0, rowspan=1, columnspan=2)  # Title on top middle of screen


# Fill in the Manual controls Side--------------------------------------------------------------------------------------
ManualFrame = tkinter.Frame(master=tkTop, height=200, width=600) # create frame for the manual controls
ManualLable = tkinter.Label(master=ManualFrame, text='Manual Stand Height Controls',
                            font=("Courier", 12, 'bold')).pack()  # manual controls lable
ManualFrame.grid(row=1, column=0)

LeftButtonsFrame = tkinter.Frame(master=ManualFrame, width=100)
LeftButtonsLable = tkinter.Label(master=LeftButtonsFrame, text='Actuator Selection',
                                 font=("Courier", 12, 'bold')).pack()

RightButtonsFrame = tkinter.Frame(master=ManualFrame, width=100)
RightButtonsLable = tkinter.Label(master=RightButtonsFrame, text='Up/Down Controls',
                                  font=("Courier", 12, 'bold')).pack()

button_left_state = tkinter.Button(LeftButtonsFrame,
                                   text="Left",
                                   command=buttonCommand_setActuatorSelectionLeft,
                                   height=4,
                                   fg="black",
                                   width=8,
                                   bd=5,
                                   activebackground='green'
                                   )
button_left_state.pack(side='top', ipadx=10, padx=10, pady=40)

button_right_state = tkinter.Button(LeftButtonsFrame,
                                    text="Right",
                                    command=buttonCommand_setActuatorSelectionRight,
                                    height=4,
                                    fg="black",
                                    width=8,
                                    bd=5,
                                    activebackground='green'
                                    )
button_right_state.pack(side='top', ipadx=10, padx=10, pady=40)

button_both_state = tkinter.Button(LeftButtonsFrame,
                                   text="Both",
                                   command=buttonCommand_setActuatorSelectionBoth,
                                   height=4,
                                   fg="black",
                                   width=8,
                                   bd=5,
                                   activebackground='green'
                                   )
button_both_state.pack(side='top', ipadx=10, padx=10, pady=40)

ActuatorSelectionLabel = tkinter.IntVar()
ActuatorSelection = tkinter.Label(master=LeftButtonsFrame, textvariable=ActuatorSelectionLabel)
ActuatorSelectionLabel.set("Both")
ActuatorSelection.pack()

button_up_state = tkinter.Button(RightButtonsFrame,
                                 text="Up",
                                 command=buttonCommand_moveUp,
                                 height=4,
                                 fg="black",
                                 width=8,
                                 bd=5,
                                 activebackground='green'
                                 )
button_up_state.pack(side='top', ipadx=10, padx=10, pady=40)

button_down_state = tkinter.Button(RightButtonsFrame,
                                   text="Down",
                                   command=buttonCommand_moveDown,
                                   height=4,
                                   fg="black",
                                   width=8,
                                   bd=5,
                                   activebackground='green'
                                   )
button_down_state.pack(side='top', ipadx=10, padx=10, pady=40)

LeftButtonsFrame.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)
RightButtonsFrame.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)

# Fill in the Automated controls Side----------------------------------------------------------------------------------------------------------------------------------------
AutoFrame = tkinter.Frame(master=tkTop, height=200, width=600, bg="gray")
AutoLable = tkinter.Label(master=AutoFrame, text='Automated Stand Height Controls', font=("Courier", 12, 'bold'), bg="gray").pack(
    side='top')  # Automated controls lable

button_Automated_on_off = tkinter.Button(AutoFrame,
                                         text="Turn Automated Controls on/off",
                                         command=buttonCommand_toggleAutomatedControls,
                                         height=4,
                                         fg="black",
                                         width=25,
                                         bd=5,
                                         activebackground='green'
                                         )
button_Automated_on_off.pack(side='top', ipadx=0, padx=0, pady=20)

varLabel = tkinter.IntVar()
tkLabel = tkinter.Label(master=AutoFrame, textvariable=varLabel, bg="gray")
varLabel.set("Automated Controls: Off")
tkLabel.pack()

TargetHeightLable = tkinter.Label(master=AutoFrame, text='Enter Target Height: ', font=("Courier", 12), bg="gray").pack(
    side='left', ipadx=10, padx=10, pady=40)  # Automated controls lable
TargetHeightEntry = tkinter.Entry(AutoFrame)
TargetHeightEntry.pack(side='left', ipadx=0, padx=0, pady=0)

button_UpdateTarget = tkinter.Button(AutoFrame,
                                     text="Update Target",
                                     command=buttonCommand_updateTargetHeight,
                                     height=2,
                                     fg="black",
                                     width=15,
                                     bd=5,
                                     activebackground='green'
                                     )
button_UpdateTarget.pack(side='left', ipadx=0, padx=20, pady=20)


AutoFrame.grid(row = 1, column = 1, stick='N')

# Fill in manual wire feed frame
ManualFrameWF = tkinter.Frame(master=tkTop, height=200, width=600)
ManWFLabel = tkinter.Label(master=ManualFrameWF,
                           text='Manual Wire Feed Controls',
                           font=("Courier", 12, 'bold')).grid(row=0, column=0, rowspan = 1, columnspan = 3, pady=20)  # Manual wire feed controls label

button_FeedWireBack = tkinter.Button(ManualFrameWF,
                                     text="Backward",
                                     command=buttonCommand_FeedWireBackward,
                                     height=2,
                                     fg="black",
                                     width=15,
                                     bd=5,
                                     activebackground='green')
button_FeedWireBack.grid(row=1,column=0, columnspan=1, pady=20, padx=10)

button_FeedWireFwd = tkinter.Button(master=ManualFrameWF,
                                     text="Forward",
                                     command=buttonCommand_FeedWireForward,
                                     height=2,
                                     fg="black",
                                     width=15,
                                     bd=5,
                                     activebackground='green')
button_FeedWireFwd.grid(row=1, column=2, columnspan=1, pady=20, padx=10)

button_Stop = tkinter.Button(master=ManualFrameWF,
                                     text="STOP",
                                     command=buttonCommand_STOP,
                                     height=2,
                                     fg="black",
                                     width=15,
                                     bd=5,
                                     activebackground='green')
button_Stop.grid(row=1, column=1, columnspan=1, pady=20, padx=10)

ManualFrameWF.grid(row=2, column=0, pady=20)

# Fill in automatic wire feed frame
AutoFrameWF = tkinter.Frame(master=tkTop, height=200, width=600, bg='gray')
AutoFrameWFLabel = tkinter.Label(master=AutoFrameWF,
                           text='Automatic Wire Feed Controls',
                           font=("Courier", 12, 'bold'),
                           bg="gray").grid(row=0, column=0, columnspan=3, pady=20)  # Automatic wire feed controls label

button_AutoWF_OnOff = tkinter.Button(AutoFrameWF,
                                     text="Automatic Wire Feed Speed On/Off",
                                     command=buttonCommand_updateAutoOnOff,
                                     height=2,
                                     fg="black",
                                     width=30,
                                     bd=5,
                                     activebackground='green'
                                     )
button_AutoWF_OnOff.grid(row=1, column=0, columnspan=3, padx=10)

varLabel1 = tkinter.IntVar()
AutoWFLabel = tkinter.Label(master=AutoFrameWF, textvariable=varLabel1, bg="gray").grid(row=2, column=1)
varLabel1.set("Automated Wire Feed Controls: Off")

AutoFrameWF.grid(row=2,column=1, pady=20, sticky='N')


TargetSpeedLabel = tkinter.Label(master=AutoFrameWF, text='Enter Target Speed [in/s]: ', font=("Courier", 12), bg="gray").grid(row=3,column=0, padx=10)  # Manual wire feed speed label
TargetSpeedEntry = tkinter.Entry(AutoFrameWF)
TargetSpeedEntry.grid(row=3, column=1, padx=10)

button_UpdateTarget = tkinter.Button(AutoFrameWF,
                                     text="Update Target",
                                     command=buttonCommand_updateTargetSpeed,
                                     height=2,
                                     fg="black",
                                     width=15,
                                     bd=5,
                                     activebackground='green'
                                     )
button_UpdateTarget.grid(row=3, column=2, padx=10)

#Fill in rotating platform manual control
ManualFrameRP = tkinter.Frame(master=tkTop, height=200, width=600)
ManualLabelRP = tkinter.Label(master=ManualFrameRP, text='Manual Platform Controls', font=("Courier", 12, 'bold')).grid(row=0, column=0, columnspan=6)
button_Clockwise = tkinter.Button(ManualFrameRP,
                                  text="Clockwise",
                                  command=buttonCommand_RotateCW,
                                  height=2,
                                  fg="black",
                                  width=15,
                                  bd=5,
                                  activebackground='green')
button_CounterClockwise = tkinter.Button(ManualFrameRP,
                                  text="Counter-Clockwise",
                                  command=buttonCommand_RotateCCW,
                                  height=2,
                                  fg="black",
                                  width=15,
                                  bd=5,
                                  activebackground='green')
button_Clockwise.grid(row=1, column=0, columnspan=3, padx=10, pady=20)
button_CounterClockwise.grid(row=1, column=3, columnspan=3, padx=10, pady=20)

RotateDirection = tkinter.IntVar()
RotateDirectionLabel = tkinter.Label(master=ManualFrameRP, textvariable=RotateDirection, font=("Courier", 12)).grid(row=2, column=0, columnspan=6, padx=10, ipadx=20, pady=5)
RotateDirection.set("Counter-Clockwise")

TargetAngleLabel = tkinter.Label(master=ManualFrameRP, text="Rotate [deg]:", font=("Courier", 12)).grid(row=3, column=0, columnspan=2, padx=10, pady=5)
TargetAngleEntry = tkinter.Entry(ManualFrameRP)
TargetAngleEntry.grid(row=3, column=2, columnspan=2, padx=10, pady=5)

button_TargetAngleUpdate = tkinter.Button(master=ManualFrameRP,
                                          text="Rotate",
                                          command=buttonCommand_Rotate,
                                          height=2,
                                          fg="black",
                                          width=15,
                                          bd=5,
                                          activebackground='green')
button_TargetAngleUpdate.grid(row=3, column=5, columnspan=2, padx=10, pady=5)

ManualFrameRP.grid(row=3, column=0, pady=20, sticky="N")

# Fill in automatic platform control frame
AutoFrameRP = tkinter.Frame(master=tkTop, height=200, width=600, bg='gray')
AutoFrameRPLabel = tkinter.Label(master=AutoFrameRP,
                           text='Automatic Rotating Platform Controls',
                           font=("Courier", 12, 'bold'),
                           bg="gray").grid(row=0, column=0, columnspan=3, pady=20)  # Automatic rotating platform controls label

button_AutoRP_OnOff = tkinter.Button(AutoFrameRP,
                                     text="Automatic Rotating Platform Speed On/Off",
                                     command=buttonCommand_updateAutoRPOnOff,
                                     height=2,
                                     fg="black",
                                     width=40,
                                     bd=5,
                                     activebackground='green'
                                     )
button_AutoRP_OnOff.grid(row=1, column=0, columnspan=3, padx=10)

AutoRPLabel = tkinter.IntVar()
AutoRP = tkinter.Label(master=AutoFrameRP, textvariable=AutoRPLabel, bg="gray").grid(row=2, column=1)
AutoRPLabel.set("Automatic Rotating Platform Controls: Off")

AutoFrameRP.grid(row=2,column=1, pady=20, sticky='N')


TargetAngleSpeedLabel = tkinter.Label(master=AutoFrameRP, text='Enter Target Angle Speed [deg/s]: ', font=("Courier", 12), bg="gray").grid(row=3,column=0, padx=10)
TargetAngleSpeedEntry = tkinter.Entry(AutoFrameRP)
TargetAngleSpeedEntry.grid(row=3, column=1, padx=10)

button_UpdateTargetAngleSpeed = tkinter.Button(AutoFrameRP,
                                     text="Update",
                                     command=buttonCommand_updateTargetAngleSpeed,
                                     height=2,
                                     fg="black",
                                     width=15,
                                     bd=5,
                                     activebackground='green'
                                     )
button_UpdateTargetAngleSpeed.grid(row=3, column=2, padx=10)

AutoFrameRP.grid(row=3, column=1)

tkinter.mainloop() # run loop watching for gui interactions

