import os
import pandas as pd
import sys
import tkinter as tk

from gui.gui_main import GUI

''' Methods'''

def overwriteGuard(filename):# prevents overwriting by checking if filename already exists in saving folder
        return os.path.exists(filename) # True = already exits, False = doesn't exist
    
def overwriteGuardPage(filename):# prevents overwriting by checking if filename already exists in saving folder
        #return os.path.exists(filename) # True = already exits, False = doesn't exist
        return False # force override
    
def data_display(visual): #changes display method    #DELETE?
    global visualizeDatastream
    visualizeDatastream = visual
    return visualizeDatastream

#if any error occurs, display popup error msg
def popup(error):
    popup = tk.Tk()
    popup.wm_title("Error")
    E_label = tk.Label(popup, text="A {} error occurred.".format(error), font=("arial", 12, "bold"))
    E_label.pack(side="top", fill="x", pady=10)               
    popup.mainloop()

def popup_chooseFolder():
    popup_chooseFolder = tk.Tk()
    popup_chooseFolder.wm_title("Choose Folder")
    E_label = tk.Label(popup_chooseFolder, text="Paste file output directory here.", font=("arial", 12, "bold"))
    #E_label.pack(side="top", fill="x", pady=10)
    E_label.grid(row=0, column=1)
    #GUI.addressInput.set("")
    folder_entry = tk.Entry(popup_chooseFolder, textvariable=GUI.addressInput, font = ("arial", 11, "bold"), width= 70, bg="white", fg="gray1")
    folder_entry.grid(row=1, column=1)
    save_button = tk.Button(popup_chooseFolder,text = "Save", font = ("arial", 14, "bold"), height = 1, width = 6, fg = "ghost white", bg = "dodgerblue3",command=lambda:updateAddress())
    save_button.grid(row=2, column=1)
    popup_chooseFolder.mainloop()
    
    ''' Frame: Folder Input Field''
    barset_frame = tk.LabelFrame(self, text='Bar Bottom Quickset',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
    barset_frame.place(x = 340, y = 230)
    ''' ''

def updateAddress():
    print("updateAddress is broken. Please develop.")
    print("GUI.addressInput.get() = ",GUI.addressInput.get())
    print("GUI.address = ",GUI.address)
    #GUI.address = GUI.addressInput.get() # broken right now
    #print("GUI.address = ",GUI.address)

def showErrors():
    GUI.show_frame(ErrorReport) # show Error Report page
    ErrorReport.showErrors2(GUI.frames[ErrorReport]) # display errors in lists

def update_filename_preTest():
    filename_preTest = nameBlackBox("preTest",GUI.filename_preTest.get())
    GUI.filename_preTest.set(filename_preTest)
    filename_all = filename_preTest.replace("preTest","all")
    GUI.filename_all.set(filename_all)

def testForNineCellFilename(): # used to identify when nine-cell force, distance, and time data exists, and passes it to state data.
    # the purpose of this is to avoid reopening CSV files in order to assess nine-cell data
    # because, we have to wait for counts after to assess EI
    # it would be easier to test right away to get peaks
    # have a check box for nine cell test
    # EI cannot be assessed for non-nine cell, because counts don't exist
    # if box not checked, post test frame goes to single input for stem count, one number, with another number for range distance of count
    # # Assessment is trigged at save state button push
    #ninecellfilename = GUI.varietyname.get()+","+GUI.plotname.get()+"_"
    ninecellfilename = GUI.varietyname.get()+","+GUI.plotname.get()
    ninecellfilename_side1 = ninecellfilename+"_side1"
    ninecellfilename_side2 = ninecellfilename+"_side2"
    ninecellfilename_side3 = ninecellfilename+"_side3"
    ninecellfilename_forward = ninecellfilename+"_foward"
    currentFilename_force = GUI.filename_force.get()
    # create GUI variable, for handling without reopening CSV's
    #if (currentFilename_force == ninecellfilename_side1):
    if (GUI.currentdirection.get() == "side1"):
        GUI.forcePushed_side1 = GUI.forcePushed
        GUI.distanceTraveled_side1 = GUI.distanceTraveled
        GUI.timeElapsed_side1 = GUI.timeElapsed
        #if (currentFilename_force == ninecellfilename_side2):
    if (GUI.currentdirection.get() == "side2"):
        GUI.forcePushed_side2 = GUI.forcePushed
        GUI.distanceTraveled_side2 = GUI.distanceTraveled
        GUI.timeElapsed_side2 = GUI.timeElapsed
        #if (currentFilename_force == ninecellfilename_side3):
    if (GUI.currentdirection.get() == "side3"):
        GUI.forcePushed_side3 = GUI.forcePushed
        GUI.distanceTraveled_side3 = GUI.distanceTraveled
        GUI.timeElapsed_side3 = GUI.timeElapsed
        #if (currentFilename_force == ninecellfilename_forward):
    if (GUI.currentdirection.get() == "forward"):
        GUI.forcePushed_forward = GUI.forcePushed
        GUI.distanceTraveled_forward = GUI.distanceTraveled
        GUI.timeElapsed_forward = GUI.timeElapsed
    


