import os,sys,pygame,math,random

class Missile:
    def __init__(self,startX,startY,passed_surface,passed_camera,trackingPos=(0,0)):
        self.x = startX
        self.y = startY
        self.surface = passed_surface
        self.rotation = 0
        self.trackX, self.trackY = trackingPos
        self.trail = []
        self.speed = 10
        self.width,self.height = (40,30)
        self.exploding = False
        self.deltaE = 0
        self.dead = False
        self.deltaAnim = 0
        self.camera = passed_camera
        self.loadSprites()

    def loadSprites(self):
        self.sprite_missile = pygame.transform.flip(pygame.transform.smoothscale(pygame.image.load("images/missile.png").convert_alpha(),(self.width,self.height)),True,False)
        self.explodingAnim = self.addAnimation("images/missile",100,100)

    def addAnimation(self,rootFolder,width,height,flip = (False,False)):
        if(rootFolder.endswith('/')):
            rootFolder = rootFolder[:-1]
        if(os.path.isdir(rootFolder)):
            temp = []
            indexCounter = 0
            for stillImage in os.listdir(rootFolder):

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
                indexCounter+=1
            return temp
        else:
            print("not a valid directory: " + rootFolder)
            return None

    def playAnimation(self,sprite,x,y,delay=3,flip=(False,False)):
        numFrames = len(sprite)
        for i in range(0,numFrames*delay):
            if((self.deltaAnim+i)%(numFrames*delay) == 0):
                self.surface.blit(pygame.transform.flip(sprite[int(math.ceil((i+1)/delay)-1)],flip[0],flip[1]),(int(x*self.camera.zoom+self.camera.x),int(y*self.camera.zoom+self.camera.y)))
                print(int(math.ceil((i+1)/delay)-1))
        
    def draw(self):
        if(not self.exploding):
            self.drawTrail()
            self.surface.blit(pygame.transform.rotate(self.sprite_missile,self.rotation),(self.x,self.y))
        elif(self.exploding):
            self.deltaE+=2
            #print(self.deltaAnim)
            self.deltaAnim +=1
            if(self.deltaAnim >= 19):
                self.deltaAnim = 0
                self.dead = True
            #pygame.draw.circle(self.surface,(255,255,0),(int(self.x+self.width/2),int(self.y+self.height/2)),self.deltaE)
            self.playAnimation(self.explodingAnim,int(self.x-self.width/2),int(self.y-self.height/2))

    def drawTrail(self):
        x,y,c = (0,1,2)
        for point in self.trail:
            if(point[c] >= 1):
                pygame.draw.circle(self.surface,(255,255,0),(int(point[x]+random.randint(-2,2)),int(point[y]+random.randint(-2,2))),int(12-point[c]))
            point[c]+=0.5
            if(point[c] >= 12):
                self.trail.remove(point)
        
    def update(self):
        if(not self.exploding):
            self.track()
            self.trail.append([self.x+int(self.width/2),self.y+int(self.height/2),0])

    def track(m):
        diffX = m.trackX - m.x
        diffY = m.trackY - m.y
        m.rotation = -math.degrees(math.atan2(diffY,diffX))
        velX = m.speed*((90-math.fabs(m.rotation))/90)
        velY = 0
        if(-m.rotation < 0):
            velY = -m.speed+math.fabs(velX)
        else:
            velY = m.speed-math.fabs(velX)
        m.x+=velX
        m.y+=velY
        if(diffX <= m.speed and diffX >= -m.speed and diffY <= m.speed and diffY >= -m.speed):
            m.exploding = True

    def setTarget(self,targetPos):
        self.trackX,self.trackY = targetPos
