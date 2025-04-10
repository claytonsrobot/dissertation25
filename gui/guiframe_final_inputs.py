from itertools import zip_longest
import tkinter as tk

import src.physics.ei_interaction_error_management
import src.physics.ei_no_interaction_error_management
# from gui.gui_main import GUI

class FinalInputs(tk.Frame):
    @classmethod
    def pass_in_GUI(cls,GUI):
        cls.GUI = GUI

    def __init__(self): # automatically runs
        #self.nope = "nope"
        self.run()
    def run(self, parent, controller): # automatically runs
        FinalInputs.mass1 = [] # TypeError: 'float' object is not iterable
        FinalInputs.mass2 = []
        FinalInputs.mass3 = []
        FinalInputs.mass4 = []
        FinalInputs.mass5 = []
        FinalInputs.mass6 = []
        FinalInputs.mass7 = []
        FinalInputs.mass8 = []
        FinalInputs.mass9 = []
        FinalInputs.count1 = [] 
        FinalInputs.count2 = []
        FinalInputs.count3 = []
        FinalInputs.count4 = []
        FinalInputs.count5 = []
        FinalInputs.count6 = []
        FinalInputs.count7 = []
        FinalInputs.count8 = []
        FinalInputs.count9 = []

        FinalInputs.diam1 = []
        FinalInputs.diam2 = []
        FinalInputs.diam3 = []
        FinalInputs.diam4 = []
        FinalInputs.diam5 = []
        FinalInputs.diam6 = []
        FinalInputs.diam7 = []
        FinalInputs.diam8 = []
        FinalInputs.diam9 = []
        
        tk.Frame.__init__(self, parent)

        ''' GUI design, non-frame '''
        pageButtons = repeatPageButtons.showButtons(self, parent, controller)
        unit_label = tk.Label(self, text=str("Mass unit is grams, diameter unit is millimeters."), font = ("arial", 12, "italic"), fg = "red4", bg="ghost white")        
        #backupFinalInputs_button = tk.Button(self, text ="Create Backup File", font = ("arial", 14, "bold"), height = 1, width = 20, fg = "ghost white", bg = "dodgerblue3", command=lambda:createBackupFile())
        savePostTestInputs_button = tk.Button(self, text ="Save Post Test Inputs", font = ("arial", 14, "bold"), height = 1, width = 20, fg = "ghost white", bg = "dodgerblue3", command=lambda:self.savePostTestInputs())
        compileNineCellData_button = tk.Button(self, text ="Compile Nine-Cell Data", font = ("arial", 14, "bold"), height = 1, width = 20, fg = "ghost white", bg = "dodgerblue3", command=lambda:self.compileNineCellData())
        
        unit_label.place(x=400+30,y=0)
        #backupFinalInputs_button.place(x = 510, y = 340+38)
        compileNineCellData_button.place(x = 510, y = 340+38)
        savePostTestInputs_button.place(x = 510, y = 340)

        ''' Frame: Cell 1 '''
        cell1_frame = tk.LabelFrame(self, text='Cell 1',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        cell1_frame.place(x = 0, y = 230)
        cell1Mass_label = tk.Label(cell1_frame, text = "Mass:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        cell1Count_label = tk.Label(cell1_frame, text = "Count:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        cell1Diameters_label = tk.Label(cell1_frame, text = "Diam:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        cell1Mass_entry = tk.Entry(cell1_frame, textvariable=GUI.cell1Mass, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=0, column=1)
        cell1Count_entry = tk.Entry(cell1_frame, textvariable=GUI.cell1Count, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=1, column=1)
        cell1Diameter1_entry = tk.Entry(cell1_frame, textvariable=GUI.cell1Diameter1, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=2, column=1)
        cell1Diameter2_entry = tk.Entry(cell1_frame, textvariable=GUI.cell1Diameter2, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=2)
        cell1Diameter3_entry = tk.Entry(cell1_frame, textvariable=GUI.cell1Diameter3, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=3)
        cell1Diameter4_entry = tk.Entry(cell1_frame, textvariable=GUI.cell1Diameter4, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=4)
        ''' end '''

        ''' Frame: Cell 2 '''
        cell2_frame = tk.LabelFrame(self, text='Cell 2',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        #cell2_frame.place(x = 250, y = 230)
        cell2_frame.place(x = 0, y = 125)
        cell2Mass_label = tk.Label(cell2_frame, text = "Mass:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        cell2Count_label = tk.Label(cell2_frame, text = "Count:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        cell2Diameters_label = tk.Label(cell2_frame, text = "Diam:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        cell2Mass_entry = tk.Entry(cell2_frame, textvariable=GUI.cell2Mass, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=0, column=1)
        cell2Count_entry = tk.Entry(cell2_frame, textvariable=GUI.cell2Count, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=1, column=1)
        cell2Diameter1_entry = tk.Entry(cell2_frame, textvariable=GUI.cell2Diameter1, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=2, column=1)
        cell2Diameter2_entry = tk.Entry(cell2_frame, textvariable=GUI.cell2Diameter2, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=2)
        cell2Diameter3_entry = tk.Entry(cell2_frame, textvariable=GUI.cell2Diameter3, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=3)
        cell2Diameter4_entry = tk.Entry(cell2_frame, textvariable=GUI.cell2Diameter4, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=4)
        ''' end '''

        ''' Frame: Cell 3 '''
        cell3_frame = tk.LabelFrame(self, text='Cell 3',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        #cell3_frame.place(x = 500, y = 230)
        cell3_frame.place(x = 0, y = 20)
        cell3Mass_label = tk.Label(cell3_frame, text = "Mass:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        cell3Count_label = tk.Label(cell3_frame, text = "Count:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        cell3Diameters_label = tk.Label(cell3_frame, text = "Diam:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        cell3Mass_entry = tk.Entry(cell3_frame, textvariable=GUI.cell3Mass, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=0, column=1)
        cell3Count_entry = tk.Entry(cell3_frame, textvariable=GUI.cell3Count, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=1, column=1)
        cell3Diameter1_entry = tk.Entry(cell3_frame, textvariable=GUI.cell3Diameter1, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=2, column=1)
        cell3Diameter2_entry = tk.Entry(cell3_frame, textvariable=GUI.cell3Diameter2, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=2)
        cell3Diameter3_entry = tk.Entry(cell3_frame, textvariable=GUI.cell3Diameter3, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=3)
        cell3Diameter4_entry = tk.Entry(cell3_frame, textvariable=GUI.cell3Diameter4, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=4)
        ''' end '''

        ''' Frame: Cell 4 '''
        cell4_frame = tk.LabelFrame(self, text='Cell 4',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        #cell4_frame.place(x = 0, y = 125)
        cell4_frame.place(x = 250, y = 230)
        cell4Mass_label = tk.Label(cell4_frame, text = "Mass:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        cell4Count_label = tk.Label(cell4_frame, text = "Count:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        cell4Diameters_label = tk.Label(cell4_frame, text = "Diam:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        cell4Mass_entry = tk.Entry(cell4_frame, textvariable=GUI.cell4Mass, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=0, column=1)
        cell4Count_entry = tk.Entry(cell4_frame, textvariable=GUI.cell4Count, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=1, column=1)
        cell4Diameter1_entry = tk.Entry(cell4_frame, textvariable=GUI.cell4Diameter1, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=2, column=1)
        cell4Diameter2_entry = tk.Entry(cell4_frame, textvariable=GUI.cell4Diameter2, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=2)
        cell4Diameter3_entry = tk.Entry(cell4_frame, textvariable=GUI.cell4Diameter3, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=3)
        cell4Diameter4_entry = tk.Entry(cell4_frame, textvariable=GUI.cell4Diameter4, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=4)
        ''' end '''

        ''' Frame: Cell 5 '''
        cell5_frame = tk.LabelFrame(self, text='Cell 5',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        cell5_frame.place(x = 250, y = 125)
        cell5Mass_label = tk.Label(cell5_frame, text = "Mass:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        cell5Count_label = tk.Label(cell5_frame, text = "Count:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        cell5Diameters_label = tk.Label(cell5_frame, text = "Diam:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        cell5Mass_entry = tk.Entry(cell5_frame, textvariable=GUI.cell5Mass, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=0, column=1)
        cell5Count_entry = tk.Entry(cell5_frame, textvariable=GUI.cell5Count, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=1, column=1)
        cell5Diameter1_entry = tk.Entry(cell5_frame, textvariable=GUI.cell5Diameter1, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=2, column=1)
        cell5Diameter2_entry = tk.Entry(cell5_frame, textvariable=GUI.cell5Diameter2, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=2)
        cell5Diameter3_entry = tk.Entry(cell5_frame, textvariable=GUI.cell5Diameter3, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=3)
        cell5Diameter4_entry = tk.Entry(cell5_frame, textvariable=GUI.cell5Diameter4, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=4)
        ''' end '''

        ''' Frame: Cell 6 '''
        cell6_frame = tk.LabelFrame(self, text='Cell 6',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        #cell6_frame.place(x = 500, y = 125)
        cell6_frame.place(x = 250, y = 20)
        cell6Mass_label = tk.Label(cell6_frame, text = "Mass:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        cell6Count_label = tk.Label(cell6_frame, text = "Count:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        cell6Diameters_label = tk.Label(cell6_frame, text = "Diam:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        cell6Mass_entry = tk.Entry(cell6_frame, textvariable=GUI.cell6Mass, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=0, column=1)
        cell6Count_entry = tk.Entry(cell6_frame, textvariable=GUI.cell6Count, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=1, column=1)
        cell6Diameter1_entry = tk.Entry(cell6_frame, textvariable=GUI.cell6Diameter1, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=2, column=1)
        cell6Diameter2_entry = tk.Entry(cell6_frame, textvariable=GUI.cell6Diameter2, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=2)
        cell6Diameter3_entry = tk.Entry(cell6_frame, textvariable=GUI.cell6Diameter3, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=3)
        cell6Diameter4_entry = tk.Entry(cell6_frame, textvariable=GUI.cell6Diameter4, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=4)
        ''' end '''

        ''' Frame: Cell 7 '''
        cell7_frame = tk.LabelFrame(self, text='Cell 7',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        #cell7_frame.place(x = 0, y = 20)
        cell7_frame.place(x = 500, y = 230)
        cell7Mass_label = tk.Label(cell7_frame, text = "Mass:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        cell7Count_label = tk.Label(cell7_frame, text = "Count:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        cell7Diameters_label = tk.Label(cell7_frame, text = "Diam:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        cell7Mass_entry = tk.Entry(cell7_frame, textvariable=GUI.cell7Mass, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=0, column=1)
        cell7Count_entry = tk.Entry(cell7_frame, textvariable=GUI.cell7Count, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=1, column=1)
        cell7Diameter1_entry = tk.Entry(cell7_frame, textvariable=GUI.cell7Diameter1, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=2, column=1)
        cell7Diameter2_entry = tk.Entry(cell7_frame, textvariable=GUI.cell7Diameter2, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=2)
        cell7Diameter3_entry = tk.Entry(cell7_frame, textvariable=GUI.cell7Diameter3, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=3)
        cell7Diameter4_entry = tk.Entry(cell7_frame, textvariable=GUI.cell7Diameter4, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=4)
        ''' end '''
        
        ''' Frame: Cell 8 '''
        cell8_frame = tk.LabelFrame(self, text='Cell 8',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        #cell8_frame.place(x = 250, y = 20)
        cell8_frame.place(x = 500, y = 125)
        cell8Mass_label = tk.Label(cell8_frame, text = "Mass:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        cell8Count_label = tk.Label(cell8_frame, text = "Count:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        cell8Diameters_label = tk.Label(cell8_frame, text = "Diam:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        cell8Mass_entry = tk.Entry(cell8_frame, textvariable=GUI.cell8Mass, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=0, column=1)
        cell8Count_entry = tk.Entry(cell8_frame, textvariable=GUI.cell8Count, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=1, column=1)
        cell8Diameter1_entry = tk.Entry(cell8_frame, textvariable=GUI.cell8Diameter1, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=2, column=1)
        cell8Diameter2_entry = tk.Entry(cell8_frame, textvariable=GUI.cell8Diameter2, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=2)
        cell8Diameter3_entry = tk.Entry(cell8_frame, textvariable=GUI.cell8Diameter3, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=3)
        cell8Diameter4_entry = tk.Entry(cell8_frame, textvariable=GUI.cell8Diameter4, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=4)
        ''' end '''
        
        ''' Frame: Cell 9 '''
        cell9_frame = tk.LabelFrame(self, text='Cell 9',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        cell9_frame.place(x = 500, y = 20)
        cell9Mass_label = tk.Label(cell9_frame, text = "Mass:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        cell9Count_label = tk.Label(cell9_frame, text = "Count:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        cell9Diameters_label = tk.Label(cell9_frame, text = "Diam:", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        cell9Mass_entry = tk.Entry(cell9_frame, textvariable=GUI.cell9Mass, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=0, column=1)
        cell9Count_entry = tk.Entry(cell9_frame, textvariable=GUI.cell9Count, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=1, column=1)
        cell9Diameter1_entry = tk.Entry(cell9_frame, textvariable=GUI.cell9Diameter1, font = ("arial", 14, "bold"), width=4, bg="white", fg="gray1").grid(row=2, column=1)
        cell9Diameter2_entry = tk.Entry(cell9_frame, textvariable=GUI.cell9Diameter2, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=2)
        cell9Diameter3_entry = tk.Entry(cell9_frame, textvariable=GUI.cell9Diameter3, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=3)
        cell9Diameter4_entry = tk.Entry(cell9_frame, textvariable=GUI.cell9Diameter4, font = ("arial", 14, "bold"), width=3, bg="white", fg="gray1").grid(row=2, column=4)
        ''' end '''

        self.bind("<<ShowFrame>>", self.on_show_frame_FinalInputs) # need this?
              
    def savePostTestInputs(self):   
        
        filename_postTest_csv = GUI.address + '/' + (GUI.filename_postTest.get()) + '.csv'
     
        FinalInputs.mass1 = [GUI.cell1Mass.get()] # TypeError: 'float' object is not iterable
        FinalInputs.mass2 = [GUI.cell2Mass.get()]
        FinalInputs.mass3 = [GUI.cell3Mass.get()]
        FinalInputs.mass4 = [GUI.cell4Mass.get()]
        FinalInputs.mass5 = [GUI.cell5Mass.get()]
        FinalInputs.mass6 = [GUI.cell6Mass.get()]
        FinalInputs.mass7 = [GUI.cell7Mass.get()]
        FinalInputs.mass8 = [GUI.cell8Mass.get()]
        FinalInputs.mass9 = [GUI.cell9Mass.get()]
        FinalInputs.count1 = [GUI.cell1Count.get()] # TypeError: 'float' object is not iterable
        FinalInputs.count2 = [GUI.cell2Count.get()]
        FinalInputs.count3 = [GUI.cell3Count.get()]
        FinalInputs.count4 = [GUI.cell4Count.get()]
        FinalInputs.count5 = [GUI.cell5Count.get()]
        FinalInputs.count6 = [GUI.cell6Count.get()]
        FinalInputs.count7 = [GUI.cell7Count.get()]
        FinalInputs.count8 = [GUI.cell8Count.get()]
        FinalInputs.count9 = [GUI.cell9Count.get()]

        FinalInputs.diam1 = [GUI.cell1Diameter1.get(),GUI.cell1Diameter2.get(),GUI.cell1Diameter3.get(),GUI.cell1Diameter4.get()]
        FinalInputs.diam2 = [GUI.cell2Diameter1.get(),GUI.cell2Diameter2.get(),GUI.cell2Diameter3.get(),GUI.cell2Diameter4.get()]
        FinalInputs.diam3 = [GUI.cell3Diameter1.get(),GUI.cell3Diameter2.get(),GUI.cell3Diameter3.get(),GUI.cell3Diameter4.get()]
        FinalInputs.diam4 = [GUI.cell4Diameter1.get(),GUI.cell4Diameter2.get(),GUI.cell4Diameter3.get(),GUI.cell4Diameter4.get()]
        FinalInputs.diam5 = [GUI.cell5Diameter1.get(),GUI.cell5Diameter2.get(),GUI.cell5Diameter3.get(),GUI.cell5Diameter4.get()]
        FinalInputs.diam6 = [GUI.cell6Diameter1.get(),GUI.cell6Diameter2.get(),GUI.cell6Diameter3.get(),GUI.cell6Diameter4.get()]
        FinalInputs.diam7 = [GUI.cell7Diameter1.get(),GUI.cell7Diameter2.get(),GUI.cell7Diameter3.get(),GUI.cell7Diameter4.get()]
        FinalInputs.diam8 = [GUI.cell8Diameter1.get(),GUI.cell8Diameter2.get(),GUI.cell8Diameter3.get(),GUI.cell8Diameter4.get()]
        FinalInputs.diam9 = [GUI.cell9Diameter1.get(),GUI.cell9Diameter2.get(),GUI.cell9Diameter3.get(),GUI.cell9Diameter4.get()]

         # Labels for Excel
        FinalInputs.diam1.insert(0,"diameters_cell1(mm)")
        FinalInputs.diam2.insert(0,"diameters_cell2(mm)")
        FinalInputs.diam3.insert(0,"diameters_cell3(mm)")
        FinalInputs.diam4.insert(0,"diameters_cell4(mm)")
        FinalInputs.diam5.insert(0,"diameters_cell5(mm)")
        FinalInputs.diam6.insert(0,"diameters_cell6(mm)")
        FinalInputs.diam7.insert(0,"diameters_cell7(mm)")
        FinalInputs.diam8.insert(0,"diameters_cell8(mm)")
        FinalInputs.diam9.insert(0,"diameters_cell9(mm)")
        FinalInputs.mass1.insert(0,"mass_cell1(g)")
        FinalInputs.mass2.insert(0,"mass_cell2(g)")
        FinalInputs.mass3.insert(0,"mass_cell3(g)")
        FinalInputs.mass4.insert(0,"mass_cell4(g)")
        FinalInputs.mass5.insert(0,"mass_cell5(g)")
        FinalInputs.mass6.insert(0,"mass_cell6(g)")
        FinalInputs.mass7.insert(0,"mass_cell7(g)")
        FinalInputs.mass8.insert(0,"mass_cell8(g)")
        FinalInputs.mass9.insert(0,"mass_cell9(g)")
        FinalInputs.count1.insert(0,"count_cell1")
        FinalInputs.count2.insert(0,"count_cell2")
        FinalInputs.count3.insert(0,"count_cell3")
        FinalInputs.count4.insert(0,"count_cell4")
        FinalInputs.count5.insert(0,"count_cell5")
        FinalInputs.count6.insert(0,"count_cell6")
        FinalInputs.count7.insert(0,"count_cell7")
        FinalInputs.count8.insert(0,"count_cell8")
        FinalInputs.count9.insert(0,"count_cell9")
        
        if overwriteGuardPage(filename_postTest_csv) == True: # filename already exists, needs to be renamed
            renamePage(GUI.filename_postTest.get()) # prompt user to rename file
        ''' write CSV'''

        GUI.data_postTest = [FinalInputs.diam1,FinalInputs.diam2,FinalInputs.diam3,FinalInputs.diam4,FinalInputs.diam5,FinalInputs.diam6,FinalInputs.diam7,FinalInputs.diam8,FinalInputs.diam9,FinalInputs.mass1,FinalInputs.mass2,FinalInputs.mass3,FinalInputs.mass4,FinalInputs.mass5,FinalInputs.mass6,FinalInputs.mass7,FinalInputs.mass8,FinalInputs.mass9,FinalInputs.count1,FinalInputs.count2,FinalInputs.count3,FinalInputs.count4,FinalInputs.count5,FinalInputs.count6,FinalInputs.count7,FinalInputs.count8,FinalInputs.count9]
        columns_data_postTest = zip_longest(*GUI.data_postTest)

        with open(filename_postTest_csv,'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerows(columns_data_postTest)
        ''' end: write CSV '''
        print("filename_postTest_csv = "+filename_postTest_csv)
        
    def saveEIs():
        GUI.EI_fullcontact.insert(0 , "EI_fullcontact(N*cm^2)")
        GUI.EI_intermediatecontact.insert(0 , "EI_intermediatecontact(N*cm^2)")
        GUI.EI_nocontact.insert(0 , "EI_nocontact(N*cm^2")
        GUI.AvgEI_intermediatecontact.insert(0 , "AvgEI_intermediatecontact(N*cm^2)")
        ''' write CSV'''
        filename_EI_csv = GUI.address + '/' + GUI.filename_force.get() + '_EI.csv'
        GUI.data_EI = [GUI.EI_fullcontact,GUI.EI_intermediatecontact,GUI.EI_nocontact,GUI.AvgEI_intermediatecontact]
        columns_data_EI = zip_longest(*GUI.data_EI)
        with open(filename_EI_csv,'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerows(columns_data_EI)
        ''' end: write CSV '''
        print("filename_EI_csv = "+filename_EI_csv)
        #print("saved:", filename_EI_csv)
        
    def compileNineCellData(self):
        createBackupFile() # fix below # numbers are for lbs, not newtons
        if importFileDataTF == True:
            importFileData()
        GUI.peaks_force = [GUI.peak_force_cell1, GUI.peak_force_cell2, GUI.peak_force_cell3, GUI.peak_force_cell4, GUI.peak_force_cell5, GUI.peak_force_cell6, GUI.peak_force_cell7, GUI.peak_force_cell8, GUI.peak_force_cell9]
        GUI.peaks_distance = [GUI.peak_distance_cell1, GUI.peak_distance_cell2, GUI.peak_distance_cell3, GUI.peak_distance_cell4, GUI.peak_distance_cell5, GUI.peak_distance_cell6, GUI.peak_distance_cell7, GUI.peak_distance_cell8, GUI.peak_distance_cell9]
        GUI.peaks_time = [GUI.peak_time_cell1, GUI.peak_time_cell2, GUI.peak_time_cell3, GUI.peak_time_cell4, GUI.peak_time_cell5, GUI.peak_time_cell6, GUI.peak_time_cell7, GUI.peak_time_cell8, GUI.peak_time_cell9] 
        GUI.stemcounts=[GUI.cell1Count.get(),GUI.cell2Count.get(),GUI.cell3Count.get(),GUI.cell4Count.get(),GUI.cell5Count.get(),GUI.cell6Count.get(),GUI.cell7Count.get(),GUI.cell8Count.get(),GUI.cell9Count.get()]
        #GUI.stemspacing_average, GUI.EI_fullcontact, GUI.EI_nocontact, GUI.EI_intermediatecontact = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        GUI.stemspacing_average, GUI.EI_fullcontact, GUI.EI_nocontact, GUI.EI_intermediatecontact = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        print("GUI.stemcounts = ",GUI.stemcounts)
        for i in range(0,9): # FIX THIS AFTER DAQ, for EI post processing
            #try:
            #print("i=",i)
            #print("float(GUI.peaks_force[i])=",float(GUI.peaks_force[i]))
            #print("GUI.stemheight.get()=",GUI.stemheight.get())
            #print("GUI.barbottom.get()=",GUI.barbottom.get())
            #print("GUI.stemcounts[i]=",GUI.stemcounts[i])
            GUI.stemspacing_average[i], GUI.EI_fullcontact[i], GUI.EI_nocontact[i],GUI.EI_intermediatecontact[i] = FinalInputs.calculateEI(float(GUI.peaks_force[i]), GUI.stemheight.get(), GUI.barbottom.get(), GUI.stemcounts[i])
            #print("i=",i)
            #except:
            #GUI.stemspacing_average[i], GUI.EI_fullcontact[i], GUI.EI_nocontact[i] = 0,0,0                
        GUI.AvgEI_intermediatecontact = [0.0] # iitialize
        GUI.AvgEI_intermediatecontact[0] = round(sum(GUI.EI_intermediatecontact)/len(GUI.EI_intermediatecontact),3)
        FinalInputs.saveEIs()
        FinalInputs.save_compiled()
        time.sleep(1) # pause x seconds
        if refreshAllAuto == True:
            GUI.refreshAll() # refresh all variables 
        #except:
        #else:
        #    print("The nine cell scheme requires exactly 9 clips, 3 from each side hit.")
        
    
    def calculateEI(peak_force, stemheight, barbottom, stemcount):
        #try:
        #if stemcount > 0:
        stemspacing_average = 1/(stemcount/barlength)
        EI_fullcontact = src.physics.ei_interaction_error_management.EI_Interaction(peak_force, stemheight, barbottom,stemspacing_average) # uses clicked forces (Y axis), force bar height, horizontal plot heights, and count density
        EI_nocontact = src.physics.ei_no_interaction_error_management.ei_calc_no(peak_force, stemheight, barbottom, stemspacing_average) # the x value of the click does nothing other than find the nearest height from horz. It is not factored in to the number of beams or the character of the beams. 
        EI_intermediatecontact = (EI_fullcontact + EI_nocontact)/2
        src.physics.ei_interaction_error_management.clear_all()
        src.physics.ei_no_interaction_error_management.clear_all()
        #except:
        #else:
        #    print('stemcount=0. Please input stemcount value.')
        '''
        stemspacing_average = 0 # if count is zero
        EI_fullcontact = 0 
        EI_nocontact = 0 
        EI_intermediatecontact = 0
        '''
            
        return stemspacing_average, EI_fullcontact, EI_nocontact, EI_intermediatecontact;
    
    def save_compiled():
        #print("Compiled Data button does not currently work correctly. Please develop.")
        # ned to change the way I handle filename_force : we need a base name, that is variety and plot
        # same for the peakcliclk setion.
        ''' write XSLX'''
        filename_compiled_xlsx = GUI.address + '/' + GUI.filename_force.get() + '_compiled.xlsx'
        
        filename_preTest_csv = GUI.address + '/' + GUI.filename_preTest.get() + '.csv'
        filename_forceSide1_csv = GUI.address + '/' + (GUI.filename_force.get()) + '_side1.csv'
        filename_forceSide2_csv = GUI.address + '/' + (GUI.filename_force.get()) + '_side2.csv'
        filename_forceSide3_csv = GUI.address + '/' + (GUI.filename_force.get()) + '_side3.csv'
        filename_peaksSide1_csv = GUI.address + '/' + (GUI.filename_force.get()) + '_side1_peaks.csv'
        filename_peaksSide2_csv = GUI.address + '/' + (GUI.filename_force.get()) + '_side2_peaks.csv'
        filename_peaksSide3_csv = GUI.address + '/' + (GUI.filename_force.get()) + '_side3_peaks.csv'
        filename_forceForward_csv = GUI.address + '/' + (GUI.filename_force.get()) + '_forward.csv'
        filename_EI_csv = GUI.address + '/' + GUI.filename_force.get() + '_EI.csv'
        filename_postTest_csv = GUI.address + '/' + (GUI.filename_postTest.get()) + '.csv'

        filenames_CSV_all = [filename_preTest_csv,filename_postTest_csv,filename_EI_csv,filename_peaksSide1_csv,filename_peaksSide2_csv,filename_peaksSide3_csv,filename_forceSide1_csv,filename_forceSide2_csv,filename_forceSide3_csv,filename_forceForward_csv]
        filenames_CSV_most = [filename_preTest_csv,filename_postTest_csv,filename_EI_csv,filename_peaksSide1_csv,filename_peaksSide2_csv,filename_peaksSide3_csv,filename_forceSide1_csv,filename_forceSide2_csv,filename_forceSide3_csv]
        sheetnames_XLSX_all = ['preTest','postTest','EI','peaks_side1','peaks_side2','peaks_side3','force_side1','force_side2','force_side3','force_forward']
        sheetnames_XLSX_most = ['preTest','postTest','EI','peaks_side1','peaks_side2','peaks_side3','force_side1','force_side2','force_side3']

        ''' test names, sans arduino'''
        filenames_CSV_some = [filename_preTest_csv,filename_postTest_csv,filename_EI_csv]
        sheetnames_XLSX_some = ['preTest','postTest','EI']

        writer = pd.ExcelWriter(filename_compiled_xlsx, engine='xlsxwriter')
        
        try:
            i=0 
            for csvfilename in filenames_CSV_all:
                df = pd.read_csv(csvfilename)
                df.to_excel(writer,sheet_name=sheetnames_XLSX_all[i])
                i+=1
            writer.save()
            print("filename_compiled_xlsx = "+filename_compiled_xlsx)
        except:
            try:
                i=0
                for csvfilename in filenames_CSV_most:
                    df = pd.read_csv(csvfilename)
                    df.to_excel(writer,sheet_name=sheetnames_XLSX_most[i])
                    i+=1
                writer.save()
                print("filename_compiled_xlsx = "+filename_compiled_xlsx)
                print("Forward hit data not included in compilation file.")
            except:
                try:
                    i=0
                    for csvfilename in filenames_CSV_some:
                        df = pd.read_csv(csvfilename)
                        df.to_excel(writer,sheet_name=sheetnames_XLSX_some[i])
                        i+=1
                    writer.save()
                    print("filename_compiled_xlsx = "+filename_compiled_xlsx)
                    print("Raw force data not included in compilation file.")
                except:
                    print("Generate at least a pre-test and post-test CSV file before trying to compile data.")
                           

    def on_show_frame_FinalInputs(self, event):
        #print("Flip to FinalInputs screen.")
        background_box = tk.Label(self, text="This is hidden text meant to cover up old text.", font = ("arial", 14, "bold"), fg = "ghost white", bg="ghost white")
        background_box.place(x=0,y=0)
        # Update stringname of postTest file, based on filename_force, if it exists. 
        filename_postTest = nameBlackBox("postTest",GUI.filename_postTest.get())
        GUI.filename_postTest.set(filename_postTest)

        # update filename text field, even if force page is never activated
        if (GUI.varietyname.get()!="" or GUI.plotname.get()!="") and (GUI.passfillednames_checkbox.get()==1): # checks if a varietyname or plotname has been given
            RecordForce.nameFresh(GUI.varietyname.get(),GUI.plotname.get()) # if so, autopopulate the basic filestructure
        filename_force = nameBlackBox("",GUI.filename_force.get())
        GUI.filename_force.set(filename_force)
        

        filename_label = tk.Label(self, text="Filename:"+filename_postTest, font = ("arial", 14, "bold"), fg = "dodgerblue3", bg="ghost white")    
        filename_label.place(x=0,y=0)
