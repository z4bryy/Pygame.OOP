import pygame
from config import *
import math

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, COIN_SIZE, COIN_SIZE)
        self.collected = False
        self.animation_offset = 0
        
    def collect(self):
        self.collected = True
        
    def draw(self, screen, camera_x):
        if self.collected:
            return
            
        # Animace mince (lehké poskakovanie + rotace)
        self.animation_offset = (self.animation_offset + 0.15) % (2 * math.pi)
        bounce = int(math.sin(self.animation_offset) * 4)
        rotation = math.sin(self.animation_offset * 2) * 0.3
        
        # Zlatá mince s 3D efektem
        center_x = self.rect.x - camera_x + COIN_SIZE // 2
        center_y = self.rect.y + COIN_SIZE // 2 + bounce
        
        # Stín mince
        shadow_surface = pygame.Surface((COIN_SIZE + 4, 4))
        shadow_surface.set_alpha(80)
        shadow_surface.fill(BLACK)
        screen.blit(shadow_surface, (center_x - COIN_SIZE//2 - 2, center_y + COIN_SIZE//2 + 2))
        
        # Vnější zlatý kruh
        pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), COIN_SIZE // 2)
        
        # Tmavší okraj pro 3D efekt
        pygame.draw.circle(screen, (218, 165, 32), (center_x, center_y), COIN_SIZE // 2, 2)
        
        # Vnitřní světlejší kruh (lesk)
        pygame.draw.circle(screen, (255, 235, 100), (center_x, center_y), COIN_SIZE // 2 - 3)
        
        # Ještě menší kruh
        pygame.draw.circle(screen, ORANGE, (center_x, center_y), COIN_SIZE // 2 - 5)
        
        # Střed mince
        pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), COIN_SIZE // 2 - 7)
        
        # Symbol "$" nebo hvězda na minci
        font = pygame.font.Font(None, 20)
        symbol = font.render("$", True, ORANGE)
        symbol_rect = symbol.get_rect(center=(center_x, center_y))
        screen.blit(symbol, symbol_rect)
        
        # Lesk/odlesk (bílé světlo v rohu)
        pygame.draw.circle(screen, WHITE, (center_x - 4, center_y - 4), 3)
        pygame.draw.circle(screen, (255, 255, 200), (center_x - 4, center_y - 4), 2)
        
        # Detailní okraj
        pygame.draw.circle(screen, (184, 134, 11), (center_x, center_y), COIN_SIZE // 2, 1)
