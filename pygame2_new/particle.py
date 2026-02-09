import pygame
import random
from config import *

class Particle:
    """Částicový efekt pro exploze, skoky atd."""
    def __init__(self, x, y, color, velocity_x=0, velocity_y=0, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x + random.uniform(-2, 2)
        self.velocity_y = velocity_y + random.uniform(-5, -2)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)
        self.gravity = 0.3
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity
        self.lifetime -= 1
        
    def draw(self, screen, camera_x):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            size = int(self.size * (self.lifetime / self.max_lifetime))
            if size > 0:
                color_with_alpha = (*self.color[:3], alpha)
                pygame.draw.circle(screen, self.color, 
                                 (int(self.x - camera_x), int(self.y)), size)
    
    def is_alive(self):
        return self.lifetime > 0


class StarParticle:
    """Hvězdičkový efekt pro speciální události"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 360)
        self.velocity_y = random.uniform(-3, -1)
        self.lifetime = 60
        self.size = random.randint(5, 10)
        self.rotation_speed = random.uniform(-5, 5)
        
    def update(self):
        self.y += self.velocity_y
        self.velocity_y += 0.1
        self.angle += self.rotation_speed
        self.lifetime -= 1
        
    def draw(self, screen, camera_x):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / 60))
            # Kreslení hvězdičky
            import math
            points = []
            for i in range(5):
                angle1 = math.radians(self.angle + i * 72)
                angle2 = math.radians(self.angle + i * 72 + 36)
                
                x1 = self.x - camera_x + math.cos(angle1) * self.size
                y1 = self.y + math.sin(angle1) * self.size
                
                x2 = self.x - camera_x + math.cos(angle2) * (self.size / 2)
                y2 = self.y + math.sin(angle2) * (self.size / 2)
                
                points.extend([(x1, y1), (x2, y2)])
            
            pygame.draw.polygon(screen, YELLOW, points)
    
    def is_alive(self):
        return self.lifetime > 0


class CoinCollectEffect:
    """Efekt při sebrání mince"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = 30
        self.velocity_y = -3
        
    def update(self):
        self.y += self.velocity_y
        self.lifetime -= 1
        
    def draw(self, screen, camera_x):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / 30))
            font = pygame.font.Font(None, 24)
            text = font.render("+10", True, YELLOW)
            text.set_alpha(alpha)
            screen.blit(text, (int(self.x - camera_x), int(self.y)))
    
    def is_alive(self):
        return self.lifetime > 0
