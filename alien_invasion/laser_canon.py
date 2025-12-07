import pygame
from pygame.sprite import Sprite

class LaserCanon(Sprite):
    """A class to manage the bullets in the game"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.new_image = pygame.image.load('images/beam.bmp').convert_alpha()
        self.rect = self.new_image.get_rect()

        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a float
        self.y = float(self.rect.y)

        self.laser_sound = pygame.mixer.Sound('sounds\laser_canon.ogg')

    def update(self):
        """Move laser up the screen"""

        # Update the exat position of the bullet
        self.y -= self.settings.laser_canon_speed
        self.rect.y = self.y

    def draw_laser(self):
        """Draw the laser to the screen"""
        self.screen.blit(self.new_image, self.rect)


    def make_laser_sound(self):
        pygame.mixer.Sound.play(self.laser_sound)