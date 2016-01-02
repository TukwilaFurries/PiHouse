#!/usr/bin/python

class Pattern:
   numColors = 0
   fadeTime = 0
   loopTime = 0
   brightLevel = 0

   def __init__(self, numColorsIn, fadeTimeIn, loopTimeIn, brightLevelIn):
      self.numColors = numColorsIn
      self.fadeTime = fadeTimeIn
      self.loopTime = loopTimeIn
      self.brightLevel = brightLevelIn

   def __getnumColors__(self):
      return self.numColors

   def __getfadeTime__(self):
      return self.fadeTime

   def __getloopTime__(self):
      return self.loopTime

   def __getbrightLevel__(self):
      return self.brightLevel
