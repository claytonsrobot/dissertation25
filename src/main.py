#!/usr/bin/python3
#do not erase (needed to be executable for autostart)

'''
StemBerry V.105
Last updated: 10/16/2022
Dev: Clayton Bennett
OG dev: Austin Bebee
Description: SOCEM GUI. Connect RPi to Arduino, collect raw data. Save text inputs.

Contents (in order):s
- Library imports
- Global Variables
- Global Functions
- GUI Class
    - Home / Initial input screen
    - Data collection (Record Force) screen
        - Runs data collection function
        - Stores data & saves data
        - Plots F v D graph
    - Load cell calibration screen
    - Error report screen
- Excute GUI command

V15
    - Change to 9 cell and 3 range count inputs
V19
    - Rip out defunct calculations
    - Clean up code, specifically by organizing statements of place for tkinter items
V37
    - Dial in functionality with pretty new GUI.
    - barbottom (not barmiddle) set to 70%-90% of stem height
V42
    - Develop top level methods
V50
    - Functional save state, save files, naming convention edge cases, and crisp appearance

V54
    - Generate CSV's, suppress XLSX's
V56
    - Retain 9-cell variables, for EI assessment upon saving counts, without reopening CSV files
V67
    - So many things.
v77
    - Serial collection functial, drinking from a waterhose, high hz
    - Tare button message.
    - PeakClick popup window.

V84
    - The way peak clicks are handled and saved was moved to the inside of the choose peaks code, becuase plt.show() won't give up.
    - Shut down plt.show after CSV file is saved.
V88
    - GUI.filename_force updated on page change to either record force frame or final inputs page
    - nameBlackBox updated to remove excess hyphen when direction ==''
    - XLSX compilation file functional, currently set to seek force and EI files
    - EI calcualtion works - only needs 1 file for all four nine-cell-scheme tests. 
    - This thing is getting heavy, 2844 lines.
V90
    - Identify OS and choose filepath accordingly.

V92
    - Trigger peak selection for all tests, with the assessAllTests boolean.
    - Noticed that encoderWorked_override is poorly implemented. No reason to fix now, but, should be alterable as opposed to needing manual suppression through commenting
    - GUI.currentdirection.get() set to "" on_frame_show RecordForce.
V94
    - Changed mass measurement from kg to gramsa
    - Fixed all time units to be (sec), not (s) or (seconds), and certainly not (ms)
V96
    - EI is now calculated in lbs*in^2, then converted to metric N*cm^2. Input is metric, conversion happens inside, processing is SAE, then conversion to metric before output to metric.
V97
    - EI calculation betaV edge cases dealt with: if nan, set betaV to 0.
v99
    - Change if statement in serConnect to retain dev_manual
Fix:
- Change compilation to access CVSV data rather than state data. This is to protect against data loss if the computer dies.
- Or, load state. Load state would be sick.
- Add more variables to state save backup text file.
- Remove auto graph button, or at least uncheck it: use it to refer to auto clicker
- Finish autoclicker by setting plt.show() into an inset tkinter gui popup, and then mainoop.
     Use: FigureCanvasTkAgg,NavigationToolbar2Tk,plt,Cursor.
- dev port is currently defined manually, given dev_manualOverride
- move header variable inputs
- make directory inputtable using dropdown menu item and textbox
- upgrade tkinter items to CustomTkinter
- PRIORITY: CREATE BASE NAME FROM VARIABLE AND PLOT: GUI.filename_force.get() is getting dangerous.
     
Notes:
- exec() is your friend. Use is to run multiple lines of code which you can copy and paste into a shell, using triple '  commenting
- save as separate CSV files, then as one combined XLSX file with multiple pages
'''

'''Local libraries'''
#import src.serial
from src.gui_main import GUI
from directories import Directories

''' Libraries '''
import tkinter as tk
#from multiprocessing import Process

