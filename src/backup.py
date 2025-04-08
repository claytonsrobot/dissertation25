import datetime
import time

import src.environment
from gui_main import GUI
def createBackupFile():
    ''' Create a temp text file, with a list of all variables and variable names, that would be awesome '''
    '''update_filename_preTest()
    update_filename_postTest()
    sniff_filename_force()
    update_filename_postTest()
    saveState_update_filenames()'''
    now = datetime.datetime.now()
    unix_now = time.mktime(now.timetuple())
    unix_now_int = int(unix_now) # still gets seconds # the purpose of this is to append to filenames
    str(unix_now_int)
    filename_savestate = "backup_stemberry_"+str(unix_now_int)+".txt"
    filename_savestate_full = GUI.address+"/"+filename_savestate
    print("State saved at "+str(datetime.datetime.fromtimestamp(unix_now_int))+": "+filename_savestate)
    # list all GUI vars, add them to a txt file
    GUI.masslist=[GUI.cell1Mass.get(),GUI.cell2Mass.get(),GUI.cell3Mass.get(),GUI.cell4Mass.get(),GUI.cell5Mass.get(),GUI.cell6Mass.get(),GUI.cell7Mass.get(),GUI.cell8Mass.get(),GUI.cell9Mass.get()] 
    GUI.stemcounts=[GUI.cell1Count.get(),GUI.cell2Count.get(),GUI.cell3Count.get(),GUI.cell4Count.get(),GUI.cell5Count.get(),GUI.cell6Count.get(),GUI.cell7Count.get(),GUI.cell8Count.get(),GUI.cell9Count.get()] 
    GUI.diameters_cell1 = [GUI.cell1Diameter1.get(),GUI.cell1Diameter2.get(),GUI.cell1Diameter3.get(),GUI.cell1Diameter4.get()]
    GUI.diameters_cell2 = [GUI.cell2Diameter1.get(),GUI.cell2Diameter2.get(),GUI.cell2Diameter3.get(),GUI.cell2Diameter4.get()]
    GUI.diameters_cell3 = [GUI.cell3Diameter1.get(),GUI.cell3Diameter2.get(),GUI.cell3Diameter3.get(),GUI.cell3Diameter4.get()]
    GUI.diameters_cell4 = [GUI.cell4Diameter1.get(),GUI.cell4Diameter2.get(),GUI.cell4Diameter3.get(),GUI.cell4Diameter4.get()]
    GUI.diameters_cell5 = [GUI.cell5Diameter1.get(),GUI.cell5Diameter2.get(),GUI.cell5Diameter3.get(),GUI.cell5Diameter4.get()]
    GUI.diameters_cell6 = [GUI.cell6Diameter1.get(),GUI.cell6Diameter2.get(),GUI.cell6Diameter3.get(),GUI.cell6Diameter4.get()]
    GUI.diameters_cell7 = [GUI.cell7Diameter1.get(),GUI.cell7Diameter2.get(),GUI.cell7Diameter3.get(),GUI.cell7Diameter4.get()]
    GUI.diameters_cell8 = [GUI.cell8Diameter1.get(),GUI.cell8Diameter2.get(),GUI.cell8Diameter3.get(),GUI.cell8Diameter4.get()]
    GUI.diameters_cell9 = [GUI.cell9Diameter1.get(),GUI.cell9Diameter2.get(),GUI.cell9Diameter3.get(),GUI.cell9Diameter4.get()]

    lines = [
        'Units: diameter (mm), height (cm), range (cm), length (cm), mass (g), time (sec), force (N) \n',
        'script = '+script,
        'directory = '+directory+'/',
        'operatingsystem = '+src.environment.get_operatingsystem(),
        'os.getlogin() = '+os.getlogin(),
        'operator = '+operator,
        'location = '+location,
        'coordinates = '+coordinates,
        'GUI.ignoreserial = '+str(GUI.ignoreserial),
        'default_stemheight = '+str(default_stemheight),
        'calibrationFactor = '+str(calibrationFactor),
        'encoderWorked_override = '+str(encoderWorked_override),
        'assessAllTests = '+str(assessAllTests),
        'barlength = '+str(barlength),
        'datestring = '+datestring,
        'unix_now_int = '+str(unix_now_int),
        'backup filename unix_now_int decoded: '+ str(datetime.datetime.fromtimestamp(unix_now_int))+'\n',
        'GUI.timestring.get() = '+GUI.timestring.get(),
        'GUI.errors = '+makeDataString(GUI.errors),
        'GUI.errorCodes = '+makeDataString(GUI.errorCodes),
        'GUI.varietyname.get() = '+GUI.varietyname.get(),
        'GUI.plotname.get() = '+GUI.plotname.get(),
        'GUI.currentdirection.get() = '+GUI.currentdirection.get(),
        'GUI.filename_force.get() = '+GUI.filename_force.get(),
        'GUI.filename_preTest.get() = '+GUI.filename_preTest.get(),
        'GUI.filename_postTest.get() = '+GUI.filename_postTest.get(),
        'GUI.stemheight.get() = '+str(GUI.stemheight.get()),
        'GUI.barmiddle.get() = '+str(GUI.barmiddle.get()),
        'GUI.barbottom.get() = '+str(GUI.barbottom.get()),
        'GUI.passfillednames_checkbox.get() = '+str(GUI.passfillednames_checkbox.get()),
        'GUI.startRange1.get() = '+str(GUI.startRange1.get()),
        'GUI.startRange2.get() = '+str(GUI.startRange2.get()),
        'GUI.startRange3.get() = '+str(GUI.startRange3.get()),
        'GUI.travelvelocity = '+str(GUI.travelvelocity),
        'GUI.samplingrate = '+str(GUI.samplingrate),
        'GUI.masslist = '+makeDataString(GUI.masslist),
        'GUI.stemcounts = '+makeDataString(GUI.stemcounts),
        'GUI.diameters_cell1 = '+makeDataString(GUI.diameters_cell1),
        'GUI.diameters_cell2 = '+makeDataString(GUI.diameters_cell2),
        'GUI.diameters_cell3 = '+makeDataString(GUI.diameters_cell3),
        'GUI.diameters_cell4 = '+makeDataString(GUI.diameters_cell4),
        'GUI.diameters_cell5 = '+makeDataString(GUI.diameters_cell5),
        'GUI.diameters_cell6 = '+makeDataString(GUI.diameters_cell6),
        'GUI.diameters_cell7 = '+makeDataString(GUI.diameters_cell7),
        'GUI.diameters_cell8 = '+makeDataString(GUI.diameters_cell8),
        'GUI.diameters_cell9 = '+makeDataString(GUI.diameters_cell9),
        'GUI.EI_fullcontact = '+makeDataString(GUI.EI_fullcontact),
        'GUI.EI_intermediatecontact = '+makeDataString(GUI.EI_intermediatecontact),
        'GUI.EI_nocontact = '+makeDataString(GUI.EI_nocontact),
        'GUI.AvgEI_intermediatecontact = '+makeDataString(GUI.AvgEI_intermediatecontact),
        str(datetime.datetime.now())+'\n']
    
    evenmorelines = [
        'GUI.filename_all.get() = '+GUI.filename_all.get(), # no longer exists, compilation XLSX
        'GUI.distanceTraveled = '+makeDataString(GUI.distanceTraveled),
        'GUI.forcePushed = '+makeDataString(GUI.forcePushed),
        'GUI.timeElapsed = '+makeDataString(GUI.timeElapsed)+'\n',
        'Collected data, nine cell scheme:',
        'GUI.forcePushed_side1 = '+makeDataString(GUI.forcePushed_side1),
        'GUI.distanceTraveled_side1 = '+makeDataString(GUI.distanceTraveled_side1),
        'GUI.timeElapsed_side1 = '+makeDataString(GUI.timeElapsed_side1),
        'GUI.forcePushed_side2 = '+makeDataString(GUI.forcePushed_side2),
        'GUI.distanceTraveled_side2 = '+makeDataString(GUI.distanceTraveled_side2),
        'GUI.timeElapsed_side2 = '+makeDataString(GUI.timeElapsed_side2),
        'GUI.forcePushed_side3 = '+makeDataString(GUI.forcePushed_side3),
        'GUI.distanceTraveled_side3 = '+makeDataString(GUI.distanceTraveled_side3),
        'GUI.timeElapsed_side3 = '+makeDataString(GUI.timeElapsed_side3),
        'GUI.forcePushed_forward = '+makeDataString(GUI.forcePushed_forward),
        'GUI.distanceTraveled_forward = '+makeDataString(GUI.distanceTraveled_forward),
        'GUI.timeElapsed_forward = '+makeDataString(GUI.timeElapsed_forward),
        str(datetime.datetime.now())]
        
    try:
        morelines = [
            '\n',
            'RecordForce.ser = '+str(RecordForce.ser),
            str(datetime.datetime.now())]
    except:
        morelines = [
            '\n',
            'RecordForce.ser = '+'error',
            str(datetime.datetime.now())]
    
    with open(filename_savestate_full, 'w') as f:
        f.write('\n'.join(lines))
        f.write('\n'.join(morelines))
        try:
            f.write('\n'.join(evenmorelines))
        except:
            pass

def makeDataString(dataVector):
    #timeElapsed_string = ' '.join(str(e) for e in GUI.timeElapsed)
    dataString = ', '.join(str(e) for e in dataVector)
    dataString = '[' + dataString + ']'
    
    return dataString

def restoreState():
    print("Please develop. Not yet functional for setting tkinter variables.")
    # choose txt file (example: backup_stemberry_1660192559.txt
    # trigger GUI directory and file selection would be sick.
    # only restore postTest fields? start there.
    # change each instance of '.get() = x' to '.set(x)'
    '''
    filename_savestate = "backup_stemberry_"+str(unix_now_int)+".txt"
    filename_savestate_full = GUI.address+"/"+filename_savestate
    '''
    filename_restorestate = (str(input('Restore backup filename: ')))

    #with open('readme.txt') as f:
    with open(GUI.address+"/"+filename_restorestate) as f:
        lines = f.readlines()
        
def importFileData():
    print("Please develop.")
    # imort data from csv files