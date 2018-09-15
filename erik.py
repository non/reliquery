#!/usr/bin/python

from gpiozero import Button
from time import sleep
from Adafruit_Thermal import *

sys.exit(0)

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

printer.println('there are only')
printer.println('ten seconds left')
printer.println('to control this unit')
printer.feed(1)
#printer.println('')
printer.println('++++++++')
printer.println('')
printer.println('if you are not running')
printer.println('you will not make it')
printer.println('')
printer.println('++++++++')
printer.println('')
printer.println('in the end')
printer.println('we are all losing')
printer.println('the same game')

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults


