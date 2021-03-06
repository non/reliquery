#!/usr/bin/python
#
# notes:
#  - 32 columns of text at normal font
#  - 384 pixels of graphic width

from Adafruit_Thermal import *
from PIL import Image
from generator import *
from gpiozero import LED, Button
from os.path import dirname, realpath
from signal import pause
from socket import socket, AF_INET, SOCK_DGRAM
from subprocess import call

import network

base = dirname(realpath(__file__))

class Reliquery(object):

    generators = [Magic8, Tarot, Potion, Labyrinth, Tiles, Npc, Cave, Diagnostic]

    def __init__(self):
        self.ip = network.ip()
        self.done = False
        self.printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
        self.switch = Button(7)
        self.led = LED(18)
        self.button = Button(23)
        wheelpins = [26, 19, 13, 6, 5, 11, 9, 10]
        self.wheelbuttons = [Button(n) for n in wheelpins]

    def feed(self, n):
        self.printer.feed(n)

    def println(self, s):
        self.printer.println(s)

    def printImage(self, img, LaaT=False):
        self.printer.printImage(img, LaaT)

    def generate(self):
        mode = self.read_mode()
        if mode < 1 or 8 < mode:
            self.println("mode selector error (got mode %d)" % mode)
        else:
            g = self.generators[mode - 1]
            if g is None:
                self.println("no mode configured for mode %d" % mode)
            else:
                g.generate(self)
        self.feed(3)

    def read_mode(self):
        for i, b in enumerate(self.wheelbuttons):
            if b.is_pressed:
                return i + 1
        return 0

    def shutdown(self):
        self.done = True
        self.led.on()
        self.println("shutting down...")
        self.println("(wait 30s before unplugging.)")
        self.feed(3)
        call("sync")
        call(["shutdown", "-h", "now"])

    def tap(self):
        if not self.done:
            self.led.on()
            self.generate()
            self.led.blink(on_time=0.2, off_time=2.0)

    def print_banner(self):
        self.println('reliquery (ip: %s)' % self.ip)
        self.feed(1)
        self.println('choose a mode; then tap button')
        self.println('hold button to exit')
        self.println('have fun!')
        self.feed(3)

    def main(self):
        self.led.on()
        self.print_banner()
        self.button.when_released = self.tap
        self.button.when_held = self.shutdown
        self.led.blink(on_time=0.2, off_time=2.0)
        pause()

if __name__ == "__main__":
    Reliquery().main()
