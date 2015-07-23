import os,sys,pygame,level
screen_width, screen_height = (500,500)

class LevelEditor:
    def __init__(self,surface,passed_level=None):
        self.surface = surface
        if(passed_level is None):
            self.level = level.Level("testLevel.txt",2000,2000,self.surface)
        else:
            self.level = passed_level
            self.level.setSurface(self.surface)
        self.grid = True
        self.mouseX, self.mouseY = (0,0)
        self.gridMouseX,self.gridMouseY = (0,0)

    def draw(self):
        self.level.draw()
        if(self.grid):
            self.drawGrid()

    def getLevel(self):
        return self.level

    def setLevel(self,passed_level):
        self.level = passed_level

    def drawGrid(self):
        if(self.grid):
            for x in range(int(screen_width/self.level.tileWidth)):
                pygame.draw.line(self.surface,(0,255,0),(x*self.level.tileWidth,0),(x*self.level.tileWidth,screen_height))
            for y in range(int(screen_height/self.level.tileHeight)):
                pygame.draw.line(self.surface,(0,255,0),(0,y*self.level.tileHeight),(screen_width,y*self.level.tileHeight))

    def update(self):
        self.mouseX,self.mouseY = pygame.mouse.get_pos()
