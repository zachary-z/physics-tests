from multiprocessing import Pool
pool = Pool()

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

class Particle():
    def __init__(self, pos, radius=10):
        # Position, velocity, and acceleration
        self.pos = pos
        self.previous_pos = self.pos
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        
        self.mass = math.pi*radius**2
        self.radius = radius
        # Forces
        self.impact_forces = Vector(0, 0)
        self.natural_forces = Vector(0, 0)
        
    ######### NATURAL FORCES #########
    def gravity(self):
        # Acceleration due to gravity
        self.natural_forces = self.natural_forces.add(Vector(0, -2).mul(self.mass))
    def fluid_drag(self):
        # -1/2*C_d*V^2*A_proj
        drag_magnitude = -2*self.vel.mag()**2*0.01
        self.natural_forces = self.natural_forces.add(self.vel.normalize().mul(self.mass*drag_magnitude))
    def wind_drag(self, wind_speed):
        wind_mag = 2*wind_speed*self.vel.mag()**2*0.01
        self.natural_forces = self.natural_forces.add(Vector(1,0).mul(wind_mag))
        
    ######### IMPACT FORCES #########
    def ground_collision(self, y_pos):
        # Checks for ground collisions and applies force if penetrating ground plane
        if self.pos.y <= y_pos+self.radius:
            n = Vector(0, 1)
            vrn = n.dot(self.vel)
            if vrn < 0:
                J = -1*vrn*1.0*self.mass
                self.impact_forces = self.impact_forces.add(n.mul(J))
                # Calculates new position
                self.pos.y = y_pos+self.radius
                self.pos.x = ((y_pos+self.pos.y-self.previous_pos.y)/
                              (self.pos.y-self.previous_pos.y)*
                              (self.pos.x-self.previous_pos.x)) + self.previous_pos.x
    def obstacle_collisions(self, obstacles):
        # Checks for collisions with circular obstacles and applies force if contacting
        for o in obstacles:
            r = self.radius+o.radius
            s = self.pos.dist(o.pos)-r
            if s <= 0:
                n = self.pos.sub(o.pos).normalize()
                vrn = self.vel.sub(o.vel).dot(n)
                if vrn < 0:
                    J = -1*vrn*1.7/(1/self.mass + 1/o.mass)
                    self.impact_forces = self.impact_forces.add(n.mul(J))
                    self.pos = self.pos.sub(n.mul(s))

    ######### INTEGRATOR #########
    def update(self, obstacles):
        # Accumulates all forces acting upon particle
        self.gravity()
        self.fluid_drag()
        self.ground_collision(20)
        self.obstacle_collisions(obstacles)
        # Motion integrator using Euler's method
        self.acc = self.acc.add(self.impact_forces.add(self.natural_forces).div(self.mass))
        self.vel = self.vel.add(self.acc)
        self.pos = self.pos.add(self.vel)
        # Resets force and acceleration to 0
        self.acc = Vector(0, 0)
        self.natural_forces, self.impact_forces = Vector(0, 0), Vector(0, 0)

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Particle Collision Test')

done = False

clock = pygame.time.Clock()

particles = []
obstacles = []

for i in range(7):
    for j in range(i):
        obstacles.append(Particle(Vector(400+(j-(i-1)/2)*95, 700-i*100),15))

#[Particle(Vector(random.randint(150,650),random.randint(100,600)),15) for i in range(50)]

def update_particle(p):
    if p.pos.y <= 25: particles.remove(p)
    p.update(obstacles)
    pygame.draw.circle(screen, (255,0,0), (int(p.pos.x),int(800-p.pos.y)), p.radius)

while not done:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: done = True
            if event.key == pygame.K_SPACE:
                for i in range(100):
                    particles.append(Particle(Vector(random.randint(390,410),random.randint(750,800)),5))
            
    screen.fill((150,200,250))
    pygame.draw.polygon(screen, (140,70,20), [(0,800),(0,780),(800,780),(800,800)])
    
    for p in particles:
        update_particle(p)
    for o in obstacles:
        pygame.draw.circle(screen, (0,255,0), (int(o.pos.x),int(800-o.pos.y)), o.radius)
    
    pygame.display.update()
    pygame.display.flip()
    clock.tick(120)
    
pygame.quit()
sys.exit()
