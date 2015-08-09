import os,sys,pygame,camera,math,missile
from euclid import *
import random

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
        self.missile = [200,200,40,25,0] #x,y,width,height and rotation(degrees)
        self.trail = []
        self.missiles = []
        self.currentWeapon = "MISSILE"
        self.currentState = "STILL"
        self.pSurface = pygame.Surface((500,500),flags = pygame.SRCALPHA)

    def loadSprites(self):
        self.sprite_still = self.addAnimation(self.rootFolder+"/STILL",self.sWidth,self.sHeight)
        self.sprite_walk = self.addAnimation(self.rootFolder+"/SwagWalk",self.sWidth,self.sHeight)

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
                try:
                    self.surface.blit(pygame.transform.flip(sprite[len(sprite)-int(math.ceil((i+1)/delay)-1)-1],flip[0],flip[1]),(int(x*self.camera.zoom+self.camera.x),int(y*self.camera.zoom+self.camera.y)))
                    print(len(sprite)-int(math.ceil((i+1)/delay)-1))
                except:
                    self.surface.blit(pygame.transform.flip(sprite[0],flip[0],flip[1]),(int(x*self.camera.zoom+self.camera.x),int(y*self.camera.zoom+self.camera.y)))
                    
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
            self.currentState = "WALK"
        elif(direction == "LEFT"):
            self.x -= self.checkSpace(self.x-self.velX,self.y,"LEFT")[1]
            self.currentState = "WALK"
            
        if(direction == "RIGHT" and self.checkSpace(self.x+self.velX,self.y,direction)[0]):
            self.x += self.velX
            self.xDir = "RIGHT"
            self.currentState = "WALK"
        elif(direction == "RIGHT"):
            self.x += self.checkSpace(self.x+self.velX,self.y,"RIGHT")[1]
            self.currentState = "WALK"

    def draw(self):
        self.deltaAnim += 1
        # pygame.draw.rect(self.surface,(0,0,255),(self.x+self.camera.x,self.y+self.camera.y,self.cWidth,self.cHeight))
        if(self.xDir == "LEFT"):
            if(self.currentState == "STILL"):
                self.playAnimation(self.sprite_still,self.x,self.y+(self.cHeight-self.sHeight))
            elif(self.currentState == "WALK"):
                self.playAnimation(self.sprite_walk,self.x,self.y+(self.cHeight-self.sHeight))
        elif(self.xDir == "RIGHT"):
            if(self.currentState == "STILL"):
                self.playAnimation(self.sprite_still,self.x,self.y+(self.cHeight-self.sHeight),3,(True,False))
            elif(self.currentState == "WALK"):
                self.playAnimation(self.sprite_walk,self.x,self.y+(self.cHeight-self.sHeight),3,(True,False))
        self.drawHUD()
        self.collisionDetection((self.x,self.y))
        self.pSurface.fill(pygame.Color(0,0,0,0))
        for m in self.missiles:
            m.drawParticles()
            self.surface.blit(self.pSurface,(0,0))
        for m in self.missiles:
            m.draw()

    def update(self):
        for m in self.missiles:
            m.setTarget(pygame.mouse.get_pos())
            m.update()
            if(m.dead):
                self.missiles.remove(m)
                print("hit")
                #break
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
            if(len(block) < 6 and not(block[y] >= py+self.cHeight or block[y]+block[h] <= py or block[x]+block[w] <= px or block[x] >= px+self.cWidth) and (block[bID] == '#' or block[bID] == '$' or block[bID] == '@' or block[bID] == '!' or block[bID] == '%' or block[bID] == '^')):
                if(direction == "UP" or direction == "JUMP"):
                    gap = self.y-(block[y]+block[h])
                elif(direction == "DOWN"):
                    gap = block[y]-(self.y+self.cHeight)
                elif(direction == "LEFT"):
                    gap = self.x-(block[x]+block[w])
                elif(direction == "RIGHT"):
                    gap = block[x]-(self.x+self.cWidth)
                return False,gap
        # return not(self.collisionDetection((px,py))),gap
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

    def collisionDetection(self,(px,py)):
        pr = ((self.x,self.y),(self.x+self.cWidth,self.y),(self.x,self.y+self.cHeight),(self.x+self.cWidth,self.y+self.cHeight))
        tl,tr,bl,br,cx,cy = (0,1,2,3,4,5)
        x,y=0,1
        p_origin = (px+int(self.cWidth/2),py+int(self.cHeight/2))
        collision = False
        for block in self.level.blockList:
            if(len(block) >= 6): #if block is rotated
                b = block[5]
                origin = (b[cx],b[cy])
                b_tl = Vector2(b[tl][x]-origin[x],b[tl][y]-origin[y])
                b_tr = Vector2(b[tr][x]-origin[x],b[tr][y]-origin[y])
                b_bl = Vector2(b[bl][x]-origin[x],b[bl][y]-origin[y])
                b_br = Vector2(b[br][x]-origin[x],b[br][y]-origin[y])
                p_tl = Vector2(self.x-origin[x],self.y-origin[y])
                p_tr = Vector2(self.x+self.cWidth-origin[x],self.y-origin[y])
                p_br = Vector2(self.x+self.cWidth-origin[x],self.y+self.cHeight-origin[y])
                p_bl = Vector2(self.x-origin[x],self.y+self.cHeight-origin[y])
                axis1 = (b_tr-b_tl).normalize()
                axis2 = (b_tr-b_br).normalize()
                axis3 = (p_tl-p_bl).normalize()
                axis4 = (p_tl-p_tr).normalize()
                self.drawAxis(axis1,origin)
                self.drawAxis(axis2,origin)
                self.drawAxis(axis3,p_origin)
                self.drawAxis(axis4,p_origin)
                pPos = (px,py)
                f1 = self.checkAxis(block,axis1,pPos)
                if(not f1):
                    continue
                f2 = self.checkAxis(block,axis2,pPos)
                if(not f2):
                    continue
                f3 = self.checkAxis(block,axis3,pPos)
                if(not f3):
                    continue
                f4 = self.checkAxis(block,axis4,pPos)
                if(f1 and f2 and f3 and f4):
                    print("collision")
                    collision = True
                    break
                else:
                    print("no collision")
        return collision

    def checkAxis(self,block,axis,(px,py)):
        tl,tr,bl,br,cx,cy = (0,1,2,3,4,5)
        x,y = (0,1)
        origin = (block[5][cx],block[5][cy])
        p_origin = (px+int(self.cWidth/2),py+int(self.cHeight/2))
        b = block[5]
        b_tl = Vector2(b[tl][x]-origin[x],b[tl][y]-origin[y])
        b_tr = Vector2(b[tr][x]-origin[x],b[tr][y]-origin[y])
        b_bl = Vector2(b[bl][x]-origin[x],b[bl][y]-origin[y])
        b_br = Vector2(b[br][x]-origin[x],b[br][y]-origin[y])
        p_tl = Vector2(px-origin[x],py-origin[y])
        p_tr = Vector2(px+self.cWidth-origin[x],py-origin[y])
        p_br = Vector2(px+self.cWidth-origin[x],py+self.cHeight-origin[y])
        p_bl = Vector2(px-origin[x],py+self.cHeight-origin[y])
        projected_tr = self.project(p_tr,axis)
        projected_tl = self.project(p_tl,axis)
        projected_bl = self.project(p_bl,axis)
        projected_br = self.project(p_br,axis)
        projected_b_tr = self.project(b_tr,axis)
        projected_b_tl = self.project(b_tl,axis)
        projected_b_bl = self.project(b_bl,axis)
        projected_b_br = self.project(b_br,axis)
        cX,cY = self.camera.x,self.camera.y
        pygame.draw.line(self.surface,(0,0,0),(projected_tr[x]+origin[x]+cX,projected_tr[y]+origin[y]+cY),(px+self.cWidth+cX,py+cY))
        pygame.draw.line(self.surface,(0,0,0),(projected_tl[x]+origin[x]+cX,projected_tl[y]+origin[y]+cY),(px+cX,py+cY))
        pygame.draw.line(self.surface,(255,0,0),(projected_b_tr[x]+origin[x]+cX,projected_b_tr[y]+origin[y]+cY),(b[tr][x]+cX,b[tr][y]+cY),2)
        pygame.draw.line(self.surface,(255,0,0),(projected_b_tl[x]+origin[x]+cX,projected_b_tl[y]+origin[y]+cY),(b[tl][x]+cX,b[tl][y]+cY),2)
        pygame.draw.line(self.surface,(255,0,0),(projected_b_bl[x]+origin[x]+cX,projected_b_bl[y]+origin[y]+cY),(b[bl][x]+cX,b[bl][y]+cY),2)
        pygame.draw.line(self.surface,(255,0,0),(projected_b_br[x]+origin[x]+cX,projected_b_br[y]+origin[y]+cY),(b[br][x]+cX,b[br][y]+cY),2)
        pygame.draw.line(self.surface,(255,0,0),(projected_bl[x]+origin[x]+cX,projected_bl[y]+origin[y]+cY),(px+cX,py+self.cHeight+cY))
        pygame.draw.line(self.surface,(255,0,0),(projected_br[x]+origin[x]+cX,projected_br[y]+origin[y]+cY),(px+self.cWidth+cX,py+self.cHeight+cY))
        projected_tr = Vector2(projected_tr[x],projected_tr[y])
        projected_tl = Vector2(projected_tl[x],projected_tl[y])
        projected_bl = Vector2(projected_bl[x],projected_bl[y])
        projected_br = Vector2(projected_br[x],projected_br[y])
        projected_b_tr = Vector2(projected_b_tr[x],projected_b_tr[y])
        projected_b_tl = Vector2(projected_b_tl[x],projected_b_tl[y])
        projected_b_bl = Vector2(projected_b_bl[x],projected_b_bl[y])
        projected_b_br = Vector2(projected_b_br[x],projected_b_br[y])
        s1 = projected_br.dot(axis)
        s2 = projected_bl.dot(axis)
        s3 = projected_tr.dot(axis)
        s4 = projected_tl.dot(axis)
        sb1 = projected_b_tr.dot(axis)
        sb2 = projected_b_tl.dot(axis)
        sb3 = projected_b_bl.dot(axis)
        sb4 = projected_b_br.dot(axis)
        box_a = (s1,s2,s3,s4)
        box_b = (sb1,sb2,sb3,sb4)
        minA = min(box_a)
        maxA = max(box_a)
        minB = min(box_b)
        maxB = max(box_b)
        if(minB <= maxA and maxB >= minA):
            return True
        else:
            return False

    def drawAxis(self,axis,origin):
        x,y = (0,1)
        pygame.draw.line(self.surface,(0,255,255),(-axis.x*300+origin[x]+self.camera.x,-axis.y*300+origin[y]+self.camera.y),(axis.x*200+origin[x]+self.camera.x,axis.y*200+origin[y]+self.camera.y),2)
        
    def project(self,point,axis):
        try:
            x = y = point.dot(axis)/axis.magnitude_squared()
        except:
            x,y = (0,0)
        return (axis.x*x,axis.y*y)

    def attack(self):
        if(self.currentWeapon == "MISSILE"):
            self.missiles.append(missile.Missile(self.x+int(self.sWidth/2)+self.camera.x,self.y+int(self.sHeight/2)+self.camera.y,self.surface,self.pSurface,self.camera,(0,0)))
