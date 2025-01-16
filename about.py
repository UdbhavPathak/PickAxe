import pygame,widgets,animation,sprite,sys,mainscreen
from pygame.locals import*
import webbrowser
pygame.init()
pygame.mixer.init()

class AboutWindow:
    def __init__(self,fullscreen,music = False):
        self.music = music
        self.music.unpause()
        self.fullscreen = fullscreen
        self.size = (1280,720)
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.size,pygame.NOFRAME | pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption("Pick Axe")

        self.fps = 60
        self.clock = pygame.time.Clock()
        self.running = True
        self.stars = widgets.Stars([(0, self.size[0]), (0,self.size[1])], [1, 3],
                           [(255, 255, 255), (100, 100, 100)])

        self.fonts = [
            pygame.font.Font("fonts/breathe_fire/Breathe Fire.otf", 100),
            pygame.font.Font("fonts/breathe_fire/Breathe Fire.otf", 60),
            pygame.font.SysFont("Verdana", 23),
            pygame.font.Font("fonts/breathe_fire/Breathe Fire.otf", 40),
            pygame.font.SysFont("Verdana", 30),
            pygame.font.SysFont("Verdana", 15),

        ]
        self.fonts[4].set_underline(True)
        self.center = [self.screen.get_width()//2,self.screen.get_height()//2]
        self.data_frame = widgets.Transparent_Frame((1200,500),(self.center[0],self.center[1]+100)
        ,(100,100,100),((200,200,200),1))
        self.axe_sign = pygame.transform.smoothscale_by(pygame.image.load("images/axe_sign.PNG"),0.3).convert_alpha()

        self.tab_names = ["About","Controls","Power Ups","Credits","Project Info"]
        self.tab_index = 0
        self.tabs = [["About",self.about_game],["Controls",self.controls_data],["Power Ups",self.power_ups],['Credits',self.credits]
            ,["Project Info",self.project_info]]

        self.right_arrowbutton = widgets.ArrowButton((1100, 250), "right")
        self.left_arrowbutton = widgets.ArrowButton((100, 250), "left")
        self.right_arrowbutton.updatesize(40,40)
        self.left_arrowbutton.updatesize(40,40)

        self.right_arrowbutton.rect.topleft = (self.data_frame.rect.right-240,self.data_frame.rect.y-65)

        self.left_arrowbutton.rect.topleft = (self.data_frame.rect.x+200,self.data_frame.rect.y-65)
        self.back_button = widgets.ImageButton("Back",(250, 70), (0, 0), "images/Ui/button.png")
        self.back_button.rect.center = (self.data_frame.rect.centerx,self.data_frame.rect.bottom-50)
        self.gameimg = pygame.image.load("images/Draw.PNG").convert_alpha()
        self.playerimgs = []
        self.powerups = []
        for i in range(1,3):
            img = pygame.transform.flip(pygame.image.load(f"images/player{i}/idle/1.png"),True,False).convert_alpha()
            img = pygame.transform.scale_by(img,0.75)
            self.playerimgs.append(img)

        self.powerups.append(sprite.Orb((self.data_frame.rect.x+50,self.data_frame.rect.y+50),"greenorb","heal"))
        self.powerups.append(sprite.Orb((self.data_frame.rect.x+50,self.data_frame.rect.y+180),"blueorb","mana"))
        self.powerups.append(sprite.Orb((self.data_frame.rect.x+50,self.data_frame.rect.y+310),"redorb",
                                    "poision"))
        self.powerups[1].animation.image = pygame.image.load("images/powerups/blueorb/sign2.png").convert_alpha()

        self.githubimg = pygame.image.load("images/Ui/github.png").convert_alpha()

        self.orb_data = {
            "heal":["Healing Orb","Adds 25% of total health",(0,255,0)],
            "mana":["Mana Orb","Restores the Mana",(0,255,255)],
            "poision":["Poision Orb","Activates the poision axe and increases the axe damage",(255, 165, 0)]
        }
        self.projectinfo = [
            "This Game is built by using Python Programming Language (Python 3.12)",
            "Using Pygame library (pygame 2.5.2 (SDL 2.28.3, Python 3.12.4)",
            "and free resources available publicly..",
        ]
        self.github_button = widgets.TranslucentButton("GitHub",
                                                       [self.data_frame.rect.centerx-100,
                                                        self.data_frame.rect.centery-30],
                                                       (0, 0, 0), ["verdana", 50])

        self.musiclink = widgets.TranslucentButton("Duneon Fighter Online - Symphony [Youtube]",
                                                       [self.data_frame.rect.x+5 ,
                                                        self.data_frame.rect.centery-50],
                                                       (0, 0, 0), ["verdana", 23])
        with open("data/about.txt","r") as about:
            self.about_data = about.read().split("\n")
        self.urls = ["https://github.com/UdbhavPathak/PickAxe","https://youtu.be/9ZOtEZkdzoI?"]

        while self.running:
            self.screen.fill((0,0,0))
            self.stars.add_data(scale=2)
            self.stars.show(self.screen)

            self.CenterLabel(self.screen,"Pick Axe",0,(200,200,200),(self.screen.get_width()//2,70))
            self.CenterLabel(self.screen, f"{self.tab_names[self.tab_index]}", 1, (200, 200, 200),
                             (self.screen.get_width() // 2, self.data_frame.rect.y-50))

            self.data_frame.show(self.screen)
            self.right_arrowbutton.show(self.screen)
            self.left_arrowbutton.show(self.screen)
            self.back_button.show(self.screen)
            if self.tab_names[self.tab_index] == self.tabs[self.tab_index][0]:
                self.tabs[self.tab_index][1]()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit(0)
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.tab_names[self.tab_index] == "Credits":
                        if self.musiclink.isover(event.pos):
                            webbrowser.open(self.urls[1])
                    if self.tab_names[self.tab_index] == "Project Info":
                        if self.github_button.isover(event.pos):
                            webbrowser.open(self.urls[0])

                    if self.back_button.isover(event.pos):
                        self.running = False
                        self.music.pause()
                        _mainscreen_ = mainscreen.MainScreen(music=self.music, fullscreen=self.fullscreen)
                        break
                    if self.right_arrowbutton.isover(event.pos):
                        if self.tab_index >= len(self.tab_names)-1:
                            self.tab_index = 0
                        else:
                            self.tab_index += 1
                    if self.left_arrowbutton.isover(event.pos):
                        if self.tab_index <= 0:
                            self.tab_index = len(self.tab_names)-1
                        else:
                            self.tab_index -= 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.tab_index >= len(self.tab_names)-1:
                            self.tab_index = 0
                        else:
                            self.tab_index += 1
                        self.right_arrowbutton.sound.play()

                    if event.key == pygame.K_LEFT:
                        if self.tab_index <= 0:
                            self.tab_index = len(self.tab_names) - 1
                        else:
                            self.tab_index -= 1
                        self.left_arrowbutton.sound.play()

            pygame.display.update()
            self.clock.tick(self.fps)

    def CenterLabel(self, screen, text, index, color, center):
        txt = self.fonts[index].render(text, True, color)
        rect = txt.get_rect()
        rect.center = center
        screen.blit(txt, rect)

    def about_game(self):
        for i,line in enumerate(self.about_data):
            self.CenterLabel(self.screen,line,2,(200,200,200),
                             (self.data_frame.rect.centerx,self.data_frame.rect.y+30 + 40*i))
        self.screen.blit(self.gameimg,
                     (self.data_frame.rect.centerx-self.gameimg.get_width()//2,self.data_frame.rect.y+140))


    def controls_data(self):
        self.Label(self.screen,"Red Player",3,(200,0,0),
                   (self.data_frame.rect.x+20,self.data_frame.rect.y+10))
        keys = [["Up Arrow","Down Arrow","Left Arrow","Right Arrow","L","O"],
                ["W","S","A","D","1","2"]]
        attributes = ["Speed Increase :","Speed Decrease :","Turn left :","Turn Right :","Throw Axe :","Shield :"]

        for i,attr in enumerate(attributes):
            self.Label(self.screen, f"{attr} {keys[0][i]}", 2, (200,200,200),
                       (self.data_frame.rect.x + 20, self.data_frame.rect.y + 70 +i*40))

        self.screen.blit(self.playerimgs[0],
                         (self.data_frame.rect.centerx-self.playerimgs[0].get_width()//2-100,self.data_frame.rect.y+80))

        pygame.draw.line(self.screen,(200,200,200),(self.data_frame.rect.centerx,self.data_frame.rect.y+30),
                         (self.data_frame.rect.centerx, self.data_frame.rect.y +350) ,1)

        self.Label(self.screen, "Blue Player", 3, (0, 150, 200),
                   (self.data_frame.rect.centerx + 30, self.data_frame.rect.y + 10))
        for i,attr in enumerate(attributes):
            self.Label(self.screen, f"{attr} {keys[1][i]}", 2, (200,200,200),
                       (self.data_frame.rect.centerx + 30, self.data_frame.rect.y + 70 +i*40))

        self.screen.blit(self.playerimgs[1],
                         (self.data_frame.rect.right - self.playerimgs[0].get_width() // 2 - 100,
                          self.data_frame.rect.y + 80))



    def project_info(self):
        self.Label(self.screen,"Language / Libraries and Versions",4,(255,255,255),
                   (self.data_frame.rect.x+30,self.data_frame.rect.y+20))
        pygame.draw.circle(self.screen,(255,255,0),
                           (self.data_frame.rect.x+30,self.data_frame.rect.y+85),5)
        for i,line in enumerate(self.projectinfo):
            self.Label(self.screen,line,2,(200,200,200),(self.data_frame.rect.x+50,
                                                         self.data_frame.rect.y + 70 + i*40))

        self.screen.blit(self.githubimg,(self.data_frame.rect.centerx-self.githubimg.get_width()//2-150,
                                         self.data_frame.rect.centery-30))
        self.github_button.show(self.screen)
        self.Label(self.screen,"Developer Contact : ",5,(255,255,255),
                   (self.github_button.rect.x+20,self.github_button.rect.bottom))
        self.Label(self.screen, "udbhavpathak23@gmail.com: ",5, (255, 255, 255),
                   (self.github_button.rect.x + 20, self.github_button.rect.bottom + 20))

    def credits(self):
        self.Label(self.screen,"Sound Effects :",4,(255,255,255),(self.data_frame.rect.x+30,
                                                                  self.data_frame.rect.y+20))
        self.Label(self.screen,"Pixabay.com , Zapsplat.com",2,(255,255,255),(self.data_frame.rect.x+30,
                                                                  self.data_frame.rect.y+75))

        self.Label(self.screen, "Background Music :", 4, (255, 255, 255), (self.data_frame.rect.x + 30,
                                                                        self.data_frame.rect.y + 150))
        self.musiclink.show(self.screen)

        pygame.draw.line(self.screen,(120,120,120),(self.data_frame.rect.centerx,self.data_frame.rect.y+30),
                         (self.data_frame.rect.centerx,self.data_frame.rect.y+300))

        self.Label(self.screen, "Images/Icons :", 4, (255, 255, 255), (self.data_frame.rect.centerx + 30,
                                                                        self.data_frame.rect.y + 20))
        self.Label(self.screen, "Flaticon.com , Google Free Resources", 2, (255, 255, 255), (self.data_frame.rect.centerx + 30,
                                                                               self.data_frame.rect.y + 75))

    def power_ups(self):
        for i,orb in enumerate(self.powerups):
            orb.show(self.screen)
            self.Label(self.screen,self.orb_data[orb.type][0],3,self.orb_data[orb.type][2],
                       (self.data_frame.rect.x+120,self.data_frame.rect.y+50 +i*130))
            self.Label(self.screen,self.orb_data[orb.type][1],2,(200,200,200),
                       (self.data_frame.rect.x + 350,self.data_frame.rect.y+55+i*130))
            pygame.draw.line(self.screen,(50,50,50),
                             (self.data_frame.rect.x+30,self.data_frame.rect.y+110+i*140),
                             (self.data_frame.rect.right-30,self.data_frame.rect.y+110+i*140))
    def Label(self, screen, text, index, color, pos):
        txt = self.fonts[index].render(text, True, color)
        screen.blit(txt, pos)


if __name__ == "__main__":
    about = AboutWindow(fullscreen=True,music=None)