def rename(filename): #if filename already exists - prompt user to rename
    popup = tk.Tk()
    popup.wm_title('Prompt Rename')
    renameIt = tk.Label(popup, text = 'Filename\n"{}"\nalready exists in the saving location.\nPlease rename and press Save.'.format(filename), font = ('arial', 10, 'bold'))
    increment_button = tk.Button(popup,text = "Auto Modify", font = ("arial", 14, "bold"), height = 2, width = 6, fg = "ghost white", bg = "dodgerblue3",command=lambda:incrementRename(filename))
    overwrite_button = tk.Button(popup, text = "Overwrite", font = ("arial", 14, "bold"), height = 2, width = 6, fg = "ghost white", bg = "red4",command=lambda:overwrite(filename))
    
    
    renameIt.pack(side='top', fill='x', ipadx=10, ipady=10)
    increment_button.pack(side='top', fill='both', ipadx=10, ipady=1)
    overwrite_button.pack(side='top', fill='both', ipadx=10,ipady=1)

    popup.mainloop()
def renamePage(filename):
    print("Please develop, prevent pages from being overwritten in the filename_all spreadsheet")
    
def incrementRename(filename):
    print("please develop, auto modify filename")
    
def overwrite(filename):
    print("please develop, overwrite filename")
        
#closes GUI (from file menubar)
def close():
    createBackupFile()
    python = sys.executable
    os.execl(python, python, * sys.argv)



def incrementName(filename):
        hyphen = "_"
        # determine last few characters from a filename
        def incrementvars(filename):
            lastchar = filename[len(filename)-1]
            secondtolastchar = filename[len(filename)-2]
            thirdtolastchar = filename[len(filename)-3]
            lastcharandsecondtolastchar = str(secondtolastchar+lastchar)
            return lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar

        #check if the last two are hyphens. if there is more than one hypthen, remove the last character until there is only one hyphen.
        def hyphencheck(filename,hyphen,lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar):
            while lastchar == hyphen and secondtolastchar == hyphen: # if two hyphens at the end
                filename = filename[:-1] # remove last character
                incrementvars()
            return filename, lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar

        if filename == "": # default, if user tried to increment without inputting any varietyname, plotname, or filename
            filename = datestring+","+GUI.timestring.get()
            
        lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar = incrementvars(filename)
        filename, lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar = hyphencheck(filename,hyphen,lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar)
        
        if lastchar == hyphen: # if last character is a hyphen
            newName = str(filename+str("1"))
        elif secondtolastchar == hyphen and lastchar.isnumeric: # if single digit preceded by a hyphen
            #newName = str(filename+str(int(lastchar)+1))
            filename = filename[:-1] # remove last character
            newName = str(filename+str(int(lastchar)+1))
        elif thirdtolastchar == hyphen and lastcharandsecondtolastchar.isnumeric: # if double digits preceded by a hyphen
            filename = filename[:-1] # remove last character
            filename = filename[:-1] # remove last character
            newName = str(filename+str(int(lastcharandsecondtolastchar)+1))
        elif filename == "":
            newName = date
        else:
            newName = str(filename+"_1")
        return newName
        #GUI.filename_force.set(newName)
    
