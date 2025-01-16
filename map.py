import sys
import pygame
import animation
import mainscreen
import sprite
import widgets
from pygame.locals import*
from icecream import ic
pygame.init()
pygame.mixer.init()

class  Map_Select_Window:
    def __init__(self,fullscreen = False,**kwargs):
        self.music = kwargs["music"]
        self.music.unpause()
        self.fullscreen = fullscreen
        self.size = (1280,720)
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.size,pygame.NOFRAME | pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)

        self.fps = 60
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption("Pick Axe")



        self.fonts = [pygame.font.Font("fonts/breathe_fire/Breathe Fire.otf",70)]
        self.stars = widgets.Stars([(0, self.size[0]), (0,self.size[1])], [1, 3],
                           [(255, 255, 255), (100, 100, 100)])

        self.wallimg = pygame.image.load("images/walls.png").convert_alpha()
        self.portalimg = pygame.image.load("images/portal.png").convert_alpha()
        self.floor = sprite.Floor()
        self.center = (self.screen.get_width() // 2, self.screen.get_height()//2-30)



        with open("data/gamedata.txt" ,"r") as gdata:
            self.gamedata = gdata.read().split("\n")

        self.frameindex = int(self.gamedata[0])
        self.selected_map = int(self.gamedata[0])
        self.no_of_maps = int(self.gamedata[1])

        self.map_surfs = []
        for i in range(1,self.no_of_maps+1):
            self.map_surfs.append(self.load_maps(i))

        self.right_arrowbutton = widgets.ArrowButton((1100, 250), "right")
        self.left_arrowbutton = widgets.ArrowButton((100, 250), "left")
        self.right_arrowbutton.rect.topleft = (self.screen.get_width()-100-self.right_arrowbutton.rect.w,
                                               self.center[1]-self.right_arrowbutton.rect.h//2,)

        self.left_arrowbutton.rect.topleft = (100,self.center[1] - self.left_arrowbutton.rect.h // 2,)

        self.back_button = widgets.ImageButton("Back",(250,70),(0,0),"images/Ui/button.png")
        self.back_button.rect.center = (self.center[0]-200,self.center[1]+290)

        self.select_button = widgets.ImageButton("Select", (250, 70), (0, 0), "images/Ui/button.png")
        self.select_button.rect.right = self.screen.get_width()-self.back_button.rect.x
        self.select_button.rect.centery = self.back_button.rect.centery





    # def run(self):
        while self.running:
            self.screen.fill((0,0,0))
            self.stars.add_data(scale=2)
            self.stars.show(self.screen)
            maprect = self.map_surfs[0].get_rect(center = self.center)

            self.screen.blit(self.map_surfs[self.frameindex-1],maprect)
            pygame.draw.rect(self.screen,(200,200,200),maprect,1)
            if self.fullscreen:
                self.CenterLabel(self.screen,f"Map : {self.frameindex}",0,(200,200,200),
                                 (self.center[0],80))
            else:
                self.CenterLabel(self.screen, f"Map : {self.frameindex}", 0, (200, 200, 200),
                                 (self.center[0], 50))

            if self.frameindex == self.selected_map:
                self.select_button.text = "Selected"
            else:
                self.select_button.text = "Select"
            self.right_arrowbutton.show(self.screen)
            self.left_arrowbutton.show(self.screen)
            self.back_button.show(self.screen)
            self.select_button.show(self.screen)




            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.frameindex < self.no_of_maps:
                            self.frameindex += 1
                        else:
                            self.frameindex = 1
                        self.left_arrowbutton.sound.play()
                    if event.key == pygame.K_LEFT:
                        if self.frameindex > 1:
                            self.frameindex -= 1
                        else:
                            self.frameindex = self.no_of_maps
                        self.left_arrowbutton.sound.play()


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.select_button.isover(event.pos):
                        self.select_map()

                    if self.back_button.isover(event.pos):
                        self.running = False
                        self.music.pause()
                        _mainscreen_ = mainscreen.MainScreen(music=self.music,fullscreen=self.fullscreen)
                        break

                    if self.left_arrowbutton.isover(event.pos):
                        if self.frameindex > 1:
                            self.frameindex -= 1
                        else:
                            self.frameindex = self.no_of_maps

                    if self.right_arrowbutton.isover(event.pos):
                        if self.frameindex < self.no_of_maps:
                            self.frameindex += 1
                        else:
                            self.frameindex = 1

            pygame.display.update()
            self.clock.tick(self.fps)

    def CenterLabel(self, screen, text, index, color, center):
        txt = self.fonts[index].render(text, True, color)
        rect = txt.get_rect()
        rect.center = center
        screen.blit(txt, rect)


    def load_maps(self,index):
        surf = pygame.Surface(self.size)
        # surf.set_colorkey((0,0,0))
        mapdata = []
        with open(f"data/maps/map{index}.txt","r") as data:
            sdata = data.read().split("\n")
            for i in sdata:
                mapdata.append(i.split(" "))
        surf.blit(self.floor.floor(),(0,0))

        for y_index,y in enumerate(mapdata):
            for x_index,x in enumerate(y):
                if x == "B" or x == "T" or x == "R" or x == "L":
                    surf.blit(self.wallimg,[40*x_index,40*y_index])
                    pygame.draw.rect(surf, (15, 10, 25),
                                     self.wallimg.get_rect(topleft =[40*x_index,40*y_index] ), 2)

                elif x == 'P':
                    surf.blit(self.portalimg, [40 * x_index, 40 * y_index])

        surf = pygame.transform.scale_by(surf,0.6)
        return surf


    def select_map(self):
        self.selected_map = self.frameindex
        self.gamedata[0] = str(self.selected_map)
        with open("data/gamedata.txt","w") as writedata:
            writedata.write("\n".join(self.gamedata))
            # ic("Selected")
            # ic(self.frameindex)
            # ic(self.selected_map)
            # ic(self.gamedata)



if __name__ == "__main__":
    maps = Map_Select_Window(fullscreen=True)
    # maps.run()