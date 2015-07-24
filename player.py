import os,sys,pygame

class Player():
    def __init__(self,startX,startY,surface):
        self.x = startX
        self.y = startY
        self.velX = 8
        self.velY = 8
        self.w = 50
        self.h = 50
        self.xDir = "LEFT"
        self.jump = False
        self.doubleJump = False
        self.surface = surface

    def setSurface(self,surface):
        self.surface = surface

    def setLevel(self,passed_level):
        self.level = passed_level

    def move(self,direction):
        direction = direction.upper()
        if((direction == "UP" or direction == "JUMP") and not self.doubleJump):
            self.jump = True
        elif(direction == "LEFT"):
            self.x -= 8
        elif(direction == "RIGHT"):
            self.x += 8

    def draw(self):
        pygame.draw.rect(self.surface,(0,0,255),(self.x,self.y,self.w,self.h))
