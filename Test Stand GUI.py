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

# Define buttons

# Delay variable for buffer management
T = 0
def buttonCommand_setActuatorSelectionLeft(): #set manual controls to actuate only the left actuators
    ser.flushInput()
    ser.flushOutput()

    global ActuatorSelection_state
    ActuatorSelection_state = 0
    ActuatorSelectionLabel.set("Left")
    ser.write(bytes('LE', 'UTF-8'))  # left Signal
    print(bytes('LE', 'UTF-8'))
    time.sleep(T)

def buttonCommand_setActuatorSelectionRight():  #set manual controls to actuate only the right actuators
    ser.flushInput()
    ser.flushOutput()

    global ActuatorSelection_state
    ActuatorSelection_state = 1
    ActuatorSelectionLabel.set("Right")
    ser.write(bytes('RE', 'UTF-8'))  # right Signal
    print(bytes('RE', 'UTF-8'))
    time.sleep(T)
def buttonCommand_setActuatorSelectionBoth():  #set manual controls to actuate both side of actuators
    ser.flushInput()
    ser.flushOutput()

    global ActuatorSelection_state
    ActuatorSelection_state = 2
    ActuatorSelectionLabel.set("Both")
    ser.write(bytes('BE', 'UTF-8'))  # both Signal
    print(bytes('BE', 'UTF-8'))
    time.sleep(T)
def buttonCommand_toggleAutomatedControls(): #toggles between manual and automated controls
    ser.flushInput()
    ser.flushOutput()

    global Automated_Controls_state

    # if we are in automated controls --> set to manual--> else set controls to automatic
    if Automated_Controls_state == 1:
        Automated_Controls_state = 0
        varLabel.set("Automated Controls: Off ")
        try:
            ser.write(bytes('ME', 'UTF-8')) #Manual Signal
        except serial.SerialTimeoutException:
            print("Write operation timed out.")
        print(bytes('ME', 'UTF-8'))
    else:
        Automated_Controls_state = 1
        varLabel.set("Automated Controls: On ")
        try:
            ser.write(bytes('AE', 'UTF-8')) #Automated Signal
        except serial.SerialTimeoutException:
            print("Write operation timed out.")
        print(bytes('AE', 'UTF-8'))
    time.sleep(T)
def buttonCommand_updateTargetHeight(): #Reads the txt entry and sends to serial message arduino to update target height
    ser.flushInput()
    ser.flushOutput()

    global TargetHeight
    TargetHeight = TargetHeightEntry.get()
    try:
        ser.write(bytes('V'+str(float(TargetHeight))+'E', 'UTF-8'))
    except serial.SerialTimeoutException:
        print("Write operation timed out.")
    print(bytes('V'+str(float(TargetHeight))+'E', 'UTF-8'))
    time.sleep(T)

def buttonCommand_moveUp():  # manual control for moving up
    ser.flushInput()
    ser.flushOutput()

    ser.write(bytes('UE', 'UTF-8'))  # up Signal
    print(bytes('UE', 'UTF-8'))
    time.sleep(T)

def buttonCommand_moveDown():  # manual control for moving down
    ser.flushInput()
    ser.flushOutput()

    ser.write(bytes('DE', 'UTF-8'))  # down Signal
    print(bytes('DE', 'UTF-8'))

def buttonCommand_FeedWireForward():  # manual control for feeding the wire forward
    ser.flushInput()
    ser.flushOutput()

    time.sleep(T)
    ser.write(bytes('FE', 'UTF-8'))   # wire forward signal
    print(bytes('FE', 'UTF-8'))
    time.sleep(T)
def buttonCommand_FeedWireBackward():  #manual control for feeding the wire backward
    ser.flushInput()
    ser.flushOutput()

    ser.write(bytes('KE', 'UTF-8'))   # wire backward signal
    print(bytes('KE', 'UTF-8'))
    time.sleep(T)
def buttonCommand_STOP(): # manual control for stopping wire feed
    ser.flushInput()
    ser.flushOutput()

    ser.write(bytes('JE','UTF-8')) # wire stop signal
    print(bytes('JE','UTF-8'))
    time.sleep(T)
def buttonCommand_updateTargetSpeed(): #Reads the txt entry and sends to serial message arduino to update target speed
    ser.flushInput()
    ser.flushOutput()

    global TargetSpeed
    TargetSpeed = TargetSpeedEntry.get()
    TargetSpeed = float(TargetSpeed)
    ser.write(bytes('S'+str(int(TargetSpeed))+'E', 'UTF-8'))
    print(bytes('S'+str(int(TargetSpeed))+'E', 'UTF-8'))
    time.sleep(T)
