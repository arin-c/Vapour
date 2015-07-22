import os, sys, pygame

class Level:
    def __init__(self,filePath,levelWidth,levelHeight,surface):
        self.tileWidth, self.tileHeight = 20, 20
        self.blockList = list()
        self.gridList = list()
        self.filePath = self.loadFile(filePath)
        self.levelWidth = levelWidth
        self.levelHeight = levelHeight
        self.surface = surface

    def setSurface(self,surface):
        self.surface = surface

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

    def draw(self,surface = None):
        if(surface is None):
            surface = self.surface
        for tile in self.blockList:
            pygame.draw.rect(self.surface,(100,100,200),(tile[0],tile[1],tile[2],tile[3]))
            
