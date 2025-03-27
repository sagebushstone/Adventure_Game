import math
import pygame
from sprite import RiddleDoor, Door, Sprite
from input import is_key_pressed

movement_speed = 32

class Player(Sprite):
    def __init__(self, image, x, y, game):
        super().__init__(image, x, y)
        self.target_x = x
        self.target_y = y
        self.game = game
        self.blockers = self.game.walls
        self.moving = False  # Prevents movement until aligned

        self.beer_count = 0
        self.beerLocs = self.game.beers
        self.doorLocs = self.game.doors

        self.riddlesCollected = []
        self.keysCollected = []

        self.npcs = self.game.npcs
        self.showMessage = False
        self.showNPCmsg = False
        self.talkedToNPC = False
        self.talkingToNPC = False
        self.showEndGameMsg = False


    def update(self):
        if self.moving:
            if self.x < self.target_x:
                self.x += 32
            elif self.x > self.target_x:
                self.x -= 32
            elif self.y < self.target_y:
                self.y += 32
            elif self.y > self.target_y:
                self.y -= 32

            # Stop moving once aligned with target
            if self.x == self.target_x and self.y == self.target_y:
                self.moving = False
                if (self.x // 32, self.y // 32) in [beer.getSpriteLoc() for beer in self.beerLocs]:
                    for beer in self.beerLocs:
                        if (self.x // 32, self.y // 32) == beer.getSpriteLoc():
                            beer.delete()
                            self.beer_count += 1
                            self.beerLocs.remove(beer)

            return
            

        if not self.moving and (self.x // 32, self.y // 32) == (10, 12):
            self.game.toggle_screen("ending")
            return


        # Only allow new movement if aligned with the grid
        new_y = self.y
        new_x = self.x

        if is_key_pressed(pygame.K_w):
            new_y -= movement_speed
        elif is_key_pressed(pygame.K_s):
            new_y += movement_speed
        elif is_key_pressed(pygame.K_a):
            new_x -= movement_speed
        elif is_key_pressed(pygame.K_d):
            new_x += movement_speed
        
        if is_key_pressed(pygame.K_TAB):
            self.showMessage = False
        

        # npc dialogue checker
        self.showNPCmsg = False
        distance = 5
        for npc in self.npcs:
            distance = math.sqrt((npc.getLoc()[0] - self.x // 32)**2 + (npc.getLoc()[1] - self.y //32)**2)
            if distance < 2 and self.talkedToNPC is False:
                self.showNPCmsg = True
                # return
    
        # if is_key_pressed(pygame.K_e) and self.talkedToNPC:
        #     self.talkingToNPC =  not self.talkingToNPC

        if is_key_pressed(pygame.K_e) and distance < 2:
            self.showNPCmsg = False
            self.talkedToNPC = True
            self.talkingToNPC = not self.talkingToNPC
            # get rid of the lock on the door at the bottom of the screen
            for door in self.doorLocs:
                if door.getLoc() == (7, 10):
                    self.doorLocs.remove(door)
        
        if self.beer_count >= 3 and (10, 12) in self.blockers:
            self.blockers.remove((10, 12))

        # self.showEndGameMsg = False
        # checks if there's a wall/blocker, if there is, the player can't go on that tile
        if (new_x // 32, new_y // 32) in self.blockers:
            if (new_x // 32, new_y // 32) == (10, 12):
                self.showEndGameMsg = True
            return
        
        # checks for doors/riddledoors
        if (new_x // 32, new_y // 32) in [door.getLoc() for door in self.doorLocs]:
            for door in self.doorLocs:
                if (new_x // 32, new_y // 32) == door.getLoc():
                    door.setSeenValue()
                    if (isinstance(door, RiddleDoor) and door.getRiddle() not in self.riddlesCollected):
                        self.riddlesCollected.append(door.getRiddle())
                        self.keysCollected.append((door.getKey(), door.getLoc()))
                        self.showMessage = True
            return
        
        # if the player presses the correct key while next to the right door, the door is unlocked
        for door in self.doorLocs[:]:
            if isinstance(door, RiddleDoor) and is_key_pressed(door.key) and ((door.getKey(), ((new_x //32) - 1, new_y//32)) in self.keysCollected or (door.getKey(), ((new_x //32) + 1, new_y//32)) in self.keysCollected):
                self.doorLocs.remove(door)
        
        # moves the player
        if new_x != self.x or new_y != self.y:  # Only move if changed
            self.target_x, self.target_y = new_x, new_y
            self.moving = True

    def drawMsg(self):
        if self.showMessage:
            font = pygame.font.Font("fonts/ByteBounce.ttf", 25)
            pygame.draw.rect(self.game.screen, (199, 186, 160), pygame.Rect(25, 9*32 - 5, 32*10 + 14, 32*2 + 10))
            pygame.draw.rect(self.game.screen, (255, 252, 219), pygame.Rect(32, 9*32, 32*10, 32*2))
            text = font.render("You found a riddle!", True, (50, 40, 15))
            text2 = font.render("Press tab to see it.", True, (50, 40, 15))
            self.game.screen.blit(text, (40, 9*32 + 7))  # Draw text on screen
            self.game.screen.blit(text2, (40, 9*32 + 35))

    def npcMsgCue(self):
        if self.showNPCmsg:
            font = pygame.font.Font("fonts/ByteBounce.ttf", 25)
            text = font.render("Press e to talk to the NPC", True, (255, 255, 0))
            self.game.screen.blit(text, (25, 160))  # Draw text on screen

    def npcMsg(self):
        if self.talkingToNPC:
            font = pygame.font.Font("fonts/ByteBounce.ttf", 25)
            pygame.draw.rect(self.game.screen, (199, 186, 160), pygame.Rect(25, 9*32 - 5, 32*10 + 14, 32*2 + 10))
            pygame.draw.rect(self.game.screen, (255, 252, 219), pygame.Rect(32, 9*32, 32*10, 32*2))
            text = font.render("Hello Traveler. Here is a riddle.", True, (50, 40, 15))
            #In my reflection, you can see your complexion.
            self.game.screen.blit(text, (40, 9*32 + 5)) 
            text = font.render("In my reflection, you can see", True, (50, 40, 15))
            self.game.screen.blit(text, (40, 9*32 + 22))
            text = font.render("your complexion. What am I?", True, (50, 40, 15))
            self.game.screen.blit(text, (40, 9*32 + 40))

    def endGameMsg(self):
        if self.showEndGameMsg:
            font = pygame.font.Font("fonts/ByteBounce.ttf", 25)
            text = font.render("You need 3 beers", True, (255, 255, 0))
            self.game.screen.blit(text, (5*32, 9*32))
            text = font.render("to leave the dungeon", True, (255, 255, 0))
            self.game.screen.blit(text, (5*32, 9*32 + 20))
    
    def allFuncs(self):
        self.drawMsg()
        self.npcMsgCue()
        self.npcMsg()
        self.endGameMsg()
            