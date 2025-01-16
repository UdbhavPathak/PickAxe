import math
import random
import pygame
import animation
import widgets
from pygame.locals import*
pygame.init()

class Floor:
    def __init__(self):
        self.size = (1280,720)
        self.surf = pygame.Surface(self.size)
        self.image = pygame.image.load("images/floor.png").convert_alpha()
        for y in range(0,self.size[1],40):
            for x in range(0,self.size[0],40):
                self.surf.blit(self.image,(x,y))

    def floor(self):
        return self.surf

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,keys,folder,poision = "redorb"):
        super().__init__()
        self.movekeys = keys
        self.rect = pygame.Rect(*pos,40,40)
        self.velocity = 0
        self.vel_limit = 5
        self.angle = 0
        self.omega = 5
        self.imgs = []
        self.health = 200
        self.axetimer = 660
        self.damage = 1
        self.poision = [False,False,3*60,poision,3] # active,hit,timer,folder
        self.poision_damage = 2
        self.mana = 100

        self.poision_effect = animation.SignEffect(self.poision[3])
        self.poision_effect.vel = [1,4]
        for i in range(1,8):
            self.imgs.append(f"images/{folder}/{i}.png")
        self.right_animation = animation.Animation(images=self.imgs,rate=1,timmer=8,zoom=[True,0.3]
                                             ,flip=[False,False,False],rect=self.rect)
        self.left_animation = animation.Animation(images=self.imgs, rate=2, timmer=10, zoom=[True, 0.3]
                                                   , flip=[True, True, False], rect=self.rect)
        self.imgs.clear()
        for i in range(1,6):
            self.imgs.append(f"images/{folder}/idle/{i}.png")
        self.idle_animation = {
            'left':animation.Animation(images=self.imgs, rate=2, timmer=10, zoom=[True, 0.3]
                                                   , flip=[True, True, False], rect=self.rect),
            'right':animation.Animation(images=self.imgs,rate=1,timmer=8,zoom=[True,0.3]
                                             ,flip=[False,False,False],rect=self.rect)}

        self.direction = True # True for right False for left
        self.right_animation.centralize = True
        self.left_animation.centralize = True
        self.idle_animation['left'].centralize = True
        self.idle_animation['right'].centralize = True
        self.rect.h = self.left_animation.images[0].get_height()
        self.rect.w = self.left_animation.images[0].get_width()
        self.axe = False
        # self.color = ((0,0,0),(0,0,0))
        self.aura = animation.Aura(self.rect.center,[1,5],[2,5],0,((0,0,0),(50,0,0)))
        self.healthbar = widgets.ProgressBar(x = self.rect.x,y = self.rect.y-20,width=50,height=6,bdcolor=(100,100,100),
                                             bd=1,icon=[True,"images/icons/heart.png"],color=(0,255,0))
        self.healthbar.padx,self.healthbar.pady= 10,5
        self.shield = Shield(self.rect.topleft)
        self.aim_arrow = animation.Arrow(self.rect.center,15)


    def show(self,win,inidcator,font):

        for i in range(self.mana//50):#this indicates the mana level
            pygame.draw.circle(win,(0,200,200),
                               (self.healthbar.rect.x+self.healthbar.width+5+7*i,self.healthbar.rect.centery),3)
        if self.damage>1:
            if not len(self.aura.particles) > 30:
                self.aura.add()

        self.aura.show(win)
        self.poision_effect.show(win)

        vx = self.velocity*math.cos(self.angle)
        vy = self.velocity*math.sin(self.angle)
        self.aura.rel_vy = -vy
        v = math.sqrt(vx**2+vy**2)
        self.aim_arrow.animation.show(win)


        if vx > 0 and v > 0:
            self.right_animation.show(win,center=self.rect.center)
        elif vx < 0 and v > 0:
            self.left_animation.show(win,center=self.rect.center)
        else:
            if self.direction:
                self.idle_animation['right'].show(win,center=self.rect.center)
            else:self.idle_animation['left'].show(win,center=self.rect.center)
        if not self.axe:
            pygame.draw.circle(win, (255, 255, 255), (self.rect.centerx + 40 * math.cos(self.angle),
                                                  self.rect.centery + 40 * math.sin(self.angle)), 3)
        else:
            self.aim_arrow.point = (self.rect.centerx + 100 * math.cos(self.angle),
             self.rect.centery + 100 * math.sin(self.angle))

            self.aim_arrow.animation.center = self.aim_arrow.point
            self.aim_arrow.angle = self.angle
            self.aim_arrow.animation.angle = self.angle+math.radians(180)
            if self.poision[0] :
                self.aim_arrow.animation.add()
            self.aim_arrow.show(win)

        self.healthbar.show(win)
        if self.shield.active:
            self.shield.show(win)
        self.aura.center = self.rect.midbottom
        if self.poision[1]:
            self.poision_effect.add(self.rect.center)

        if self.poision[1] and self.poision[2] > 0:
            self.poision[2] -= 1
            if self.poision[2]/60 == self.poision[2]//60:
                self.health -= self.poision_damage
                label = widgets.DamageLabel(f'-{self.poision_damage}', font,
                                    self.rect.x + 10, self.rect.y)
                inidcator.append(label)

        elif self.poision[2] <= 0:
            self.poision[2] = self.poision[4]*60
            self.poision[1] = False




    def move(self,tiles):
        collision_type = {"top":False,"bottom":False,"left":False,"right":False}
        vx = self.velocity*math.cos(self.angle)
        self.rect.x += vx
        hitlist = self.check_collision(tiles)
        for tile in hitlist:
            if vx < 0:
                self.rect.left = tile.rect.right
            elif vx > 0:
                self.rect.right = tile.rect.left

        vy = self.velocity * math.sin(self.angle)
        self.rect.y += vy
        hitlist = self.check_collision(tiles)
        for tile in hitlist:
            if vy < 0:
                self.rect.top = tile.rect.bottom
            elif vy > 0:
                self.rect.bottom = tile.rect.top


        self.healthbar.rect.w = self.health//4
        self.healthbar.rect.x,self.healthbar.rect.y = (self.rect.x ,self.rect.y-8)
        self.left_animation.rate = 1+ abs(self.velocity/2)
        self.right_animation.rate = 1+ abs(self.velocity/2)
        self.shield.rect.center = self.rect.center

    def check_orb_collide(self,orb,infolabels,sounds,fonts):
        if self.rect.colliderect(orb.rect):
            if orb.type == "mana":
                label = widgets.DamageLabel("MANA+", fonts[4],
                                            self.rect.x + 10, self.rect.y, (0, 255, 255))
                infolabels.append(label)
                self.mana = 100
                sounds[10].play()

            if orb.type == "heal":
                if self.health > 150:
                    self.health += 200 - self.health

                else:
                    self.health += 50
                sounds[8].play()

                label = widgets.DamageLabel("HEALTH+", fonts[4],
                                            self.rect.x + 10, self.rect.y, (0, 255, 0))
                infolabels.append(label)

            if orb.type == "poision":
                if self.poision[0]:
                    self.damage += 0.25
                    label = widgets.DamageLabel("DAMAGE+", fonts[4],
                                                self.rect.x + 10, self.rect.y, (255, 165, 0))

                    infolabels.append(label)
                else:
                    self.poision[0] = True
                    label = widgets.DamageLabel("POISION+", fonts[4],
                                                self.rect.x + 10, self.rect.y, (255, 165, 0))
                    infolabels.append(label)
                sounds[9].play()

            orb.rect.topleft = (-200, -200)
            return True

        else:
            return False


    def check_collision(self,tiles):
        return [tile for tile in tiles if self.rect.colliderect(tile.rect)]

    def keycomands(self,keys):
        if keys[self.movekeys[2]]:
            self.angle -= math.radians(self.omega)
        if keys[self.movekeys[3]]:
            self.angle += math.radians(self.omega)


class Axe(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load("images/syth.png").convert_alpha()
        self.rect = pygame.Rect(*pos,self.image.get_width(),self.image.get_height())
        self.imageangle = 0
        self.angle = math.radians(-90)
        self.state = "notpicked"
        self.velocity = 11
        self.movement = [0,0]
        self.player_id = 0
        self.timer = 120
        self.const_timer = 120
        self.animation = animation.ShinnyParticles(self.rect.center,[1,5],[2,5],self.angle,
                                                   [(255,255,255),(40,40,40)])
        self.hitcheck = [False,False]
        self.rect.h = self.rect.h*0.75
        self.rect.w = self.rect.w*0.75


    def show(self,win,direction = False):
        self.animation.angle = self.angle
        self.animation.center = self.rect.center
        self.animation.show(win)
        if self.state == "fire":
            self.animation.add()
            img = pygame.transform.rotozoom(self.image,self.imageangle,1)
            imgrect = img.get_rect(center = self.rect.center)
            win.blit(img,imgrect)
            if self.imageangle < 360:
                self.imageangle += 25
            elif self.imageangle >= 360:
                self.imageangle = 0

        else:
            if direction:
                imgrect = self.image.get_rect(center=(self.rect.midleft[0] - 5, self.rect.midleft[1] - 10))
                win.blit(self.image, imgrect)

            else:
                img = pygame.transform.rotozoom(self.image, -math.degrees(self.angle)-90, 1)
                imgrect = img.get_rect(center=self.rect.center)
                win.blit(img, imgrect)


    def move(self,tiles):
        collision_type = {'top':False,'bottom':False,'left':False,'right':False}
        vx = self.velocity * math.cos(self.angle)
        self.movement[0] = vx
        self.rect.x += self.movement[0]
        hitlist = self.check_collision(tiles)
        for tile in hitlist:
            if vx < 0:
                self.rect.left = tile.rect.right
                collision_type['left'] = True
            elif vx > 0:
                self.rect.right = tile.rect.left
                collision_type['right'] = True

        vy = self.velocity*math.sin(self.angle)
        self.movement[1] = vy
        self.rect.y += self.movement[1]
        hitlist = self.check_collision(tiles)
        for tile in hitlist:
            if vy > 0:
                self.rect.bottom = tile.rect.top
                collision_type['bottom'] = True
            elif vy < 0:
                self.rect.top = tile.rect.bottom
                collision_type['top'] = True

        return collision_type


    def check_collision(self,tiles):
        return [tile for tile in tiles if self.rect.colliderect(tile.rect)]

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,type):
        super().__init__()
        self.rect = pygame.Rect(*pos,40,40)
        self.type = type
        self.image = pygame.image.load("images/walls.png").convert_alpha()
        # if self.type == "B":
        #     self.image = pygame.transform.flip(self.image,False,True)
        # elif self.type == "L":
        #     self.image = pygame.transform.rotozoom(self.image,90,1)
        # elif self.type == "R":
        #     self.image = pygame.transform.rotozoom(self.image,-90,1)

    def show(self,win):
        pygame.draw.rect(win,(15,10,25),self.rect)
        win.blit(self.image,self.rect)
        pygame.draw.rect(win,(15,10,25),self.rect,2)


class Torch:
    def __init__(self,pos):
        self.imgs = []
        for i in range(0,7):
            self.imgs.append(f"images/torch/{i}.png")
        self.rect = pygame.Rect(*pos,40,40)
        self.animation = animation.Animation(timmer=10,rate=2,rect=self.rect,images=self.imgs,
                                             zoom=[False,False],flip=[False,False,False])
        self.animation.centralize = True

    def show(self,win):
        self.animation.show(win,center=self.rect.center)



class Portal(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('images/portal.png').convert_alpha()
        self.img_angle = 0
        self.destination = 0
        self.rect = self.image.get_rect(topleft = pos)
        self.id = 0
        self.rect.w = 60
        self.rect.h = 60


    def show(self,win):
        if self.img_angle > 360:
            self.img_angle = 0
        else: self.img_angle -= 5

        img = pygame.transform.rotozoom(self.image,self.img_angle,1)
        r = img.get_rect(center = self.rect.center)
        win.blit(img,r)

class Orb(pygame.sprite.Sprite):
    def __init__(self,pos,folder,type):
        super().__init__()
        self.pos = pos
        self.type = type
        self.orbs_img = []
        for i in range(0,28):
            self.orbs_img.append(f"images/powerups/{folder}/{i}.png")
        self.rect = pygame.Rect(*self.pos,40,40)
        self.orbanimation = animation.Animation(timmer=8,rate=2,rect=self.rect,images=self.orbs_img,
                                                zoom=[True,0.11],flip=[False,False,False])
        self.orbanimation.centralize = True
        self.y_limit = 5
        self.cy = self.rect.y
        self.vel = 1
        self.animation = animation.SignEffect(folder)

    def show(self,win):
        self.animation.add(self.rect.center)
        self.animation.show(win)

        # pygame.draw.rect(win,(255,255,255),self.rect,1)
        self.orbanimation.show(win,center=(self.rect.centerx,self.rect.centery-16))

        # win.blit(self.image,(self.rect.x,self.rect.y))

    def move(self):
        if self.rect.y > self.cy+self.y_limit or self.rect.y < self.cy-self.y_limit:
            self.vel *= -1
        self.rect.y += self.vel

class Shield(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.active = False
        self.color = [(50,50,50),(255,255,255)]
        self.c_radius = 50
        self.radius = 0
        self.rect = pygame.Rect(*pos,self.c_radius*2,self.c_radius*2)
        self.timer = 5*60
        self.conts_timer = 5*60
        self.inlarge = False

    def show(self,win):
        if self.radius < self.c_radius and not self.inlarge:
            self.radius += 5
        else:self.inlarge = True

        if self.timer > 0:
            self.timer -= 1
        else:
            if self.radius > 0:
                self.radius -= 5
            else:
                self.active = False
                self.inlarge = False
                self.timer = self.conts_timer

        surf = self.circle_surf(self.radius,self.color[0])
        win.blit(surf,(self.rect.centerx-self.radius,self.rect.centery-self.radius),special_flags=BLEND_RGB_ADD)
        pygame.draw.circle(win,self.color[1], self.rect.center,self.radius, 1)

    def circle_surf(self,radius,color):
        surf = pygame.Surface((radius*2,radius*2))
        pygame.draw.circle(surf,color,(radius,radius),radius)
        return surf




# [(key,1),----]
# {key:val,----}