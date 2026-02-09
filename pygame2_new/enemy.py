import pygame
from config import *

class Enemy:
    def __init__(self, x, y, move_range=100):
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.velocity_x = ENEMY_SPEED
        self.velocity_y = 0
        self.start_x = x
        self.move_range = move_range
        self.alive = True
        
    def update(self, platforms):
        if not self.alive:
            return
            
        # Pohyb tam a zpět
        self.rect.x += self.velocity_x
        
        # Kontrola hranic pohybu
        if self.rect.x > self.start_x + self.move_range:
            self.velocity_x = -ENEMY_SPEED
        elif self.rect.x < self.start_x - self.move_range:
            self.velocity_x = ENEMY_SPEED
            
        # Gravitace
        self.velocity_y += GRAVITY
        if self.velocity_y > 20:
            self.velocity_y = 20
            
        self.rect.y += self.velocity_y
        
        # Kolize s platformami
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    
        # Kolize se zemí
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = 0
            
    def kill(self):
        self.alive = False
        
    def draw(self, screen, camera_x):
        if not self.alive:
            return
            
        x = self.rect.x - camera_x
        y = self.rect.y
        
        # === GOOMBA (HOUBA NEPŘÍTEL) ===
        # Hlavní tělo - hnědá houba
        mushroom_color = (139, 90, 43)
        top_color = (160, 82, 45)
        
        # Kmen houby (nohy)
        stem_color = (222, 184, 135)
        pygame.draw.rect(screen, stem_color, (x + 12, y + 28, 16, 12))
        pygame.draw.ellipse(screen, stem_color, (x + 10, y + 36, 20, 8))
        
        # Horní část houby (kopule)
        pygame.draw.ellipse(screen, top_color, (x, y, self.rect.width, 30))
        
        # Bílé tečky na houbě (více detailní)
        spots = [
            (x + 8, y + 8, 6),
            (x + 26, y + 8, 6),
            (x + 14, y + 18, 5),
            (x + 24, y + 16, 4),
            (x + 18, y + 6, 4),
        ]
        for spot_x, spot_y, radius in spots:
            pygame.draw.circle(screen, WHITE, (spot_x, spot_y), radius)
            pygame.draw.circle(screen, (240, 240, 240), (spot_x, spot_y), radius - 1)
        
        # === TVÁŘ ===
        # Oči (zlé/mrzuté)
        eye_color = WHITE
        pupil_color = BLACK
        
        # Levé oko
        pygame.draw.ellipse(screen, eye_color, (x + 10, y + 20, 7, 8))
        pygame.draw.ellipse(screen, pupil_color, (x + 11, y + 23, 5, 5))
        # Světlo v oku
        pygame.draw.circle(screen, WHITE, (x + 13, y + 24), 1)
        
        # Pravé oko
        pygame.draw.ellipse(screen, eye_color, (x + 23, y + 20, 7, 8))
        pygame.draw.ellipse(screen, pupil_color, (x + 24, y + 23, 5, 5))
        # Světlo v oku
        pygame.draw.circle(screen, WHITE, (x + 26, y + 24), 1)
        
        # Obočí (mrzutý výraz)
        pygame.draw.line(screen, BLACK, (x + 10, y + 19), (x + 16, y + 21), 2)
        pygame.draw.line(screen, BLACK, (x + 24, y + 21), (x + 30, y + 19), 2)
        
        # Ústa (mrzutý výraz)
        pygame.draw.arc(screen, BLACK, (x + 12, y + 28, 16, 8), 3.14, 6.28, 2)
        
        # Zuby (ostré)
        pygame.draw.line(screen, WHITE, (x + 16, y + 30), (x + 16, y + 33), 2)
        pygame.draw.line(screen, WHITE, (x + 20, y + 30), (x + 20, y + 33), 2)
        pygame.draw.line(screen, WHITE, (x + 24, y + 30), (x + 24, y + 33), 2)
        
        # Obrys pro větší kontrast
        pygame.draw.ellipse(screen, BLACK, (x, y, self.rect.width, 30), 2)
        
        # Stín
        shadow_surface = pygame.Surface((self.rect.width, 3))
        shadow_surface.set_alpha(60)
        shadow_surface.fill(BLACK)
        screen.blit(shadow_surface, (x, y + self.rect.height))
