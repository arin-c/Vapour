import os,sys, pygame,random
from euclid import *

class Particle():
    def __init__(self,surface,texture,position,velocity,angle,angularVelocity,color,size,duration):
        self.surface = surface
        self.texture = pygame.transform.scale(texture,(size,size))
        self.position = position
        self.velocity = velocity
        self.angle = angle
        self.angularVelocity = angularVelocity
        self.color = color
        self.size = size
        self.duration = duration

    def update(self):
        self.duration -= 1
        self.position= self.position + self.velocity
        #self.angle += self.angularVelocity

    def draw(self):
        self.surface.blit(self.texture,(self.position.x,self.position.y))
        #pygame.draw.circle(self.surface,self.color,(int(self.position.x),int(self.position.y)),self.size)
