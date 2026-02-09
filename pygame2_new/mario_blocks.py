import pygame
from config import *

class Block:
    """Otázníkový blok nebo cihlový blok"""
    def __init__(self, x, y, block_type="question", content=None):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.block_type = block_type  # "question", "brick", "solid"
        self.content = content  # "coin", "powerup", None
        self.hit = False
        self.animation_offset = 0
        self.bump_offset = 0
        self.broken = False
        
    def hit_block(self, player):
        """Udeří do bloku - vrátí co má dát podle stavu Maria"""
        if self.broken or (self.hit and self.block_type == "question"):
            return None
            
        if self.block_type == "brick":
            # Cihla se rozbije pouze pokud je Mario velký
            if player.power_state >= 1:  # Super Mario nebo větší
                self.broken = True
                return "break"
            else:
                self.bump_offset = -10
                return None
        
        elif self.block_type == "question":
            self.hit = True
            self.bump_offset = -10
            
            # Podle obsahu bloku
            if self.content == "coin":
                return "coin"
            elif self.content == "powerup":
                # Podle stavu Maria vrátíme mushroom nebo flower
                if player.power_state == POWER_SMALL:
                    return "mushroom"
                else:
                    return "flower"
            
        return None
    
    def update(self):
        # Animace otázníku
        if not self.hit and self.block_type == "question":
            self.animation_offset = (self.animation_offset + 0.1) % (2 * 3.14159)
        
        # Bump animace
        if self.bump_offset < 0:
            self.bump_offset += 2
            
    def draw(self, screen, camera_x):
        if self.broken:
            return
            
        x = self.rect.x - camera_x
        y = self.rect.y + self.bump_offset
        
        if self.block_type == "question":
            if self.hit:
                # Použitý blok (tmavý)
                pygame.draw.rect(screen, (139, 90, 43), (x, y, 40, 40))
                pygame.draw.rect(screen, (100, 60, 30), (x, y, 40, 40), 3)
                
                # Prázdný vzor
                pygame.draw.rect(screen, (100, 60, 30), (x + 10, y + 10, 20, 20))
            else:
                # Aktivní otázníkový blok
                # Oranžová barva s gradientem
                pygame.draw.rect(screen, (255, 180, 0), (x, y, 40, 40))
                pygame.draw.rect(screen, (255, 140, 0), (x + 2, y + 2, 36, 36))
                pygame.draw.rect(screen, (255, 200, 50), (x + 5, y + 5, 30, 30))
                
                # Otazník
                import math
                bounce = int(math.sin(self.animation_offset) * 2)
                font = pygame.font.Font(None, 36)
                question_text = font.render("?", True, WHITE)
                text_rect = question_text.get_rect(center=(x + 20, y + 20 + bounce))
                screen.blit(question_text, text_rect)
                
                # Okraj
                pygame.draw.rect(screen, (200, 120, 0), (x, y, 40, 40), 3)
                
        elif self.block_type == "brick":
            # Cihlový blok
            brick_color = (178, 34, 34)
            pygame.draw.rect(screen, brick_color, (x, y, 40, 40))
            
            # Vzor cihel
            pygame.draw.rect(screen, (205, 92, 92), (x, y, 40, 2))
            pygame.draw.rect(screen, (205, 92, 92), (x, y, 2, 40))
            
            # Čáry mezi cihlami
            pygame.draw.line(screen, (139, 0, 0), (x + 20, y), (x + 20, y + 40), 2)
            pygame.draw.line(screen, (139, 0, 0), (x, y + 20), (x + 40, y + 20), 2)
            
            # Okraj
            pygame.draw.rect(screen, (128, 0, 0), (x, y, 40, 40), 2)
            
        elif self.block_type == "solid":
            # Pevný blok (nelze rozbít)
            pygame.draw.rect(screen, (120, 120, 120), (x, y, 40, 40))
            pygame.draw.rect(screen, (160, 160, 160), (x + 2, y + 2, 36, 36))
            pygame.draw.rect(screen, (80, 80, 80), (x, y, 40, 40), 2)


