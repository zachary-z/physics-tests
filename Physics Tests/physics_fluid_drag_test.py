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
        self.pos = Vector(250, 200)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.mass = math.pi*radius**2
        # Pygame.sprite.Sprite handling
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.set_colorkey((0,0,0))
        self.image.fill((0,0,0))
        self.radius = radius
        pygame.draw.circle(self.image, (255,0,0), (radius,radius), radius)
        self.rect = self.image.get_rect()
    def thruster(self, direction):
        if direction == 'U': self.acc = self.acc.add(Vector(0, 2))
        if direction == 'D': self.acc = self.acc.add(Vector(0, -2))
        if direction == 'L': self.acc = self.acc.add(Vector(1, 0))
        if direction == 'R': self.acc = self.acc.add(Vector(-1, 0))
    def gravity(self):
        self.acc = self.acc.add(Vector(0, -0.5))
    def fluid_drag(self):
        drag_magnitude = 0
        if self.pos.y > 150:
            drag_magnitude = -0.5*self.vel.mag()**2*0.01
        if self.pos.y <= 150:
            drag_magnitude = -0.5*self.vel.mag()**2*0.1
        self.acc = self.acc.add(self.vel.normalize().mul(drag_magnitude))
    def update(self):
        self.gravity()
        # self.fluid_drag()
        # Update position, velocity, and acceleration
        self.vel = self.vel.add(self.acc)
        self.pos = self.pos.add(self.vel)
        self.acc = Vector(0, 0)
        self.rect.center = (self.pos.x, 400-self.pos.y)
        # Confined to the screen

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Basic Drag Test')

background = pygame.Surface((400, 400))
background.fill((120, 195, 255))
screen.blit(background, (0, 0))

done = False

spring_bob = pygame.sprite.Group()
sb = Particle()
sb.pos = Vector(150, 250)
bs = Particle()
bs.pos = Vector(250, 250)
spring_bob.add(sb)
spring_bob.add(bs)

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: done = True
            if event.key == pygame.K_RIGHT: sb.thruster('R')
            if event.key == pygame.K_LEFT: sb.thruster('L')
            if event.key == pygame.K_DOWN: sb.thruster('D')
            if event.key == pygame.K_UP: sb.thruster('U')
    
    screen.fill((120, 195, 255))
            
    # pygame.draw.line(screen, (255,255,255), (150, 400-300), (sb.pos.x, 400-sb.pos.y), 2)
    # pygame.draw.line(screen, (255,255,255), (250, 400-300), (sb.pos.x, 400-sb.pos.y), 2)

    pygame.draw.rect(screen, (0,0,255), [0, 250, 200, 300])
    pygame.draw.rect(screen, (0,0,0), [200, 0, 400, 400])
    
    spring_bob.clear(screen, background)
    spring_bob.update()
    sb.fluid_drag()
    spring_bob.draw(screen)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
sys.exit()
