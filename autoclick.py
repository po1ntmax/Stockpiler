from pynput.mouse import Controller,Button
import time
import numpy as np
from global_hotkeys import *

run_clicker = False
def toggle_clicker():
    global run_clicker
    if run_clicker:
        run_clicker=False
    else:
        run_clicker = True
register_hotkeys([[["f4"], None, toggle_clicker]])
start_checking_hotkeys()
mouse = Controller()
counter = 1

while True:
    time.sleep(0.5)
    if run_clicker:
        counter+=1
        print(counter)
        mouse.click(Button.left)