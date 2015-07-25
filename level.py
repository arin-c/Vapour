import os, sys, pygame,camera

class Level:
    def __init__(self,filePath,levelWidth,levelHeight,passed_camera,surface):
        self.tileWidth, self.tileHeight = 25, 25
        self.camera = passed_camera
        self.blockList = list()
        self.gridList = list()
        self.width = levelWidth
        self.height = levelHeight
        self.surface = surface
        self.filePath = self.load(filePath)
        self.save("2sweg.txt")
        self.loadSprites()

    def setSurface(self,surface):
        self.surface = surface

    def loadSprites(self):
        self.sprite_grass_TL = pygame.transform.scale(pygame.image.load("images/tiles/Grass_TL.png"),(self.tileWidth,self.tileHeight))
        self.sprite_grass_TM = pygame.transform.scale(pygame.image.load("images/tiles/Grass_TM.png"),(self.tileWidth,self.tileHeight))
        self.sprite_grass_TR = pygame.transform.scale(pygame.image.load("images/tiles/Grass_TR.png"),(self.tileWidth,self.tileHeight))
        self.sprite_grass_Centre = pygame.transform.scale(pygame.image.load("images/tiles/Grass_Centre.png"),(self.tileWidth,self.tileHeight))
        self.sprite_grass_L = pygame.transform.scale(pygame.image.load("images/tiles/Grass_L.png"),(self.tileWidth,self.tileHeight))
        self.sprite_grass_R = pygame.transform.scale(pygame.image.load("images/tiles/Grass_R.png"),(self.tileWidth,self.tileHeight))

    def insertSpaces(self,filePath):
        numOfChars_width = int(self.width/self.tileWidth)
        numOfChars_height = int(self.height/self.tileHeight)
        charCounter = 0
        lineCounter = 0
        for row in self.gridList:
            charCounter = 0
            for char in row:
                charCounter+=1
            if(charCounter < numOfChars_width):
                spacesToAdd = numOfChars_width-charCounter
                for i in range(spacesToAdd-1):
                    self.gridList[lineCounter].append(' ')
            lineCounter+=1
        if(lineCounter < numOfChars_height):
            spacesToAdd = numOfChars_height-lineCounter
            for j in range(spacesToAdd):
                self.gridList.append(list())
                for k in range(numOfChars_width-1):
                    self.gridList[lineCounter].append(' ')
                lineCounter+=1

    def load(self,filePath):
        print("loading file: %s"%(filePath))
        self.blockList = list()
        file = list(open(filePath))
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
        self.insertSpaces(filePath)

    def save(self,filePath):
        saveFile = open(filePath,'w')
        for row in self.gridList:
            for char in row:
                saveFile.write(char)
            saveFile.write("\n")

    def drawRect(self,color,rect):
        pygame.draw.rect(self.surface,color,((rect[0]+self.camera.x)*self.camera.zoom,(rect[1]+self.camera.y)*self.camera.zoom,rect[2]*self.camera.zoom,rect[3]*self.camera.zoom))

    def draw(self,surface = None):
        if(surface is None):
            surface = self.surface
        for tile in self.blockList:
            if(tile[4] == '#'):
                self.surface.blit(self.sprite_grass_Centre,(tile[0]+self.camera.x,tile[1]+self.camera.y))
            elif(tile[4] == '$'):
                self.surface.blit(self.sprite_grass_TM,(tile[0]+self.camera.x,tile[1]+self.camera.y))
            elif(tile[4] == '@'):
                self.surface.blit(self.sprite_grass_TL,(tile[0]+self.camera.x,tile[1]+self.camera.y))
            elif(tile[4] == '!'):
                self.surface.blit(self.sprite_grass_TR,(tile[0]+self.camera.x,tile[1]+self.camera.y))
            elif(tile[4] == '%'):
                self.surface.blit(self.sprite_grass_L,(tile[0]+self.camera.x,tile[1]+self.camera.y))
