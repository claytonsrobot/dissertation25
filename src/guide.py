import tkinter as tk
import PIL.ImageTk
import PIL.Image

from gui_main import GUI
# Guide page 
class Guide(tk.Frame):
    def __init__(self, parent, controller): # automatically runs
        tk.Frame.__init__(self, parent)

        pageButtons = repeatPageButtons.showButtons(self, parent, controller)

        # button that enters Calibrate page/class
        calibrate_button = tk.Button(self, text = "Calibrate\nForce\nSensor", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2", command=lambda:GUI.show_frame(Calibrate)) #tares/zeros load cell
        calibrate_button.place(x = 510, y = 340)
        
        # instruction steps:
        '''
        Nine-cell scheme design:
        '''
        guide_frame = tk.LabelFrame(self, text='Nine-Cell Scheme',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        guide_frame.place(x = 0, y = 20)
        #guideHeader = tk.Label(self, text = "Nine-cell scheme design", font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=350,y=0)
        one = tk.Label(guide_frame, text = '1.  Equalize stem heights', font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        two = tk.Label(guide_frame, text = '2.  Record Variety and Plot names', font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        three = tk.Label(guide_frame, text = '3.  Enter stem height and cell location data', font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        four = tk.Label(guide_frame, text = '4.  Perform four SOCEM tests (3 side hits, 1 forward hit)', font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=3, column=0)
        five = tk.Label(guide_frame, text = '5.  Collect stems for mass, count, and diameters.', font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=4, column=0)
        six = tk.Label(guide_frame, text = '6.  Press compile to complete nine-cell data object.\nGo on to the next small plot!', font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=5, column=0)  
        
        try:
            # SOCEM diagram of use # 
            load = PIL.Image.open(directory+'/'+'GuideSOCEM_2022.png')
            load = load.resize((275,275))
            render = PIL.ImageTk.PhotoImage(load)
            img = tk.Label(self, image=render)
            img.image = render
            img.place(x = 520, y = 35)
        except:
            print("Guide image not found.")
