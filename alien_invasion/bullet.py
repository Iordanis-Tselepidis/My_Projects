import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage the bullets in the game"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.new_image = pygame.image.load('images/awesome_bullet.bmp').convert_alpha()
        self.rect = self.new_image.get_rect()

        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a float
        self.y = float(self.rect.y)

        self.bullet_sound = pygame.mixer.Sound('sounds\\slimeball.ogg')

    def update(self):
        """Move bullet up the screen"""

        # Update the exat position of the bullet
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.new_image, self.rect)


    def make_bullet_sound(self):
        pygame.mixer.Sound.play(self.bullet_sound)