''' Edge cases: Filenaming '''
def nameDirectionScrub(filename):
    if ("_side1" in filename):
        filename=filename.replace("_side1","")
        print(filename)
    if ("_side2" in filename):
        filename=filename.replace("_side2","")
    if ("_side3" in filename):
        filename=filename.replace("_side3","")
    if ("_forward" in filename):
        filename=filename.replace("_forward","")
    if ("_postTest" in filename):
        filename=filename.replace("_postTest","")
    return filename

def nameMissing(varietyname,plotname):
    if varietyname == "":
        varietyname = datestring
    if plotname == "":
        plotname = GUI.timestring.get() # plotname = GUI.timestring.get() # if you want the timestring (serving at plotname) to not change...but then it will never change
    return varietyname, plotname

def nameBlackBox(direction,filename):
    varietyname = GUI.varietyname.get()
    plotname = GUI.plotname.get()
    check=GUI.passfillednames_checkbox.get()
    if GUI.filename_force.get()=="" and check==1 and direction=='':
        varietyname, plotname = nameMissing(varietyname, plotname)
        #print(varietyname, plotname)
        filename = str(varietyname+str(",")+plotname)
    elif GUI.filename_force.get()=="" and check==1 and direction!='':
        varietyname, plotname = nameMissing(varietyname, plotname)
        filename = str(varietyname+str(",")+plotname+"_"+direction)
    elif GUI.filename_force.get()=="" and check==0 and direction !='':
        filename = datestring+","+time.strftime("%H%M")+"_"+direction
    elif GUI.filename_force.get()!="" and check==1 and direction !='':
        varietyname, plotname = nameMissing(varietyname, plotname)
        filename = str(varietyname+str(",")+plotname+str("_")+direction)
    elif GUI.filename_force.get()!="" and check==0 and direction !='':
        if ("side1" in filename) or ("side2" in filename) or ("side3" in filename) or ("forward" in filename) or ("postTest" in filename):
            filename = nameDirectionScrub(GUI.filename_force.get())
            filename = filename+"_"+direction
        else:
            filename = filename+"_"+direction
    elif GUI.filename_force.get()=="" and check==0 and direction =='':
        filename = datestring+","+time.strftime("%H%M")
    elif GUI.filename_force.get()!="" and check==1 and direction =='':
        varietyname, plotname = nameMissing(varietyname, plotname)
        filename = str(varietyname+str(",")+plotname)
    elif GUI.filename_force.get()!="" and check==0 and direction =='':
        if ("side1" in filename) or ("side2" in filename) or ("side3" in filename) or ("forward" in filename) or ("postTest" in filename):
            filename = nameDirectionScrub(GUI.filename_force.get())
            filename = filename
        else:
            filename = filename
    #GUI.filename_postTest.set(filename_postTest)
    return filename
''' end: Edge cases: Filenaming '''

''' Single XLSX workbook created from all expected CSV files for 9-cell study'''
def generateXSLXcombinedFile():
    writer = pd.ExcelWriter('default.xlsx')
    for csvfilename in sys.ar[1:]:
        df = pd.read.csv(csvfilename)
        #FIX df.to_excel(writer.sheet_names=os.path.splitext(csvfilename)[0]) # "keyword cannot be an expression"
    writer.save()
    
def peakClickRunAndSave(filename):
    PeakClick() # you cannot put in counts first....because they haven't been collected yet!
    #ergo, run clicks after triggered XLSX workbook creation
''' trigger with button, on Initial Inputs page. Button also clears all data from stemberry, wait it dods not triggers PeakClick.py, which saves to a separate CSV before all CSV's are wrapped into a xlsx workbook.
'''