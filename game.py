import pygame
import math
import mainscreen
import sprite
import random
import animation
import widgets
from pygame.locals import*
pygame.init()
pygame.mixer.init()

class Camera:
    def __init__(self,size):
        self.size = size
        self.half_size = [self.size[0]//2,self.size[1]//2]
        self.scale = 1
        self.offset = pygame.math.Vector2()

    def targetcenter(self,center):
        self.offset.x = self.scale*center[0]-self.half_size[0]*self.scale
        self.offset.y = self.scale*center[1]-self.half_size[1]*self.scale

class Game:
    def __init__(self,fullscreen = False):
        self.size = (1280,720)
        self.fullscreen = fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN | pygame.NOFRAME)
            self.reference_point = [self.screen.get_width()//2-640,self.screen.get_height()//2-360]
        else:
            self.screen = pygame.display.set_mode(self.size)
            self.reference_point = [0, 0]

        pygame.display.set_caption("PickAxe")
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.running = True
        self.window = pygame.Surface(self.size)

        self.fonts = [pygame.font.Font("fonts/breathe_fire/Breathe Fire.otf",120),
                      pygame.font.Font("fonts/snorkad/Snorkad-Regular.ttf", 20),
                      pygame.font.Font("fonts/snorkad/Snorkad-Regular.ttf", 15),
                      pygame.font.SysFont("Times New Roman", 20),
                      pygame.font.Font("fonts/pixel/pixel.ttf",15),
                      pygame.font.Font("fonts/pixel/pixel.ttf", 10),
                      pygame.font.Font("fonts/snorkad/Snorkad-Regular.ttf", 50)
                      ]
        self.CenterLabel(self.screen, "Loading....", 0, (200, 200, 200), (self.screen.get_width() // 2,
                                                                          self.screen.get_height() // 2))
        pygame.display.update()

        self.sounds = [pygame.mixer.Sound("sounds/bounce.mp3"),#0
                       pygame.mixer.Sound("sounds/stab.mp3"),#1
                       pygame.mixer.Sound("sounds/throw.mp3"),#2
                       pygame.mixer.Sound("sounds/pickup.mp3"),#3
                       pygame.mixer.Sound("sounds/teleport.mp3"),#4
                       pygame.mixer.Sound("sounds/shield.mp3"),#5
                       pygame.mixer.Sound("sounds/shield_deactivate.mp3"),#6
                       pygame.mixer.Sound("sounds/spawn.mp3"),#7
                       pygame.mixer.Sound("sounds/heal.mp3"),#8
                       pygame.mixer.Sound("sounds/poision.mp3"),#9
                       pygame.mixer.Sound("sounds/mana.mp3"),#10
                       ]

        self.bgmusic = pygame.mixer.Sound("sounds/music.mp3")
        self.bgmusic.set_volume(0.5)
        self.bgmusic.play(-1)



        pygame.mixer.set_num_channels(20)

        self.player1 = sprite.Player((500,400),
                                     [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT],
                                     "player1")
        self.player2 = sprite.Player((900, 200),
                                     [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d],
                                     "player2",poision="blueorb")
        
        self.player1.aura.color  = ((0,0,0),(80,0,0))
        self.player1.aim_arrow.animation.color =  ((255,255,255),(80,0,0))
        self.player1.shield.color = [(50,0,0),(100,100,100)]

        self.player2.aura.color = ((0,0,0),(0,0,80))
        self.player2.aim_arrow.animation.color =  ((255,255,255),(0,0,80))
        self.player2.shield.color = [(0,0,50),(100,100,100)]

        self.player2.angle = math.radians(180)
        self.player2.direction = False


        self.axe = sprite.Axe((0,0))
        self.axe.rect.center = (self.size[0]//2,self.size[1]//2)
        self.player1.rect.center = (self.size[0]//2- 200,self.size[1]//2)
        self.player2.rect.center = (self.size[0]//2+ 200,self.size[1]//2)

        self.floor = sprite.Floor()
        self.camera = Camera(self.size)
        self.scale = 1
        self.limitscale = 1.1
        self.stars = widgets.Stars([(0, self.size[0]), (0,self.size[1])], [1, 3],
                           [(255, 255, 255), (100, 100, 0)])

        self.mapdata = []
        self.platforms = []
        self.torches = []
        self.bloodanimations = []
        self.infolabels = []
        self.collectivedamage = [0,0] #player1 ,player 2
        self.floorcoords = []
        self.portal_locs = []
        self.portalslist = []


        with open("data/gamedata.txt","r") as gdata:
            self.gamedata = gdata.read().split("\n")
        with open(f"data/maps/map{self.gamedata[0]}.txt","r") as data:
            mapdata = data.read().split("\n")
            for i in mapdata:
                n = i.split(" ")
                self.mapdata.append(n)

        for y_index,y in enumerate(self.mapdata):
            for x_index,x in enumerate(y):
                if x == "B" or x == "T" or x == "R" or x == "L":
                    tile = sprite.Tile([40*x_index,40*y_index],x)
                    self.platforms.append(tile)

                elif x == 'P':
                    self.portal_locs.append([40 * x_index, 40 * y_index])

                elif x == "_":
                    self.floorcoords.append([40*x_index,40*y_index])

        self.entity_group = pygame.sprite.Group()
        self.entity_group.add(self.player1)
        self.entity_group.add(self.player2)
        self.entity_group.add(self.axe)

        self.players_group = [self.player1,self.player2]




        self.shake_status = [False,15]
        self.orbs = [sprite.Orb((-200,-200),"redorb","poision"),
                     sprite.Orb((-200,-200), "greenorb", "heal"),
                     sprite.Orb((-200,-200),"blueorb","mana")]
        self.orbs[2].animation.image = pygame.image.load("images/powerups/blueorb/sign2.png").convert_alpha()
        self.spawn_status = [12*60,12*60,False]

        self.portals_group = pygame.sprite.Group()
        for id,loc in enumerate(self.portal_locs):
           p = sprite.Portal(loc)
           p.id = id
           self.portalslist.append(p)
           self.portals_group.add(p)

        self.portal_stats = [3*60,False]
        self.game_over = False
        self.player_won = [None,None,None]
        self.screen_fade = widgets.ScreenFade(self.screen.get_size())
        self.dead_imgs = [pygame.image.load('images/blue_dead.PNG').convert_alpha(),
                          pygame.image.load('images/red_dead.PNG').convert_alpha(),
                          pygame.image.load('images/Draw.PNG').convert_alpha(),
                       ]

        self.continue_button = widgets.ImageButton("Continue",(250,70),(0,0),"images/Ui/button.png")
        self.continue_button.rect.center = (self.screen.get_width()//2,self.screen.get_height()//2+230)

        self.gameover_music = pygame.mixer.Sound("sounds/music2.mp3")
        for sound in self.sounds:
            sound.set_volume(int(self.gamedata[2])/100)
        self.bgmusic.set_volume(int(self.gamedata[2])/100)
        self.gameover_music.set_volume(int(self.gamedata[2])/100)
        while self.running:
            self.screen.fill((0,0,0))
            self.stars.add_data(scale = 3)
            self.stars.show(self.screen)

            if not self.game_over:
                keys = pygame.key.get_pressed()
                self.player1.keycomands(keys)
                self.player2.keycomands(keys)
                self.CenterLabel(self.screen, "Pick Axe", 0, (200, 200, 200), (640, 70))
                self.window.blit(self.floor.surf,(0,0))

                self.player1.move(self.platforms)
                self.player2.move(self.platforms)


                if self.axe.state == "notpicked":
                    if self.axe.hitcheck[0]:
                        ry = self.player1.rect.y
                        label = widgets.DamageLabel(str(int(self.collectivedamage[0])),self.fonts[1],self.player1.rect.x + 10,
                                                    ry)
                        self.infolabels.append(label)
                        self.axe.hitcheck[0] = False
                        self.collectivedamage[0] = 0

                    elif self.axe.hitcheck[1]:
                        ry = self.player2.rect.y
                        label = widgets.DamageLabel(str(int(self.collectivedamage[1])),self.fonts[1],self.player2.rect.x + 10,
                                                    ry)
                        self.infolabels.append(label)
                        self.axe.hitcheck[1] = False
                        self.collectivedamage[1] = 0

                    self.axe.hitcheck = [False,False]
                    self.collectivedamage = [0,0]

                    if self.player1.rect.colliderect(self.axe.rect):
                        self.axe.player_id = 1
                        self.axe.timer = self.axe.const_timer
                        self.player1.axe = True
                        self.axe.state = "picked"
                        self.axe.animation.color = ((255,255,255),(100,0,0))
                        self.sounds[3].play()


                    elif self.player2.rect.colliderect(self.axe.rect):
                        self.axe.player_id = 2
                        self.axe.timer = self.axe.const_timer
                        self.player2.axe = True
                        self.axe.state = "picked"
                        self.axe.animation.color = ((255,255,255),(0,0,100))
                        self.sounds[3].play()

                elif self.axe.state == "picked":
                    if self.axe.player_id == 1:
                        self.axe.rect.center = self.player1.rect.center
                        self.CenterLabel(self.window,str(self.player1.axetimer//60),2,(255,255,255),
                                         (self.player1.rect.centerx,self.player1.rect.centery-60))
                        if self.player1.axetimer >= 60:
                            self.player1.axetimer -= 1
                        else:
                            self.axe.state = "fire"
                            self.player1.axe = False
                            self.sounds[2].play()
                            self.player1.axetimer = 660
                        self.axe.angle = self.player1.angle

                    elif self.axe.player_id == 2:
                        self.axe.rect.center = self.player2.rect.center
                        self.CenterLabel(self.window, str(self.player2.axetimer // 60), 2, (255, 255, 255),
                                         (self.player2.rect.centerx, self.player2.rect.centery - 60))
                        if self.player2.axetimer >= 60:
                            self.player2.axetimer -= 1
                        else:
                            self.axe.state = "fire"
                            self.player2.axe = False
                            self.sounds[2].play()
                            self.player2.axetimer = 660
                        self.axe.angle = self.player2.angle


                elif self.axe.state == "fire":
                    if self.axe.timer >= 0:
                        self.axe.timer -= 1
                        #moving the axe and checking boundary collision
                        if self.player1.shield.active and not self.axe.player_id == 1:
                            moveaxe = self.axe.move(self.platforms+[self.player1])
                        elif self.player2.shield.active and not self.axe.player_id == 2:
                            moveaxe = self.axe.move(self.platforms+[self.player2])
                        else:
                            moveaxe = self.axe.move(self.platforms)
                        if self.axe.rect.right > self.size[0]:
                            self.axe.rect.right = self.size[0]
                            self.axe.movement[0] *= -1
                        elif self.axe.rect.left < 0:
                            self.axe.rect.left = 0
                            self.axe.movement[0] *= -1

                        if self.axe.rect.bottom > self.size[1]:
                            self.axe.rect.bottom = self.size[1]
                            self.axe.movement[1] *= -1
                        elif self.axe.rect.top < 0:
                            self.axe.rect.top = 0
                            self.axe.movement[1] *= -1

                        if moveaxe['bottom'] or moveaxe['top']:
                            self.axe.movement[1] *= -1
                            self.axe.angle = math.atan2(self.axe.movement[1], self.axe.movement[0])
                            self.sounds[0].play()
                        if moveaxe['left'] or moveaxe['right']:
                            self.axe.movement[0] *= -1
                            self.axe.angle = math.atan2(self.axe.movement[1], self.axe.movement[0])
                            self.sounds[0].play()

                        #checking for axe collision with players separately
                        #Player One -- > Red Player
                        if self.axe.rect.colliderect(self.player1.rect):
                            # if not self.axe.hitcheck[0] and not self.axe.player_id == 1:
                            if not self.axe.player_id == 1:#check in if the axe is thrown by other player
                                if self.player2.poision[0]:
                                    self.player1.poision[1] = True
                                # if self.player1.poision[1]:
                                #     self.player1.poision[2] = self.player1.poision[4]*60

                                self.player1.health -= self.player2.damage
                                self.collectivedamage[0] -= self.player2.damage
                                if not self.axe.hitcheck[0]:#adding effects by checking hits
                                    s = animation.Sparks((200, 0, 0), [1,6], 1.1, limit=20, bd=[True, (150,0, 0)])
                                    s.add(*self.player1.rect.center)
                                    self.bloodanimations.append(s)
                                    self.sounds[1].play()
                                    self.shake_status[0] = True
                                self.axe.hitcheck[0] = True

                        else:
                            if self.axe.hitcheck[0]:#adding total damage indicator while the axe was collided with player
                                ry = self.player1.rect.y
                                label = widgets.DamageLabel(str(int(self.collectivedamage[0])), self.fonts[1], self.player1.rect.x+10, ry)
                                self.infolabels.append(label)
                                self.axe.hitcheck[0] = False
                                self.collectivedamage[0] = 0

                        if self.axe.rect.colliderect(self.player2.rect):#checking axe collision for player 2 --> Blue One
                            if not self.axe.player_id == 2:#check in if the axe is thrown by other player
                                if self.player1.poision[0]:
                                    self.player2.poision[1] = True

                                # if self.player2.poision[1]:
                                #     self.player2.poision[2] = self.player2.poision[4]*60

                                self.player2.health -= self.player1.damage
                                self.collectivedamage[1] -= self.player1.damage
                                if not self.axe.hitcheck[1]:#adding effects by checking hits
                                    s = animation.Sparks((0, 100, 250), [1,6], 1.1, limit=20, bd=[True, (0,0, 150)])
                                    s.add(*self.player2.rect.center)
                                    self.bloodanimations.append(s)
                                    self.sounds[1].play()
                                    self.shake_status[0] = True

                                self.axe.hitcheck[1] = True

                        else:
                            if self.axe.hitcheck[1]:#adding total damage indicator while the axe was collided with player
                                ry = self.player2.rect.y
                                label = widgets.DamageLabel(str(int(self.collectivedamage[1])),self.fonts[1],self.player2.rect.x+10,ry)
                                self.infolabels.append(label)
                                self.collectivedamage[1] = 0
                                self.axe.hitcheck[1] = False

                    else:
                        self.axe.state = "notpicked"


                for portal in self.portalslist:
                    portal.show(self.window)
                    if not self.portal_stats[1]:
                        hitlist = pygame.sprite.spritecollide(portal,self.entity_group,False)
                        if hitlist:
                            self.sounds[4].play()
                        for entity in hitlist:
                            if portal.id+1 >= len(self.portalslist):
                                entity.rect.center = self.portalslist[0].rect.center
                                self.portal_stats[1] = True
                                s = animation.Sparks((255, 255, 255), [1, 5], 1.1, limit=20, bd=[True, (0, 0, 0)])
                                s.add2(*self.portalslist[portal.id-1].rect.center, -0.2)
                                s.add2(*portal.rect.center,-0.2)
                                self.bloodanimations.append(s)

                            else:
                                entity.rect.center = self.portalslist[portal.id+1].rect.center
                                self.portal_stats[1] = True
                                s = animation.Sparks((255, 255, 255), [1, 5], 1.1, limit=20, bd=[True, (0, 0, 0)])
                                s.add2(*portal.rect.center, -0.2)
                                s.add2(*self.portalslist[portal.id + 1].rect.center, -0.2)
                                self.bloodanimations.append(s)

                    else:
                        if self.portal_stats[0] >= 0:
                            self.CenterLabel(self.window,f"{self.portal_stats[0]//60}",3,(255,255,255),
                                             (portal.rect.centerx,portal.rect.y-20))

                if self.portal_stats[1]:
                    if self.portal_stats[0] >= 0:
                        self.portal_stats[0]-= 1
                    else:
                        self.portal_stats = [3*60,False]

                # self.heal.move()

                #Spawn Items
                if self.spawn_status[0] > 0 and not self.spawn_status[2]:
                    self.spawn_status[0] -= 1

                elif self.spawn_status[0] == 0 and not self.spawn_status[2]:
                    orb = random.choices(self.orbs,k=1,weights=[0.2,0.4,0.6])
                    rf = random.choice(self.floorcoords)
                    orb[0].rect.topleft = rf
                    self.spawn_status[2] = True
                    self.spawn_status[0] = self.spawn_status[1]
                    self.sounds[7].play()

                # elif self.spawn_status[0]

                if int(self.player1.health) <= 0 :
                    self.game_over = True
                    self.player_won = ["Blue Player",(0,230,255),2]
                    self.stars.color[1] = (0, 100, 150)
                    self.bgmusic.stop()
                    self.gameover_music.play(-1)

                elif int(self.player2.health) <= 0:
                    self.game_over = True
                    self.player_won = ["Red Player",(255,0,0),1]
                    self.stars.color[1] = (150,0,0)
                    self.bgmusic.stop()
                    self.gameover_music.play(-1)

                elif int(self.player1.health) == 0 and int(self.player2.health) == 0:
                    self.game_over = True
                    self.player_won = ["Draw",(255,255,0),3]
                    self.bgmusic.stop()
                    self.gameover_music.play(-1)



                if self.axe.player_id == 1 and self.axe.state == "picked":
                    self.axe.show(self.window,True)

                elif self.axe.player_id == 2 and self.axe.state == "picked":
                    self.axe.show(self.window,True)

                else:
                    self.axe.show(self.window)


                for platform in self.platforms:
                    platform.show(self.window)

                for torch in self.torches:
                    torch.show(self.window)

                for blood in self.bloodanimations:
                    blood.show(self.window)

                for i,info in enumerate(self.infolabels):
                    info.show(self.window)
                    info.move()
                    if not info.alive:
                        self.infolabels.pop(i)


                distance = self.getdistance(self.player1.rect.center,self.player2.rect.center)
                if distance < 200:
                    if self.scale < self.limitscale:
                        self.scale += 0.001
                else:
                    if self.scale > 1:
                        self.scale -= 0.001

                self.camera.scale = self.scale

                targetcenter = [(self.player1.rect.centerx+self.player2.rect.centerx)/2,
                                (self.player1.rect.centery+self.player2.rect.centery)/2]

                # targetcenter = [(self.player1.rect.centerx + self.player2.rect.centerx + self.axe.rect.centerx) / 3,
                #                 (self.player1.rect.centery + self.player2.rect.centery + self.axe.rect.centery) / 3]


                #showing mana
                # self.CenterLabel(self.window,f'{self.player1.mana}',5,(0,255,255),
                #                  (self.player1.healthbar.rect.x+self.player1.healthbar.width+10,
                #                   self.player1.healthbar.rect.y))
                # self.CenterLabel(self.window, f'{self.player2.mana}', 5, (0, 255, 255),
                #                  (self.player2.healthbar.rect.x+self.player2.healthbar.width+10, self.player2.healthbar.rect.y))


                for player in sorted(self.players_group,key = lambda player: player.rect.y):
                    player.show(self.window, self.infolabels, self.fonts[1])

                for orb in self.orbs:
                    orb.show(self.window)
                    collided1 = self.player1.check_orb_collide(orb,self.infolabels,self.sounds,self.fonts)
                    collided2 = self.player2.check_orb_collide(orb,self.infolabels,self.sounds,self.fonts)
                    if collided1:
                        self.spawn_status[2] = False
                    elif collided2:
                        self.spawn_status[2] = False



                if self.shake_status[0]:
                    if self.shake_status[1] > 0:
                        self.shake_status[1] -= 1
                    else:
                        self.shake_status = [False,15]
                    rp = [self.reference_point[0]+random.randint(-3,3),
                      self.reference_point[1]+random.randint(-3,3)]
                else:
                    rp = self.reference_point



                # self.CenterLabel(self.screen,"Developer Contact : udbhavpathak23@gmail.com",
                #                  3,(200,200,200),(640,150))

                self.camera.targetcenter(targetcenter)
                self.screen.blit(pygame.transform.scale(self.window,(self.size[0]*self.scale,self.size[1]*self.scale)),
                                 rp-self.camera.offset)
            else:
                # self.CenterLabel(self.screen, "Pick Axe", 0, (200, 200, 200), (640, 50))
                self.CenterLabel(self.screen, "Game Over", 0, (255,255,255), (640, 90))
                self.continue_button.show(self.screen)
                if not self.player_won[0] == "Draw":
                    self.CenterLabel(self.screen,f'{self.player_won[0]} Wins !!' ,
                                     6, self.player_won[1], (640, 200))

                    rect = self.dead_imgs[self.player_won[2]-1].get_rect(center = (self.screen.get_width()//2,self.screen.get_height()//2))
                    self.screen.blit(self.dead_imgs[self.player_won[2]-1],rect)

                else:
                    self.CenterLabel(self.screen,"Draw !!",
                                     6, self.player_won[1], (640, 200))

                    rect = self.dead_imgs[self.player_won[2] - 1].get_rect(
                        center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
                    self.screen.blit(self.dead_imgs[self.player_won[2] - 1], rect)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_q:
                            #only for development purpose
                            self.game_over = True
                            # self.player_won = ["Blue Player",(0,230,255),2]
                            # self.player_won = ["Red Player",(255,0,0),1]
                            self.player_won = ["Draw", (255, 255, 0), 3]
                            # self.stars.color[1] = (0, 100, 150)
                            self.bgmusic.stop()
                            self.gameover_music.play(-1)

                        if event.key == pygame.K_LEFT:
                            self.player1.direction = False
                        if event.key == pygame.K_RIGHT:
                            self.player1.direction = True

                        if event.key == pygame.K_UP:
                            if self.player1.velocity < self.player1.vel_limit:
                                self.player1.velocity += 1
                            else:self.player1.velocity = self.player1.vel_limit
                        if event.key == pygame.K_DOWN:
                            if self.player1.velocity > -self.player1.vel_limit:
                                self.player1.velocity -= 1
                            else:self.player1.velocity = -self.player1.vel_limit


                        if event.key == pygame.K_a:
                            self.player2.direction = False
                        if event.key == pygame.K_d:
                            self.player2.direction = True

                        if event.key == pygame.K_w:
                            if self.player2.velocity < self.player2.vel_limit:
                                self.player2.velocity += 1
                            else:self.player2.velocity = self.player2.vel_limit
                        if event.key == pygame.K_s:
                            if self.player2.velocity > -self.player2.vel_limit:
                                self.player2.velocity -= 1
                            else:self.player2.velocity = -self.player2.vel_limit

                        if event.key == pygame.K_l:
                            if self.axe.state == "picked" and self.axe.player_id == 1:
                                self.axe.state = "fire"
                                self.player1.axe = False
                                self.player1.axetimer = 660
                                self.sounds[2].play()


                        if event.key == pygame.K_1:
                            if self.axe.state == "picked" and self.axe.player_id == 2:
                                self.axe.state = "fire"
                                self.player2.axe = False
                                self.player2.axetimer = 660
                                self.sounds[2].play()

                        if event.key == pygame.K_o:
                            if not self.player1.shield.active:
                                if self.player1.mana >= 50:
                                    self.player1.mana -= 50
                                    self.player1.shield.active = True
                                    self.sounds[5].play()

                        if event.key == pygame.K_2:
                            if not self.player2.shield.active:
                                if self.player2.mana >= 50:
                                    self.player2.mana -= 50
                                    self.player2.shield.active = True
                                    self.sounds[5].play()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        if self.continue_button.isover(event.pos):
                            self.bgmusic.stop()
                            self.gameover_music.stop()
                            self.running = False
                            _mainscreen_ = mainscreen.MainScreen(fullscreen= self.fullscreen)
                            break

            pygame.display.update()
            self.clock.tick(self.fps)

    def getdistance(self,p1,p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def CenterLabel(self,screen,text,index,color,center):
        txt = self.fonts[index].render(text, True, color)
        rect = txt.get_rect()
        rect.center = center
        screen.blit(txt, rect)

if __name__ == "__main__":
    game = Game(fullscreen=True)


