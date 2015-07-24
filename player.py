import os,sys,pygame

class Player():
    def __init__(self,startX,startY,surface):
        self.x = startX
        self.y = startY
        self.velX = 8
        self.velY = 8
        self.cWidth = 50
        self.cHeight = 50
        self.sWidth = 50
        self.sHeight = 50
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
        elif(direction == "LEFT" and self.checkSpace(self.x-self.velX,self.y)):
            self.x -= self.velX
        elif(direction == "RIGHT" and self.checkSpace(self.x+self.velX,self.y)):
            self.x += self.velX

    def draw(self):
        pygame.draw.rect(self.surface,(0,0,255),(self.x,self.y,self.cWidth,self.cHeight))

    def update(self):
        if(self.checkSpace(self.x,self.y+self.velY)):
            self.y+=self.velY
            print("free space down")
        else:
            print("no free space down")

    def checkSpace(self,px,py):
        x,y,w,h,bID = (0,1,2,3,4)
        for block in self.level.blockList:
            if(not(block[y] >= py+self.cHeight or block[y]+block[h] <= py or block[x]+block[w] <= px or block[x] >= px+self.cWidth) and (block[bID] == '#' or block[bID] == '4' or block[bID] == '3' or block[bID] == '2' or block[bID] == '1' or block[bID] == '0')):
                return False
        return True
