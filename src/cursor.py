from matplotlib.widgets import Cursor
class Cursor(object):
    '''
    Cursor crosshair that follows mouse
    '''

    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='orange', linewidth=1, linestyle="--")
        self.ly = ax.axvline(color='orange', linewidth=1, linestyle="--")
        #text location in axes coords
        self.txt = ax.text(0.7, 0.9, '',transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        #update line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        self.ax.figure.canvas.draw()
