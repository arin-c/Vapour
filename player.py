import os,sys,pygame,camera,math

class Player():
    def __init__(self,startX,startY,passed_camera,surface,rootFolder):
        self.x = self.startX = startX
        self.y = self.startY = startY
        self.camera = passed_camera
        self.velX = 16
        self.velY = 16
        self.cWidth = 45
        self.cHeight = 70
        self.sWidth = 45
        self.sHeight = 80
        self.xDir = "LEFT"
        self.jump = False
        self.doubleJump = False
        self.surface = surface
        self.fall = False
        self.rootFolder = rootFolder
        self.loadSprites()
        self.deltaAnim = 0

    def loadSprites(self):
        self.sprite_still = self.addAnimation(self.rootFolder+"/STILL",self.sWidth,self.sHeight)

    def addAnimation(self,rootFolder,width,height,flip = (False,False)):
        if(rootFolder.endswith('/')):
            rootFolder = rootFolder[:-1]
        if(os.path.isdir(rootFolder)):
            temp = []
            indexCounter = 0
            for stillImage in os.listdir(rootFolder):
                indexCounter+=1
                if(os.path.isfile(rootFolder+"/"+str(indexCounter)+".gif")):
                    temp.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(rootFolder+"/"+str(indexCounter)+".gif"),(int(width*self.camera.zoom),int(height*self.camera.zoom))),flip[0],flip[1]))
                elif(os.path.isfile(rootFolder+"/"+str(indexCounter)+".png")):
                    temp.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(rootFolder+"/"+str(indexCounter)+".png"),(int(width*self.camera.zoom),int(height*self.camera.zoom))),flip[0],flip[1]))
                elif(os.path.isfile(rootFolder+"/"+str(indexCounter)+".jpg")):
                    temp.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(rootFolder+"/"+str(indexCounter)+".jpg"),(int(width*self.camera.zoom),int(height*self.camera.zoom))),flip[0],flip[1]))
                elif(os.path.isfile(rootFolder+"/"+str(indexCounter)+".jpeg")):
                    temp.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(rootFolder+"/"+str(indexCounter)+".jpeg"),(int(width*self.camera.zoom),int(height*self.camera.zoom))),flip[0],flip[1]))
                else:
                    break
            return temp
        else:
            print("not a valid directory: " + rootFolder)
            return None

    def playAnimation(self,sprite,x,y,delay=3,flip=(False,False)):
        numFrames = len(sprite)
        for i in range(0,numFrames*delay):
            if((self.deltaAnim+i)%(numFrames*delay) == 0):
                self.surface.blit(pygame.transform.flip(sprite[int(math.ceil((i+1)/delay)-1)],flip[0],flip[1]),(int(x*self.camera.zoom+self.camera.x),int(y*self.camera.zoom+self.camera.y)))

    def setSurface(self,surface):
        self.surface = surface

    def setLevel(self,passed_level):
        self.level = passed_level

    def move(self,direction):
        direction = direction.upper()
        if((direction == "UP" or direction == "JUMP") and not self.doubleJump and self.checkSpace(self.x,self.y-self.velY,direction)[0]):
            self.jump = True
            self.velY = 16
        elif(direction == "UP" or direction == "JUMP"):
            self.y -= self.checkSpace(self.x,self.y-self.velY,direction)[1]

        if(direction == "LEFT" and self.checkSpace(self.x-self.velX,self.y,direction)[0]):
            self.x -= self.velX
            self.xDir = "LEFT"
        elif(direction == "LEFT"):
            self.x -= self.checkSpace(self.x-self.velX,self.y,"LEFT")[1]

        if(direction == "RIGHT" and self.checkSpace(self.x+self.velX,self.y,direction)[0]):
            self.x += self.velX
            self.xDir = "RIGHT"
        elif(direction == "RIGHT"):
            self.x += self.checkSpace(self.x+self.velX,self.y,"RIGHT")[1]

    def draw(self):
        self.deltaAnim += 1
        #pygame.draw.rect(self.surface,(0,0,255),(self.x+self.camera.x,self.y+self.camera.y,self.cWidth,self.cHeight))
        if(self.xDir == "LEFT"):
            self.playAnimation(self.sprite_still,self.x,self.y+(self.cHeight-self.sHeight))
        elif(self.xDir == "RIGHT"):
            self.playAnimation(self.sprite_still,self.x,self.y+(self.cHeight-self.sHeight),3,(True,False))

    def update(self):
        if(self.jump):
            if(self.checkSpace(self.x,self.y-self.velY,"UP")[0]):
                self.y-=self.velY
            else:
                self.y -= self.checkSpace(self.x,self.y-self.velY,"UP")[1]
                self.velY = 1
            self.velY-=1
            if(self.velY <= 0):
                self.jump = False
                self.fall = True
        elif(self.checkSpace(self.x,self.y+self.velY,"DOWN")[0] or self.fall): #if no space under or fall
            self.y+=self.velY
            if(self.velY < 30):
                self.velY+=1
        if(not self.checkSpace(self.x,self.y+self.velY,"DOWN")[0]):  #if there is space under the ground
            self.fall = False
            self.velY = 16
            self.y += self.checkSpace(self.x,self.y+self.velY,"DOWN")[1]

    def checkSpace(self,px,py,direction):
        x,y,w,h,bID = (0,1,2,3,4)
        gap = 0
        for block in self.level.blockList:
            if(not(block[y] >= py+self.cHeight or block[y]+block[h] <= py or block[x]+block[w] <= px or block[x] >= px+self.cWidth) and (block[bID] == '#' or block[bID] == '$' or block[bID] == '@' or block[bID] == '!' or block[bID] == '%' or block[bID] == '^')):
                if(direction == "UP" or direction == "JUMP"):
                    gap = self.y-(block[y]+block[h])
                elif(direction == "DOWN"):
                    gap = block[y]-(self.y+self.cHeight)
                elif(direction == "LEFT"):
                    gap = self.x-(block[x]+block[w])
                elif(direction == "RIGHT"):
                    gap = block[x]-(self.x+self.cWidth)
                return False,gap
        return True,gap
