#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import termios
import tty
import pigpio
import time
import signal 
from decimal import *
from thread import start_new_thread
import threading

DEBUG_NONE = 0
DEBUG_TYPICAL = 1
DEBUG_ALL = 2

class PiLights:
    RED_PIN   = 17
    GREEN_PIN = 22
    BLUE_PIN  = 24
    RED = 0
    GREEN = 1
    BLUE = 2

    DEBUG_NONE = 0
    DEBUG_TYPICAL = 1
    DEBUG_ALL = 2

    # fadeTime = The total time to move from one color to the next
    # loopTime = The total time to move through the entire pattern list
    # brightLevel = The total brightness to use
    # pattern = The array of patterns to transition between
    def mainLoop(self):
        while (self.kill == False):
            time.sleep(1)
            if (self.debug_level == DEBUG_ALL):
                print "Kill = " + str(self.kill)
                print "fadeTime = " + str(self.fadeTime)
                print "loopTime = " + str(self.loopTime)
        if (self.debug_level > DEBUG_NONE):
            print "Program Terminating"
   
    def __init__(self):
        self.debug_level = DEBUG_ALL  
        self.kill = False
        self.fadeTime = 30
        self.loopTime = 15
        self.brightLevel = 255
        self.pattern = [ [0, 0, 255],
                         [255, 0, 0],
                         [0, 255, 0],
                         [0, 0, 255] ]
        self.mainLoopThread = threading.Thread(target=self.mainLoop)
        self.mainLoopThread.daemon = True
        self.mainLoopThread.start()
        self.mainLoopLock = False

    def setFadeTime(self, ft):
        if (self.debug_level == DEBUG_ALL):
            print "setFadeTime(" + str(ft) + ")"
        self.fadeTime = ft

    def setLoopTime(self, lt):
        if (self.debug_level == DEBUG_ALL):
            print "setLoopTime(" + str(lt) + ")"
        self.loopTime = lt

    def setBrightLevel(self, bl):
        if (self.debug_level == DEBUG_ALL):
            print "setBrightLevel(" + str(bl) + ")"
        self.brightLevel = bl

    def killProgram(self):
        if (self.debug_level == DEBUG_ALL):
            print "killProgram()"
        self.kill = True
        self.mainLoopThread.join()




def runLoop():                  
    pi = pigpio.pi()
    
    try:
        while True:
            
            if kill:
                print "kill = True"
                break
            else:
                print "kill = False"

            print "fadeTime = " + str(fadeTime)
            print "loopTime = " + str(loopTime)
            print "brightne = " + str(brightLevel)
            time.sleep(2)

            continue

            for x in range (0, len(pattern)):
                currentR = pattern[x][RED]
                currentG = pattern[x][GREEN]
                currentB = pattern[x][BLUE]
                setLights(pi, RED_PIN, currentR, brightLevel)           
                setLights(pi, GREEN_PIN, currentG, brightLevel)
                setLights(pi, BLUE_PIN, currentB, brightLevel)            

                if (x == (len(pattern)-1)):
                    futureR = pattern[0][RED]
                    futureG = pattern[0][GREEN]
                    futureB = pattern[0][BLUE]
                else:
                    futureR = pattern[x+1][RED]
                    futureG = pattern[x+1][GREEN]
                    futureB = pattern[x+1][BLUE]

                print "Current [" + str(currentR) + "," + str(currentG) + "," + str(currentB) + "]"
                print " Future [" + str(futureR)  + "," + str(futureG)  + "," + str(futureB)  + "]"
                print "Incrementing by |" + str() + "| interval"
               
                rDone = False
                gDone = False
                bDone = False

                while True:
                    # current (positive direction) future
                    
                    if (((pattern[x][RED] <= futureR) and (currentR >= futureR)) or 
                        ((pattern[x][RED] >= futureR) and (currentR <= futureR))):
                        print "rDone is good"
                        rDone = True
                    
                    if (((pattern[x][GREEN] <= futureG) and (currentG >= futureG)) or 
                        ((pattern[x][GREEN] >= futureG) and (currentG <= futureG))):
                        print "gDone is good"
                        gDone = True
                    
                    if (((pattern[x][BLUE] <= futureB) and (currentB >= futureB)) or 
                        ((pattern[x][BLUE] >= futureB) and (currentB <= futureB))):
                        print "bDone is good"
                        bDone = True

                    if (rDone and bDone and gDone):
                        break

                    if (not rDone):
                        print "rDone is not good"
                        currentR = updateColor(currentR, ((futureR - pattern[x][RED]) / fadeTime))
                    if (not gDone):
                        print "gDone is not good"
                        currentG = updateColor(currentG, ((futureG - pattern[x][GREEN]) / fadeTime))
                    if (not bDone):
                        print "bDone is not good"
                        currentB = updateColor(currentB, ((futureB - pattern[x][BLUE]) / fadeTime))
                    time.sleep(.1)
                    setLights(pi, RED_PIN, currentR, brightLevel)           
                    setLights(pi, GREEN_PIN, currentG, brightLevel)
                    setLights(pi, BLUE_PIN, currentB, brightLevel)           
                    print "        [" + str(currentR) + "," + str(currentG) + "," + str(currentB) + "]" 
                time.sleep(loopTime / len(pattern))
    except KeyboardInterrupt:
        pass

    print ("Aborting...\n")
    setLights(pi, RED_PIN, 0, 0)
    setLights(pi, GREEN_PIN, 0, 0)
    setLights(pi, BLUE_PIN, 0, 0)

    time.sleep(0.5)

    pi.stop()


def updateColor(color, step):
    print step
    color += step
    if color > 255:
        return 255
    if color < 0:
        return 0

    return color

def setLights(pi, pin, brightness, bright):
    print ("Setting Pin " + str(pin) + " = " + str(brightness))
    brightness = updateColor(brightness, 0)
    realBrightness = int(int(brightness) * (float(bright) / 255.0))
    pi.set_PWM_dutycycle(pin, realBrightness)