def buttonCommand_updateAutoOnOff(): # Toggles between manual and automated control of wire feed speed
    ser.flushInput()
    ser.flushOutput()

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

    time.sleep(T)
def buttonCommand_RotateCW(): # manual control for rotating platform clockwise
    ser2.flushInput()
    ser2.flushOutput()

    global RotateDirectionState
    RotateDirectionState = 1
    RotateDirection.set("Clockwise")
    ser2.write(bytes('ZE', 'UTF-8'))   # Rotate platform clockwise signal
    print(bytes('ZE', 'UTF-8'))
    time.sleep(T)
def buttonCommand_RotateCCW(): # manual control for rotating platform counterclockwise
    ser2.flushInput()
    ser2.flushOutput()

    global RotateDirectionState
    RotateDirectionState = 0
    RotateDirection.set("Counter-Clockwise")
    ser2.write(bytes('XE', 'UTF-8'))   # Rotate platform clockwise signal
    print(bytes('XE', 'UTF-8'))
    time.sleep(T)
def buttonCommand_Rotate(): # manual control for rotating platform clockwise
    ser2.flushInput()
    ser2.flushOutput()

    global TargetAngle
    TargetAngle = TargetAngleEntry.get()

    ser2.write(bytes('C'+str(int(TargetAngle))+'E', 'UTF-8'))
    print(bytes('C'+str(int(TargetAngle))+'E', 'UTF-8'))
    time.sleep(T)
def buttonCommand_updateAutoRPOnOff(): # Toggles between manual and automated control of rotating platform speed
    ser2.flushInput()
    ser2.flushOutput()

    global Automated_Controls_stateRP

    # if we are in automated controls --> set to manual--> else set controls to automatic
    if Automated_Controls_stateRP == 1:
        Automated_Controls_stateRP = 0
        AutoRPLabel.set("Automated Rotating Platform Controls: Off ")
        ser2.write(bytes('OE', 'UTF-8'))  # Manual Signal
        print(bytes('OE', 'UTF-8'))
    else:
        Automated_Controls_stateRP = 1
        AutoRPLabel.set("Automated Rotating Platform Controls: On ")
        ser2.write(bytes('PE', 'UTF-8'))  # Automated Signal
        print(bytes('PE', 'UTF-8'))
    time.sleep(T)
def buttonCommand_updateTargetAngleSpeed(): #Reads the txt entry and sends to serial message arduino to update target speed
    ser.flushInput()
    ser.flushOutput()
    ser2.flushInput()
    ser2.flushOutput()

    global TargetAngleSpeed
    TargetAngleSpeed = TargetAngleSpeedEntry.get()

    ser2.write(bytes('I'+str(int(TargetAngleSpeed))+'E', 'UTF-8'))
    print(bytes('I'+str(int(TargetAngleSpeed))+'E', 'UTF-8'))

    ser.write(bytes('I'+str(int(TargetAngleSpeed))+'E', 'UTF-8'))
    print(bytes('I'+str(int(TargetAngleSpeed))+'E', 'UTF-8'))
    time.sleep(T)
def buttonCommand_StartRotation():
    ser.flushInput()
    ser.flushOutput()
    ser2.flushInput()
    ser2.flushOutput()

    global DeltaH
    DeltaH = DecreaseHeightEntry.get()

    ser.write(bytes('Q'+str(int(DeltaH))+'E', 'UTF-8'))
    print(bytes('Q'+str(int(DeltaH))+'E', 'UTF-8'))

    ser2.write(bytes('QE', 'UTF-8'))
    print(bytes('QE', 'UTF-8'))
    time.sleep(T)
def buttonCommand_UpdateNOT():
    global ser
    global ser2
    global NumberOfTurns

    ser.flushInput()
    ser.flushOutput()
    ser2.flushInput()
    ser2.flushOutput()

    NumberOfTurns = NumberOfTurnsEntry.get()

    ser.write(bytes('Y'+str(int(NumberOfTurns))+'E', 'UTF-8'))
    print(bytes('Y'+str(int(NumberOfTurns))+'E', 'UTF-8'))

    ser2.write(bytes('Y'+str(int(NumberOfTurns))+'E', 'UTF-8'))
    print(bytes('Y'+str(int(NumberOfTurns))+'E', 'UTF-8'))
    time.sleep(T)
def buttonCommand_STOPEVERYTHING():
    ser.flushInput()
    ser.flushOutput()
    ser2.flushInput()
    ser2.flushOutput()

    ser.write(bytes('WE', 'UTF-8'))  # STOP Signal
    print(bytes('WE', 'UTF-8'))

    ser2.write(bytes('WE', 'UTF-8'))  # STOP Signal
    print(bytes('WE', 'UTF-8'))
    time.sleep(T)