class Pipe:
    """Zelená roura jako v Mario"""
    def __init__(self, x, y, height=2):
        self.rect = pygame.Rect(x, y, 60, height * 40)
        self.height = height
        
    def draw(self, screen, camera_x):
        x = self.rect.x - camera_x
        y = self.rect.y
        
        # Zelená barva roury
        pipe_green = (0, 180, 0)
        pipe_dark = (0, 130, 0)
        
        # Hlavní tělo roury
        pygame.draw.rect(screen, pipe_green, (x, y + 20, 60, self.rect.height - 20))
        
        # Vrchol roury (širší)
        pygame.draw.rect(screen, pipe_green, (x - 5, y, 70, 20))
        pygame.draw.rect(screen, pipe_dark, (x - 5, y, 70, 8))
        
        # Vnitřek roury (černá díra)
        pygame.draw.ellipse(screen, BLACK, (x + 10, y + 8, 40, 16))
        pygame.draw.ellipse(screen, (20, 20, 20), (x + 12, y + 10, 36, 12))
        
        # Svislé čáry pro texturu
        for i in range(3):
            line_x = x + 15 + i * 15
            pygame.draw.line(screen, pipe_dark, (line_x, y + 20), 
                           (line_x, y + self.rect.height), 2)
        
        # Okraje
        pygame.draw.rect(screen, pipe_dark, (x - 5, y, 70, 20), 3)
        pygame.draw.rect(screen, pipe_dark, (x, y + 20, 60, self.rect.height - 20), 3)


class Mushroom:
    """Power-up houba pro zvětšení Maria"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocity_x = 2
        self.velocity_y = 0
        self.collected = False
        self.spawning = True
        self.spawn_offset = 40
        
    def update(self, platforms):
        if self.collected:
            return
            
        # Spawn animace
        if self.spawning:
            self.spawn_offset -= 1
            if self.spawn_offset <= 0:
                self.spawning = False
            return
        
        # Pohyb
        self.rect.x += self.velocity_x
        
        # Gravitace
        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y = 10
            
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
    
    def draw(self, screen, camera_x):
        if self.collected:
            return
            
        x = self.rect.x - camera_x
        y = self.rect.y - self.spawn_offset
        
        # Červená houba s bílými tečkami
        pygame.draw.ellipse(screen, (220, 20, 20), (x, y, 30, 30))
        
        # Bílé tečky
        pygame.draw.circle(screen, WHITE, (x + 8, y + 8), 4)
        pygame.draw.circle(screen, WHITE, (x + 22, y + 8), 4)
        pygame.draw.circle(screen, WHITE, (x + 15, y + 18), 3)
        
        # Stopka houby
        pygame.draw.rect(screen, (255, 230, 180), (x + 12, y + 20, 6, 10))
        
        # Oči
        pygame.draw.circle(screen, BLACK, (x + 10, y + 15), 2)
        pygame.draw.circle(screen, BLACK, (x + 20, y + 15), 2)


class FireFlower:
    """Ohnivá květina pro fire power"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.collected = False
        self.animation_offset = 0
        self.spawning = True
        self.spawn_offset = 40
        
    def update(self):
        if self.collected:
            return
            
        # Spawn animace
        if self.spawning:
            self.spawn_offset -= 1
            if self.spawn_offset <= 0:
                self.spawning = False
            return
            
        self.animation_offset = (self.animation_offset + 0.1) % (2 * 3.14159)
    
    def draw(self, screen, camera_x):
        if self.collected:
            return
            
        x = self.rect.x - camera_x
        y = self.rect.y - self.spawn_offset
        
        import math
        
        # Stonek
        pygame.draw.rect(screen, (0, 180, 0), (x + 12, y + 20, 6, 10))
        
        # Květina (4 okvětní lístky)
        colors = [(255, 100, 0), (255, 200, 0), (255, 50, 0), (255, 150, 0)]
        for i in range(4):
            angle = (i * 90 + math.degrees(self.animation_offset)) % 360
            rad = math.radians(angle)
            petal_x = x + 15 + math.cos(rad) * 8
            petal_y = y + 15 + math.sin(rad) * 8
            pygame.draw.circle(screen, colors[i], (int(petal_x), int(petal_y)), 6)
        
        # Střed květiny
        pygame.draw.circle(screen, YELLOW, (x + 15, y + 15), 5)
        pygame.draw.circle(screen, ORANGE, (x + 15, y + 15), 3)


class Fireball:
    """Ohnivá koule vystřelená Mariem"""
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 12, 12)
        self.velocity_x = 8 * direction
        self.velocity_y = -3
        self.lifetime = 180
        self.direction = direction
        
    def update(self, platforms):
        self.lifetime -= 1
        
        self.rect.x += self.velocity_x
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y
        
        # Odskok od země
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = -8
        
        # Odskok od platforem
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = -8
    
    def draw(self, screen, camera_x):
        if self.lifetime <= 0:
            return
            
        x = self.rect.x - camera_x
        y = self.rect.y
        
        # Ohnivá koule
        pygame.draw.circle(screen, (255, 100, 0), (x + 6, y + 6), 6)
        pygame.draw.circle(screen, (255, 200, 0), (x + 6, y + 6), 4)
        pygame.draw.circle(screen, (255, 255, 100), (x + 6, y + 6), 2)
        
    def is_alive(self):
        return self.lifetime > 0
