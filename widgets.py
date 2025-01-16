import pygame
import math
import random
from pygame.locals import*
import animation
pygame.init()
pygame.mixer.init()
class Stars:
    def __init__(self,posrange,sizerange,color):#Color --> [center color ,glow color]
        self.color = color
        self.posrange = posrange
        self.sizerange = sizerange
        self.stars = []

    def add_data(self,scale = False):
        if scale:
            for i in range(scale):
                pos = [random.randint(*self.posrange[0]),random.randint(*self.posrange[0])]
                size = random.randint(*self.sizerange)
                data = [pos,size,size*2]
                self.stars.append(data)
        else:
            pos = [random.randint(*self.posrange[0]), random.randint(*self.posrange[0])]
            size = random.randint(*self.sizerange)
            data = [pos, size, size * 2]
            self.stars.append(data)

    def circle_surf(self,radius,color):
        surf = pygame.Surface((radius*2,radius*2))
        pygame.draw.circle(surf,color,(radius,radius),radius)
        surf.set_colorkey((0,0,0))
        return surf

    def show(self,win):
        for i,star in enumerate(self.stars):
            if star[1] <= 0:
                self.stars.pop(i)
            star[1] -= 0.05
            star[2] -= 0.1
            glowsurf = self.circle_surf(star[2],self.color[1])
            win.blit(glowsurf,(star[0][0]-star[2],star[0][1]-star[2]),special_flags=BLEND_RGB_ADD)
            pygame.draw.circle(win, self.color[0], star[0], star[1])

class ProgressBar:
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.width = kwargs["width"]
        self.height = kwargs["height"]
        self.color = kwargs["color"]
        self.bd = kwargs["bd"]
        self.bdcolor = kwargs["bdcolor"]
        # self.showicon = pygame.image.load(kwargs["showicon"]).convert_alpha()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pady = 3
        self.padx = 20
        self.icon = kwargs['icon']
        if self.icon[0]:
            self.iconimage = pygame.transform.rotozoom(pygame.image.load(self.icon[1]),0,0.8).convert_alpha()

    def show(self, window):
        pygame.draw.rect(window,self.color,self.rect)
        pygame.draw.rect(window, self.bdcolor,
                         (self.rect.x - self.bd, self.rect.y - self.bd, self.width + self.bd, self.height + self.bd),
                         self.bd)
        if self.icon[0]:
            window.blit(self.iconimage,(self.rect.x-self.padx,self.rect.y-self.pady))

class DamageLabel:
     def __init__(self,text,font,x,y,color = (255,255,255)):
         self.text = text
         self.zoom = 1
         self.font = font
         self.x = x
         self.y = y
         self.cy = y
         self.color = color
         self.velocity = 2
         self.limit = 100
         self.label = self.font.render(self.text,True,self.color)
         self.size = self.label.get_size()
         # self.x -= self.size[0]//2
         self.alive = True

     def show(self,win):
         # win.blit(pygame.transform.rotozoom(self.label,0,self.zoom),(self.x,self.y))
         # surf = pygame.transform.scale(self.label, (self.size[0] * self.zoom, self.size[1] * self.zoom))
         win.blit(self.label,(self.x,self.y))
     def move(self):
         if self.y <= self.cy - self.limit:
             self.velocity = 0
             self.alive = False
         else:
             self.y -= self.velocity
             # self.zoom -= 0.02

class ScreenFade:
    def __init__(self,size):
        self.size = size
        self.surf = pygame.Surface(self.size)
        self.color  = 0
        self.faded = False

    def show(self,win,rp):
        self.surf.fill((self.color,self.color,self.color))
        win.blit(self.surf,rp,special_flags=BLEND_RGB_SUB)
        if self.color < 255-1:
            self.color += 2
        else: self.faded = True


class Transparent_Frame:
    def __init__(self,size,center,color,bd):
        self.center = center
        self.color = color
        self.bd = bd
        self.size = size
        self.surf = pygame.Surface(self.size)
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center = self.center)
        self.image = pygame.image.load("images/wood.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image,self.size).convert_alpha()

    def show(self,screen,imageshow = False):
        screen.blit(self.surf,self.rect,special_flags=BLEND_RGB_SUB)
        if imageshow:
            screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,self.bd[0],self.rect,self.bd[1])

class ImageButton:
    def __init__(self,text,size,pos,image):
        self.pos = pos
        self.size = size
        self.text = text
        self.font = pygame.font.Font("fonts/breathe_fire/Breathe Fire.otf",40)
        self.image = pygame.image.load(image).convert_alpha()
        self.sound = pygame.mixer.Sound("sounds/button.mp3")
        # self.image1 = pygame.transform.rotozoom(self.image1,0,1.5).convert_alpha()
        # self.image2 = pygame.transform.rotozoom(self.image1,0,1.05).convert_alpha()
        # self.image = self.image1

        self.rect = pygame.Rect(*pos,*self.image.get_size())

    def isover(self,pos,sound = True):
        if pos[0] > self.rect.x and pos[0] < self.rect.right:
            if pos[1] > self.rect.y and pos[1] < self.rect.bottom:
                if sound:
                    self.sound.play()
                return True
        return False

    def show(self,win):
        if self.text != "":
            txt = self.font.render(self.text,True,(200,200,200))
            rect = txt.get_rect(center = self.rect.center)

        r = self.image.get_rect(center = self.rect.center)
        win.blit(self.image,r)
        if self.text != "":
            win.blit(txt,rect)

