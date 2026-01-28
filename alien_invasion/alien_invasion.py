import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from left_bullet import LeftBullet
from right_bullet import RightBullet
from laser_canon import LaserCanon
from alien import Alien 
from button import Button
from scoreboard import Scoreboard




class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init() 
        pygame.mixer.init()  
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.bg_image = pygame.image.load('images/back.bmp')
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.left_bullets = pygame.sprite.Group()
        self.right_bullets = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.make_boom = pygame.mixer.Sound('sounds//explosion.ogg')
        self.life_lost = pygame.mixer.Sound('sounds//life_lost.ogg')
        self.game_active = False
        self.play_button = Button(self, "Play")


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_lasers()
                self._update_left_bullets()
                self._update_right_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(80)


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_active:
                    self._check_mousedown_events(event)
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
        

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        #elif event.key == pygame.K_w:
            #self.ship.moving_up = True
        #elif event.key == pygame.K_s:
            #self.ship.moving_down = True
        elif event.key == pygame.K_ESCAPE:
            contents = self.stats.path.read_text()
            true_contents = int(contents)
            if self.stats.high_score > true_contents:
                self.stats.path.write_text(str(self.stats.high_score))
            sys.exit()
        #elif event.key == pygame.K_SPACE:
            #self._fire_bullet()
            

    def _check_mousedown_events(self, event):
        if event.button == 1:
            self._fire_bullet()
        elif event.button == 3:
            self._fire_right_bullets()
            self._fire_left_bullets()
        elif event.button == 2:
            self._fire_laser_canon()
        

    def _check_keyup_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            new_bullet.make_bullet_sound()


    def _fire_left_bullets(self):
        if len(self.left_bullets) < self.settings.left_bullets_allowed:
            new_left_bullet = LeftBullet(self)
            self.left_bullets.add(new_left_bullet)

    
    def _fire_right_bullets(self):
        if len(self.right_bullets) < self.settings.right_bullets_allowed:
            new_right_bullet = RightBullet(self)
            self.right_bullets.add(new_right_bullet)
            new_right_bullet.make_right_bullet_sound()


    def _fire_laser_canon(self):
        if len(self.lasers) < self.settings.lasers_allowed:
            new_laser = LaserCanon(self)
            self.lasers.add(new_laser)
            new_laser.make_laser_sound()


    def _update_bullets(self):
        """Update position of bullets and get rid of the old bullets"""
        self.bullets.update()

        # Get rid of bullets that have dissapeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

       
    def _update_left_bullets(self):
        self.left_bullets.update()

        for left_bullet in self.left_bullets.copy():
            if left_bullet.rect.bottom <= 0:
                self.left_bullets.remove(left_bullet)

        # Check for bullets that have hit aliens. Ge rid of aliens & bullets.
        collisions = pygame.sprite.groupcollide(
            self.left_bullets, self.aliens, True, True)
        
        # Whenever there is a collision, we produce a sound.
        if collisions:
            pygame.mixer.Sound.play(self.make_boom)
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

    
    def _update_right_bullets(self):
        self.right_bullets.update()

        for right_bullet in self.right_bullets.copy():
            if right_bullet.rect.bottom <= 0:
                self.right_bullets.remove(right_bullet)

    # Check for bullets that have hit aliens. Ge rid of aliens & bullets.
        collisions = pygame.sprite.groupcollide(
            self.right_bullets, self.aliens, True, True)
        #pygame.sprite.collide_rect_ratio(0.75)

        # Whenever there is a collision, we produce a sound.
        if collisions:
            pygame.mixer.Sound.play(self.make_boom)
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()


    def _update_lasers(self):
        self.lasers.update()

        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

        # Check for bullets that have hit aliens. Ge rid of aliens & bullets.
        collisions = pygame.sprite.groupcollide(
            self.lasers, self.aliens, True, True, pygame.sprite.collide_rect_ratio(0.75))
        
        # Whenever there is a collision, we produce a sound.
        if collisions:
            pygame.mixer.Sound.play(self.make_boom)
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()


    def _update_aliens(self):
        """Update the position of all the aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens,
                pygame.sprite.collide_rect_ratio(0.7)):
            self._ship_hit()
            pygame.mixer.Sound.play(self.life_lost)

        self._check_aliens_bottom()
        

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _create_fleet(self):
        """Create the fleet of aliens"""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height 

        current_x = alien_width
        current_y = alien_height
        while current_y < (self.settings.screen_height - 4 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height


    def _check_bullet_alien_collision(self):
        # Check for bullets that have hit aliens. Ge rid of aliens & bullets.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True, pygame.sprite.collide_rect_ratio(0.5))
        
        # Whenever there is a collision, we produce a sound.
        if collisions:
            pygame.mixer.Sound.play(self.make_boom)
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()


    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active= False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                pygame.mixer.Sound.play(self.life_lost)
                break


    def _update_screen(self):
        #self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.bg_image,(0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for left_bullet in self.left_bullets.sprites():
            left_bullet.draw_left_bullet()
        for right_bullet in self.right_bullets.sprites():
            right_bullet.draw_right_bullet()
        for laser in self.lasers.sprites():
            laser.draw_laser()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()   