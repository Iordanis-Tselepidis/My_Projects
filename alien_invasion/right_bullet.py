import pygame
from pygame.sprite import Sprite

class RightBullet(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.new_image = pygame.image.load('images/spaceMissiles_003.bmp').convert_alpha()
        self.big_smoke_image = pygame.image.load('images/smoke.bmp').convert_alpha()
        self.smoke_image = pygame.transform.scale_by(self.big_smoke_image, 0.5)
        self.rect = self.new_image.get_rect()
        self.smoke_rect = self.smoke_image.get_rect()

        self.rect.topright = ai_game.ship.rect.topright
        self.smoke_rect.topright = self.rect.bottomright

        self.y = float(self.rect.y)
        self.smoke_y = float(self.smoke_rect.y)

        self.right_bullet_sound = pygame.mixer.Sound('sounds\launch.ogg')


    def update(self):
        """Move bullet up the screen"""

        # Update the exact position of the bullet
        self.y -= self.settings.right_bullet_speed
        self.rect.y = self.y
        self.smoke_y -= self.settings.right_bullet_speed
        self.smoke_rect.y = self.smoke_y

    def draw_right_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.new_image, self.rect)
        self.screen.blit(self.smoke_image, self.smoke_rect)

    
    def make_right_bullet_sound(self):
        pygame.mixer.Sound.play(self.right_bullet_sound)