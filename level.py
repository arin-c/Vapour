import os, sys, pygame

class Level:
    def __init__(self,filePath,levelWidth,levelHeight,surface):
        self.tileWidth, self.tileHeight = 20, 20
        self.blockList = list()
        self.gridList = list()
        self.levelWidth = levelWidth
        self.levelHeight = levelHeight
        self.surface = surface
        self.filePath = self.loadFile(filePath)

    def setSurface(self,surface):
        self.surface = surface

    def insertSpaces(self,filePath):
        numOfChars_width = int(self.levelWidth/self.tileWidth)
        numOfChars_height = int(self.levelHeight/self.tileHeight)
        file = list(open(filePath,'r'))
        lineCounter = 0
        charCounter = 0
        for line in file:
            charCounter = 0
            for char in line:
                charCounter+=1
            if(charCounter <= numOfChars_width):
                charCounter = charCounter
        lineCounter+=1

    def loadFile(self,filePath):
        print("loading file: %s"%(filePath))
        self.blockList = list()
        file = list(open(filePath))
        self.insertSpaces(filePath)
        lineCounter = 0
        charCounter = 0
        for line in file:
            self.gridList.append(list())
            charCounter = 0
            for char in line:
                if(char != '\n' and char != '\r'):
                    if(char != ' '):
                        self.blockList.append((charCounter*self.tileWidth,lineCounter*self.tileHeight,self.tileWidth,self.tileHeight,char))
                    self.gridList[lineCounter].append(char)
                charCounter+=1
            lineCounter+=1
        print(self.gridList)

    def draw(self,surface = None):
        if(surface is None):
            surface = self.surface
        for tile in self.blockList:
            pygame.draw.rect(self.surface,(100,100,200),(tile[0],tile[1],tile[2],tile[3]))
