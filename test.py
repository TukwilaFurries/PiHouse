#!/usr/bin/python
# -*- coding: utf-8 -*-
from light_controller import *
import time
if __name__ == '__main__':
	piLights = PiLights()
	for x in range(0, 10):
		piLights.setFadeTime(x)
		piLights.setLoopTime(x)
		time.sleep(.5)
	piLights.killProgram()
