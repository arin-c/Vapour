import os, sys, pygame

class Level:
    def __init__(self,filePath,levelWidth,levelHeight,surface):
        self.tileWidth, self.tileHeight = 20, 20
        self.blockList = list()
        self.gridList = list()
        self.levelWidth = levelWidth
        self.levelHeight = levelHeight
        self.surface = surface
        self.filePath = self.load(filePath)
        self.save("2sweg.txt")

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

    def load(self,filePath):
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

    def save(self,filePath):
        saveFile = open(filePath,'w')
        for row in self.gridList:
            for char in row:
                saveFile.write(char)
            saveFile.write("\n")

    def draw(self,surface = None):
        if(surface is None):
            surface = self.surface
        for tile in self.blockList:
            if(tile[4] == '#'): #if charID is # then draw red square
                pygame.draw.rect(self.surface,(180,30,30),(tile[0],tile[1],tile[2],tile[3]))
                pygame.draw.rect(self.surface,(250,30,30),(tile[0]+2,tile[1]+2,tile[2]-4,tile[3]-4))
