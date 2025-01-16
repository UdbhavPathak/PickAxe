import pygame
import sys
import map
import widgets
import game
import about
pygame.init()
pygame.mixer.init()

class MainScreen:
    def __init__(self,fullscreen = False,music = False):

        with open("data/gamedata.txt","r") as gdata:
            self.game_data = gdata.read().split("\n")

        self.size = (1280, 720)
        self.fullscreen = fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN | pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode(self.size)

        self.fonts = [
            pygame.font.Font("fonts/breathe_fire/Breathe Fire.otf", 120),
            pygame.font.Font("fonts/breathe_fire/Breathe Fire.otf", 45),
            pygame.font.Font("fonts/pixel/pixel.ttf", 40),
            pygame.font.Font("fonts/pixel/pixel.ttf", 20),

        ]
        pygame.display.set_caption("PickAxe")
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.running = True




        if not music:
            self.bgmusic = pygame.mixer.music
            self.bgmusic.load("sounds/music2.mp3")
            self.bgmusic.set_volume(int(self.game_data[2]) / 100)
            self.bgmusic.play(-1)
        else:
            self.bgmusic = music
            self.bgmusic.set_volume(int(self.game_data[2]) / 100)
            self.bgmusic.unpause()


        self.stars = widgets.Stars([(0, self.size[0]), (0,self.size[1])], [1, 3],
                           [(255, 255, 255), (100, 100, 100)])
        self.axe_sign = pygame.transform.smoothscale_by(pygame.image.load("images/axe_sign.PNG"),0.5).convert_alpha()
        self.center = (self.screen.get_width()//2,self.screen.get_height()//2)
        self.button_frame = widgets.Transparent_Frame((580,400),[self.center[0],self.center[1]+70],
                                                      (50,50,50),[(200,200,200),1])

        self.play_button = widgets.ImageButton("Play",(250,70),(0,0),"images/Ui/button.png")
        self.play_button.rect.center = [self.center[0],self.center[1]-30]

        self.maps_button = widgets.ImageButton("Maps",(250,70),(0,0),"images/Ui/button.png")
        self.maps_button.rect.center =[self.play_button.rect.center[0],self.play_button.rect.center[1]+100]

        self.quit_button = widgets.ImageButton("Quit", (250, 70), (0, 0), "images/Ui/button.png")
        self.quit_button.rect.center = [self.maps_button.rect.center[0], self.maps_button.rect.center[1] + 100]

        self.about_button = widgets.ImageButton("", (50, 50), (self.center[0]*2-70,20), "images/Ui/about.png")
        self.sound_button = widgets.ImageButton("", (50, 50), (self.center[0]*2-70,90), "images/Ui/sound.png")
        self.sound_frame = widgets.Transparent_Frame((350,200),
                                                     [self.sound_button.rect.x-320//2,self.sound_button.rect.bottom+120],
                                                     (150,150,150),((150,150,150),1))

        self.sound_bar = widgets.Scale(x = self.sound_frame.rect.x+30,y = self.sound_frame.rect.y+100,
                           barcolor=(0,0,0),bordercolor=[(200,200,200),(200,200,200)],radius=10,height=7,width=200,
                           circlecolor=(0,0,0),border=1,fill=(200,200,200),value=int(self.game_data[2]))

        self.apply_button = widgets.SimpleButton(x = self.sound_frame.rect.centerx-75,
                                                 y = self.sound_frame.rect.bottom - 60,width=150,height=40
                                                 ,text="APPLY",font = self.fonts[3],bdcolor=(200,200,200),color=(30,30,30)
                                                 ,bd = 1,padx = 45,pady=5)

        self.active_sound = False
        while self.running:
            self.screen.fill((0,0,0))
            self.stars.add_data(scale=3)
            self.stars.show(self.screen)
            self.button_frame.show(self.screen,imageshow=True)
            self.screen.blit(self.axe_sign,((self.screen.get_width()//2-self.axe_sign.get_width()//2)+8,
                                            (self.screen.get_height()//2-self.axe_sign.get_height()//2)+50))
            self.CenterLabel(self.screen,"Pick Axe",0,(200,200,200),(self.screen.get_width()//2,100))

            self.play_button.show(self.screen)
            self.maps_button.show(self.screen)
            self.quit_button.show(self.screen)
            self.about_button.show(self.screen)
            self.sound_button.show(self.screen)
            if self.active_sound:
                self.sound_frame.show(self.screen,False)
                self.CenterLabel(self.screen,"Sound :",1,(200,200,200),(self.sound_frame.rect.centerx,
                                                                        self.sound_frame.rect.centery-60))

                self.CenterLabel(self.screen,f"{self.sound_bar.get()}",2,(200,200,200),
                                 (self.sound_bar.rect.right+50,self.sound_bar.rect.y-5))

                self.sound_bar.show(self.screen)
                self.sound_bar.update()
                self.sound_bar.move()
                self.apply_button.draw(self.screen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                self.sound_bar.checkevent(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.apply_button.isover(event.pos):
                        self.play_button.sound.play()
                        self.game_data[2] = str(self.sound_bar.get())
                        self.bgmusic.set_volume(self.sound_bar.get()/100)
                        self.save_file()

                    if self.sound_button.isover(event.pos):
                        if not self.active_sound:
                            self.active_sound = True
                        else:self.active_sound = False

                    if self.about_button.isover(event.pos):
                        self.bgmusic.pause()
                        self.running = False
                        _about_ = about.AboutWindow(fullscreen=self.fullscreen,music=self.bgmusic)
                        break

                    if self.play_button.isover(event.pos):
                        self.bgmusic.stop()
                        self.running = False
                        self.play_button.sound.play()
                        _game_ = game.Game(fullscreen = self.fullscreen)
                        break

                    if self.maps_button.isover(event.pos):
                        self.bgmusic.pause()
                        self.running = False
                        self.maps_button.sound.play()
                        _maps_ = map.Map_Select_Window(fullscreen = self.fullscreen,music=self.bgmusic)
                        break

                    if self.quit_button.isover(event.pos):
                        self.running = False
                        pygame.quit()
                        sys.exit(0)


            pygame.display.update()
            self.clock.tick(self.fps)

    def CenterLabel(self, screen, text, index, color, center):
        txt = self.fonts[index].render(text, True, color)
        rect = txt.get_rect()
        rect.center = center
        screen.blit(txt, rect)

    def save_file(self):
        with open("data/gamedata.txt","w") as gamedata:
            newdata = gamedata.write("\n".join(self.game_data))

if __name__ == "__main__":
    mainscreen = MainScreen(fullscreen=True)