class ArrowButton:
    def __init__(self,pos,direction):
        self.pos = pos
        self.image = pygame.image.load("images/Ui/arrowbutton.png").convert_alpha()
        self.rect = pygame.Rect(*self.pos,*self.image.get_size())
        if direction == "left":
            self.image = pygame.transform.flip(self.image,True,False).convert_alpha()

        self.sound = pygame.mixer.Sound("sounds/button.mp3")
    def show(self,win):
        win.blit(self.image,self.rect)

    def updatesize(self,w,h):
        self.image = pygame.transform.smoothscale(self.image,(w,h)).convert_alpha()
        self.rect = pygame.Rect(*self.pos,*self.image.get_size())

    def isover(self,pos,sound = True):
        if pos[0] > self.rect.x and pos[0] < self.rect.right:
            if pos[1] > self.rect.y and pos[1] < self.rect.bottom:
                if sound:
                    self.sound.play()
                return True
        return False


class Scale:
    def __init__(self,**kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.width = kwargs["width"]
        self.height = kwargs["height"]
        self.barcolor = kwargs["barcolor"]
        self.circlecolor = kwargs["circlecolor"]
        self.bordercolor = kwargs["bordercolor"]
        self.border = kwargs["border"]
        self.radius = kwargs["radius"]
        self.fillcolor=kwargs["fill"]
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.crect = pygame.Rect(self.x,self.y,self.radius*2,self.radius*2)
        self.crect.centery = self.rect.centery
        try:
            self.value = kwargs["value"]
        except:
            self.value = 0
        self.valuerect = pygame.Rect(self.x,self.y,self.value*(self.width//100),self.height)
        self.crect.centerx = self.valuerect.right
        self.touched = False



    def show(self,window):
        window.fill(self.barcolor,self.rect)
        window.fill(self.fillcolor,self.valuerect)
        pygame.draw.rect(window,self.bordercolor[0],self.rect,self.border)
        pygame.draw.circle(window,self.circlecolor,self.crect.center,self.radius)
        pygame.draw.circle(window,self.bordercolor[1],self.crect.center,self.radius,self.border)


    def update(self):
        self.valuerect.width = abs(self.crect.centerx-self.x)
        self.value = self.valuerect.width//(self.width//100)

    def set(self,value):
        self.crect.centerx = self.x+(value*(self.width//100))
        self.update()

    def move(self):
        if self.touched:
            self.crect.centerx = pygame.mouse.get_pos()[0]
            if self.crect.centerx >= self.rect.right:
                self.crect.centerx = self.rect.right
            if self.crect.centerx <= self.rect.left:
                self.crect.centerx = self.rect.left
            self.update()

    def get(self):
        return self.value
        #Use commands
        # self.scale.show(self.window)
        # self.scale.move()

    def checkevent(self,event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.touched:
                self.touched = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.crect.collidepoint(event.pos):
                self.touched = True

class SimpleButton:
    def __init__(self,**kwargs):
        self.text = kwargs["text"]
        self.color = kwargs["color"]
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.width = kwargs["width"]
        self.height = kwargs["height"]
        self.font = kwargs["font"]
        self.bd = kwargs["bd"]
        self.bdcolor = kwargs["bdcolor"]
        self.padx = kwargs["padx"]
        self.pady = kwargs["pady"]
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def draw(self, win):
        if self.color:
            win.fill(self.color,self.rect)
        if self.bdcolor:
            pygame.draw.rect(win, self.bdcolor,self.rect, self.bd)
        if self.text != '':
            txt = self.font.render(self.text, True, (255, 255, 255))
            win.blit(txt, (self.rect.x+self.padx, self.rect.y+self.pady))

    def isover(self,pos):
        if self.rect.collidepoint(*pos):
            return True

        else:
            return False


class TranslucentButton:
    def __init__(self,text,pos,color,font):
        self.text = text
        self.pos = pos
        self.fontdata = font
        self.font = pygame.font.SysFont(self.fontdata[0],self.fontdata[1])
        self.color =  color
        self.txtsurf = self.font.render(self.text, True, (255, 255, 255))
        self.surf = pygame.Surface((self.txtsurf.get_width()+50,self.txtsurf.get_height()+10))
        self.surf.fill(self.color)
        self.rect = pygame.Rect(*pos, *self.surf.get_size())
        self.txtrect = self.txtsurf.get_rect(center=self.rect.center)


    def show(self,win):
        self.txtsurf = self.font.render(self.text, True, (255, 255, 255))
        win.blit(self.surf,self.rect,special_flags=BLEND_RGB_SUB)
        win.blit(self.txtsurf,self.txtrect)
        if self.isover(pygame.mouse.get_pos()):
            self.font.set_underline(1)
        else:self.font.set_underline(0)

    def update(self):
        self.surf = pygame.Surface((self.txtsurf.get_width() + 50, self.txtsurf.get_height() + 10))
        self.surf.fill(self.color)
        self.rect = pygame.Rect(self.rect.x,self.rect.y, *self.surf.get_size())
        self.txtrect = self.txtsurf.get_rect(center=self.rect.center)

    def isover(self,pos):
        if self.rect.collidepoint(pos):
            return True
        else:False

