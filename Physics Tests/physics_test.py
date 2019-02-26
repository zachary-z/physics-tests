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
    def tuple(self):
        return tuple([self.x, self.y])
    def copy(self):
        return Vector(self.x, self.y)

class Particle(pygame.sprite.Sprite):
    def __init__(self, radius=5):
        self.pos = Vector(200, 200)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.mass = math.pi*radius**2
        # Pygame.sprite.Sprite handling
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.radius = radius
        pygame.draw.circle(self.image, (255,0,0,255), (radius,radius), radius)
        self.rect = self.image.get_rect()
    def thruster(self, direction):
        if direction == 'U': self.acc = self.acc.add(Vector(0, 2))
        if direction == 'D': self.acc = self.acc.add(Vector(0, -2))
        if direction == 'L': self.acc = self.acc.add(Vector(1, 0))
        if direction == 'R': self.acc = self.acc.add(Vector(-1, 0))
    def gravity(self):
        self.acc = self.acc.add(Vector(0, -0.5))
    def air_drag(self):
        drag_coeff = -1/2*1*self.vel.mag()**2*2*self.radius*1 # -1/2*rho*speed^2*proj_area*c_drag
        self.acc = self.acc.add(self.vel.normalize().mul(drag_coeff))
    def confinement(self):
        '''
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = -0.5*self.vel.x
        if self.pos.x > 400:
            self.pos.x = 400
            self.vel.x = -0.5*self.vel.x
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = -0.5*self.vel.y
        if self.pos.y > 400:
            self.pos.y = 400
            self.vel.y = -0.5*self.vel.y
        '''
        RESTITUTION = 0.6
        if self.pos.y <= 200:
            n = Vector(0, 1)
            vrn = self.vel.copy().dot(n)
            if vrn < 0:
                J = -1*vrn*(RESTITUTION+1)*self.mass
                self.acc = self.acc.add(n.mul(J))
    def collisions(self, obstacles):
        RESTITUTION = 0.6
        for o in obstacles:
            r = self.radius+o.radius
            d = self.pos.sub(o.pos)
            s = d.mag()-r
            if s <= 0:
                d.normalize()
                if self.vel.sub(o.vel).dot(d) < 0:
                    J = (self.vel.sub(o.vel).dot(d).mul((RESTITUTION+1)/(1/self.mass+1/o.mass)))
                    d.copy().mult(J)
                    self.pos.sub(d.mul(s))
    def update(self):
        self.gravity()
        # self.air_drag()
        # Update position, velocity, and acceleration
        self.vel = self.vel.add(self.acc)
        self.pos = self.pos.add(self.vel)
        self.acc = Vector(0, 0)
        self.confinement()
        self.rect.center = (self.pos.x, 400-self.pos.y)
        # Confined to the screen

'''
class Frame(pygame.sprite.Sprite):
    def __init__(self, vertices, pos, ang, tvel, rvel):
        self.vertices = vertices # Ordered list of vertices
        self.edges = [self.vertices[i:i+2] for i in range(len(self.vertices)-1)]
        self.edges.append([self.vertices[-1],self.vertices[0]])

        self.pos = pos # Global coordinates for center of mass
        self.ang = ang # Angle originally headed

        self.tvel = tvel
        self.rvel = rvel
        self.tacc = Vector(0, 0)
        self.racc = 0

        self.radius = max([i.mag() for i in self.vertices])
        d = 1
        self.mass = 0
        for i in self.edges:
            a, b, c = i[0].dist(i[1]), i[0].mag(), i[1].mag()
            s = (a+b+c)/2
            self.mass += d*math.sqrt(s*(s-a)*(s-b)*(s-c))

        pygame.sprite.Sprite.__init__(self)
        self.color = (255, 128, 0, 255)
        self.image = pygame.Surface((self.radius*2, self.radius*2)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.image,
                            self.color,
                            [i.add(Vector(self.radius, self.radius)).tuple() for i in self.vertices])
        self.rect = self.image.get_rect()

    def rotate(self, angle):
        vps = []
        for i in self.vertices:
            vps.append(Vector(math.cos(i.angle()+angle),
                              math.sin(i.angle()+angle)).mul(i.mag()))
        self.vertices = vps
        self.edges = [self.vertices[i:i+2] for i in range(len(self.vertices))]
        self.edges.append([self.vertices[-1], self.vertices[0]])

    def redraw(self):
        self.image = pygame.Surface((self.radius*2, self.radius*2)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.image,
                            self.color,
                            [i.add(Vector(self.radius, self.radius)).tuple() for i in self.vertices])
        self.rect = self.image.get_rect()

    def update(self):
        self.tvel = self.tvel.add(self.tacc)
        self.pos = self.pos.add(self.tvel)
        self.rvel += self.racc
        self.ang += self.rvel

        self.rotate(self.rvel)
        self.redraw()
        self.rect.center = (self.pos.x, 400-self.pos.y)

class Rectangle(Frame):
    def __init__(self, width, height):
        pos = Vector(random.randint(0, 400), random.randint(0, 400))
        ang = random.random()*2*math.pi
        tvel = Vector(0, 0)
        rvel = 0.1
        vertices = [Vector(-1*width/2, -1*height/2),
                    Vector(-1*width/2, height/2),
                    Vector(width/2, height/2),
                    Vector(width/2, -1*height/2)]
        Frame.__init__(self, vertices, pos, ang, tvel, rvel)
'''        

screen = pygame.display.set_mode((400,400))
pygame.display.set_caption('Basic Physics Test')

background = pygame.Surface((400,400))
background.fill((120,190,255))
screen.blit(background, (0,0))

done = False

'''
P = Player()
player = pygame.sprite.Group()
player.add(P)
'''
particles = pygame.sprite.Group()
for i in range(200):
    a = Particle()
    a.pos = Vector(random.randint(100, 300), random.randint(300, 400))
    a.vel = Vector(0, 0)
    particles.add(a)
obstacles = pygame.sprite.Group()
for i in range(8):
    o = Particle(20)
    o.pos = Vector(random.randint(100, 300), random.randint(50, 250))
    o.vel = Vector(0, 0)
    obstacles.add(o)

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: done == True
        # Key binding
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: P.thruster('U')
            if event.key == pygame.K_DOWN: P.thruster('D')
            if event.key == pygame.K_LEFT: P.thruster('L')
            if event.key == pygame.K_RIGHT: P.thruster('R')
        '''
    # Updates
    particles.clear(screen, background)
    particles.update()
    particles.draw(screen)

    # obstacles.draw(screen)
    
    '''
    player.clear(screen, background)
    player.update()
    player.draw(screen)
    '''
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
sys.exit()
