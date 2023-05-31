import pygame
import random

SW = 600
SH = 400

class Fish:
    def __init__(self):
        self.fish = random.randint(1, 5)
        self.image = pygame.image.load(f"assets/Fish{self.fish}.png")
        self.image = pygame.transform.scale(self.image, (60, 40))
        self.x = 0
        self.y = random.randint(50, SH - 50)
        self.speed = random.uniform(0.2, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.is_caught = False

    def update(self, line_rect):
        if not self.is_caught:
            self.x += self.speed
            self.rect.center = (self.x, self.y)
        elif line_rect.width > 0:
            self.rect.centerx = line_rect.centerx
            self.y -= 0.5
            self.rect.centery = self.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)
