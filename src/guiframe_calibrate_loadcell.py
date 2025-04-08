import tkinter as tk

from src.gui_main import GUI
# Load cell calibration page 
class Calibrate(tk.Frame):
    
    def __init__(self, parent, controller): # automatically runs
        
        tk.Frame.__init__(self, parent)
        
        ''' GUI design, non-frame '''
        pageButtons = repeatPageButtons.showButtons(self, parent, controller)
        header_label = tk.Label(self, text = "FORCE SENSOR CALIBRATION", font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white")
        tareIt_label = tk.Label(self, text = "1. Tare w/ no weight", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        inputWeight_label = tk.Label(self, text = "2. Input weight (kg)", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        caliIt_label = tk.Label(self, text = '3. Place weight', font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        caliIt4_label = tk.Label(self, text = '4. Optimize so Diff. = 0', font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        testWeight_label = tk.Label(self, text = "Weight:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")

        header_label.place(x=235,y=0)
        tareIt_label.place(x=5,y=43)
        inputWeight_label.place(x=5,y=73)
        caliIt_label.place(x=5,y=103)
        caliIt4_label.place(x=5,y=133)
        testWeight_label.place(x=5,y=183)
        

        self.knownWeight = tk.DoubleVar() # know weight textvariable
        self.knownWeight.set(0.0) # initially = 1.0 kg (assuming 1.0 kg will be used)
        knownW_entry = tk.Entry(self, textvariable=self.knownWeight, font = ("arial", 14, "bold"), width= 5, bg="white", fg="gray1").place(x = 80, y =183)

        kg = tk.Label(self, text = "kg", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=140,y=183)

        self.force = self.knownWeight.get() * convert_KgToN # convert known weight kg to N
        self.strWeight = str('%.3f' % self.force) # store as string
        self.strForce = tk.StringVar() # for displaying & updating on GUI
        self.strForce.set(self.strWeight) # initial value = self.knownWeight

        eq_label = tk.Label(self, text = '= ', font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        force_label = tk.Label(self, textvariable = self.strForce, font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        unit_label = tk.Label(self, text = " N", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        cali_label = tk.Label(self, text = "Cali. Factor:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")

        eq_label.place(x=170,y=183)
        force_label.place(x=187,y=183)
        unit_label.place(x=249,y=183)
        cali_label.place(x=5,y=223)
    
        self.calibra = tk.DoubleVar() 
        #self.calibra.set(199750) # initial calibration num. Has been working well. AB.
        self.calibra.set(calibrationFactor) # initial calibration num. Has been working well. AB.
        #self.calibra.set(1997500) # death to the infidels. CB.
        self.factor = self.calibra.get() 
        self.calibra_entry = tk.Entry(self, textvariable=self.calibra, font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        

        #tares/zeros load cell
        tare_button = tk.Button(self, text = "Tare", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",command=lambda:RecordForce.tare) # confirm this works
        # updates cali factor & starts/continues cali. process
        cali_button = tk.Button(self, text ="Update\nCali.\nFactor", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2", command=lambda:self.caliThread())
        # stops cali. process
        done_button = tk.Button(self, text ="Done", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2", command=lambda:self.doneCali())
        # + 1000 to calibra
        p1000_button = tk.Button(self, text ="+1000", font = ("arial", 16, "bold"), height = 1, width = 8, fg = "ghost white", bg = "gray2", command=lambda:self.updateCali(1000))
        # - 1000 to calibra
        n1000_button = tk.Button(self, text ="-1000", font = ("arial", 16, "bold"), height = 1, width = 8, fg = "ghost white", bg = "gray2", command=lambda:self.updateCali(-1000))
        # + 100
        p100_button = tk.Button(self, text ="+100", font = ("arial", 16, "bold"), height = 1, width = 8, fg = "ghost white", bg = "gray2", command=lambda:self.updateCali(100))
        # - 100
        n100_button = tk.Button(self, text ="-100", font = ("arial", 16, "bold"), height = 1, width = 8, fg = "ghost white", bg = "gray2", command=lambda:self.updateCali(-100))

        scroll = tk.Scrollbar(self)

        self.LC_label = tk.Label(self, text = "N",font = ("arial", 14, "bold"), fg = "dodgerblue3", bg = "ghost white")
        self.LClist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 10, font = ("arial", 14, "bold"), fg = "dodgerblue3")
        self.Diff_label = tk.Label(self, text = "Diff.",font = ("arial", 14, "bold"), fg = "dodgerblue3", bg = "ghost white")
        self.Difflist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 10, font = ("arial", 14, "bold"), fg = "dodgerblue3")

        self.calibra_entry.place(x = 125, y = 223)
        tare_button.place(x = 559, y = 44)
        cali_button.place(x = 675, y = 44)
        done_button.place(x = 675, y = 224)
        p1000_button.place(x = 559, y = 136)
        n1000_button.place(x = 559, y = 136+44)
        p100_button.place(x = 675, y = 136)
        n100_button.place(x = 675, y = 136+44)
        
        self.LC_label.place(x = 330, y = 43)
        self.LClist.place(x = 310, y = 73)
        self.Diff_label.place(x = 420, y = 43)
        self.Difflist.place(x = 400, y = 73)

    def updateCali(self, cali): # update calibration factor
        self.factor = self.calibra.get() + cali
        self.calibra_entry.delete(0, 'end')
        self.calibra_entry.insert(0, self.factor)
        return self.factor

    def tare(self):
        RecordForce.ser.flush()#wait until all data is written
        tare = 't'
        RecordForce.ser.write(tare.encode()) #sends 't' to arduino, telling it to tare
        print("Tare.")
        time.sleep(0.3)#wait x seconds for Arduino to tare load cell (for smoothing)
       
    def caliFactor(self):
        self.force = self.knownWeight.get() * convert_KgToN # convert known weight kg to N
        self.strW = str('%.3f' % self.force) # store as string
        self.strForce.set(self.strW) # update GUI text
        
        scroll = tk.Scrollbar(self)
        self.factor = self.calibra.get() # get user input calibration factor
        self.doneCali() # if Arduino sending force data, this will momentarily stop it 
        
        strFactor = str(self.factor) # cali factor as string
        RecordForce.ser.write(strFactor.encode()) # send cali factor to Arduino
        RecordForce.ser.flush() # make sure it gets it before proceeding

        global caliLoop
        caliLoop = True

        while caliLoop == True: # loop to continuously print Arduino force readings

            if RecordForce.ser.inWaiting() > 0: #checks to see if Serial is available 
                    
                try: #make sure serial data can be read/is there
                    ser_bytes = RecordForce.ser.readline()
                except:
                    GUI.errors.append('serial read')
                    eCode = 'e8'
                    GUI.errorCodes.append(eCode)
                    print("eCode = "+eCode)
                    #popup("serial read")
                    
                bytesDecoded = (ser_bytes[0:len(ser_bytes)-2].decode("utf-8")) # force reading bytes
                try:
                    reading = float(bytesDecoded) # convert bytes to float
                    diff = self.force - reading # difference between reading & known weight
                    self.LClist.insert(END, str('%.2f' % reading)) # scrollbar list for force readings
                    self.Difflist.see(END)
                    self.Difflist.insert(END, str('%.1f' % diff)) # scrollbar list for forcebar - known weight 
                    self.LClist.see(END)
                except:
                    pass 

                
    def caliThread(self): #threading calibrate function (simultaneously performs caliFactor function in backend)
        thread = threading.Thread(target = Calibrate.caliFactor,args=(self,))
        thread.start()

    def doneCali(self): # stops calibration process
        # RecordForce.ser.reset_input_buffer()# clear the input buffer # suppressed 9/6/22 CB
        global caliLoop
        caliLoop = False # stop loop asking for data
        
        send = 'd' # stop Arduino sending
        RecordForce.ser.write(send.encode()) # send 'd' to stop Arduino sending data
