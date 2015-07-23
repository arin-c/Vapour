import os,sys,pygame,level

class LevelEditor:
    def __init__(self,surface,passed_level=None):
        self.surface = surface
        if(passed_level is None):
            self.level = level.Level("testLevel.txt",2000,2000,self.surface)
        else:
            self.level = passed_level
            self.level.setSurface(self.surface)

    def draw(self):
        self.level.draw()
