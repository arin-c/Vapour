import os,sys,pygame,level,camera
screen_width, screen_height = (500,500)

class LevelEditor:
    def __init__(self,surface,passed_camera,passed_level=None):
        self.surface = surface
        self.camera = passed_camera
        if(passed_level is None):
            self.level = level.Level("testLevel.txt",2000,2000,self.camera,self.surface)
        else:
            self.level = passed_level
            self.level.setSurface(self.surface)
        self.grid = True
        self.mouseX, self.mouseY = (0,0)
        self.gridMouseX,self.gridMouseY = (-1,-1)
        self.currentBID = '#'

    def draw(self):
        self.level.draw()
        if(self.grid):
            self.drawGrid()
        self.drawUI()

    def getLevel(self):
        return self.level

    def setLevel(self,passed_level):
        self.level = passed_level

    def drawGrid(self):
        if(self.grid):
            gridColor = (100,0,0)
            for x in range(int(self.level.width/self.level.tileWidth)+1):
                pygame.draw.line(self.surface,gridColor,(x*self.level.tileWidth+self.camera.x,0+self.camera.y),(x*self.level.tileWidth+self.camera.x,self.level.height+self.camera.y))
            for y in range(int(self.level.height/self.level.tileHeight)+1):
                pygame.draw.line(self.surface,gridColor,(0+self.camera.x,y*self.level.tileHeight+self.camera.y),(self.level.width+self.camera.x,y*self.level.tileHeight+self.camera.y))
            pygame.draw.rect(self.surface,gridColor,(self.gridMouseX*self.level.tileWidth+self.camera.x,self.gridMouseY*self.level.tileHeight+self.camera.y,self.level.tileWidth,self.level.tileHeight))

    def updateGrid(self):
        if(self.grid):
            mx = (self.mouseX-self.camera.x) - ((self.mouseX-self.camera.x)%self.level.tileWidth)  #round mouseX to a multiple of level tileWidth
            my = (self.mouseY-self.camera.y) - ((self.mouseY-self.camera.y)%self.level.tileHeight) #round mouseY to a multiple of level tileHeight
            self.gridMouseX = mx/self.level.tileWidth
            self.gridMouseY = my/self.level.tileHeight

    def update(self):
        self.mouseX,self.mouseY = pygame.mouse.get_pos()
        self.updateGrid()
        if(pygame.mouse.get_pressed()[0]):
            self.level.gridList[int(self.gridMouseY)][int(self.gridMouseX)] = self.currentBID
            self.level.blockList.append((self.gridMouseX*self.level.tileWidth,self.gridMouseY*self.level.tileHeight,self.level.tileWidth,self.level.tileHeight,self.currentBID))
            print("mouse was pressed")

    def drawUI(self):
        startX,startY,uiW,uiH = (0,screen_height-85,screen_width,85)
        pygame.draw.rect(self.surface,(30,30,30),(startX,startY,uiW,uiH))
        self.drawUIBlock((200,0,0),(startX+5,startY+5,35,35),'#')
        self.drawUIBlock((0,200,0),(startX+45,startY+5,35,35),'$')
        self.drawUIBlock((0,0,200),(startX+85,startY+5,35,35),'@')
        self.drawUIBlock((200,200,0),(startX+125,startY+5,35,35),'!')
        self.drawUIBlock((200,0,200),(startX+5,startY+45,35,35),'%')

    def drawUIBlock(self,color,rect,bID):
        x,y,w,h = (0,1,2,3)
        if(self.mouseX >= rect[x] and self.mouseX <= rect[x]+rect[w] and self.mouseY >= rect[y] and self.mouseY <= rect[y]+rect[h]):
            pygame.draw.rect(self.surface,color,rect)
            if(pygame.mouse.get_pressed()[0]):
                self.currentBID = bIDs
                print("bid = %s"%(bID))
        else:
            pygame.draw.rect(self.surface,(color[0]*0.6,color[1]*0.6,color[2]*0.6),rect)
