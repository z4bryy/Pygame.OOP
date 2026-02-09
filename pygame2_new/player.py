import pygame
from config import *

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, SMALL_MARIO_HEIGHT)
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.animation_frame = 0
        self.jump_particles = []
        self.is_jumping = False
        self.speed_multiplier = 1.0
        self.speed_boost_timer = 0
        
        # Power stavy
        self.power_state = POWER_SMALL  # 0=malý, 1=super, 2=fire
        self.invincible_timer = 0
        self.transform_timer = 0
        
        # Fire Mario
        self.fireballs = []
        self.can_shoot = True
        self.shoot_cooldown = 0
        
    def update(self, keys, platforms):
        # Speed boost
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            self.speed_multiplier = 1.5
        else:
            self.speed_multiplier = 1.0
        
        # Invincibility timer
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        # Transform animation
        if self.transform_timer > 0:
            self.transform_timer -= 1
            
        # Shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            self.can_shoot = True
            
        # Horizontální pohyb
        self.velocity_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -PLAYER_SPEED * self.speed_multiplier
            self.facing_right = False
            if self.on_ground:
                self.animation_frame += 0.3
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = PLAYER_SPEED * self.speed_multiplier
            self.facing_right = True
            if self.on_ground:
                self.animation_frame += 0.3
        
        # Update fireballs
        for fireball in self.fireballs[:]:
            fireball.update(platforms)
            if not fireball.is_alive():
                self.fireballs.remove(fireball)
            
        # Aplikace gravitace
        self.velocity_y += GRAVITY
        
        # Maximální rychlost pádu
        if self.velocity_y > 20:
            self.velocity_y = 20
            
        # Aktualizace pozice
        self.rect.x += self.velocity_x
        self.check_collision_x(platforms)
        
        self.rect.y += self.velocity_y
        self.on_ground = False
        self.check_collision_y(platforms)
        
    def check_collision_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:  # Pohyb doprava
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:  # Pohyb doleva
                    self.rect.left = platform.rect.right
                    
    def check_collision_y(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Padání dolů
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Skok nahoru
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    
        # Kolize se zemí
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = 0
            self.on_ground = True
            
    def jump(self):
        self.velocity_y = -PLAYER_JUMP_POWER
        self.is_jumping = True
        # Částice při skoku
        from particle import Particle
        for _ in range(8):
            self.jump_particles.append(
                Particle(self.rect.centerx, self.rect.bottom, 
                        (200, 200, 200), 0, 2, 20)
            )
    
    def activate_speed_boost(self):
        self.speed_boost_timer = 300  # 5 sekund při 60 FPS
    
    def power_up(self):
        """Zvětšení Maria (houba)"""
        if self.power_state == POWER_SMALL:
            self.power_state = POWER_SUPER
            old_bottom = self.rect.bottom
            self.rect.height = SUPER_MARIO_HEIGHT
            self.rect.bottom = old_bottom
            self.transform_timer = 20
            return True
        return False
    
    def fire_power_up(self):
        """Fire power (květina)"""
        if self.power_state < POWER_FIRE:
            self.power_state = POWER_FIRE
            if self.power_state == POWER_SMALL:
                old_bottom = self.rect.bottom
                self.rect.height = SUPER_MARIO_HEIGHT
                self.rect.bottom = old_bottom
            self.transform_timer = 20
            return True
        return False
    
    def take_damage(self):
        """Zranění Maria - jako v originálním Mario Bros"""
        if self.invincible_timer > 0:
            return False
            
        if self.power_state > POWER_SMALL:
            # V originálním Mario: Super i Fire Mario se změní na Small při zranění
            self.power_state = POWER_SMALL
            old_bottom = self.rect.bottom
            self.rect.height = SMALL_MARIO_HEIGHT
            self.rect.bottom = old_bottom
            self.invincible_timer = 120  # 2 sekundy neporazitelnosti
            self.transform_timer = 20
            return False
        else:
            # Smrt - Small Mario umře
            return True
    
    def shoot_fireball(self):
        """Vystřelení ohnivé koule"""
        if self.power_state == POWER_FIRE and self.can_shoot and len(self.fireballs) < 2:
            from mario_blocks import Fireball
            direction = 1 if self.facing_right else -1
            fireball = Fireball(self.rect.centerx, self.rect.centery, direction)
            self.fireballs.append(fireball)
            self.can_shoot = False
            self.shoot_cooldown = 15
        
    def draw(self, screen, camera_x):
        x = self.rect.x - camera_x
        y = self.rect.y
        
        # Blikání při neporazitelnosti
        if self.invincible_timer > 0 and (self.invincible_timer // 5) % 2 == 0:
            return
        
        # Vykreslení ohnivých koulí
        for fireball in self.fireballs:
            fireball.draw(screen, camera_x)
        
        # Vykreslení částic skoku
        for particle in self.jump_particles[:]:
            particle.update()
            particle.draw(screen, camera_x)
            if not particle.is_alive():
                self.jump_particles.remove(particle)
        
        # Speed boost efekt (modrá aura)
        if self.speed_boost_timer > 0:
            glow_size = 60
            glow_surface = pygame.Surface((glow_size, glow_size))
            glow_surface.set_alpha(100)
            pygame.draw.circle(glow_surface, (0, 150, 255), 
                             (glow_size//2, glow_size//2), glow_size//2)
            screen.blit(glow_surface, (x + 20 - glow_size//2, y + self.rect.height//2 - glow_size//2))
        
        # Barva podle power stavu
        if self.power_state == POWER_FIRE:
            body_color = WHITE  # Bílá kombinéza pro Fire Mario
            shirt_color = RED
        elif self.power_state == POWER_SUPER:
            body_color = (0, 100, 255)  # Modrá kombinéza
            shirt_color = RED
        else:
            body_color = (0, 100, 255)
            shirt_color = RED
        
        # Transform animace
        if self.transform_timer > 0 and (self.transform_timer // 3) % 2 == 0:
            body_color = (body_color[0] + 50, body_color[1] + 50, body_color[2] + 50)
        
        # Animace běhu (pohyb nohou)
        leg_offset = 0
        if self.velocity_x != 0 and self.on_ground:
            leg_offset = int(abs(self.animation_frame) % 4 - 2)
        
        # Výpočet proporcí podle velikosti
        scale = self.rect.height / SUPER_MARIO_HEIGHT
        
        # === TĚLO MARIA ===
        body_height = int(18 * scale)
        body_y = y + self.rect.height - body_height - int(12 * scale)
        
        # Hlavní tělo (kombinéza)
        pygame.draw.rect(screen, body_color, (x + 8, body_y, 24, body_height))
        
        # Ramínka kombinézy
        pygame.draw.rect(screen, body_color, (x + 8, body_y - 2, 6, 8))
        pygame.draw.rect(screen, body_color, (x + 26, body_y - 2, 6, 8))
        
        # Triko pod kombinézou
        pygame.draw.rect(screen, shirt_color, (x + 10, body_y + 2, 20, int(14 * scale)))
        
        # Žluté knoflíky na kombinéze
        pygame.draw.circle(screen, YELLOW, (x + 14, body_y + 4), 2)
        pygame.draw.circle(screen, YELLOW, (x + 26, body_y + 4), 2)
        
        # === NOHY (HNĚDÉ BOTY) s animací ===
        boot_color = (139, 69, 19)
        legs_y = y + self.rect.height - 12
        
        # Levá noha
        pygame.draw.rect(screen, body_color, (x + 10, legs_y, 8, 8))
        pygame.draw.ellipse(screen, boot_color, (x + 8 + leg_offset, legs_y + 6, 12, 6))
        # Pravá noha
        pygame.draw.rect(screen, body_color, (x + 22, legs_y, 8, 8))
        pygame.draw.ellipse(screen, boot_color, (x + 20 - leg_offset, legs_y + 6, 12, 6))
        
        # === HLAVA (BÉŽOVÁ POKOŽKA) ===
        skin_color = (255, 220, 177)
        head_y = body_y - int(20 * scale)
        # Tvář (kruh)
        pygame.draw.circle(screen, skin_color, (x + 20, head_y + 10), int(10 * scale))
        
        # === ČERVENÁ ČEPICE ===
        cap_color = (220, 20, 20)
        # Hlavní část čepice (půlkruh)
        pygame.draw.ellipse(screen, cap_color, (x + 10, head_y, 20, int(14 * scale)))
        # Kšilt čepice
        pygame.draw.ellipse(screen, cap_color, (x + 12, head_y + int(10 * scale), 16, 6))
        
        # Logo "M" na čepici
        pygame.draw.circle(screen, WHITE, (x + 20, head_y + int(6 * scale)), 4)
        font = pygame.font.Font(None, 16)
        m_text = font.render("M", True, RED)
        screen.blit(m_text, (x + 17, head_y + int(2 * scale)))
        
        # === OČI ===
        eye_y = head_y + int(11 * scale)
        if self.facing_right:
            # Pravý pohled
            pygame.draw.ellipse(screen, WHITE, (x + 14, eye_y, 5, 6))
            pygame.draw.circle(screen, BLACK, (x + 16, eye_y + 3), 2)
            pygame.draw.ellipse(screen, WHITE, (x + 21, eye_y, 5, 6))
            pygame.draw.circle(screen, BLACK, (x + 24, eye_y + 3), 2)
        else:
            # Levý pohled
            pygame.draw.ellipse(screen, WHITE, (x + 14, eye_y, 5, 6))
            pygame.draw.circle(screen, BLACK, (x + 15, eye_y + 3), 2)
            pygame.draw.ellipse(screen, WHITE, (x + 21, eye_y, 5, 6))
            pygame.draw.circle(screen, BLACK, (x + 22, eye_y + 3), 2)
        
        # === KNÍR ===
        mustache_color = (101, 67, 33)
        mustache_y = head_y + int(14 * scale)
        if self.facing_right:
            pygame.draw.ellipse(screen, mustache_color, (x + 16, mustache_y, 10, 4))
            pygame.draw.ellipse(screen, mustache_color, (x + 12, mustache_y + 1, 8, 3))
        else:
            pygame.draw.ellipse(screen, mustache_color, (x + 14, mustache_y, 10, 4))
            pygame.draw.ellipse(screen, mustache_color, (x + 20, mustache_y + 1, 8, 3))
        
        # === NOS ===
        pygame.draw.circle(screen, (255, 180, 140), (x + 20, head_y + int(13 * scale)), 3)
        
        # === RUCE s animací ===
        glove_color = WHITE
        arm_swing = 0
        arms_y = body_y + int(8 * scale)
        if self.velocity_x != 0 and self.on_ground:
            arm_swing = int(self.animation_frame % 4 - 2) * 2
            
        if self.facing_right:
            pygame.draw.circle(screen, glove_color, (x + 34, arms_y + arm_swing), 4)
            pygame.draw.circle(screen, glove_color, (x + 6, arms_y - arm_swing), 4)
        else:
            pygame.draw.circle(screen, glove_color, (x + 6, arms_y + arm_swing), 4)
            pygame.draw.circle(screen, glove_color, (x + 34, arms_y - arm_swing), 4)
        
        # Stín
        shadow_surface = pygame.Surface((self.rect.width, 4))
        shadow_surface.set_alpha(50)
        shadow_surface.fill(BLACK)
        screen.blit(shadow_surface, (x, y + self.rect.height))
