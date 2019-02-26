# Physics simulator

import pygame
import random
import math
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
        return Vector(self.x+v.x, self.y+v.y)
    def mul(self, c):
        return Vector(self.x*c+self.y*c)
    def div(self, c):
        return Vector(self.x/c+self.y/c)
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

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, vel):
        # Motion
        self.pos = pos
        self.vel = vel
        self.acc = Vector()
        # Attributes
        self.radius = 5
        self.mass = 25*math.pi
        self.color = random.choice([(255,0,0),(255,255,0),(0,255,0),(0,0,255)])
        # Pygame Sprite Handling
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.radius*2, self.radius*2))
        self.image.fill((0,0,0,127))
        pygame.draw.circle(self.image, self.color, (self.pos.x, self.pos.y), self.radius)
        self.rect = self.image.get_rect()
    def forces(self, ad=True, gr=True):
        gravity = Vector(0, 9.8).mul(gr)
        air_drag = Vector() # self.vel.normalize().mul(-1*self.vel.mag()**2) # air_drag = self.vel.normalize().mul(-0.5*math.pi*(self.radius**2)*1.2*0.47*(self.vel.mag()**2)).mul(ad)
        self.acc = self.acc.add(gravity.mul(gr))
        self.acc = self.acc.add(air_drag.mul(ad))
    def update(self):
        self.acc = self.acc.add(Vector(0,9.8))
        self.vel = self.vel.add(self.acc)
        self.pos = self.pos.add(self.vel)
        self.acc = Vector()

'''
class Frame(pygame.sprite.Sprite):
    def __init__(self, pos, angle, vertices, edges, tvel, rvel, density, color):
        # Physics handling
        self.vertices = vertices # ORDERED list of vertex positions relative to the center of mass
        self.edges = [self.vertices[i:i+2] for i in range(len(self.vertices)-1)].append([self.vertices[0], self.vertices[-1]]) # Pairs of vertices

        self.pos = pos # Global coordinates for the center of gravity
        self.angle = angle # Angle that the frame is headed

        self.tvel = tvel
        self.rvel = rvel
        self.tacc = Vector()
        self.racc = Vector()

        self.radius = max([i.mag() for i in self.vertices]) # Length of vertex furthest from the center of mass
        self.density = density
        self.mass = 0 # Mass is the area of the polygon times density
        for i in self.edges:
            a, b, c = i[0].dist(i[1]), i[0].mag(), i[1].mag()
            s = (a+b+c)/2
            self.mass += self.density*math.sqrt(s*(s-a)*(s-b)*(s-c))
        # Image and sprite handling
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pygame.Surface((self.radius*2, self.radius*2))
        self.image.fill((0,0,0,50))
        pygame.draw.polygon(self.image,
                            self.color,
                            [[i.add(Vector(self.radius, self.radius)).x, i.add(Vector(self.radius, self.radius)).y] for i in self.vertices],
                            width=1)
        self.rect = self.image.get_rect()

    def rotate(self, angle):
        vps = []
        # Rotates vertices by a given angle
        for v in vertices: vps.append(Vector(math.cos(v.angle()+angle), math.sin(v.angle()+angle)).mul(v.mag()))
        self.vertices = vps
        # Recreates image
        self.image = pygame.Surface((self.radius*2, self.radius*2))
        self.image.fill((0,0,0,50))
        pygame.draw.polygon(self.image,
                            self.color,
                            [[i.add(Vector(self.radius, self.radius)).x, i.add(Vector(self.radius, self.radius)).y] for i in self.vertices],
                            width=1)
        self.rect = self.image.get_rect()
    def update(self):
        # Translation
        self.tvel = self.tvel.add(self.tacc)
        self.pos = self.pos.add(self.tvel)
        self.tacc = Vector()
        # Rotation
        self.rvel = self.rvel.add(self.racc)
        self.angle += self.rvel
        self.rotate(self.rvel)
        self.racc = Vector()

class Cube(Frame):
    def __init__(self, pos, size, tvel, rvel, density, color):
        v = [Vector(size, size), Vector(size, -1*size), Vector(-1*size, -1*size), Vector(-1*size, size)]
        e = [[v[0],v[1]], [v[1],v[2]], [v[2],v[3]], [v[3],v[0]]]
        Frame.__init__(self, pos, 0, v, e, tvel, rvel, 1, color)
'''

screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("Physics Models")

background = pygame.Surface((400,400))
background.fill((120,190,255))
screen.blit(background, (0,0))

done = False

clock = pygame.time.Clock()

particles = pygame.sprite.Group()

while not done:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            done = True
    if pygame.mouse.get_pressed()[0] == True:
        angle = random.random()*2*math.pi
        particles.add(Particle(pos=Vector(random.randint(0, 400), random.randint(0, 400)), vel=Vector(0,0)))
    particles.clear(screen, background)
    particles.update()
    particles.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
