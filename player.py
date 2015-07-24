import os,sys,pygame

class Player():
    def __init__(self,startX,startY):
        self.x = startX
        self.y = startY
        self.velX = 8
        self.velY = 8
        self.w = 50
        self.h = 50
        self.xDir = "LEFT"
        self.jump = False
        self.doubleJump = False

    def move(self,direction):
        direction = direction.upper()
        if((direction == "UP" or direction == "JUMP") and not self.doubleJump):
            self.jump = True
        elif(direction == "LEFT"):
            self.x -= 8
        elif(direction == "RIGHT"):
            self.x += 8
