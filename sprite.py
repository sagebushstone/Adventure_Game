import pygame

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image, x, y):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image)
            loaded[image] = self.image
        self.x = x
        self.y = y
        sprites.append(self)

    def delete(self):
        sprites.remove(self)
    
    def getLoc(self):
        return (self.x // 32, self.y // 32)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def getSpriteLoc(self):
        return (self.x // 32, self.y // 32)

class Door:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hasBeenSeen = False
    
    def getLoc(self):
        return (self.x, self.y)
    
    def setSeenValue(self):
        self.hasBeenSeen = True

class RiddleDoor(Door):
    def __init__(self, x, y, riddle, key):
        super().__init__(x, y)
        self.riddle = riddle
        self.key = key

    def getRiddle(self):
        return self.riddle
    
    def getKey(self):
        return self.key