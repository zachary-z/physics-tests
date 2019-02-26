import pygame
import random
import math
import time
import sys
import os

pygame.init()

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def angle(self):
        return math.atan2(self.y, self.x)
    def mag(self):
        return math.sqrt(self.y*self.y+self.x*self.x)
    def add(self, v):
        return Vector(self.x+v.x, self.y+v.y)
    def sub(self, v):
        return Vector(self.x-v.x, self.y-v.y)
    def mul(self, c):
        return Vector(self.x*c, self.y*c)
    def div(self, c):
        return Vector(self.x/c, self.y/c)
    def dot(self, v):
        return self.x*v.x + self.y*v.y
    def normalize(self):
        return Vector(math.cos(self.angle()), math.sin(self.angle()))
    def dist(self, v):
        return math.sqrt((self.x-v.x)**2 + (self.y-v.y)**2)
    def randomUnit(self):
        angle = random.random()*math.pi*2
        self.x = math.cos(angle)
        self.y = math.sin(angle)
    def tuple(self):
        return tuple([self.x, self.y])
    def copy(self):
        return Vector(self.x, self.y)

class Particle:
    def __init__(self, x, y):
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.mass = 1
    def gravity(self):
        self.acc = self.acc.add(Vector(0, -0.5))
    def air_drag(self):
        drag_magnitude = -2*self.vel.mag()**2*0.01
        self.acc = self.acc.add(self.vel.normalize().mul(self.mass*drag_magnitude))
    def update(self):
        self.gravity()
        self.air_drag()
        # Update position, velocity, and acceleration
        self.vel = self.vel.add(self.acc)
        self.pos = self.pos.add(self.vel)
        self.acc = Vector(0, 0)

rp = [Particle(400, 600) for i in range(10)]
# for i in range(len(rp)): rp[i].vel = Vector(3,6).mul(i) 
# rp[len(rp)-1].mass = 5
# rp[19].vel = Vector(100,100)

def spring_force(particle_1, particle_2):
    distance = particle_1.pos.dist(particle_2.pos)
    force_magnitude = -0.3*(distance-10)
    force = particle_1.pos.sub(particle_2.pos).normalize().mul(force_magnitude)
    return force

def update():
    rp[len(rp)-1].acc = rp[len(rp)-1].acc.add(spring_force(rp[len(rp)-1],rp[len(rp)-2]))
    rp[len(rp)-1].update()
    for i in range(len(rp)-2):
        p = 10-(i+2)
        rp[p].acc = rp[p].acc.add(spring_force(rp[p],rp[p+1]))
        rp[p].acc = rp[p].acc.add(spring_force(rp[p],rp[p-1]))
        rp[p].update()
    '''
    rp[19].acc = rp[19].acc.add(spring_force(rp[19],rp[18]))
    rp[19].update()
    rp[18].acc = rp[18].acc.add(spring_force(rp[18],rp[19]))
    rp[18].acc = rp[18].acc.add(spring_force(rp[18],rp[17]))
    rp[18].update()
    rp[17].acc = rp[17].acc.add(spring_force(rp[17],rp[18]))
    rp[17].acc = rp[17].acc.add(spring_force(rp[17],rp[16]))
    rp[17].update()
    rp[16].acc = rp[16].acc.add(spring_force(rp[16],rp[17]))
    rp[16].acc = rp[16].acc.add(spring_force(rp[16],rp[15]))
    rp[16].update()
    rp[15].acc = rp[15].acc.add(spring_force(rp[15],rp[16]))
    rp[15].acc = rp[15].acc.add(spring_force(rp[15],rp[14]))
    rp[15].update()
    rp[14].acc = rp[14].acc.add(spring_force(rp[14],rp[15]))
    rp[14].acc = rp[14].acc.add(spring_force(rp[14],rp[13]))
    rp[14].update()
    rp[13].acc = rp[13].acc.add(spring_force(rp[13],rp[14]))
    rp[13].acc = rp[13].acc.add(spring_force(rp[13],rp[12]))
    rp[13].update()
    rp[12].acc = rp[12].acc.add(spring_force(rp[12],rp[13]))
    rp[12].acc = rp[12].acc.add(spring_force(rp[12],rp[11]))
    rp[12].update()
    rp[11].acc = rp[11].acc.add(spring_force(rp[11],rp[12]))
    rp[11].acc = rp[11].acc.add(spring_force(rp[11],rp[10]))
    rp[11].update()
    rp[10].acc = rp[10].acc.add(spring_force(rp[10],rp[11]))
    rp[10].acc = rp[10].acc.add(spring_force(rp[10],rp[9]))
    rp[10].update()
    rp[9].acc = rp[9].acc.add(spring_force(rp[9],rp[10]))
    rp[9].acc = rp[9].acc.add(spring_force(rp[9],rp[8]))
    rp[9].update()
    rp[8].acc = rp[8].acc.add(spring_force(rp[8],rp[9]))
    rp[8].acc = rp[8].acc.add(spring_force(rp[8],rp[7]))
    rp[8].update()
    rp[7].acc = rp[7].acc.add(spring_force(rp[7],rp[8]))
    rp[7].acc = rp[7].acc.add(spring_force(rp[7],rp[6]))
    rp[7].update()
    rp[6].acc = rp[6].acc.add(spring_force(rp[6],rp[7]))
    rp[6].acc = rp[6].acc.add(spring_force(rp[6],rp[5]))
    rp[6].update()
    rp[5].acc = rp[5].acc.add(spring_force(rp[5],rp[6]))
    rp[5].acc = rp[5].acc.add(spring_force(rp[5],rp[4]))
    rp[5].update()
    rp[4].acc = rp[4].acc.add(spring_force(rp[4],rp[5]))
    rp[4].acc = rp[4].acc.add(spring_force(rp[4],rp[3]))
    rp[4].update()
    rp[3].acc = rp[3].acc.add(spring_force(rp[3],rp[4]))
    rp[3].acc = rp[3].acc.add(spring_force(rp[3],rp[2]))
    rp[3].update()
    rp[2].acc = rp[2].acc.add(spring_force(rp[2],rp[3]))
    rp[2].acc = rp[2].acc.add(spring_force(rp[2],rp[1]))
    rp[2].update()
    rp[1].acc = rp[1].acc.add(spring_force(rp[1],rp[2]))
    rp[1].acc = rp[1].acc.add(spring_force(rp[1],rp[0]))
    rp[1].update()
    '''

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Rope Test')

# background = pygame.Surface((400, 400))
# background.fill((120, 195, 255))
# screen.blit(background, (0, 0))

done = False

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: done = True
    
    screen.fill((0, 0, 150))

    update()
    for p in range(len(rp)-1):
        pygame.draw.line(screen,(210,180,140),(rp[p].pos.x,800-rp[p].pos.y),(rp[p+1].pos.x,800-rp[p+1].pos.y),6)
    
    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
sys.exit()
