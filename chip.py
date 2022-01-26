import pygame


class Chip(pygame.sprite.Sprite):
    def __init__(self, type, colorIndex):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = 0
        self.type = type
        self.colorIndex = colorIndex
        self.rect = 0

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move(15, 25)

    def getImage(self):
        return self.image

    def setImage(self, image):
        self.image = image
        self.rect = image.get_rect()

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getColor(self):
        return self.colorIndex

    def setColor(self, colorIndex):
        self.colorIndex = colorIndex
