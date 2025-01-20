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
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)

        self.fonts = [
            pygame.font.Font("fonts/breathe_fire/Breathe Fire.otf", 120),
            pygame.font.Font("fonts/breathe_fire/Breathe Fire.otf", 45),
            pygame.font.Font("fonts/pixel/pixel.ttf", 40),
            pygame.font.Font("fonts/pixel/pixel.ttf", 20),
            pygame.font.Font("fonts/pixel/pixel.ttf", 30),

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
        self.settings_button = widgets.ImageButton("", (50, 50), (self.center[0]*2-70,90), "images/Ui/settings.png")
        self.settings_frame = widgets.Transparent_Frame((600,400),
                                     [self.center[0],self.center[1]+50],
                                      (255,255,255),((150,150,150),1))

        self.sound_bar = widgets.Scale(x = self.settings_frame.rect.x+150,y = self.settings_frame.rect.y+100,
                           barcolor=(0,0,0),bordercolor=[(200,200,200),(200,200,200)],radius=10,height=7,width=200,
                           circlecolor=(0,0,0),border=1,fill=(200,200,200),value=int(self.game_data[2]))

        self.apply_button = widgets.SimpleButton(x = self.settings_frame.rect.centerx-75,
                                                 y = self.settings_frame.rect.bottom - 60,width=150,height=40
                                                 ,text="APPLY",font = self.fonts[3],bdcolor=(200,200,200),color=(30,30,30)
                                                 ,bd = 1,padx = 45,pady=5)

        self.camera_button = widgets.TranslucentButton("ON",
               (self.settings_frame.rect.x + 300,self.sound_bar.rect.y+50),(0,0,0),("verdana",25))

        self.fullscreen_button = widgets.TranslucentButton("ON",
                       (self.settings_frame.rect.x + 300, self.sound_bar.rect.y + 130),
                       (0, 0, 0), ("verdana", 25))

        if self.fullscreen:
            self.fullscreen_button.text = "ON"
        else: self.fullscreen_button.text = "OFF"
        if bool(int(self.game_data[3])):
            self.camera_button.text = "ON"
        else:self.camera_button.text = "OFF"
        self.close_settings= widgets.ImageButton("",(40,40), (0,0), "images/icons/delete.png")
        self.close_settings.rect.center = self.settings_frame.rect.topright

        self.s_angle = 0

        self.active_settings = False
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
            self.settings_button.show(self.screen)

            if self.active_settings:
                self.settings_frame.show(self.screen,False)
                self.CenterLabel(self.screen,"Settings ",1,(200,200,200),(self.settings_frame.rect.x+150,
                                                                        self.settings_frame.rect.y+35))

                self.CenterLabel(self.screen,f"{self.sound_bar.get()}",2,(200,200,200),
                                 (self.sound_bar.rect.right+50,self.sound_bar.rect.y-5))
                img = pygame.transform.rotozoom(self.settings_button.image,self.s_angle,1)
                r = img.get_rect(center = (self.settings_frame.rect.x+40,self.settings_frame.rect.y+35))
                self.screen.blit(img,r)
                if self.s_angle >= 360:self.s_angle = 0
                else:self.s_angle -= 1
                self.Label(self.screen,"Sound :",4,(200,200,200),
                           (self.settings_frame.rect.x+20,self.sound_bar.rect.y-20))
                self.Label(self.screen, "Camera Motion :", 4, (200, 200, 200),
                           (self.settings_frame.rect.x + 20, self.sound_bar.rect.y+50))
                self.Label(self.screen, "FullScreen :", 4, (200, 200, 200),
                           (self.settings_frame.rect.x + 20, self.sound_bar.rect.y + 130))

                self.sound_bar.show(self.screen)
                self.sound_bar.update()
                self.sound_bar.move()
                self.fullscreen_button.show(self.screen)
                self.camera_button.show(self.screen)
                self.apply_button.draw(self.screen)
                self.close_settings.show(self.screen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                self.sound_bar.checkevent(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.camera_button.isover(event.pos) and self.active_settings:
                        self.play_button.sound.play()
                        if bool(int(self.game_data[3])):
                            self.game_data[3] = "0"
                            self.camera_button.text = "OFF"
                        else:
                            self.game_data[3] = "1"
                            self.camera_button.text = "ON"
                        self.save_file()
                    if self.fullscreen_button.isover(event.pos) and self.active_settings:
                        pygame.display.toggle_fullscreen()
                        self.play_button.sound.play()
                        if self.fullscreen:
                            self.fullscreen = False
                            self.fullscreen_button.text = "OFF"
                        else:
                            self.fullscreen = True
                            self.fullscreen_button.text = "ON"


                    if self.apply_button.isover(event.pos) and self.active_settings:
                        self.play_button.sound.play()
                        self.game_data[2] = str(self.sound_bar.get())
                        self.bgmusic.set_volume(self.sound_bar.get()/100)
                        self.save_file()

                    if self.settings_button.isover(event.pos):
                        if not self.active_settings:
                            self.active_settings = True
                        else:self.active_settings = False

                    if self.close_settings.isover(event.pos) and self.active_settings:
                        self.active_settings = False

                    if not self.active_settings:
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

    def Label(self, screen, text, index, color, pos):
        txt = self.fonts[index].render(text, True, color)
        screen.blit(txt, pos)

    def save_file(self):
        with open("data/gamedata.txt","w") as gamedata:
            newdata = gamedata.write("\n".join(self.game_data))

if __name__ == "__main__":
    mainscreen = MainScreen(fullscreen=True)