import matplotlib
from matplotlib import style
matplotlib.use("TkAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.figure import Figure
#import matplotlib.pyplot as plt

import os
import platform

#import peakutils
#from PeakUtils.Plot import plot as pplot
import math
#import struct # what is this?
#import datetime
from datetime import date
import time
# import xlsxwriter # csv now, xlsxwriter not used

''' Global Variables --> Config'''

operator = 'Clayton Bennett'
location = 'EP425' # 'Kambitsch Farm'
coordinates = '46.592516,-116.946268'
script = os.path.basename(__file__)
directory = os.path.dirname(__file__)

today = date.today()
datestring = today.strftime("%b-%d-%Y")
ignoreserial = False # True 
#ignoreserial = True # delete this # if RecordForce.ser.isOpen() == False:
barlength = 76 # cm. this shouldn't ever change, unless the bar is replaced. i.e. the width of a side hit cell.
#dev_manual = 'COM7' # manual override
dev_manual = '/dev/ttyACM0' # manual override
#dev_manual = 'COM7' # manual override
dev_manualOverride = True
useInitialPlot_PeackClick = False
distance_referenced_PeakClick = False
barradius = .8 # 1 cm = 0.32 inches
#barradius = 1 # 1 cm = 0.32 inches
default_stemheight = 10.0 # cm
initial_barbottomOverStemheight_coeff = 0.8
convert_KgToLbs = 2.20462262 #kg to lbs
convert_KgToN = 1/9.81 #kg to N # CHECK FOR ACCURACY CB 8/9/2022
convert_NToLbs = 4.44822
#calibrationFactor = 199750 # 23.4 N > 5 lbs; 5 lbs = 22.2411
calibrationFactor = 204200 # 22.24 N = 5 lbs

inchonvert = (((math.pi*(0.764))*31.4136)/359) # converts displacement to inches, wheel diameter = 31.4136
visualizeDatastream = False #True #set to live graph for data display
sleepSend = 0.5
encoderWorked_override = False # False means encoder will be trated as not working. this is poor code and should be improved.
assessAllTests = True
refreshAllAuto = False
autopopulatestemcount = True
defaultstemcount = 33
importFileDataTF = True
#visualizeDatastream = True
# visualizeDatastream ( search: "def datafeed(" ) is broken right now. Refer to earlier versions (pre v65)for reference of how Bebee left it.
vis = 's' # legacy
vis = 'nope' # 

        
''' matplotlib Graph Settings '''
'''
style.use("ggplot")
f = Figure(figsize=(4.85,3.9), dpi=75)
a = f.add_subplot(111)
a.set_ylim(0, 25)
'''



#Bebee legacy
# * # DATA COLLECTION FUNCTION - Acquires live data from Arduino # * #
def run(self, ser):
    try:        
        started = 's'
        ser.write(started.encode()) #sends 's' to arduino, telling it to start
        print('send s to arduino, legacy')
    except:
        errors.append('serial com. (start data)') # label 
        eCode = 'e2'
        errorCodes.append(eCode)
        popup('start data collect')
        
    ser.flush()
    time.sleep(.1)
    #Don't need this:
    #try:
    #ser_bytes = ser.readline()
    #decoded_bytes.insert(0,(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")))#translates bytes to string, inserts incoming data in decoded_bytes list
    #except:
     #  popup("communication")

    #DATA COLLECTION CODE

    if vis == 's':# data displayed in scrollbars (default)
        # Displays incoming data 
        scroll = tk.Scrollbar(self)

        RecordForce.timeLabel = tk.Label(self, text = "s",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        RecordForce.timeLabel.place(x = 274, y = 70)
        RecordForce.Timelist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 1, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        RecordForce.Timelist.place(x = 240, y = 100)

        RecordForce.disLabel = tk.Label(self, text = "in.",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        RecordForce.disLabel.place(x = 357, y = 70)
        RecordForce.Dislist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 1, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        RecordForce.Dislist.place(x = 330, y = 100)

        RecordForce.forceLabel = tk.Label(self, text = "lbs.",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        RecordForce.forceLabel.place(x = 444, y = 70)
        RecordForce.Forcelist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 11, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        RecordForce.Forcelist.place(x = 420, y = 100)

    else:# user decided for no data display
        try:#clear scrollbars if they were there
            RecordForce.Dislist.place_forget()
            RecordForce.Forcelist.place_forget()
            RecordForce.Timelist.place_forget()
            RecordForce.disLabel.place_forget()
            RecordForce.forceLabel.place_forget()
            RecordForce.timeLabel.place_forget()
        except:# no scrollbars
            print("no scrollbars")
            pass
    
    i = 0
    print("i = 0")
    RecordForce.elapsed = []
    RecordForce.dis = []
    RecordForce.force = []
    string = list()

    #try:
    
    while RecordForce.collect == True: # GUI in frontend controls value of collect to start/stop loop            
        if ser.inWaiting() > 0: #checks to see if Serial is available 
        
            try: #make sure serial data can be read/is there
                ser_bytes = ser.readline()
            except:
                errors.append('serial read') # label 
                eCode = 'e3'
                errorCodes.append(eCode)
                popup("serial read")
    

            if i == 0:
                start = time.time() #stopwatch starts

            #DELETE?
            #decoded_bytes.insert(i,(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))) # acquires & decodes bytes (incoming Arduino data)
            #string.insert(i,str(decoded_bytes[i])) # inserts decoded bytes into string

            bytesDecoded = (ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            #print("bytesDecoded = ",bytesDecoded)
            string.insert(i,str(bytesDecoded)) # inserts decoded bytes into string
            #print(' run ser read ', string[i]) # useful debugging tool
            split = string[i].split("|") # splits data at | (1st = distance, 2nd = force)
            print("split = ",split)
            if len(split) >= 2 and split[0] != "" and split[1] != "": #makes sure data is in proper formatting before processing (else pair: A)
                inches = split[0]
                pounds = split[1]
                
                try:
                    RecordForce.elapsed.insert(i, time.time() - start)# list of elapsed time
                    RecordForce.dis.insert(i, float(inches))# list of inches traveled
                    RecordForce.force.insert(i, float(pounds))# list of force traveled

                except:
                    errors.append('data append') # label 
                    eCode = 'e4'
                    errorCodes.append(eCode)  
                 #   popup("Arduino data error")
                  #  print(string[i])

                '''Scrollbars Options'''
                '''
                # if scrollbars option = on:
                try: # puts data on GUI display by default (user can turn off)  
                    self.Dislist.insert(END, str(dis[i]))# inserts at end of listbox to actually display
                    self.Dislist.see(END)# makes sure listbox is at end so it displays live data
                    self.Forcelist.insert(END, str('%.2f' % force[i]))
                    self.Forcelist.see(END)
                    self.Timelist.insert(END, str('%.2f' % elapsed[i]))
                    self.Timelist.see(END)

                #scrollbars options = off        
                except:
                    pass
                
                i = i+1

                          '''
            else: # skips incoming data if not in right format (if pair: A
                errors.append('data skip (incorrect format)') # label 
                eCode = 'e5'
                errorCodes.append(eCode)
                '''
    except:
        if RecordForce.collect == True:
            errors.append('serial disconnect')
            eCode = 'e6'
            errorCodes.append(eCode)
        else:
            pass
            '''
        

        

if __name__ == "__main__":

    ''' Main '''
    print("StemBerry is loading.....")
    print("output: address = "+address)
    print("script = "+script)
    print("directory = "+Directories.get_core_dir())
    print("ignoreserial = "+str(ignoreserial))
    app = GUI() 
    app.run() # INITIATES GUI TO START
    app.title("StemBerry")
    app.geometry("800x480+0+0")
    app.aspect()
    #app.geometry("700x700+0+0")
    #fig = plt.figure()
    #app.iconbitmap(s'/home/pi/Desktop/SOCEM Code')
    #app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth()-3,app.winfo_screenheight()-3)) #full screen:
    app.mainloop()
    ''' End '''
