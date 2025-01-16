import math
import random
import pygame
from pygame.locals import*
pygame.init()
class Animation:
    def __init__(self, **kwargs):  # rate,imagespath,pos,timmer,zoom,flip
        self.rate = kwargs["rate"]
        self.images_path = kwargs["images"]
        self.timmer = kwargs["timmer"]
        self.constant_timmer = kwargs["timmer"]
        self.images = []
        self.zoom = kwargs["zoom"]
        self.flip = kwargs['flip']  # permission,xbool,ybool

        for i in self.images_path:
            img = pygame.image.load(i).convert_alpha()
            if self.flip[0]:
                img = pygame.transform.flip(img, self.flip[1], self.flip[2]).convert_alpha()
            if self.zoom[0]:
                img = pygame.transform.smoothscale_by(img,  self.zoom[1]).convert_alpha()
                # img = pygame.transform.smoothscale(img,
                #                    (img.get_width()*self.zoom[1],img.get_height()*self.zoom[1])).convert_alpha()
            self.images.append(img)
        self.frame_number = len(self.images)
        self.index = 0
        self.centralize = False
        self.rect = kwargs['rect']

    def show(self, win, pause=False, **kwargs):
        if self.centralize:
            imgrect = self.images[self.index].get_rect(center=kwargs['center'])
            win.blit(self.images[self.index], imgrect)
        else:
            win.blit(self.images[self.index], self.rect)
        if not pause:
            if self.timmer <= 0:
                self.timmer = self.constant_timmer
                if self.index >= self.frame_number - 1:
                    self.index = 0
                else:
                    self.index += 1
            else:
                self.timmer -= self.rate


class ShinnyParticles:
    def __init__(self,center,size,vel,angle,color):
        self.particles = []
        self.size = size
        self.vel = vel
        self.angle = angle
        self.center  =  center
        self.color= color

    def add(self):
        a = self.angle
        x1 = int(self.center[0]-30*math.cos(a))
        x2 = int(self.center[0] + 30 * math.cos(a))
        if x1>x2:
            x1,x2 = x2,x1

        y1 = int(self.center[1] - 30 * math.sin(a))
        y2 = int(self.center[1] + 30 * math.sin(a))
        if y1 > y2:
            y1, y2 = y2, y1

        x = random.randint(x1,x2)
        y = random.randint(y1,y2)

        pos = [x,y]

        # pos = list(self.center)
        s = random.randint(*self.size)
        v = random.randint(*self.vel)

        data = [pos,s,v,a]
        self.particles.append(data)

    def show(self,win):
        for i,particle in enumerate(self.particles):
            if particle[1] <= 0:
                self.particles.pop(i)
            else:
                particle[1] -= 0.1

            particle[0][0] += particle[2]*math.cos(particle[3])
            particle[0][1] += particle[2]*math.sin(particle[3])

            surf = self.circle_surf(int(2*particle[1]),self.color[1])
            win.blit(surf,(particle[0][0]-2*particle[1],particle[0][1]-2*particle[1]),special_flags=BLEND_RGB_ADD)
            pygame.draw.circle(win,self.color[0],particle[0],particle[1])


    def circle_surf(self,radius,color):
        surf = pygame.Surface((radius*2,radius*2))
        pygame.draw.circle(surf,color,(radius,radius),radius)
        surf.set_colorkey((0,0,0))
        return surf

class Aura(ShinnyParticles):
    def __init__(self,center,size,vel,angle,color):
        super().__init__(center,size,vel,angle,color)
        self.angle = math.radians(-90)
        self.rel_vy = 0
        self.limit = 20

    def add(self):
        a = self.angle
        y = self.center[1]
        x = random.randint(self.center[0]-self.limit,self.center[0]+self.limit)
        pos = [x,y]
        s = random.randint(*self.size)
        v = random.randint(*self.vel)# + self.rel_vy
        data = [pos,s,v,a]
        self.particles.append(data)

