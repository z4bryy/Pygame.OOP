import pygame
from config import *

class Platform:
    def __init__(self, x, y, width, height, color=PLATFORM_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        
    def draw(self, screen, camera_x):
        x = self.rect.x - camera_x
        y = self.rect.y
        
        # === CIHLOVÁ PLATFORMA ===
        # Základní barva
        brick_color = (178, 34, 34)
        mortar_color = (139, 69, 19)
        highlight_color = (205, 92, 92)
        shadow_color = (128, 0, 0)
        
        # Vykreslení hlavního obdélníku
        pygame.draw.rect(screen, self.color, (x, y, self.rect.width, self.rect.height))
        
        # Horní světlý okraj (3D efekt)
        pygame.draw.line(screen, highlight_color, (x, y), (x + self.rect.width, y), 2)
        pygame.draw.line(screen, highlight_color, (x, y), (x, y + self.rect.height), 2)
        
        # Spodní tmavý okraj (3D efekt)
        pygame.draw.line(screen, shadow_color, (x, y + self.rect.height - 1), 
                        (x + self.rect.width, y + self.rect.height - 1), 2)
        pygame.draw.line(screen, shadow_color, (x + self.rect.width - 1, y), 
                        (x + self.rect.width - 1, y + self.rect.height), 2)
        
        # Vzor cihel
        brick_width = 30
        brick_height = 10
        
        for row in range(0, self.rect.height, brick_height):
            # Střídání řad pro cihlový vzor
            offset = (brick_width // 2) if (row // brick_height) % 2 == 0 else 0
            
            for col in range(-brick_width, self.rect.width + brick_width, brick_width):
                brick_x = x + col + offset
                brick_y = y + row
                
                # Zkontrolovat, zda je cihla v hranicích platformy
                if brick_x >= x - brick_width and brick_x < x + self.rect.width:
                    # Svislé čáry mezi cihlami (malta)
                    pygame.draw.line(screen, mortar_color, 
                                   (brick_x, brick_y), 
                                   (brick_x, brick_y + brick_height), 1)
                    
            # Vodorovné čáry mezi cihlami
            if row > 0:
                pygame.draw.line(screen, mortar_color, 
                               (x, brick_y), 
                               (x + self.rect.width, brick_y), 1)
        
        # Vnější černý okraj
        pygame.draw.rect(screen, BLACK, (x, y, self.rect.width, self.rect.height), 1)
