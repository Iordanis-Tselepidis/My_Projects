import pygame
from pygame.sprite import Sprite
from settings import Settings

class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.image = pygame.image.load('images/screenshot.bmp').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)


    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
       

        
    def update(self):
        """Move the alien to the right or left"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x