from itertools import zip_longest
import matplotlib.pyplot as plt
import numpy as np

import src.cursor
from src.gui_main import GUI

''' Figure Interation classes '''
class SnaptoCursor(object):
    '''
    Cursor crossshair snaps to nearest x, y point.
    '''
    def __init__(self, ax, x, y):
        self.ax = ax
        #self.lx = ax.axhline(color='gold') # horizontal line
        self.ly = ax.axvline(color='orange', linewidth=1, linestyle="--") # vertical line
        self.x = x
        self.y = y
        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        indx = min(np.searchsorted(self.x, x), len(self.x)-1)
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        #self.lx.set_ydata(y) # why is this commented out
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        #print('x=%1.2f, y=%1.2f' % (x, y))
        self.ax.figure.canvas.draw()


''' Peak click plotter methods'''
def initialPlot(distanceTraveled, forcePushed, timeElapsed, encoderWorked, variety_plotname_detail, documentationFolder,averageVelocity):
    fig, ax = plt.subplots()
    encoderWorked = encoderWorked_override 
    ''' vertical lines, for suggesting edge effect regions for forward tests '''
    if encoderWorked == True:  
        start = 50 # cm , cut off 1st 50cm = 20" usually #
        end = 305 # cm, cut off after 120 inches = 305 cm usually
    else:
        startDis = 50 # cut off 1st 50cm = 20" usually
        try:
            speed = averageVelocity # assume cm/ms . would need encode to work.....
            start = startDis/speed # CB edit # 20/speed # find t where SOCEM ~ 20" into plot
        except:
            speed = 50 # assume 50 cm/s
            start = startDis/speed # CB edit # 20/speed # find t where SOCEM ~ 20" into plot
        endDis = 305 # cut of after 120" usually
        end = endDis/speed # CB edit # time[-1] - (20/speed) # find t where SOCME ~ 20" before end of plot
        
        distance_referenced_input = str(input('Would you like to type in known distance points (y/n)? '))
        if distance_referenced_input == 'y':
            distance_referenced_PeakClick = True
        elif distance_referenced_input == 'n':
            distance_referenced_PeakClick = False
        else: # just in case
            distance_referenced_PeakClick = False
            
        if distance_referenced_PeakClick == True:
            startDisRef = (int(input('Start point x (in): ')))
            endDisRef = (int(input('End point x (in): ')))
              
        ''' '''
    maxPt = max(forcePushed)
    # draw cut off lines
    cutStart = [start, start]
    cutEnd = [end, end]
    cutLine = [0, maxPt]
    ax.plot(cutStart,cutLine, color = 'red') # start cut off line
    ax.plot(cutEnd, cutLine, color = 'red') # end cut off line
    
    
    # plot dis vs forcePushed    
    if encoderWorked == True:
        ax.plot(distanceTraveled, forcePushed, color='midnightblue')
        ax.set_xlabel('Distance (cm)')
        snap_cursor = SnaptoCursor(ax, distanceTraveled, forcePushed) # create snap cursor object
    # plot time vs forcePushed
    else:
        ax.plot(timeElapsed, forcePushed, color='midnightblue')
        ax.set_xlabel('Time (sec)')
        snap_cursor = SnaptoCursor(ax, timeElapsed, forcePushed) # create snap cursor object
        
    title3 = '\n*click outside plot if red lines good*'
    fig.suptitle(GUI.filename_force.get() + '\nCut off edges: click start x pt, then end x pt.' + title3)
    #ax.set_title('*click outside plot if red lines good*')
    ax.set_ylabel('Force (N)')
    
    snap = fig.canvas.mpl_connect('motion_notify_event', snap_cursor.mouse_move) # update snap cursor upon mouse movement

    xCut = [] # stores where to cut off ends of plot (eliminate edge effects)
    def click(event): # get x coord once mouse is pressed
        x = event.xdata
        if x is None:
            print('red lines')
            xCut.append((start))
            xCut.append((end))
        else:
            print('x clicked = %1.2f' % x)
            xCut.append((x))
          #  self.fig.canvas.mpl_disconnect(cid)
        if len(xCut) >= 2:
            fig.canvas.mpl_disconnect(cid)
            fig.canvas.mpl_disconnect(snap)
            #fig.canvas.set_window_title('InitialPlot')
            fig.canvas.manager.set_window_title('InitialPlot')
            if encoderWorked == True:
                savename = GUI.filename_force.get() + '_' + str(round(xCut[0],1)) + '-' + str(round(xCut[1],1)) + '_raw.PNG'
            elif encoderWorked == False and distance_referenced_PeakClick == True:
                savename = GUI.filename_force.get() + '_' + str(round(xCut[0],1)) + '-' + str(round(xCut[1],1)) + '_disref' + '_raw.PNG'
            elif encoderWorked == False and distance_referenced_PeakClick == False:
                savename = GUI.filename_force.get() + '_' + str(round(xCut[0],1)) + '-' + str(round(xCut[1],1)) + '_timebased' + '_raw.PNG'
            else:
                savename = GUI.filename_force.get() + '_' + str(round(xCut[0],1)) + '-' + str(round(xCut[1],1)) + '_else' + '_raw.PNG'
            ax.plot([xCut[0],xCut[0]],cutLine, color = 'orange', linewidth=1, linestyle="--") # start cut off line
            ax.plot([xCut[1],xCut[1]], cutLine, color = 'orange', linewidth=1, linestyle="--") # end cut off line
            #print("Initial plot show...")
            #plt.show()
            #print("Initial plot shown.")
            if not os.path.exists(documentationFolder):
              os.makedirs(documentationFolder) # Create documentationFolder because it does not exist
            print("did")
            plt.savefig(documentationFolder + '/' + savename)
            print("did2")
            plt.close(block)
            print("xCut = ",xCut)
        return xCut # return start & end x (dis. or time) pts
    
    cid = fig.canvas.mpl_connect('button_press_event', click) # connects click event
    print("cid")

    #clicked = snap_cursor.click()
    #print('clicked', snap_cursor.click.coords)
    plt.draw()
    plt.ion()
    plt.show() # never getting past this
    #plt.show(block=False) # never getting past this
    print("did4")
    print("encoderWorked = ",encoderWorked)
    print("distance_referenced_PeakClick = ",distance_referenced)
    if encoderWorked == True:
        return xCut
    elif encoderWorked == False and distance_referenced_PeakClick == True:
        return xCut, distance_referenced, disNew, i, j
    elif distance_referenced_PeakClick == False:
        disNew = []
        return xCut, distance_referenced, disNew, i, j
    print("Complete initial plot.")
    print("xCut, distance_referenced, disNew,i,j = ", xCut, distance_referenced, disNew,i,j)


