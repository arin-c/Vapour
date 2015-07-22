import os, sys, pygame

class Level:
    def __init__(self,filePath,levelWidth,levelHeight):
        self.tileWidth, self.tileHeight = 20, 20
        self.blockList = list()
        self.gridList = list()
        self.filePath = self.loadFile(filePath)
        self.levelWidth = levelWidth
        self.levelHeight = levelHeight
        
    def loadFile(self,filePath):
        print("loading file: %s"%(filePath))
        self.blockList = list()
        file = list(open(filePath))
        lineCounter = 0
        charCounter = 0
        for line in file:
            self.gridList.append(list())
            charCounter = 0
            for char in line:
                charCounter+=1
                if(char != '\n' and char != '\r'):
                    if(char != ' '):
                        self.blockList.append((charCounter*self.tileWidth,lineCounter*self.tileHeight,self.tileWidth,self.tileHeight,char))
                    self.gridList[lineCounter].append(char)
            lineCounter+=1
        print(self.gridList)
        print("File loaded.\nNum of blocks = %i"%(len(self.blockList)))
