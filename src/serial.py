import serial
from serial import Serial
# from serial import *
import serial.tools.list_ports # need this

from src.gui_main import GUI

# Determine Arduino serial port address
def serial_connect():
    #try:
    ports = serial.tools.list_ports.comports()
    try:
        dev = ports[0].device
    except:
        #dev = '/dev/ttyACM0' # only works on pi
        dev = dev_guess # based on operating system
    if dev_manualOverride == True:
        dev = dev_manual # manual override
    try:
        ser = serial.Serial(dev, 115200, timeout=4,writeTimeout = 2,) # 1 second timeout
        #print(type(ser))
        print("dev = "+dev)
        ser.reset_input_buffer()  
        #ser.isOpen()
        #GUI.ignoreserial = False
        return ser # this is the only spot it should be called ser, not RecordForce.ser
    
    except:
        GUI.ignoreserial = True
        error = 'serial connection never established'
        eCode = 'e1' # eCode = e1
        GUI.errors.append(error) # append error label
        GUI.errorCodes.append(eCode) # append error code
        #popup('serial connection')
        print("eCode = "+eCode)

# if serial disconnect (unplugged) reconnect - NOTE: doesn't properly work currently. 
def serial_reconnect():
    print("serial_reconnect()")
    try:
    #if GUI.ignoreserial == False:
        GUI.ignoreserial = False
        try:
            RecordForce.ser.close()
            GUI.ignoreserial = False
        except:
            GUI.ignoreserial = True
        RecordForce.ser = serial_connect()
        
    except:
    #else:
        GUI.ignoreserial = True
        print("\nYou hit the 'serial_reconnect' dropdown menu item while GUI.ignoreserial == True.\nSerial cannot be reconnected because\neither an arduino is not connected to your computer\nor the arduino is not sought by StemBerry.")
        RecordForce.message_connectArduino()