###############################################################################

def choosePeaks(xData, forcePushed, xCut, variety_plotname_detail, encoderWorked, distance_referenced, documentationFolder):
    #please: EMBED THE MATPLOTLIB PLOT INTO A TKINTER WINDOW< WHICH CAB BE A POPUP< LEADING TO POPUP.MAINLOOP()
    encoderWorked = encoderWorked_override
    def nearest_pt(pt): # get nearest dis index to starting pt in disCut
        idx = (np.abs(np.asarray(xData)- pt)).argmin()
        #print('idx ', idx)
        return idx
    peakclick.peaks_force = [] # force peaks
    peakclick.peaks_xaxis = [] # x (distance) pt of force peak
    
    startIdx = nearest_pt(xCut[0]) # starting index
    #print('startIdx = ',startIdx) # , dis[startIdx])
    endIdx = nearest_pt(xCut[1])
    print('Closest distance pts: ', [xData[startIdx] , xData[endIdx]]) 
    xCenter = xData[startIdx:endIdx]
    fCenter = forcePushed[startIdx:endIdx]
    
    fig, ax = plt.subplots()
    #fig.canvas.set_window_title('ChoosePeaks')
    fig.canvas.manager.set_window_title('ChoosePeaks')
    fig.suptitle(GUI.filename_force.get() + '\nSelect Force Peaks, *click outside when done*')
    #fig.suptitle(GUI.filename_force.get() + '\nCut off edges: click start x pt, then end x pt.' + title3)
    #ax.set_title('*click outside when done*')
    ax.plot(xCenter, fCenter) # needed?
    maxPt = max(forcePushed)
    ax.set_xlim(min(xCenter)-5, max(xCenter)+5)
    ax.set_ylabel('Force (Newtons)')
    ''' # set secondary vertical axis
    xold = np.asarray(xCenter)
    xnew = xold*convert_NToLbs
    def forward(x):
        return np.interp(x, xold, xnew)
    def inverse(x):
        return np.interp(x, xnew, xold)
    axis_pounds = ax.secondary_yaxis('right', functions=(forward,inverse))
    axis_pounds.set_ylabel('Force (pounds)')
    '''
    if encoderWorked == True or distance_referenced_PeakClick == True:
        ax.set_xlabel('Distance (cm)')
    else:
        ax.set_xlabel('Time (sec)')
            
    cursor = src.cursor.Cursor(ax) # create snap cursor object
    cursorMove = fig.canvas.mpl_connect('motion_notify_event', cursor.mouse_move) # update snap cursor upon mouse movement
    
    closeplt = False
    def click(event): # get x coord once mouse is pressed
        y, x = event.ydata, event.xdata
        #if y is None and len(peakclick.peaks_force)>2: # requires 3 clicks, or the window wont close
        #if y is None and len(peakclick.peaks_force)>0: # requires 1 click, or the window wont close
        if y is None: # window will close whenever you click out of the axes frame.
            cursorMove = fig.canvas.mpl_connect('motion_notify_event', cursor.mouse_move) # update snap cursor upon mouse movement
            fig.canvas.mpl_disconnect(cid)
            fig.canvas.mpl_disconnect(cursorMove)
            # auto save file
            # example: CF452_24hr_4_23-156_disref_clicks.PNG
            if encoderWorked == True:
                savename = GUI.filename_force.get() + '_' + str(round(xCut[0],1)) + '-' + str(round(xCut[1],1)) + '_clicks.PNG'
            elif encoderWorked == False and distance_referenced_PeakClick == True:
                savename = GUI.filename_force.get() + '_' + str(round(xCut[0],1)) + '-' + str(round(xCut[1],1)) + '_disref' + '_clicks.PNG'
            elif encoderWorked == False and distance_referenced_PeakClick == False:
                savename = GUI.filename_force.get() + '_' + str(round(xCut[0],1)) + '-' + str(round(xCut[1],1)) + '_timebased' + '_clicks.PNG'
            plt.savefig(documentationFolder + '/' + savename)
            print("choosePeaks: ",savename)

            print('peaks_xaxis = ', peakclick.peaks_xaxis)

            # lists of numbers, from analysis choice
            xCutL = ['xCut(in)'] # Distance, analysis range
            tCutL = ['tCut(sec)']# Time, analysis range
            print("test")
            plt.close()

            if encoderWorked == True:
                peakclick.peaks_distance = peakclick.peaks_xaxis
                peakclick.peaks_time = peakclick.findmatchtime(forcePushed,distanceTraveled,timeElapsed,peaks_distance)
                print("peaks_force =",peakclick.peaks_force) 
            elif encoderWorked == False and distance_referenced_PeakClick == True:
                peakclick.peaks_distance = peakclick.peaks_xaxis
                peakclick.peaks_time = peakclick.findmatchtime(forcePushed,distanceTraveled,timeElapsed,peaks_distance)
                print("peaks_force =",peakclick.peaks_force)
            else: #elif encoderWorked == False and distance_referenced_PeakClick == False: # possible issue dave
                peakclick.peaks_time = peakclick.peaks_xaxis
                peakclick.peaks_distance = [0, 0, 0] # might error, if there are not three clicks
                print("peaks_force =",peakclick.peaks_force)
                
            peakclick.saveCSV(GUI.filename_force.get(),GUI.address)
            RecordForce.closedplt = True
        else:
            # print('Force clicked = %1.2f at %1.2f' % (y, x)) # hide, CB
            peakclick.peaks_force.append((y))
            peakclick.peaks_xaxis.append((x))
            '''
            peaks_force.append((y))
            peaks_xaxis.append((x))
            '''
            ax.scatter(x, y, color='red')
            cursorMove = fig.canvas.mpl_connect('motion_notify_event', cursor.mouse_move) # update snap cursor upon mouse movement
            fig.canvas.draw()
            
        if peakclick.peaks_force == []:
            quit()

    #plt.draw() # the magic ingredient
    plt.ion()
    #fig.canvas.draw()
    cid = fig.canvas.mpl_connect('button_press_event', click) # connects click event
    #fig.canvas.draw()
    plt.show()
        
