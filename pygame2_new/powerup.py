import pygame
import math
from config import *

class PowerUp:
    """Power-up prvky jako extra život, speed boost, etc."""
    def __init__(self, x, y, powerup_type="extra_life"):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.powerup_type = powerup_type
        self.collected = False
        self.animation_offset = 0
        
    def update(self):
        self.animation_offset = (self.animation_offset + 0.1) % (2 * math.pi)
        
    def collect(self):
        self.collected = True
        
    def draw(self, screen, camera_x):
        if self.collected:
            return
            
        # Animace (poskakování)
        bounce = int(math.sin(self.animation_offset) * 5)
        x = self.rect.x - camera_x
        y = self.rect.y + bounce
        
        if self.powerup_type == "extra_life":
            # Zelené srdce (extra život)
            heart_color = (0, 255, 0)
            pygame.draw.circle(screen, heart_color, (x + 8, y + 10), 8)
            pygame.draw.circle(screen, heart_color, (x + 22, y + 10), 8)
            points = [(x, y + 10), (x + 30, y + 10), (x + 15, y + 28)]
            pygame.draw.polygon(screen, heart_color, points)
            pygame.draw.circle(screen, (100, 255, 100), (x + 11, y + 8), 3)
            
            # Obrys
            pygame.draw.circle(screen, (0, 200, 0), (x + 8, y + 10), 8, 2)
            pygame.draw.circle(screen, (0, 200, 0), (x + 22, y + 10), 8, 2)
            
        elif self.powerup_type == "speed_boost":
            # Modrá šipka (speed boost)
            points = [
                (x + 5, y + 15),
                (x + 20, y + 5),
                (x + 20, y + 12),
                (x + 25, y + 12),
                (x + 25, y + 18),
                (x + 20, y + 18),
                (x + 20, y + 25)
            ]
            pygame.draw.polygon(screen, (0, 150, 255), points)
            pygame.draw.polygon(screen, (0, 100, 200), points, 2)
            
        # Světélkování
        glow_size = int(40 + math.sin(self.animation_offset * 2) * 5)
        glow_surface = pygame.Surface((glow_size, glow_size))
        glow_surface.set_alpha(50)
        pygame.draw.circle(glow_surface, YELLOW, (glow_size//2, glow_size//2), glow_size//2)
        screen.blit(glow_surface, (x + 15 - glow_size//2, y + 15 - glow_size//2))
