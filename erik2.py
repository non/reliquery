#!/usr/bin/python

from __future__ import print_function
from gpiozero import LED, Button
from signal import pause
import subprocess, time, socket, sys
from PIL import Image
from Adafruit_Thermal import *

#ledPin       = 18
#buttonPin    = 23
#holdTime     = 2     # Duration for button hold (shutdown)
#tapTime      = 0.01  # Debounce time for button taps

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

led = LED(18)
button = Button(23)
done = False

wheelpins = [26, 19, 13, 6, 5, 11, 9, 10]
wheelbuttons = [Button(n) for n in wheelpins]

def read_mode():
  for i, b in enumerate(wheelbuttons):
    if b.is_pressed:
      return i + 1
  return 0

print('initialized')

def print_ip():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 0))
        ip = s.getsockname()[0]
		printer.println('My IP address is ' + ip)
	except:
		printer.boldOn()
		printer.println('Network is unreachable.')
	printer.feed(3)


# Called when button is briefly tapped.  Invokes time/temperature script.
def tap():
  print('tap')
  if done:
    return
  led.on()
  print('doing something cool')
  print(read_mode())
  led.off()

# Called when button is held down.  Prints image, invokes shutdown process.
def hold():
  print('hold')
  return
  global done
  done = True
  led.on()
  printer.printImage(Image.open('gfx/goodbye.png'), True)
  printer.feed(3)
  subprocess.call("sync")
  subprocess.call(["shutdown", "-h", "now"])
  led.off()

led.on()

# Processor load is heavy at startup; wait a moment to avoid
# stalling during greeting.

###time.sleep(30)

print('starting...')

print_ip()

# Print greeting image
###printer.printImage(Image.open('gfx/hello.png'), True)
###printer.feed(3)
#GPIO.output(ledPin, GPIO.LOW)
led.off()

#button.when_pressed = lambda: print('press')
button.when_released = tap
button.when_held = hold

led.blink(on_time=0.2, off_time=2.0)

print('pause loop...')
pause()