# MAIN
class PeakClick:
    '''
    - Finish autoclicker by setting plt.show() into an inset tkinter gui popup, and then mainloop.
         Use: FigureCanvasTkAgg,NavigationToolbar2Tk,plt,Cursor.
    '''
    def __init__():
        PeakClick.peaks_force = []
        PeakClick.peaks_distance = []
        PeakClick.peaks_time = []
    
    def findmatchtime(forcePushed,distanceTraveled,timeElapsed,peaks_distance):
        i=0
        for peaks_distance_i in peaks_distance:
            peaks_time = timeElapsed[distanceTraveled.find(peaks_axis_i)]
            i+=1
        return peaks_time
    
    # peaks_force,peaks_distance,peaks_time = PeakClick.input(GUI.forcePushed,GUI.distanceTraveled,GUI.timeElapsed,GUI.filename_force.get(),GUI.address)
    def peakclick_do(forcePushed,distanceTraveled,timeElapsed,variety_plotname_detail,address,averageVelocity):
        
        #documentationFolder = GUI.address + '/' + 'documentation'
        documentationFolder = GUI.address # for PNG and raw data to go to the same place.
        if max(distanceTraveled) > 10: # Assess if the encoder worked or not. Assuems that if it worked, the max value would exceeed 1 inch.
            encoderWorked = True # 
        else: encoderWorked = False
        encoderWorked = encoderWorked_override # leaving this here means all graphs will be shown in force vs time

        #print('Encoder? ', encoderWorked)
        #print('max(distanceTraveled) = ', str(max(distanceTraveled)))
        print(GUI.filename_force.get())

        if useInitialPlot_PeackClick == True:
            if encoderWorked == False:
                xCut, distance_referenced, disNew,i,j = initialPlot(distanceTraveled, forcePushed, timeElapsed, encoderWorked, GUI.filename_force.get(), documentationFolder,averageVelocity)
            elif encoderWorked == True:
                xCut = initialPlot(distanceTraveled, forcePushed, timeElapsed, encoderWorked,GUI.filename_force.get(), documentationFolder,averageVelocity)
                distance_referenced_PeakClick = False
        else:
            xCut = [min(distanceTraveled),max(distanceTraveled)]
            tCut = [min(timeElapsed),max(timeElapsed)]
            distance_referenced_PeakClick = False
            
        if encoderWorked == True:
            print('Distance cut at: ', xCut) # cut forcePushed and horz!!! 
            #peakclick.peaks_force,peakclick.peaks_xaxis = choosePeaks(distanceTraveled, forcePushed, xCut,GUI.filename_force.get(),encoderWorked, distance_referenced_PeakClick,documentationFolder)
            choosePeaks(distanceTraveled, forcePushed, xCut,GUI.filename_force.get(),encoderWorked, distance_referenced_PeakClick,documentationFolder) 
        elif encoderWorked == False and distance_referenced_PeakClick == True:
            print('troubleshoot702')
            print('Distance cut at: ', xCut)
            #peakclick.peaks_force,peakclick.peaks_xaxis = choosePeaks(disNew, forcePushed, xCut,GUI.filename_force.get(),encoderWorked, distance_referenced_PeakClick, documentationFolder)
            choosePeaks(disNew, forcePushed, xCut,GUI.filename_force.get(),encoderWorked, distance_referenced_PeakClick, documentationFolder)
        else: #elif encoderWorked == False and distance_referenced_PeakClick == False: # possible issue dave
            xCut=tCut
            print('Time cut at: ', xCut)
            #peakclick.peaks_force,peakclick.peaks_xaxis = choosePeaks(timeElapsed, forcePushed, xCut,GUI.filename_force.get(),encoderWorked, distance_referenced_PeakClick, documentationFolder)
            choosePeaks(timeElapsed, forcePushed, xCut,GUI.filename_force.get(),encoderWorked, distance_referenced_PeakClick, documentationFolder)

        #peakclick.saveCSV(GUI.filename_force.get(),GUI.address)
        #return peakclick.peaks_force,peakclick.peaks_distance,peakclick.peaks_time

    def saveCSV(variety_plotname_detail,address):
        #print("not yet saved. develop.")
        filename_peaks_csv = GUI.address + "/" + GUI.filename_force.get() + "_peaks.csv"
        ''' write CSV'''
        GUI.data_peaks = [peakclick.peaks_force,peakclick.peaks_distance,peakclick.peaks_time]
        RecordForce.peaks_force = peakclick.peaks_force
        RecordForce.peaks_distance = peakclick.peaks_distance
        RecordForce.peaks_time = peakclick.peaks_time
        RecordForce.peaks_distance.insert(0, "PeaksDistance(cm)")
        RecordForce.peaks_force.insert(0, "PeaksForce(N)")
        RecordForce.peaks_time.insert(0 , "PeaksTime(sec)")
        columns_data_peaks = zip_longest(*GUI.data_peaks)
        with open(filename_peaks_csv,'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerows(columns_data_peaks)
        ''' end: write CSV '''
        print("filename_peaks_csv = "+filename_peaks_csv)
        RecordForce.peaks_force = peakclick.peaks_force
        RecordForce.peaks_distance = peakclick.peaks_distance
        RecordForce.peaks_time = peakclick.peaks_time

