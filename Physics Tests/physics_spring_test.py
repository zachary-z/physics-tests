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

class Particle(pygame.sprite.Sprite):
    def __init__(self, radius=10):
        self.pos = Vector(200, 200)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.mass = math.pi*radius**2
        # Pygame.sprite.Sprite handling
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.radius = radius
        pygame.draw.circle(self.image, (255,0,0,255), (radius,radius), radius)
        self.rect = self.image.get_rect()

        self.hand1 = True
        self.hand2 = True
    def thruster(self, direction):
        if direction == 'U': self.acc = self.acc.add(Vector(0, 2))
        if direction == 'D': self.acc = self.acc.add(Vector(0, -2))
        if direction == 'L':
            v = self.pos.sub(Vector(150,300)).normalize().mul(-5)
            self.acc = self.acc.add(v)
        if direction == 'R':
            v = self.pos.sub(Vector(250,300)).normalize().mul(-5)
            self.acc = self.acc.add(v)
    def gravity(self):
        self.acc = self.acc.add(Vector(0, -0.5))
    def air_drag(self):
        drag_magnitude = -0.5*self.vel.mag()**2*0.01
        self.acc = self.acc.add(self.vel.normalize().mul(drag_magnitude))
    def spring_force_1(self):
        sp = Vector(150, 300)
        force_mag = -0.01*(self.pos.dist(sp)-100)
        force = self.pos.sub(sp).normalize()
        self.acc = self.acc.add(force.mul(force_mag))
    def spring_force_2(self):
        sp = Vector(250, 300)
        force_mag = -0.01*(self.pos.dist(sp)-100)
        force = self.pos.sub(sp).normalize()
        self.acc = self.acc.add(force.mul(force_mag))
    def update(self):
        self.gravity()
        self.air_drag()
        if self.hand1: self.spring_force_1()
        if self.hand2: self.spring_force_2()
        # Update position, velocity, and acceleration
        self.vel = self.vel.add(self.acc)
        self.pos = self.pos.add(self.vel)
        self.acc = Vector(0, 0)
        self.rect.center = (self.pos.x, 400-self.pos.y)
        # Confined to the screen

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Basic Spring Test')

background = pygame.Surface((400, 400))
background.fill((120, 195, 255))
screen.blit(background, (0, 0))

done = False

spring_bob = pygame.sprite.Group()
sb = Particle()
spring_bob.add(sb)

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: done = True
            if event.key == pygame.K_RIGHT: sb.thruster('R')
            if event.key == pygame.K_LEFT: sb.thruster('L')
            if event.key == pygame.K_DOWN: sb.hand2 = False
            if event.key == pygame.K_UP: sb.hand1 = False
    
    screen.fill((120, 195, 255))
            
    if sb.hand1: pygame.draw.line(screen, (255,255,255), (150, 400-300), (sb.pos.x, 400-sb.pos.y), 2)
    if sb.hand2: pygame.draw.line(screen, (255,255,255), (250, 400-300), (sb.pos.x, 400-sb.pos.y), 2)
    
    spring_bob.clear(screen, background)
    spring_bob.update()
    spring_bob.draw(screen)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
sys.exit()
