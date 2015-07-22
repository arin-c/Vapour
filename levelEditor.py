import os,sys,pygame,level

class LevelEditor:
    def __init__(self,passed_level=None):
        if(passed_level is None):
            self.level = level.Level("swag.txt",2000,2000)
        else:
            self.level = passed_level
