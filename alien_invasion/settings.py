class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        
        # Screen settings
        self.screen_width = 1500
        self.screen_height = 750
        self.bg_color = (0, 0, 0)

        # Ship's settings
        self.ship_limit = 3

        # Bullet\Laser settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (230, 0, 0)
        self.bullets_allowed = 10
        self.left_bullets_allowed = 10
        self.right_bullets_allowed = 10
        self.laser_canon_speed = 15.0
        self.lasers_allowed = 10
        self.left_bullet_speed = 10.0
        self.right_bullet_speed = 10.0

        # Alien settings
        self.fleet_drop_speed = 22.5
        self.speedup_scale = 1.2

        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        self.bullet_speed = 5.0
        self.ship_speed = 5.0
        self.alien_speed = 1.5
        self.alien_points = 50

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1


    def increase_speed(self):
        """Increase speed settings."""
        self.alien_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        