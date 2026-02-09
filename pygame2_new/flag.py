import pygame
import math
from config import *

class Flag:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, FLAG_WIDTH, FLAG_HEIGHT)
        
    def draw(self, screen, camera_x):
        x = self.rect.x - camera_x
        y = self.rect.y
        
        # === CÍLOVÁ VLAJKA ===
        # Tyč vlajky (tmavě šedá s 3D efektem)
        pole_color = (80, 80, 80)
        pole_highlight = (120, 120, 120)
        pole_shadow = (40, 40, 40)
        
        # Hlavní tyč
        pygame.draw.rect(screen, pole_color, (x, y, 6, self.rect.height))
        
        # Světlý okraj (3D efekt)
        pygame.draw.line(screen, pole_highlight, (x, y), (x, y + self.rect.height), 2)
        
        # Tmavý okraj (3D efekt)
        pygame.draw.line(screen, pole_shadow, (x + 5, y), (x + 5, y + self.rect.height), 1)
        
        # Zlatý vrchol tyče (koule)
        pygame.draw.circle(screen, (255, 215, 0), (x + 3, y - 3), 8)
        pygame.draw.circle(screen, (255, 235, 100), (x + 3, y - 3), 6)
        pygame.draw.circle(screen, (218, 165, 32), (x + 3, y - 3), 8, 2)
        # Lesk na kouli
        pygame.draw.circle(screen, WHITE, (x + 1, y - 5), 3)
        
        # === VLAJKA (ZELENÁ S BÍLOU HVĚZDOU) ===
        # Vlajka body
        flag_points = [
            (x + 6, y + 10),
            (x + 55, y + 25),
            (x + 6, y + 40)
        ]
        
        # Stín vlajky
        shadow_points = [(px + 2, py + 2) for px, py in flag_points]
        shadow_surface = pygame.Surface((60, 50))
        shadow_surface.set_alpha(80)
        pygame.draw.polygon(shadow_surface, BLACK, [(px - x, py - y) for px, py in shadow_points])
        screen.blit(shadow_surface, (x, y))
        
        # Hlavní zelená vlajka
        flag_green = (0, 180, 0)
        pygame.draw.polygon(screen, flag_green, flag_points)
        
        # Světlejší okraj pro 3D efekt
        pygame.draw.polygon(screen, (0, 220, 0), [
            (x + 6, y + 10),
            (x + 50, y + 23),
            (x + 6, y + 35)
        ])
        
        # Černý obrys
        pygame.draw.polygon(screen, BLACK, flag_points, 2)
        
        # === BÍLÁ HVĚZDA NA VLAJCE ===
        star_center_x = x + 25
        star_center_y = y + 25
        star_size = 8
        
        # Hvězda (5 cípů)
        star_points = []
        for i in range(10):
            angle = math.pi / 2 + (2 * math.pi * i / 10)
            radius = star_size if i % 2 == 0 else star_size / 2
            px = star_center_x + radius * math.cos(angle)
            py = star_center_y - radius * math.sin(angle)
            star_points.append((px, py))
        
        # Žlutá hvězda
        pygame.draw.polygon(screen, YELLOW, star_points)
        pygame.draw.polygon(screen, (255, 215, 0), star_points)
        pygame.draw.polygon(screen, BLACK, star_points, 1)
        
        # Detaily na vlajce (ozdobné čáry)
        pygame.draw.line(screen, (0, 150, 0), (x + 6, y + 15), (x + 45, y + 25), 1)
        pygame.draw.line(screen, (0, 150, 0), (x + 6, y + 35), (x + 45, y + 25), 1)
