import csv
import datetime
from itertools import zip_longest
import threading
import time
import tkinter as tk

from src.gui_main import GUI

# Data collection page
class RecordForce(tk.Frame):
    def __init__(self, parent, controller):# automatically runs

        RecordForce.peaks_force = []
        RecordForce.peaks_distance = []
        RecordForce.peaks_time = []
        
        self.legends = []
        
        tk.Frame.__init__(self, parent)
        self.controller = controller # fuck?

        RecordForce.container = tk.Frame(self)
        
        ''' GUI design, non-frame '''
        pageButtons = repeatPageButtons.showButtons(self, parent, controller)
        title = tk.Label(self, text ="RECORD FORCE", font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white")
        filename_label = tk.Label(self, text = "Filename: ", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        filename_entryBox = tk.Entry(self, textvariable=GUI.filename_force, font = ("arial", 14, "bold"), width="32", bg="white", fg="gray1")
        self.checkAutoGraph = tk.IntVar() # on/off control of auto graph after stopping & saving data
        #self.checkAutoGraph.set(1)
        self.checkAutoGraph.set(0)
        graph_checkbox = tk.Checkbutton(self, text = "Auto graph", variable = self.checkAutoGraph, width = 13, height = 2, bg = 'ghost white')

        title.place(x=275,y=0)
        filename_label.place(x=0,y=80)
        filename_entryBox.place(x = 110, y = 80)
        graph_checkbox.place(x = 675 , y = 0)

        RecordForce.datafeed_frame = tk.LabelFrame(self, text='Data Feed',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        RecordForce.datafeed_frame.place(x = 20, y = 0)
        clear_button = tk.Button(RecordForce.datafeed_frame,text = "Clear",font = ("arial", 16, "bold"), height = 1, width = 6, fg = "ghost white", bg = "red4",command=lambda:RecordForce.clearDisplay())
        clear_button.grid(row=0, column=0)
        RecordForce.msgbox =  tk.LabelFrame(self, text='',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")

        RecordForce.msgbox.place(x = 5, y = 120)
        #forceSaved_label.place(x=5, y = 120)
        
        ''' Frame: Filename Quickset buttons'''
        nameset_frame = tk.LabelFrame(self, text='Filename\nQuickset',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        nameset_frame.place(x = 570, y = 40)
        #button that calculates optimized force bar height
        side1TestButton = tk.Button(nameset_frame, text = "Side 1", font = ("arial", 16, "bold"), height = 1, width = 6, fg = "ghost white", bg = "red4",command=lambda:self.nameSide1())
        side2TestButton = tk.Button(nameset_frame, text = "Side 2", font = ("arial", 16, "bold"), height = 1, width = 6, fg = "ghost white", bg = "red4",command=lambda:self.nameSide2())
        side3TestButton = tk.Button(nameset_frame, text = "Side 3", font = ("arial", 16, "bold"), height = 1, width = 6,fg = "ghost white", bg = "red4",command=lambda:self.nameSide3())
        forwardTestButton = tk.Button(nameset_frame, text = "Forward", font = ("arial", 16, "bold"), height = 1, width = 6, fg = "ghost white", bg = "red4",command=lambda:self.nameForward())
        increment_button = tk.Button(nameset_frame, text = "+1", font = ("arial", 16, "bold"), height = 1, width = 6, fg = "ghost white", bg = "purple4",command=lambda:self.incrementName_Force(GUI.filename_force.get()))
        
        side1TestButton.grid(row=0, column=0)
        side2TestButton.grid(row=1, column=0)
        side3TestButton.grid(row=2, column=0)
        forwardTestButton.grid(row=3, column=0)
        increment_button.grid(row=4, column=0)
        ''' end '''

        ''' Record Data Frame'''
        dataButtons_frame = tk.LabelFrame(self, text='',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        dataButtons_frame.place(x = 675, y = 40)
        #tells Arduino to start collecting data
        start_button = tk.Button(dataButtons_frame, text = "Start", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "dodgerblue3",command=lambda:RecordForce.startCollect())
        #tells Arduino to stop collecting data & saves the data (calls filename function)
        stop_button = tk.Button(dataButtons_frame, text = "Stop\n&\nSave", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "dodgerblue3",command=lambda:RecordForce.stopAndSave())
        #LEGACY, NOPE: stop_button = tk.Button(dataButtons_frame, text = "Stop\n&\nSave", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "dodgerblue3",command=lambda:RecordForce.stop())
        #tares/zeros load cell
        tare_button = tk.Button(dataButtons_frame, text = "Tare", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "dodgerblue3",command=lambda:RecordForce.tare())
        
        start_button.grid(row = 1, column = 0)
        stop_button.grid(row = 2, column = 0)
        tare_button.grid(row = 3, column = 0)
        ''' end frame'''
        
        self.bind("<<ShowFrame>>", self.on_show_frame_RecordForce)

    def nameForward(self):
        direction = "forward"
        filename_force = nameBlackBox(direction,GUI.filename_force.get())
        GUI.filename_force.set(filename_force)
        GUI.currentdirection.set(direction)
    def nameSide1(self):
        direction = "side1"
        filename_force = nameBlackBox(direction,GUI.filename_force.get())
        GUI.filename_force.set(filename_force)
        GUI.currentdirection.set(direction)
    def nameSide2(self):
        direction = "side2"
        filename_force = nameBlackBox(direction,GUI.filename_force.get())
        GUI.filename_force.set(filename_force)
        GUI.currentdirection.set(direction)
    def nameSide3(self):
        direction = "side3"
        filename_force = nameBlackBox(direction,GUI.filename_force.get())
        GUI.filename_force.set(filename_force)
        GUI.currentdirection.set(direction)
    def nameFresh(varietyname,plotname):
        direction = ""
        filename_force = nameBlackBox(direction,GUI.filename_force.get())
        GUI.filename_force.set(filename_force)
        set(direction)
    
    def clearDisplay():
        time.sleep(0.3)
        print('You hit the "Clear" button. Please develop clearDisplay().')
        GUI.refreshAll()
        '''
        try:
            RecordForce.Forcelist.delete(0, 'end')
            RecordForce.Dislist.delete(0, 'end')
            RecordForce.Timelist.delete(0, 'end')
            print('You hit the "Clear" button and deleted recorded data. This was not useful.')
        except:
            pass
            '''
        
    def incrementName_Force(self,filename):
        newName = incrementName(filename)
        GUI.filename_force.set(newName)
    
        
    # calls run function (for collecting Arduino data) to run in backend while GUI runs in frontend     
    def startCollect():
        now = datetime.datetime.now()
        unix_now = time.mktime(now.timetuple())
        time.sleep(0.4) # for visual effect
        #threading run function (simultaneously performs run function in backend)
        if GUI.ignoreserial == False:
            if RecordForce.ser.isOpen() == False:
               RecordForce.ser.open()
            RecordForce.legacy = False # bebee frankserial, lez go, 08/31/2022
            print("RecordForce.legacy = ",RecordForce.legacy)
            if RecordForce.legacy == False:
                runDataCollect()
            elif RecordForce.legacy == True:
                RecordForce.start()
            if visualizeDatastream == True:
                thread2_visualizeData = threading.Thread(target = datafeed,args=(RecordForce.container))
                thread2_visualizeData.start()
        else:
            print("Data collection not run, because GUI.ignoreserial ==",str(GUI.ignoreserial),"...")

    # saves raw force data # Bebee legacy method
    def start():
        RecordForce.collect = True
        if RecordForce.ser.isOpen() == False:
           RecordForce.ser.open()
        #threading run function (simultaneously performs run function in backend)
        t1 = threading.Thread(target = run,args=(RecordForce, RecordForce.ser))
        t1.start()

    #bebee Legacy
    def stop():
        RecordForce.ser.flushInput()# wait until all data is written
        RecordForce.collect = False
        
        try:
            stopped = 'x'
            RecordForce.ser.write(stopped.encode())# sends 'x' to Arduino to stop reading sensors
            time.sleep(.5)# for potential error protection?
            #ser.close()
        except:
            errors.append('serial com. (stopping data)') # error label
            eCode = 'e7'
            errorCodes.append(eCode)
        finally:
            
            GUI.timeElapsed = RecordForce.elapsed
            GUI.distanceTraveled = RecordForce.dis
            GUI.forcePushed = RecordForce.force
            RecordForce.saveForce()# run the Save Raw Data function

        
    def sendStart():
        if RecordForce.ser.isOpen() == False:
           RecordForce.ser.open()
           
        started = 's'
        print("\nPython sent "+started+".")
        RecordForce.hasStarted = False
        RecordForce.hasSentStop = False
        RecordForce.hasStopped = False
        # wipe vars
        GUI.forcePushed = []
        GUI.distanceTraveled = []
        GUI.timeElapsed = []
        RecordForce.datastream = []
        #thread2_count_stop.start()
        while RecordForce.hasStarted == False: # len(line)==0
            RecordForce.ser.write(started.encode())
            time.sleep(sleepSend) # if this is on, it takes another two seconds to start, but the arduino yells less.
            if RecordForce.ser.in_waiting > 0: # this does happen
                ser_bytes = RecordForce.ser.readline()
                line = ser_bytes.decode('utf-8').rstrip()
                if line =="Started!": #if line == started:
                    RecordForce.hasStarted = True
                    RecordForce.startTime = time.time() #stopwatch starts
                    RecordForce.i = 0
                    print(started+" received by arduino.")
                    
    def sendStop():
        stopped = 'x'
        RecordForce.hasSentStop = True
        print("Python sent "+stopped+".")
        
        while RecordForce.hasStopped == False: # len(line)==0
            print("brake", end =" ")
            RecordForce.ser.write(stopped.encode())
            RecordForce.ser.flush()
            time.sleep(sleepSend)
            if RecordForce.ser.in_waiting > 0: # this does happen
                bytecount = RecordForce.ser.in_waiting
                ser_bytes = RecordForce.ser.read(bytecount)
                line = ser_bytes.decode('utf-8').rstrip()
                datapacket = line.splitlines()
                #print(line)
                if line =="Stopped!" or ("Stopped!" in datapacket): #if line == stopped:
                #if ("Stopped!" in ser_bytes): #if line == stopped:
                    RecordForce.hasStopped = True
                    print(stopped+" received by arduino.")
                    #RecordForce.ser.close()
                    #print(RecordForce.dataStream)
                    '''
                    RecordForce.allocateNineCellData() # what is this for, nine cell stuff?
                    '''
        RecordForce.ser.close()
        print("Test runtime: ",max(GUI.timeElapsed)," seconds.") # /1000
                        
    def stopAndSave():
        if RecordForce.legacy == True:
            RecordForce.stop()
        else:
            time.sleep(.1)
            if GUI.ignoreserial == False:
                    
                testForNineCellFilename()
                if RecordForce.ser.isOpen():
                    try:
                        RecordForce.ser.flushInput()# wait until all data is written
                        #print("Not flushing input.")
                    except:
                        print("failed RecordForce.ser.flushInput()")
                    RecordForce.sendStop()
                    
                RecordForce.saveForce()
            else:
                print("File not saved. GUI.ignoreserial == True.")

    def saveForce():
        createBackupFile()
        # force data filename
        filename_force = GUI.filename_force.get()
        filename_force_csv = GUI.address + '/' + (GUI.filename_force.get()) + '.csv'
        if overwriteGuard(filename_force_csv) == True: # filename already exists, needs to be renamed
            rename(filename_force) # prompt user to rename file

        #ave. SOCEM velocity
        avelocity = ["AvgTravelVelocity(cm/s)"]
        try:
            travelvelocity = max(GUI.distanceTraveled)/(max(GUI.timeElapsed)) #cm/s # /1000
            avelocity.append(travelvelocity)
        except:
            travelvelocity=0
            avelocity.append(travelvelocity)

        #Sampling Rate
        sampling=["SamplingRate(Hz)"]
        hz = list()
        try:
            for i in range(len(GUI.distanceTraveled)-1):
                change = GUI.timeElapsed[i+1] - GUI.timeElapsed[i] # ms
                hz.append(change)
            rate = sum(hz)/len(hz) # why flip? 
            sampling.append(1/rate) # why flip?
        except:
            rate = 0
            sampling.append(0)

        GUI.travelvelocity = travelvelocity
        GUI.samplingrate = 1/rate # changed from 1/rate, to avoid a divide by zero error

        RecordForce.sidehit_peakclick_do()
                
        if GUI.ignoreserial == False and len(GUI.forcePushed)>0:
            GUI.distanceTraveled.insert(0, "Distance(cm)")
            GUI.forcePushed.insert(0, "Force(N)")
            GUI.timeElapsed.insert(0 , "Time(sec)")

            ''' write CSV'''
            GUI.data_recordForce = [GUI.timeElapsed,GUI.distanceTraveled, GUI.forcePushed, avelocity, sampling,RecordForce.peaks_force,RecordForce.peaks_distance,RecordForce.peaks_time]
            columns_data_recordForce = zip_longest(*GUI.data_recordForce)
            with open(filename_force_csv,'w',newline='') as f:
                writer = csv.writer(f)
                writer.writerows(columns_data_recordForce)
            ''' end: write CSV '''
            print("filename_force_csv = "+filename_force_csv)
            
            # tell user raw data was saved
            #print("File saved: "+GUI.filename_force.get()+".csv\n")
            try:
                forceSaved_label = tk.Label(RecordForce.msgbox, text = "Force data saved.", font = ("arial", 14, "bold"), fg = "dodgerblue3", bg = "ghost white")
                #forceSaved_label = tk.Label(RecordForce.msgbox, text = "Force data saved.", font = ("arial", 14, "bold"), fg = "dodgerblue3", bg = "ghost white").grid(row=0, column=0)
            except:
                print("attempt to generate in-window forceSaved_label messsage. fail, dave.")
        else:
            print("Force data not saved. GUI.ignoreserial = "+str(GUI.ignoreserial)+". len(GUI.forcePushed) = ",len(GUI.forcePushed))
            
        #RecordForce.clearDisplay()
        '''
        self.instantGraph()
        '''
        '''
        Why clear?
        GUI.timeElapsed.clear()
        GUI.forcePushed.clear()
        GUI.distanceTraveled.clear()
        avelocity.clear()
        hz.clear()
        sampling.clear()
        '''

    '''
    #auto graph feature 
    def instantGraph(self):
        try:
        #if self.dataset-1 <= 1:
            self.legends = []
        except:
            pass
            
        if not plt.get_fignums():#if graph figure was closed, reset legend
            self.legends.clear()
            #print("new fig who dis")
        self.legends.append(GUI.filename_force.get())#add current filename to legend
        #fig = plt.figure(figsize=(8,4.8)) #fig size control 
        #plots force displacement graph
        print("len(GUI.distanceTraveled) = ",len(GUI.distanceTraveled))
        if self.checkAutoGraph.get() == 1 and len(GUI.distanceTraveled)>5 and GUI.ignoreserial == False:
            plt.plot(GUI.distanceTraveled, GUI,forcePushed)
            plt.xlabel("Distance (cm)")
            plt.ylabel("Force (N)")
            plt.title(filename.get())
            plt.legend(self.legends)
            plt.axis = ([min(distance), max(distance), min(force), max(force)])
            plt.show()
        else:
            print("There is no data to graph. Try GUI.ignoreserial = False, in StemBerry.")
        '''
    def sidehit_peakclick_do():
        RecordForce.peaks_force,RecordForce.peaks_distance,RecordForce.peaks_time= [],[],[]
        # currently only lauches click assessment for side1, side2, side3
        #print("GUI.currentdirection = ",GUI.currentdirection.get())
        #print("len(GUI.forcePushed) = ",len(GUI.forcePushed))
        if (assessAllTests == True) or (GUI.currentdirection.get() == "side1") or (GUI.currentdirection.get() == "side2") or (GUI.currentdirection.get() == "side3"): 
        #if True:
            if len(GUI.forcePushed)>0:
                variety_plotname_detail = GUI.filename_force.get()
                RecordForce.plotshown = True
                RecordForce.closedplt = False
                RecordForce.thread3_plotchecker = threading.Thread(target = RecordForce.plotchecker)
                RecordForce.thread3_plotchecker.start()
                PeakClick.peakclick_do(GUI.forcePushed,GUI.distanceTraveled,GUI.timeElapsed,GUI.filename_force.get(),GUI.address,GUI.travelvelocity)
                #RecordForce.peaks_force,RecordForce.peaks_distance,RecordForce.peaks_time = peakclick.peaks_force,peakclick.peaks_distance,peakclick.peaks_time
                # RecordForce.sortClicks(RecordForce.peaks_force,RecordForce.peaks_distance,RecordForce.peaks_time)
            else:
                print("PeaksClick figure not triggered because len(GUI.forcePushed) = 0.")
    def plotchecker():
        while RecordForce.plotshown == True:
            time.sleep(.1)
            if RecordForce.closedplt == True:
                time.sleep(.1)
                RecordForce.sortClicks()
                RecordForce.plotshown = False
            '''
            else:
                print("loop while")
                '''
    def allocateNineCellData():
        print("allocate")

    def sortClicks():
        '''
        if GUI.currentdirection.get() == "side1":
            if len(RecordForce.peaks_force) == 3:
                GUI.peak_force_cell1, GUI.peak_force_cell2, GUI.peak_force_cell3 = RecordForce.peaks_force[0],RecordForce.peaks_force[1],RecordForce.peaks_force[2]
            elif len(RecordForce.peaks_force) == 4:
                GUI.peak_force_cell1, GUI.peak_force_cell2, GUI.peak_force_cell3 = RecordForce.peaks_force[1],RecordForce.peaks_force[2],RecordForce.peaks_force[3]
            if len(RecordForce.peaks_distance) == 3:
                GUI.peak_distance_cell1, GUI.peak_distance_cell2, GUI.peak_distance_cell3 = RecordForce.peaks_distance[0],RecordForce.peaks_distance[1],RecordForce.peaks_distance[2]
            elif len(RecordForce.peaks_distance) == 4:
                GUI.peak_distance_cell1, GUI.peak_distance_cell2, GUI.peak_distance_cell3 = RecordForce.peaks_distance[1],RecordForce.peaks_distance[2],RecordForce.peaks_distance[3]
            if len(RecordForce.peaks_time) == 3:
                GUI.peak_time_cell1, GUI.peak_time_cell2, GUI.peak_time_cell3=RecordForce.peaks_time[0],RecordForce.peaks_time[1],RecordForce.peaks_time[2]
            elif len(RecordForce.peaks_time) == 4:
                 GUI.peak_time_cell1, GUI.peak_time_cell2, GUI.peak_time_cell3=RecordForce.peaks_time[1],RecordForce.peaks_time[2],RecordForce.peaks_time[3]

        '''
        print("RecordForce.peaks_force = ",RecordForce.peaks_force)
        # this can be cleaned up. assumes if four clicks ignore first one
        # clicks must be done in order
        # only for nine cell
        # cell numbers should be switched to be 123, 456, 789; not 147, 258, 369
        if GUI.currentdirection.get() == "side1":
            if len(RecordForce.peaks_force) == 3:
                GUI.peak_force_cell1, GUI.peak_force_cell4, GUI.peak_force_cell7 = RecordForce.peaks_force[0],RecordForce.peaks_force[1],RecordForce.peaks_force[2]
            elif len(RecordForce.peaks_force) == 4:
                GUI.peak_force_cell1, GUI.peak_force_cell4, GUI.peak_force_cell7 = RecordForce.peaks_force[1],RecordForce.peaks_force[2],RecordForce.peaks_force[3]
            else:
                GUI.peak_force_cell1, GUI.peak_force_cell4, GUI.peak_force_cell7 = RecordForce.peaks_force[0],RecordForce.peaks_force[1],RecordForce.peaks_force[2]
            if len(RecordForce.peaks_distance) == 3:
                GUI.peak_distance_cell1, GUI.peak_distance_cell4, GUI.peak_distance_cell7 = RecordForce.peaks_distance[0],RecordForce.peaks_distance[1],RecordForce.peaks_distance[2]
            elif len(RecordForce.peaks_distance) == 4:
                GUI.peak_distance_cell1, GUI.peak_distance_cell4, GUI.peak_distance_cell7 = RecordForce.peaks_distance[1],RecordForce.peaks_distance[2],RecordForce.peaks_distance[3]
            
            if len(RecordForce.peaks_time) == 3:
                GUI.peak_time_cell1, GUI.peak_time_cell4, GUI.peak_time_cell7=RecordForce.peaks_time[0],RecordForce.peaks_time[1],RecordForce.peaks_time[2]
            elif len(RecordForce.peaks_time) == 4:
                 GUI.peak_time_cell1, GUI.peak_time_cell4, GUI.peak_time_cell7=RecordForce.peaks_time[1],RecordForce.peaks_time[2],RecordForce.peaks_time[3]
        elif GUI.currentdirection.get() == "side2":
            if len(RecordForce.peaks_force) == 3:
                GUI.peak_force_cell2, GUI.peak_force_cell5, GUI.peak_force_cell8 = RecordForce.peaks_force[0],RecordForce.peaks_force[1],RecordForce.peaks_force[2]
            elif len(RecordForce.peaks_force) == 4:
                GUI.peak_force_cell2, GUI.peak_force_cell5, GUI.peak_force_cell8 = RecordForce.peaks_force[1],RecordForce.peaks_force[2],RecordForce.peaks_force[3]
            if len(RecordForce.peaks_distance) == 3:
                GUI.peak_distance_cell2, GUI.peak_distance_cell5, GUI.peak_distance_cell8 = RecordForce.peaks_distance[0],RecordForce.peaks_distance[1],RecordForce.peaks_distance[2]
            elif len(RecordForce.peaks_distance) == 4:
                GUI.peak_distance_cell2, GUI.peak_distance_cell5, GUI.peak_distance_cell8 = RecordForce.peaks_distance[1],RecordForce.peaks_distance[2],RecordForce.peaks_distance[3]
            if len(RecordForce.peaks_time) == 3:
                GUI.peak_time_cell2, GUI.peak_time_cell5, GUI.peak_time_cell8=RecordForce.peaks_time[0],RecordForce.peaks_time[1],RecordForce.peaks_time[2]
            elif len(RecordForce.peaks_time) == 4:
                GUI.peak_time_cell2, GUI.peak_time_cell5, GUI.peak_time_cell8=RecordForce.peaks_time[1],RecordForce.peaks_time[2],RecordForce.peaks_time[3]
            #GUI.peak_distance_cell4, GUI.peak_distance_cell5, GUI.peak_distance_cell6 = RecordForce.peaks_distance[0],RecordForce.peaks_distance[1],RecordForce.peaks_distance[2]
            #GUI.peak_time_cell4, GUI.peak_time_cell5, GUI.peak_time_cell6=RecordForce.peaks_time[0],RecordForce.peaks_time[1],RecordForce.peaks_time[2]
        elif GUI.currentdirection.get() == "side3":
            if len(RecordForce.peaks_force) == 3:
                GUI.peak_force_cell3, GUI.peak_force_cell6, GUI.peak_force_cell9 = RecordForce.peaks_force[0],RecordForce.peaks_force[1],RecordForce.peaks_force[2]
            elif len(RecordForce.peaks_force) == 4:
                GUI.peak_force_cell3, GUI.peak_force_cell6, GUI.peak_force_cell9 = RecordForce.peaks_force[1],RecordForce.peaks_force[2],RecordForce.peaks_force[3]
            if len(RecordForce.peaks_distance) == 3:
                GUI.peak_distance_cell3, GUI.peak_distance_cell6, GUI.peak_distance_cell9 = RecordForce.peaks_distance[0],RecordForce.peaks_distance[1],RecordForce.peaks_distance[2]
            elif len(RecordForce.peaks_distance) == 4:
                GUI.peak_distance_cell3, GUI.peak_distance_cell6, GUI.peak_distance_cell9 = RecordForce.peaks_distance[1],RecordForce.peaks_distance[2],RecordForce.peaks_distance[3]
            if len(RecordForce.peaks_time) == 3:
                GUI.peak_time_cell3, GUI.peak_time_cell6, GUI.peak_time_cell9=RecordForce.peaks_time[0],RecordForce.peaks_time[1],RecordForce.peaks_time[2]
            elif len(RecordForce.peaks_time) == 4:
                GUI.peak_time_cell3, GUI.peak_time_cell6, GUI.peak_time_cell9=RecordForce.peaks_time[1],RecordForce.peaks_time[2],RecordForce.peaks_time[3] 
            #GUI.peak_distance_cell7, GUI.peak_distance_cell8, GUI.peak_distance_cell9 = RecordForce.peaks_distance[0],RecordForce.peaks_distance[1],RecordForce.peaks_distance[2]
            #GUI.peak_time_cell7, GUI.peak_time_cell8, GUI.peak_time_cell9=RecordForce.peaks_time[0],RecordForce.peaks_time[1],RecordForce.peaks_time[2]

    #zeroes load cell measurement
            
    def tare():
        if GUI.ignoreserial == False:
            print("Tare")
            RecordForce.ser.flush()#wait until all data is written
            
            tare = 't'
            RecordForce.ser.write(tare.encode()) #sends 't' to arduino, telling it to tare
            time.sleep(0.3)#wait x seconds for Arduino to tare load cell (for smoothing)
        else:
            print("\nYou hit the 'tare' button while GUI.ignoreserial == True.\nLoadcell cannot be tared because it is neither connected nor sought.")
            RecordForce.message_connectArduino()
            
    def message_connectArduino():
        #print("\nYou hit the 'tare' button while GUI.ignoreserial == True.\nLoadcell cannot be tared because it is neither connected nor sought.\n\nConnect an arduino.\nFlash Ardunio with serialConnection_v11.ino(&+).\n\nIn StemBerry header variables:\nGUI.ignoreserial = False.\nMatch dev_manual port ID with ID on Arduino IDE.\n\nSigned, Clayton Bennett, August 25, 2022.")
        print("\n\nConnect an arduino.\nFlash Ardunio with serialConnection_v11.ino(&+).\n\nIn StemBerry header variables:\nGUI.ignoreserial = False.\nMatch dev_manual port ID with ID on Arduino IDE.\n\nSigned, Clayton Bennett, August 25, 2022.")

    def on_show_frame_RecordForce(self, event):
        #Flip to data collection screen, GUI variables
        if (GUI.varietyname.get()!="" or GUI.plotname.get()!="") and (GUI.passfillednames_checkbox.get()==1): # checks if a varietyname or plotname has been given
            RecordForce.nameFresh(GUI.varietyname.get(),GUI.plotname.get()) # if so, autopopulate the basic filestructure
        filename_force = nameBlackBox("",GUI.filename_force.get())
        GUI.filename_force.set(filename_force)
        GUI.currentdirection.set("") # so that sortClicks will funtion properly, if a new name is assigned # this is non-deal coding
