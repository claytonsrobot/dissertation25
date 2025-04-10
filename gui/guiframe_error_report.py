import tkinter as tk

from gui.gui_main import GUI
# error page for displaying errors
class ErrorReport(tk.Frame):

    def __init__(self, parent, controller): # automatically runs
        tk.Frame.__init__(self, parent)

        # button that returns to Geo. Inputs page
        initialInputs_button = tk.Button(self, text ="Initial\nInputs", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",command=lambda:GUI.show_frame(InitialInputs))
        initialInputs_button.place(x = 675, y = 316)
        # button that returns to RecordForce page
        recordForce_button = tk.Button(self, text = "Record\nForce",font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",command=lambda:GUI.show_frame(RecordForce))
        recordForce_button.place(x = 675, y = 225)
        
        scroll = tk.Scrollbar(self)
        
        self.ErrorCode_label = tk.Label(self, text = "Error Code\n(Location)",font = ("arial", 14, "bold"), fg = "gray3", bg = "ghost white").place(x = 179, y = 50)
        self.ErrorCodeList = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 10, height = 13, font = ("arial", 14, "bold"), fg = "dodgerblue3")
        self.ErrorCodeList.place(x = 175, y = 100)

        self.Error_label = tk.Label(self, text = "Description",font = ("arial", 14, "bold"), fg = "gray3", bg = "ghost white")
        self.Error_label.place(x = 400, y = 75)
        self.ErrorDesc = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 30, height = 13, font = ("arial", 14, "bold"), fg = "dodgerblue3")
        self.ErrorDesc.place(x = 289, y = 100)
        
    def showErrors2(self):

        self.ErrorCodeList.delete(0, 'end')
        self.ErrorDesc.delete(0, 'end')

        for e in range(len(GUI.errorCodes)):
            self.ErrorCodeList.insert(END, GUI.errorCodes[e])# inserts at end of listbox to actually display
            self.ErrorCodeList.see(END)# makes sure listbox is at end so it displays live data
            self.ErrorDesc.insert(END, GUI.errors[e])
            self.ErrorDesc.see(END)
