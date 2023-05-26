import serial
import time
import tkinter


# Define what happens when you push the  different buttons------------------------------------------------------------------------------------
def set_ActuatorSelection_left_state():
    global ActuatorSelection_state
    ActuatorSelection_state = 0
    ActuatorSelectionLabel.set("Left")
    ser.write(bytes('L', 'UTF-8'))  # left Signal


Automated_Controls_state = 0


def set_ActuatorSelection_right_state():
    global ActuatorSelection_state
    ActuatorSelection_state = 1
    ActuatorSelectionLabel.set("Right")
    ser.write(bytes('R', 'UTF-8'))  # right Signal


def set_ActuatorSelection_both_state():
    global ActuatorSelection_state
    ActuatorSelection_state = 2
    ActuatorSelectionLabel.set("Both")
    ser.write(bytes('B', 'UTF-8'))  # both Signal


def set_automated_controls_state():
    global Automated_Controls_state
    if Automated_Controls_state == 1:
        Automated_Controls_state = 0
        varLabel.set("Automated Controls: Off ")
        ser.write(bytes('M', 'UTF-8')) #Manual Signal
    else:
        Automated_Controls_state = 1
        varLabel.set("Automated Controls: On ")
        ser.write(bytes('A', 'UTF-8')) #Automated Signal

def set_update_target_state():
    ser.write(bytes('V', 'UTF-8'))  # Update Signal


def set_ButtonUp_state():
    ser.write(bytes('U', 'UTF-8')) #up Signal


def set_ButtonDown_state():
    ser.write(bytes('D', 'UTF-8')) #down Signal

#Set up Serial Communication with Arduino---------------------------------------------------------------------------------------------------------------------------------
ser = serial.Serial('com5', 9600) #create Serial Object

time.sleep(3) #delay 3 seconds to allow serial com to get established
ser.write(bytes('L', 'UTF-8')) # send "L" to arduino to reset it when first connecting
print("Reset Arduino")


# Build GUI------------------------------------------------------------------------------------------------------------------------------------------------------------
tkTop = tkinter.Tk()  # Create GUI Box
tkTop.geometry('1200x800')  # size of GUI
tkTop.title("Test Stand Controller")  # title in top left of window

Title = tkinter.Label(text='Test Stand Controls', font=("Courier", 14, 'bold')).pack()  # Title on top middle of screen

# Fill in the Manual controls Side----------------------------------------------------------------------------------------------------------------------------------------
ManualFrame = tkinter.Frame(master=tkTop, width=600) # create frame for the manual controls
ManualLable = tkinter.Label(master=ManualFrame, text='Manual Controls',
                            font=("Courier", 12, 'bold')).pack()  # manual controls lable
ManualFrame.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)

LeftButtonsFrame = tkinter.Frame(master=ManualFrame, width=100)
LeftButtonsLable = tkinter.Label(master=LeftButtonsFrame, text='Actuator Selection',
                                 font=("Courier", 12, 'bold')).pack()

RightButtonsFrame = tkinter.Frame(master=ManualFrame, width=100)
RightButtonsLable = tkinter.Label(master=RightButtonsFrame, text='Up/Down Controls',
                                  font=("Courier", 12, 'bold')).pack()

button_left_state = tkinter.Button(LeftButtonsFrame,
                                   text="Left",
                                   command=set_ActuatorSelection_left_state,
                                   height=4,
                                   fg="black",
                                   width=8,
                                   bd=5,
                                   activebackground='green'
                                   )
button_left_state.pack(side='top', ipadx=10, padx=10, pady=40)

button_right_state = tkinter.Button(LeftButtonsFrame,
                                    text="Right",
                                    command=set_ActuatorSelection_right_state,
                                    height=4,
                                    fg="black",
                                    width=8,
                                    bd=5,
                                    activebackground='green'
                                    )
button_right_state.pack(side='top', ipadx=10, padx=10, pady=40)

button_both_state = tkinter.Button(LeftButtonsFrame,
                                   text="Both",
                                   command=set_ActuatorSelection_both_state,
                                   height=4,
                                   fg="black",
                                   width=8,
                                   bd=5,
                                   activebackground='green'
                                   )
button_both_state.pack(side='top', ipadx=10, padx=10, pady=40)

ActuatorSelectionLabel = tkinter.IntVar()
ActuatorSelection = tkinter.Label(master=LeftButtonsFrame, textvariable=ActuatorSelectionLabel)
ActuatorSelection.pack()

button_up_state = tkinter.Button(RightButtonsFrame,
                                 text="Up",
                                 command=set_ButtonUp_state,
                                 height=4,
                                 fg="black",
                                 width=8,
                                 bd=5,
                                 activebackground='green'
                                 )
button_up_state.pack(side='top', ipadx=10, padx=10, pady=40)

button_down_state = tkinter.Button(RightButtonsFrame,
                                   text="Down",
                                   command=set_ButtonDown_state,
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
AutoFrame = tkinter.Frame(master=tkTop, width=600, bg="gray")
AutoLable = tkinter.Label(master=AutoFrame, text='Automated Controls', font=("Courier", 12, 'bold'), bg="gray").pack(
    side='top', ipadx=10, padx=10, pady=40)  # Automated controls lable

button_Automated_on_off = tkinter.Button(AutoFrame,
                                         text="Turn Automated Controls on/off",
                                         command=set_automated_controls_state,
                                         height=4,
                                         fg="black",
                                         width=25,
                                         bd=5,
                                         activebackground='green'
                                         )
button_Automated_on_off.pack(side='top', ipadx=0, padx=0, pady=0)

varLabel = tkinter.IntVar()
tkLabel = tkinter.Label(master=AutoFrame, textvariable=varLabel, bg="gray")
tkLabel.pack()

TargetHeightLable = tkinter.Label(master=AutoFrame, text='Enter Target Height: ', font=("Courier", 12), bg="gray").pack(
    side='left', ipadx=10, padx=10, pady=40)  # Automated controls lable
TargetHeightEntry = tkinter.Entry(AutoFrame)
TargetHeightEntry.pack(side='left', ipadx=0, padx=0, pady=0)

button_UpdateTarget = tkinter.Button(AutoFrame,
                                         text="Update Target",
                                         command=set_update_target_state,
                                         height=2,
                                         fg="black",
                                         width=15,
                                         bd=5,
                                         activebackground='green'
                                         )
button_UpdateTarget.pack(side='left', ipadx=0, padx=20, pady=20)


AutoFrame.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True)

TargetHeight = TargetHeightEntry.get()



tkinter.mainloop() # run loop watching for gui interactions

