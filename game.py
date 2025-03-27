import pygame
from sprite import sprites, Sprite, Door, RiddleDoor
from player import Player
from input import keys_down, is_key_pressed
from map import *
from os import path
import sys


class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((384, 384))
        pg.display.set_caption("Adventure Game")
        self.clock = pg.time.Clock()
        self.load_data()
        self.game_state = "game"
    
    def load_data(self):
        game_folder = path.abspath(path.dirname(__file__))
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'dungeonmap.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, "player.png")).convert_alpha()
        print(img_folder)
        self.parchment_img = pg.image.load(path.join(img_folder, "riddlesBG.png")).convert_alpha()
    
    def new(self):
        # self.all_sprites = pg.sprite.Group()
        self.walls = []
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'wall':
                self.walls.append((tile_object.x // 32, tile_object.y // 32))
        self.walls.append((-1, 0))
        for i in range(8):
            self.walls.append((i, -1))
        self.walls.append((10, 12))

        self.doors = [RiddleDoor(1, 0, "I'm not the alphabet, but I have letters. I'm not a pole, but I have a flag.", pygame.K_k), RiddleDoor(5, 4, "What gets wetter the more it dries?", pygame.K_i), Door(7, 10), RiddleDoor(8, 2, "What word has the most letters in it?", pygame.K_p)]
        
        self.beers = [Sprite("images/beer.png", 0, 0), Sprite("images/beer.png", 4*32, 10*32), Sprite("images/beer.png", 9*32, 2*32)]
        self.npcs = [Sprite("images/npcSage.png", 2*32, 7*32)]
        self.player = Player("images/player.png", 64, 0, self)
    
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            pygame.time.delay(100)
    
    def wordwarp(self, font, text, width):
        lines = []
        x = 0
        w = len(text)

        while x < w:
            while font.size(text[x:w])[0] > width:
                w -= 1

            if w != len(text):
                while text[w] != " ":
                    w -= 1

            lines.append(text[x:w].strip())
            x = w
            w = len(text)

        return lines
    
    def displayRiddles(self):
        self.screen.fill((207, 202, 177))
        self.screen.blit(self.parchment_img, (0, 0))
        font = pg.font.Font("fonts/ByteBounce.ttf", 40)
        text = font.render("RIDDLES COLLECTED", True, (50, 40, 15))
        font = pg.font.Font("fonts/ByteBounce.ttf", 30)
        text2 = font.render("(Press tab to exit)", True, (50, 40, 15))
        self.screen.blit(text, (47, 32))
        self.screen.blit(text2, (95, 32+30))

        startingY = 100
        for i, riddle in enumerate(self.player.riddlesCollected):
            textlines = []
            riddle = str(i+1) + ". " + riddle
            for line in self.wordwarp(font, riddle, 350):
                riddleText = font.render(f"{line}", True, (50, 40, 15))
                textlines.append(riddleText)
            for line in textlines:
                self.screen.blit(line, (25, startingY))
                startingY += 30
            startingY += 10
    
    def endingScreen(self):
        self.screen.fill((207, 202, 177))
        game_folder = path.abspath(path.dirname(__file__))
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'endingmap.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.screen.blit(self.map_img, (0, 0))

        self.doors.clear()
        self.walls.clear()
        self.beers.clear()
        self.player.x, self.player.y = 6*32, 6*32
        self.player.blockers.clear()
        global sprites
        sprites = [s for s in sprites if isinstance(s, Player)]
        self.npcs = [Sprite("images/npcSage.png", 7*32, 8*32), Sprite("images/npcForrest.png", 4*32, 4*32), Sprite("images/npcMom.png", 6*32, 3*32), Sprite("images/npcDuet.png", 3*32, 6*32), Sprite("images/npcChickpea.png", 8*32, 5*32)]
        sprites.extend(self.npcs)
        self.player.blockers.extend([npc.getLoc() for npc in self.npcs])


    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        if self.game_state in ["game", "ending"]:
            self.player.update()
        
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                keys_down.add(event.key)
                if event.key == pg.K_TAB:  # Press TAB to toggle screens
                    self.toggle_screen("inventory")
            if event.type == pg.KEYUP:
                keys_down.remove(event.key)
    
    def toggle_screen(self, toScreen):
        if toScreen == "inventory":
            if self.game_state == "game":
                self.game_state = "inventory"
            elif self.game_state == "ending":
                self.game_state = "ending"
            else:
                self.game_state = "game"
        else:
            self.game_state = "ending"
            self.endingScreen() 
    
    def draw(self):
        if self.game_state == "game":
            self.screen.fill((30, 150, 50))  # Green background for game
            self.screen.blit(self.map_img, (0, 0))
            for s in sprites:
                s.draw(self.screen)
            # self.player.drawMsg()
            # self.player.npcMsgCue()
            # self.player.npcMsg()
            self.player.allFuncs()
        elif self.game_state == "inventory":
            self.displayRiddles()
        elif self.game_state == "ending":
            self.screen.fill((207, 202, 177))  # Background for ending
            self.screen.blit(self.map_img, (0, 0))  # Ensure ending map is drawn
            for s in sprites:
                s.draw(self.screen)
            font = pygame.font.Font("fonts/ByteBounce.ttf", 40)
            text = font.render("HAPPY BIRTHDAY!", True, (255, 255, 255))
            self.screen.blit(text, (64, 32))  # Draw text on screen
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass



g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()