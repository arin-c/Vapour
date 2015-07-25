import os,sys,pygame

class Camera():
    def __init__(self,width=500,height=500):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.width = width
        self.height = height

    def centre(self,player):
        self.x = player.startX-player.x
        self.y = player.startY-player.y
