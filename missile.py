import os,sys,pygame,math,random,particle
from euclid import *

class Missile:
    def __init__(self,startX,startY,passed_surface,passed_pSurface,passed_camera,trackingPos=(0,0)):
        self.x = startX
        self.y = startY
        self.surface = passed_surface
        self.rotation = 0
        self.trackX, self.trackY = trackingPos
        self.trail = []
        self.speed = 15
        self.width,self.height = (40,30)
        self.exploding = False
        self.deltaE = 0
        self.dead = False
        self.deltaAnim = 0
        self.camera = passed_camera
        self.loadSprites()
        self.particles = []
        self.pSurface = passed_pSurface

    def loadSprites(self):
        self.sprite_missile = pygame.transform.flip(pygame.transform.smoothscale(pygame.image.load("images/missile.png").convert_alpha(),(self.width,self.height)),True,False)
        self.explodingAnim = self.addAnimation("images/missile",120,120)
        self.particle_fire = pygame.image.load("images/particle/fire.png").convert_alpha()
        self.particle_smallfire = pygame.image.load("images/particle/small_fire.png").convert_alpha()
        self.particle_box = pygame.image.load("images/particle/box.png")

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
                    temp.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(rootFolder+"/"+str(indexCounter)+".png"),(int(width*self.camera.zoom),int(height*self.camera.zoom))),flip[0],flip[1]).convert_alpha())
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

    def playAnimation(self,sprite,x,y,delay=2,flip=(False,False)):
        numFrames = len(sprite)
        for i in range(0,numFrames*delay):
            if((self.deltaAnim+i)%(numFrames*delay) == 0):
                try:
                    self.surface.blit(pygame.transform.flip(sprite[len(sprite)-int(math.ceil((i+1)/delay)-1)-1],flip[0],flip[1]),(int(x*self.camera.zoom),int(y*self.camera.zoom)))
                except:
                    pass
        
    def draw(self):
        self.drawParticles()
        if(not self.exploding):
            self.surface.blit(pygame.transform.rotate(self.sprite_missile,-self.rotation),(self.x,self.y))
        elif(self.exploding):
            self.deltaE+=2
            self.deltaAnim +=1
            if(self.deltaAnim >= len(self.explodingAnim)*2):
                self.deltaAnim = len(self.explodingAnim)*2
            else:
                self.playAnimation(self.explodingAnim,int(self.x-60),int(self.y-60))

    def update(self):
        if(not self.exploding):
            self.track()
            self.trail.append([self.x+int(self.width/2),self.y+int(self.height/2),0])
        self.updateParticles()

    def drawParticles(self):
        for p in self.particles:
            p.draw()

    def updateParticles(self):
        if(not self.exploding):
            pps = 15 #particles per second
            for i in range(0,pps):
                self.particles.append(self.createParticle())
        for p in self.particles:
            p.update()
            if(p.duration <= 0):
                self.particles.remove(p)
        if(self.exploding and len(self.particles) == 0):
            self.dead = True

    def createParticle(self):
        ePos = (int(self.x+(self.width/2)),int(self.y+self.height/2))
        ri = random.randint(0,1)
        if(ri == 0):
            texture = self.particle_fire
        elif(ri == 1):
            texture = self.particle_smallfire
        position = Vector2(ePos[0],ePos[1])
        vel = Vector2(random.uniform(-1,1),random.uniform(-1,1))
        angle = 0
        angularVelocity = random.uniform(-0.1,0.1)
        #color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        color = (0,0,0)
        #size = random.randint(7,16)
        size = random.randint(7,16)
        duration = 20+random.randint(0,40)
        return particle.Particle(self.pSurface,texture,position,vel,angle,angularVelocity,color,size,duration)

    def track(m):
        diffX = m.trackX - m.x
        diffY = m.trackY - m.y
        ease = 10
        rotation = math.degrees(math.atan2(diffY,diffX))
        if(math.fabs(rotation-m.rotation) > 180):
            if(rotation > 0 and m.rotation < 0):
                print("0 before mr = %i r = %i"%(m.rotation,rotation))
                m.rotation -= (360 - rotation + m.rotation)/ease
                #if(rotation > 0):
                #    m.rotation += 5
                if(m.rotation <= -180):
                    m.rotation += 360
                print("0 after mr = %i"%(m.rotation))
            elif(m.rotation > 0 and rotation < 0):
                print("1 before mr = %i r = %i"%(m.rotation,rotation))
                #if(rotation < 0):
                #    m.rotation -= 10
                m.rotation += (360 +rotation - m.rotation)/ease
                if(m.rotation >= 180):
                    m.rotation -= 360
                print("1 after mr = %i"%m.rotation)
        elif(rotation < m.rotation):
            print("2 before mr = %i r = %i"%(m.rotation,rotation))
            m.rotation -= math.fabs(m.rotation - rotation)/ease
            print("2 after mr = %i"%m.rotation)
        else:
            print("3 before mr = %i r = %i"%(m.rotation,rotation))
            m.rotation += math.fabs(rotation - m.rotation)/ease
            print("3 after mr = %i"%(m.rotation))
        velX = m.speed*((90-math.fabs(m.rotation))/90)
        velY = 0
        if(m.rotation < 0):
            velY = -m.speed+math.fabs(velX)
        else:
            velY = m.speed-math.fabs(velX)
        m.x+=velX
        m.y+=velY
        if(diffX <= m.speed and diffX >= -m.speed and diffY <= m.speed and diffY >= -m.speed):
            m.exploding = True

    def setTarget(self,targetPos):
        self.trackX,self.trackY = targetPos
