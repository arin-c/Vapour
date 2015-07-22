import os, sys, pygame

class Map:
    def __init__(self,filePath):
        self.filePath = self.loadFile(filePath)
        self.tileWidth, self.tileHeight = 20, 20
        self.blockList = list()
        self.gridList = list()
        
    def loadFile(self,filePath):
        file = list(open(filePath))
        lineCounter = 0
        charCounter = 0
        for line in file:
            lineCounter+=1
            charCounter = 0
            for char in line:
                charCounter+=1
                if(char != 'c' and char != '\n' and char != '\r'):
                    self.blockList.append(charCounter*self.tileWidth,lineCounter*self.tileHeight)