def buttonCommand_UpdateSerialPorts():

    global ser
    global ser2

    SerPort1 = SerPort1Entry.get()
    SerPort2 = SerPort2Entry.get()

    SerPort1Label21.set(SerPort1)
    SerPort2Label21.set(SerPort2)

    # Set up Serial Communication with Arduino------------------------------------------------------------------------------
    ser = serial.Serial(SerPort1, 115200, timeout=1, writeTimeout=2)  # create Serial Object
    ser2 = serial.Serial(SerPort2, 9600, timeout=1, writeTimeout=2)  # Serial object for Nano

    ser.flushInput()
    ser.flushOutput()
    ser2.flushInput()
    ser2.flushOutput()

    time.sleep(T)

# declare the automated controls to default at 0 (manual controls)
Automated_Controls_state = 0
Automated_Controls_stateWF = 0
Automated_Controls_stateRP = 0

# Actuator default selection is both
ActuatorSelection_state = 2

# Platform Rotation Direction default is counterclockwise
RotateDirectionState = 0

# Serial Ports
SerPort1 = 'com3'
SerPort2 = 'com4'

time.sleep(3)  # delay 3 seconds to allow serial com to get established


# Build GUI-------------------------------------------------------------------------------------------------------------
tkTop = tkinter.Tk()  # Create GUI Box
tkTop.geometry('1920x1080')  # size of GUI
tkTop.title("Test Stand Controller")  # title in top left of window

Title = tkinter.Label(tkTop,text='Test Stand Controls', font=("Courier", 14, 'bold')).grid(row=0, column=0, rowspan=1, columnspan=2)  # Title on top middle of screen


# Fill in the Manual controls Side--------------------------------------------------------------------------------------
ManualFrame = tkinter.Frame(master=tkTop, height=200, width=900) # create frame for the manual controls
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
button_left_state.pack(side='top', ipadx=10, padx=10, pady=10)

button_right_state = tkinter.Button(LeftButtonsFrame,

                                  text="Right",

                                  command=buttonCommand_setActuatorSelectionRight,
                                    height=4,
                                    fg="black",
                                    width=8,
                                    bd=5,
                                    activebackground='green'
                                    )
button_right_state.pack(side='top', ipadx=10, padx=10, pady=10)

button_both_state = tkinter.Button(LeftButtonsFrame,
                                   text="Both",
                                   command=buttonCommand_setActuatorSelectionBoth,
                                   height=4,
                                   fg="black",
                                   width=8,
                                   bd=5,
                                   activebackground='green'
                                   )
button_both_state.pack(side='top', ipadx=10, padx=10, pady=10)

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
button_up_state.pack(side='top', ipadx=10, padx=10, pady=10)

button_down_state = tkinter.Button(RightButtonsFrame,
                                   text="Down",
                                   command=buttonCommand_moveDown,
                                   height=4,
                                   fg="black",
                                   width=8,
                                   bd=5,
                                   activebackground='green'
                                   )
button_down_state.pack(side='top', ipadx=10, padx=10, pady=10)

LeftButtonsFrame.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)
RightButtonsFrame.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)

# Fill in the Automated controls Side----------------------------------------------------------------------------------------------------------------------------------------
AutoFrame = tkinter.Frame(master=tkTop, height=200, width=900, bg="gray")
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
button_Automated_on_off.pack(side='top', ipadx=0, padx=0, pady=10)

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
button_UpdateTarget.pack(side='left', ipadx=0, padx=20, pady=10)


AutoFrame.grid(row = 1, column = 1, stick='N')

# Fill in manual wire feed frame
ManualFrameWF = tkinter.Frame(master=tkTop, height=200, width=900)
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
#button_AutoWF_OnOff.grid(row=1, column=0, columnspan=3, padx=10)

varLabel1 = tkinter.IntVar()
#AutoWFLabel = tkinter.Label(master=AutoFrameWF, textvariable=varLabel1, bg="gray").grid(row=2, column=1)
varLabel1.set("Automated Wire Feed Controls: Off")

AutoFrameWF.grid(row=2,column=1, pady=20, sticky='N')


TargetSpeedLabel = tkinter.Label(master=AutoFrameWF, text='Enter Target Speed [in/s]: ', font=("Courier", 12), bg="gray").grid(row=2,column=0, padx=10)  # Manual wire feed speed label
TargetSpeedEntry = tkinter.Entry(AutoFrameWF)
TargetSpeedEntry.grid(row=2, column=1, padx=10)