class SparkParticle:
    def __init__(self,**kwargs):
        self.pos = kwargs['pos']
        self.color = kwargs['color']
        self.scale = kwargs['scale']
        self.speed = kwargs['speed']
        self.angle = math.radians(kwargs['angle'])
        self.bd = kwargs['bd']
        self.omega = 0
        self.alive = True
    def displacement(self,dt):
        dx = math.cos(self.angle)*self.speed*dt
        dy = math.sin(self.angle)*self.speed*dt
        return dx,dy

    def move(self):
        movement = self.displacement(1)
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]
        self.speed -= 0.1
        self.angle += self.omega
        if self.speed <=0:
            self.alive = False

    def show(self,win):
        points = [
            [self.pos[0] + math.cos(self.angle) * self.speed * self.scale,
             self.pos[1] + math.sin(self.angle) * self.speed * self.scale],

            [self.pos[0] + math.cos(self.angle+math.pi/2) * self.speed * self.scale * 0.4,
             self.pos[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.4],

            [self.pos[0] - math.cos(self.angle) * self.speed * self.scale * 3.5,
             self.pos[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],

            [self.pos[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.4,
             self.pos[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.4],
        ]
        pygame.draw.polygon(win,self.color,points)
        if self.bd[0]:
            pygame.draw.polygon(win,self.bd[1],points,1)



class Sparks:
    def __init__(self,color,speed,scale = 1,**kwargs):
        self.particles = []
        self.color = color
        self.speed = speed
        self.scale = scale
        self.limit = kwargs['limit']
        self.bd = kwargs['bd']

    def add(self,x,y):
        for i in range(self.limit):
            s = SparkParticle(pos = [x,y],color = self.color,scale=self.scale,
                                         speed = random.randint(*self.speed),angle=random.randint(0,360),
                                             bd= self.bd)
            # s.omega = -0.1
            self.particles.append(s)

    def show(self,win):
        for i,spark in enumerate(self.particles):
            spark.move()
            spark.show(win)
            if not spark.alive:
                self.particles.pop(i)
                # print(len(self.sparks))

    def add2(self,x,y,omega):
        for i in range(self.limit):
            s = SparkParticle(pos = [x,y],color = self.color,scale=self.scale,
                                         speed = random.randint(*self.speed),angle=random.randint(0,360),
                                             bd= self.bd)
            s.omega = omega
            self.particles.append(s)

    def add_one(self,x,y,omega):
        s = SparkParticle(pos=[x, y], color=self.color, scale=self.scale,
                          speed=random.randint(*self.speed), angle=random.randint(0, 360),
                          bd=self.bd)
        s.omega = omega
        self.particles.append(s)


class Bubbles(Aura):
    def __init__(self,center,size,vel,angle,color):
        super().__init__(center,size,vel,angle,color)
        self.angle = 0
        self.limit = 0

    def add(self):
        a = self.angle
        y = self.center[1]
        x = self.center[0]
        pos = [x,y]
        s = random.randint(*self.size)
        v = random.randint(*self.vel)# + self.rel_vy
        data = [pos,s,v,a]
        self.particles.append(data)


class Arrow:
    def __init__(self,point,lenght):
        self.length = lenght
        self.point = point
        self.arrow_angle = math.radians(20)
        self.angle = 0
        self.animation = Bubbles(list(point),[1,4],[1,3],0,((255,255,255),(60,60,60)))

    def show(self,win):
        points = [self.point,(self.point[0] - self.length*math.cos(self.angle + self.arrow_angle),
                              self.point[1]-self.length*math.sin(self.angle+self.arrow_angle)),
                  (self.point[0] - self.length * math.cos(self.angle - self.arrow_angle),
                   self.point[1] - self.length* math.sin(self.angle - self.arrow_angle))]
        pygame.draw.polygon(win, (255, 255, 255), points)


class SignEffect:
    def __init__(self,folder):
        self.data = []
        self.image = pygame.image.load(f"images/powerups/{folder}/sign.png").convert_alpha()
        self.vel = [1,3]
        self.x_limit = 7
        self.limit = 5

    def add(self,center):
        if len(self.data) < self.limit:
            self.data.append([[random.randint(center[0]-2*self.x_limit,center[0]+self.x_limit),center[1]],
                              random.randint(*self.vel)])

    def show(self,win):
        for i,item in enumerate(self.data):
            if item[1] > 0:
                item[0][1] -= item[1]
                item[1] -= 0.1
            else:
                self.data.pop(i)
                continue
            win.blit(self.image,item[0])


