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
        self.health = 100
        self.maxHealth = 100
        self.hudFont = pygame.font.Font("visitor1.ttf",13)
        self.hudFont.set_bold(True)
        self.xp = 30
        self.xpOnCurrentLevel = 0
        self.xpToNextLevel = 100
        self.xpNextLevel = 100
        self.hudPlayerIcon = pygame.transform.scale(pygame.image.load("images/HUDplayer.gif"),(40,40))
        self.xpLevel = 1

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
        self.drawHUD()
        self.collisionDetection()

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

    def drawHUD(self):
        #outLineColor = (240,180,0)
        outLineColor = (0,0,150)
        pygame.draw.rect(self.surface,outLineColor,(40,15,173,22))
        pygame.draw.rect(self.surface,(255,255,255),(46,17,165,8)) #health bar rect
        pygame.draw.rect(self.surface,(0,255,0),(46,17,(float(self.health)/float(self.maxHealth))*165,8))
        self.surface.blit(self.hudFont.render(str(int(self.health)) + '/' + str(int(self.maxHealth)),1,(0,0,0)),(50,15))
        pygame.draw.rect(self.surface,(255,255,255),(46,27,165,8)) #xp bar rect
        pygame.draw.rect(self.surface,(204,153,0),(46,27,(float(self.xpOnCurrentLevel)/float(self.xpToNextLevel))*165,8))
        self.surface.blit(self.hudFont.render(str(int(self.xp)) + '/' + str(self.xpNextLevel),1,(0,0,0)),(50,25))
        pygame.draw.circle(self.surface,outLineColor,(25,25),22)
        self.surface.blit(self.hudPlayerIcon,(5,5))
        self.surface.blit(self.hudFont.render("lvl " + str(self.xpLevel),1,(0,0,0)),(10,43))
        self.surface.blit(self.hudFont.render("Vapour",0,(0,0,0)),(45,5))

    def collisionDetection(self):
        a1x,a1y,a2x,a2y,a3x,a3y,a4x,a4y = 0,0,0,0,0,0,0,0
        pr = ((self.x,self.y),(self.x+self.cWidth,self.y),(self.x,self.y+self.cHeight),(self.x+self.cWidth,self.y+self.cHeight))
        tl,tr,bl,br,cx,cy = (0,1,2,3,4,5)
        x,y=0,1
        #print("collision detection")
        for block in self.level.blockList:
            if(len(block) >= 6):
                origin = (block[5][cx],block[5][cy])
                a1 = self.minusVector(block[5][tr],block[5][tl],origin)
                a2 = self.minusVector(block[5][tr],block[5][br],origin)
                pOrigin = (self.x+int(self.cWidth/2),self.y+int(self.cHeight/2))
                a3 = self.minusVector((self.x,self.y),(self.x,self.y+self.cHeight),pOrigin)
                a4 = self.minusVector((self.x,self.y),(self.x+self.cWidth,self.y),pOrigin)
                self.drawVector(a1,origin)
                self.drawVector(a2,origin)
                self.drawVector(a3,pOrigin)
                self.drawVector(a4,pOrigin)
                dp = self.dotProduct(block[5][tr],a1,origin)
                ms = (((a1[x]-origin[x])**2)+((a1[y]-origin[y])**2))
                s = float(dp)/float(ms)
                prjA1 = (s*(a1[x]-origin[x]),s*(a1[y]-origin[y]))
                print(prjA1,origin)
                #pygame.draw.rect(self.surface,(255,255,0),(prjA1[x]+origin[x],prjA1[y]+origin[y],2,2))
                pygame.draw.line(self.surface,(255,255,0),(prjA1[x]+origin[x],prjA1[y]+origin[y]),(prjA1[x]+origin[x],prjA1[y]+origin[y]),10)
                self.drawVector((prjA1[x]+origin[x],prjA1[y]+origin[y]),(block[5][tr]))

    def minusVector(self,v1,v2,origin):
        x,y= (0,1)
        v1x = v1[x]-origin[x]
        v1y = v1[y]-origin[y]
        v2x = v2[x]-origin[x]
        v2y = v2[y]-origin[y]
        return ((v1x-v2x)+origin[x],v1y-v2y+origin[y])

    def dotProduct(self,v1,v2,origin):
        x,y, = (0,1)
        #setup vectors around origin
        v1x = v1[x]-origin[x]
        v1y = v1[y]-origin[y]
        v2x = v2[x]-origin[x]
        v2y = v2[y]-origin[y]
        return ((v1x*v2x)+(v1y*v2y))
    
    def drawVector(self,v,origin):
        x,y = (0,1)
        pygame.draw.line(self.surface,(0,0,255),(v[x]+self.camera.x,v[y]+self.camera.y),(origin[x]+self.camera.x,origin[y]+self.camera.y),3)
