import tkinter as tk
import time

from gui_main import GUI
from guiframe_record_force import RecordForce
def datafeed():
    #frame = tk.Frame.RecordForce
    frame = RecordForce.container
    RecordForce.datafeed_frame
    print("frame = ",frame)
    if visualizeDatastream == True:# data displayed in scrollbars (default)
        # Displays incoming data
        # scroll = tk.Scrollbar(RecordForce.datafeed_frame)
        scroll = tk.Scrollbar(frame)# what is this? TK!
        print("scroll = ",scroll)
        #scroll = tk.Scrollbar(self)# what is this? TK!
        ''
        RecordForce.time_label = tk.Label(RecordForce.datafeed_frame, text = "Time (sec)",font = ("arial", 14, "bold"), fg = "dodgerblue3", bg = "ghost white")
        RecordForce.Timelist = tk.Listbox(RecordForce.datafeed_frame, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 1, font = ("arial", 14, "bold"), fg = "dodgerblue3")
        RecordForce.dis_label = tk.Label(RecordForce.datafeed_frame, text = "Distance (cm)",font = ("arial", 14, "bold"), fg = "dodgerblue3", bg = "ghost white")
        RecordForce.Dislist = tk.Listbox(RecordForce.datafeed_frame, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 1, font = ("arial", 14, "bold"), fg = "dodgerblue3")
        RecordForce.force_label = tk.Label(RecordForce.datafeed_frame, text = "Force (N)",font = ("arial", 14, "bold"), fg = "dodgerblue3", bg = "ghost white")
        RecordForce.Forcelist = tk.Listbox(RecordForce.datafeed_frame, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 5, font = ("arial", 14, "bold"), fg = "dodgerblue3")
        RecordForce.time_label.place(x = 180, y = 110)

        RecordForce.Timelist.place(x = 180, y = 140)
        RecordForce.dis_label.place(x = 280, y = 110)
        RecordForce.Dislist.place(x = 280, y = 140)
        RecordForce.force_label.place(x = 420, y = 110)
        RecordForce.Forcelist.place(x = 420, y = 140)

    else:# user decided for no data display
        try:#clear scrollbars if they were there
            RecordForce.Dislist.place_forget()
            RecordForce.Forcelist.place_forget()
            RecordForce.Timelist.place_forget()
            RecordForce.dis_label.place_forget()
            RecordForce.force_label.place_forget()
            RecordForce.time_label.place_forget()
        except:# no scrollbars
            pass
        
def passData():

    '''Scrollbars Options'''
    # if scrollbars option = on:
    if visualizeDatastream == True:
        try: # puts data on GUI display by default (user can turn off)
            
            RecordForce.Dislist.insert(END, str(GUI.distanceTraveled[i]))# inserts at end of listbox to actually display
            RecordForce.Dislist.see(END)# makes sure listbox is at end so it displays live data
            RecordForce.Forcelist.insert(END, str('%.2f' % GUI.forcePushed[i]))
            RecordForce.Forcelist.see(END)
            RecordForce.Timelist.insert(END, str('%.2f' % GUI.timeElapsed[i]))
            RecordForce.Timelist.see(END)

            #scrollbars options = off
            '''
        except:
            pass
        '''
        except:
            GUI.errors.append('data append') # label 
            eCode = 'e4'
            GUI.errorCodes.append(eCode)
            print("eCode = "+eCode) # eCode = e4
                

# * # DATA COLLECTION FUNCTION - Acquires live data from Arduino # * #
def collectData():
    hang=0
    j=0
    nothingToRead=0 # controls timeout
    blankline = "b'\n"
    lasttimetick = -1
    while RecordForce.hasStarted==True and RecordForce.hasSentStop==False:
        time.sleep(0.02)
        bytecount = RecordForce.ser.in_waiting
        #print("RecordForce.ser.in_waiting = ",bytecount)
        if bytecount > 5 and RecordForce.hasSentStop==False: # this does happen
            #print("datachunk...") # stopping after this
            
            try:
                time.sleep(0.2) # no luck
                ser_bytes = RecordForce.ser.read(bytecount)        
                if blankline in str(ser_bytes):
                    print("blankline")
                    continue
            except:
                print("Failed: ser_bytes = RecordForce.ser.readline()")
                continue
            hang = 0
            nothingToRead=0
            #print("ser_bytes = ",ser_bytes)
            line = ser_bytes.decode('utf-8').rstrip()
            datapacket = line.splitlines()
            # parse datapacket
            for i in datapacket:
                split = i.split("|")
                if RecordForce.hasSentStop == False:
                    try:
                        #print("split = ",split, float(split[0]),float(split[1]),float(split[2]))
                        if round(j/10,0) == float(j/10):
                            print("j, split = ",j, ",",split)
                        distance = round(float(split[0]),3)
                        force = round(float(split[1]),3)
                        timetick = round(float(split[2]),3)/1000 # convert milliseconds to seconds
                        if timetick > lasttimetick:
                            GUI.timeElapsed.append(timetick)# list of GUI.distanceTraveled time
                        else:
                            timetick = lasttimetick # good enough.
                            GUI.timeElapsed.append(timetick)# list of GUI.distanceTraveled time
                        GUI.distanceTraveled.append(distance)# list of inches traveled @ does this happen with the whole list, or one element at a time?
                        GUI.forcePushed.append(force)# list of force traveled
                        lasttimetick = timetick
                    except:
                        print("missed a line, list index out of range.")
                        pass
                
                j+=1
            if line =="Stopped!": 
                RecordForce.sendStop()
                
        # the purpose of this elif is to allow the while loop to iterate if there's nothing to read.
        # But also, it has primarily been entered if the serial connection has already timed out
        elif bytecount < 6 and bytecount > 0 : 
            ser_bytes = RecordForce.ser.read(bytecount)
            #print("ser_bytes = ",ser_bytes)
            nothingToRead +=1
            if nothingToRead>5: # if the while loop goes through five iterations, without seeing anything worth recording, give up.
                RecordForce.sendStop()
                print("Hung up.")
                src.serial.serial_reconnect()
                GUI.show_frame(InitialInputs)
        else:
            hang +=1
            print("go back to top of while loop")
            if hang>10: # if the while loop goes through ten iterations of radio silence, give up. The serial connection probably timed out. search 'timeout = '
                RecordForce.sendStop()
                print("Hung up, timeout.")
                src.serial.serial_reconnect()
                GUI.show_frame(InitialInputs)

def runDataCollect():
    try:        
        RecordForce.sendStart()
    except:
        print("run fail")
        GUI.errors.append('serial com. (start data)') # label 
        eCode = 'e2' # eCode = e2
        GUI.errorCodes.append(eCode)
        print("eCode = "+eCode)
        popup('start data collect')

    RecordForce.thread2_collectData = threading.Thread(target = collectData)
    RecordForce.thread2_collectData.start()