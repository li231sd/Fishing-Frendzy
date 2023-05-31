import pygame
import random

SW = 600
SH = 400

class Bomb:
    def __init__(self):
        self.image = pygame.image.load("assets/bomb.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.x = SW
        self.y = random.randint(50, SH - 50)
        self.speed = random.uniform(0.2, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        self.x -= self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
