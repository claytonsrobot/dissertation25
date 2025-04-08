'''
Title: environment.py
Author: Clayton Bennett
Created: 23 July 2024
'''
import platform
import sys
def windows():
    if 'win' in platform.platform().lower():
        windows=True
    else:
        windows=False
    return windows

def pyinstaller():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        pyinstaller = True
    else:
        pyinstaller = False
    return pyinstaller

def frozen():
    if getattr(sys, 'frozen', True):
        frozen = True
    else:
        frozen = False
    return frozen

def get_operatingsystem():
    return platform.system() #determine OS