button_UpdateTarget = tkinter.Button(AutoFrameWF,
                                     text="Update Target",
                                     command=buttonCommand_updateTargetSpeed,
                                     height=2,
                                     fg="black",
                                     width=15,
                                     bd=5,
                                     activebackground='green'
                                     )
button_UpdateTarget.grid(row=2, column=2, padx=10)

#Fill in rotating platform manual control
ManualFrameRP = tkinter.Frame(master=tkTop, height=200, width=900)
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

# Fill in Rotation plus h mm decrease frame
RotationFrame = tkinter.Frame(master=tkTop, height=200, width=900)
RotationLabel = tkinter.Label(master=RotationFrame,  text='Decrease h [mm] per 360 [deg] Rotation Function', font=("Courier", 12, 'bold')).grid(row=0, column = 0, columnspan=6)

NumberOfTurnsLabel = tkinter.Label(master=RotationFrame,  text='Number of rotations:', font=("Courier", 12)).grid(row=1, column = 0, columnspan=2, padx=10, pady=5)
NumberOfTurnsEntry = tkinter.Entry(RotationFrame)
NumberOfTurnsEntry.grid(row=1, column=2, columnspan=2, pady=5, padx=10)

button_UpdateNOT = tkinter.Button(master=RotationFrame,
                                  text="Update",
                                  command=buttonCommand_UpdateNOT,
                                  height=2,
                                  fg="black",
                                  width=15,
                                  bd=5,
                                  activebackground='green'
                                  )
button_UpdateNOT.grid(row=1, column=5, columnspan=2, pady=5, padx=10)

DecreaseHeightLabel = tkinter.Label(master=RotationFrame, text='Delta h [mm]:', font=("Courier", 12)).grid(row=2, column=0, columnspan=3)
DecreaseHeightEntry = tkinter.Entry(RotationFrame)
DecreaseHeightEntry.grid(row=2, column=3, columnspan=3, pady=5, padx=20)

button_StartFunction = tkinter.Button(master=RotationFrame,
                                      text='START',
                                      command=buttonCommand_StartRotation,
                                      height=2,
                                      fg='black',
                                      width=15,
                                      bd=5,
                                      activebackground='green')
button_StartFunction.grid(row=3, column=0, columnspan=6, pady=5)

RotationFrame.grid(row=4, column=0)

button_STOPEVERYTHING = tkinter.Button(master=tkTop,
                                       text='STOP ALL OPERATIONS',
                                       command=buttonCommand_STOPEVERYTHING,
                                       height=10,
                                       fg='white',
                                       width=50,
                                       background='red',
                                       bd=5)
button_STOPEVERYTHING.grid(row=4,column=1)

# Serial Port selection frame
SerPortSelFrame = tkinter.Frame(master=tkTop, height=200, width=900)
SerPortLabel = tkinter.Label(master = SerPortSelFrame, text='Serial Port Selection',font=("Courier", 12, 'bold')).grid(row=0, column=0, columnspan=3)

SerPort1Label1 = tkinter.Label(master=SerPortSelFrame, text='Serial Port 1 (Arduino Mega com port):',font=("Courier", 12, 'bold')).grid(row=1, column=0, padx=5, pady=10)
SerPort1Entry = tkinter.Entry(SerPortSelFrame)
SerPort1Entry.grid(row=1,column=1, padx=5, pady=10)

SerPort1Label21 = tkinter.IntVar()
SerPort1Label2 = tkinter.Label(master=SerPortSelFrame, textvariable=SerPort1Label21,font=("Courier", 12, 'bold')).grid(row=1, column=2, padx=5, pady=10)
SerPort1Label21.set(SerPort1)

SerPort2Label1 = tkinter.Label(master=SerPortSelFrame, text='Serial Port 2 (Arduino Nano com port):',font=("Courier", 12, 'bold')).grid(row=2, column=0, padx=5, pady=10)
SerPort2Entry = tkinter.Entry(SerPortSelFrame)
SerPort2Entry.grid(row=2,column=1, padx=5, pady=10)

SerPort2Label21 = tkinter.IntVar()
SerPort2Label2 = tkinter.Label(master=SerPortSelFrame, textvariable=SerPort2Label21,font=("Courier", 12, 'bold')).grid(row=2, column=2, padx=5, pady=10)
SerPort2Label21.set(SerPort2)

button_SerPortUpdate = tkinter.Button(master=SerPortSelFrame,
                                      text='Update',
                                      command=buttonCommand_UpdateSerialPorts,
                                      height=2,
                                      fg='white',
                                      width=20,
                                      background='gray',
                                      bd=5)

button_SerPortUpdate.grid(row=3, column=1, pady=10)

SerPortSelFrame.grid(row=1, column=2)



tkinter.mainloop() # run loop watching for gui interactions

