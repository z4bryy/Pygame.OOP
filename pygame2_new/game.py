import pygame
from config import *
from player import Player
from enemy import Enemy
from platform import Platform
from coin import Coin
from flag import Flag
from level import Level
from particle import Particle, StarParticle, CoinCollectEffect
from mario_blocks import Mushroom, FireFlower

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Herní stav
        self.lives = MAX_LIVES
        self.score = 0
        self.current_level = 1
        self.max_level = 3
        
        # Timer
        self.time_remaining = LEVEL_TIME
        self.time_counter = 0
        
        # Font pro text
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Inicializace prvního levelu
        self.level = Level(self.current_level)
        self.player = Player(100, SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT)
        
        # Kamera offset
        self.camera_x = 0
        
        # Herní stavy
        self.game_state = "playing"  # playing, level_complete, game_over, win
        self.state_timer = 0
        
        # Částicové efekty
        self.particles = []
        self.effects = []
        
        # Combo systém
        self.combo = 0
        self.combo_timer = 0
        
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            
            if self.game_state == "playing":
                self.update()
            elif self.game_state == "level_complete":
                self.handle_level_complete()
            elif self.game_state == "game_over":
                self.handle_game_over()
            elif self.game_state == "win":
                self.handle_win()
                
            self.draw()
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.on_ground:
                    self.player.jump()
                elif event.key == pygame.K_x or event.key == pygame.K_LSHIFT:
                    # Střelba ohnivých koulí
                    self.player.shoot_fireball()
                elif event.key == pygame.K_r and (self.game_state == "game_over" or self.game_state == "win"):
                    self.reset_game()
                elif event.key == pygame.K_RETURN and self.game_state == "level_complete":
                    self.next_level()
                    
    def update(self):
        # Timer
        if self.game_state == "playing":
            self.time_counter += 1
            if self.time_counter >= 60:  # 1 sekunda při 60 FPS
                self.time_counter = 0
                self.time_remaining -= 1
                if self.time_remaining <= 0:
                    self.player_hit()
        
        # Získání stisknutých kláves
        keys = pygame.key.get_pressed()
        
        # Pohyb hráče
        self.player.update(keys, self.level.platforms)
        
        # Update bloků
        for block in self.level.blocks:
            block.update()
            
            # Kontrola kolize Maria s blokem (zdola)
            if self.player.rect.colliderect(block.rect):
                if self.player.velocity_y < 0:  # Mario skáče nahoru
                    overlap = self.player.rect.top - block.rect.bottom
                    if overlap > -10:  # Udření zdola
                        self.player.rect.top = block.rect.bottom
                        self.player.velocity_y = 0
                        
                        # Hit blok
                        content = block.hit_block(self.player)
                        if content == "coin":
                            self.score += 100
                        elif content == "mushroom":
                            mushroom = Mushroom(block.rect.x, block.rect.y)
                            self.level.mushrooms.append(mushroom)
                            self.score += 1000
                        elif content == "flower":
                            flower = FireFlower(block.rect.x, block.rect.y)
                            self.level.flowers.append(flower)
                            self.score += 1000
                        elif content == "break":
                            self.score += 50
                            # Částice rozbitých cihel
                            for _ in range(8):
                                self.particles.append(
                                    Particle(block.rect.centerx, block.rect.centery,
                                           (178, 34, 34), 0, -5, 30)
                                )
        
        # Update hub
        for mushroom in self.level.mushrooms[:]:
            mushroom.update(self.level.platforms)
            if self.player.rect.colliderect(mushroom.rect) and not mushroom.collected:
                mushroom.collected = True
                self.level.mushrooms.remove(mushroom)
                if self.player.power_up():
                    # Hvězdičkový efekt
                    for _ in range(15):
                        self.particles.append(StarParticle(mushroom.rect.centerx, mushroom.rect.centery))
        
        # Update květin
        for flower in self.level.flowers[:]:
            flower.update()
            if self.player.rect.colliderect(flower.rect) and not flower.collected:
                flower.collected = True
                self.level.flowers.remove(flower)
                if self.player.fire_power_up():
                    # Ohnivý efekt
                    for _ in range(20):
                        self.particles.append(
                            Particle(flower.rect.centerx, flower.rect.centery,
                                   (255, 100, 0), 0, -3, 40)
                        )
        
        # Update power-upů (staré)
        for powerup in self.level.powerups[:]:
            powerup.update()
            if self.player.rect.colliderect(powerup.rect) and not powerup.collected:
                powerup.collect()
                self.level.powerups.remove(powerup)
                
                if powerup.powerup_type == "extra_life":
                    if self.lives < MAX_LIVES:
                        self.lives += 1
                    self.score += 100
                    for _ in range(15):
                        self.particles.append(StarParticle(powerup.rect.centerx, powerup.rect.centery))
                        
                elif powerup.powerup_type == "speed_boost":
                    self.player.activate_speed_boost()
                    self.score += 50
                    for _ in range(20):
                        self.particles.append(
                            Particle(powerup.rect.centerx, powerup.rect.centery,
                                   (0, 150, 255), 0, 0, 40)
                        )
        
        # Aktualizace nepřátel
        for enemy in self.level.enemies:
            enemy.update(self.level.platforms)
            
            # Kolize s ohnivou koulí
            for fireball in self.player.fireballs[:]:
                if fireball.rect.colliderect(enemy.rect) and enemy.alive:
                    enemy.kill()
                    self.level.enemies.remove(enemy)
                    self.player.fireballs.remove(fireball)
                    self.score += 100
                    # Exploze
                    for _ in range(10):
                        self.particles.append(
                            Particle(enemy.rect.centerx, enemy.rect.centery,
                                   (255, 100, 0), 0, -3, 25)
                        )
                    break
            
            # Kolize s nepřítelem
            if self.player.rect.colliderect(enemy.rect) and enemy.alive:
                if self.player.velocity_y > 0 and self.player.rect.bottom - 10 < enemy.rect.centery:
                    # Skok na nepřítele
                    enemy.kill()
                    self.level.enemies.remove(enemy)
                    self.player.velocity_y = -10
                    
                    # Combo systém
                    self.combo += 1
                    self.combo_timer = 120
                    bonus = 100 * self.combo
                    self.score += bonus
                    
                    # Částicový efekt
                    for _ in range(15):
                        self.particles.append(
                            Particle(enemy.rect.centerx, enemy.rect.centery,
                                   (139, 90, 43), 0, -2, 30)
                        )
                    
                    if self.combo > 1:
                        self.effects.append(self.create_combo_text(enemy.rect.centerx, enemy.rect.centery))
                else:
                    # Hráč byl zasažen
                    if self.player.take_damage():
                        self.player_hit()
        
        # Combo timer
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo = 0
                    
        # Kolize s mincemi
        for coin in self.level.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                coin.collect()
                self.level.coins.remove(coin)
                self.score += 100
                
                self.effects.append(CoinCollectEffect(coin.rect.centerx, coin.rect.centery))
                
                for _ in range(8):
                    self.particles.append(
                        Particle(coin.rect.centerx, coin.rect.centery,
                               YELLOW, 0, -2, 25)
                    )
        
        # Update částic a efektů
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
                
        for effect in self.effects[:]:
            effect.update()
            if not effect.is_alive():
                self.effects.remove(effect)
                
        # Kontrola dosažení vlajky
        if self.player.rect.colliderect(self.level.flag.rect):
            self.game_state = "level_complete"
            self.state_timer = pygame.time.get_ticks()
            bonus_score = self.time_remaining * 10
            self.score += bonus_score
            
            for _ in range(50):
                self.particles.append(StarParticle(self.level.flag.rect.centerx, 
                                                   self.level.flag.rect.centery))
            
        # Kontrola pádu do propasti
        if self.player.rect.top > SCREEN_HEIGHT:
            self.player_hit()
            
        # Aktualizace kamery
        self.update_camera()
    
    def create_combo_text(self, x, y):
        """Vytvoří textový efekt pro combo"""
        class ComboText:
            def __init__(self, x, y, combo):
                self.x = x
                self.y = y
                self.combo = combo
                self.lifetime = 60
                self.velocity_y = -2
                
            def update(self):
                self.y += self.velocity_y
                self.lifetime -= 1
                
            def draw(self, screen, camera_x):
                if self.lifetime > 0:
                    alpha = int(255 * (self.lifetime / 60))
                    font = pygame.font.Font(None, 36)
                    text = font.render(f"COMBO x{self.combo}!", True, ORANGE)
                    text.set_alpha(alpha)
                    screen.blit(text, (int(self.x - camera_x - 50), int(self.y)))
            
            def is_alive(self):
                return self.lifetime > 0
        
        return ComboText(x, y, self.combo)
        
    def update_camera(self):
        # Kamera sleduje hráče
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 3
        self.camera_x = max(0, target_x)
        
    def player_hit(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_state = "game_over"
            self.state_timer = pygame.time.get_ticks()
        else:
            # Restart pozice hráče
            self.player.rect.x = 100
            self.player.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
            self.player.velocity_y = 0
            self.camera_x = 0
            
    def next_level(self):
        self.current_level += 1
        if self.current_level > self.max_level:
            self.game_state = "win"
            self.state_timer = pygame.time.get_ticks()
        else:
            self.level = Level(self.current_level)
            self.player.rect.x = 100
            self.player.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
            self.player.velocity_y = 0
            self.camera_x = 0
            self.game_state = "playing"
            
    def reset_game(self):
        self.lives = MAX_LIVES
        self.score = 0
        self.current_level = 1
        self.level = Level(self.current_level)
        self.player.rect.x = 100
        self.player.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
        self.player.velocity_y = 0
        self.camera_x = 0
        self.game_state = "playing"
        
    def handle_level_complete(self):
        pass  # Čeká na stisknutí Enter
        
    def handle_game_over(self):
        pass  # Čeká na stisknutí R
        
    def handle_win(self):
        pass  # Čeká na stisknutí R
        
    def draw(self):
        # === POZADÍ S GRADIENTEM ===
        # Horní část nebe (světlejší)
        for i in range(SCREEN_HEIGHT):
            ratio = i / SCREEN_HEIGHT
            r = int(135 + (200 - 135) * ratio)
            g = int(206 + (230 - 206) * ratio)
            b = int(235 + (255 - 235) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))
        
        # Mraky (animované)
        cloud_positions = [
            (100 + (self.camera_x * 0.1) % SCREEN_WIDTH, 50),
            (300 + (self.camera_x * 0.15) % SCREEN_WIDTH, 80),
            (600 + (self.camera_x * 0.12) % SCREEN_WIDTH, 40),
            (800 + (self.camera_x * 0.08) % SCREEN_WIDTH, 100),
        ]
        
        for cloud_x, cloud_y in cloud_positions:
            self.draw_cloud(cloud_x, cloud_y)
        
        # Země s travou
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        
        # Zemina (hnědá)
        pygame.draw.rect(self.screen, (139, 90, 43), 
                        (0, ground_y, SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Tráva nahoře (zelená)
        pygame.draw.rect(self.screen, (34, 139, 34), 
                        (0, ground_y, SCREEN_WIDTH, 8))
        
        # Stébla trávy
        for i in range(0, SCREEN_WIDTH, 30):
            grass_x = i + (self.camera_x % 30)
            pygame.draw.line(self.screen, (0, 180, 0), 
                           (grass_x, ground_y), 
                           (grass_x - 3, ground_y - 8), 2)
            pygame.draw.line(self.screen, (0, 180, 0), 
                           (grass_x + 10, ground_y), 
                           (grass_x + 13, ground_y - 10), 2)
            pygame.draw.line(self.screen, (0, 180, 0), 
                           (grass_x + 20, ground_y), 
                           (grass_x + 18, ground_y - 7), 2)
        
        # Vykreslení levelu s kamerou
        for platform in self.level.platforms:
            platform.draw(self.screen, self.camera_x)
        
        # Bloky (otázníkové, cihlové)
        for block in self.level.blocks:
            block.draw(self.screen, self.camera_x)
        
        # Roury
        for pipe in self.level.pipes:
            pipe.draw(self.screen, self.camera_x)
        
        # Houby a květiny
        for mushroom in self.level.mushrooms:
            mushroom.draw(self.screen, self.camera_x)
        
        for flower in self.level.flowers:
            flower.draw(self.screen, self.camera_x)
        
        # Power-upy (staré)
        for powerup in self.level.powerups:
            powerup.draw(self.screen, self.camera_x)
            
        for coin in self.level.coins:
            coin.draw(self.screen, self.camera_x)
            
        for enemy in self.level.enemies:
            enemy.draw(self.screen, self.camera_x)
        
        # Částice a efekty
        for particle in self.particles:
            particle.draw(self.screen, self.camera_x)
            
        for effect in self.effects:
            effect.draw(self.screen, self.camera_x)
            
        self.level.flag.draw(self.screen, self.camera_x)
        
        # Vykreslení hráče
        self.player.draw(self.screen, self.camera_x)
        
        # GUI
        self.draw_gui()
        
        # Překryvné obrazovky
        if self.game_state == "level_complete":
            self.draw_level_complete()
        elif self.game_state == "game_over":
            self.draw_game_over()
        elif self.game_state == "win":
            self.draw_win()
        
        pygame.display.flip()
    
    def draw_cloud(self, x, y):
        """Vykreslí hezký mrak"""
        cloud_color = (255, 255, 255)
        # Hlavní části mraku
        pygame.draw.circle(self.screen, cloud_color, (int(x), int(y)), 20)
        pygame.draw.circle(self.screen, cloud_color, (int(x + 20), int(y - 5)), 25)
        pygame.draw.circle(self.screen, cloud_color, (int(x + 40), int(y)), 20)
        pygame.draw.circle(self.screen, cloud_color, (int(x + 25), int(y + 10)), 18)
        # Stín mraku (jemný)
        pygame.draw.circle(self.screen, (240, 240, 240), (int(x + 5), int(y + 3)), 18)
        pygame.draw.circle(self.screen, (240, 240, 240), (int(x + 25), int(y - 2)), 23)
        
    def draw_gui(self):
        """GUI jako v originálním Super Mario Bros"""
        # === ČERNÉ HUD POZADÍ NAHOŘE ===
        hud_height = 50
        hud_bg = pygame.Surface((SCREEN_WIDTH, hud_height))
        hud_bg.fill((0, 0, 0))
        self.screen.blit(hud_bg, (0, 0))
        
        # === MARIO SKÓRE (vlevo nahoře) ===
        mario_label = self.font_small.render("MARIO", True, WHITE)
        self.screen.blit(mario_label, (30, 10))
        
        # Skóre s nulami vpředu (formát: 001000)
        score_str = str(self.score).zfill(6)
        score_text = self.font_small.render(score_str, True, WHITE)
        self.screen.blit(score_text, (30, 28))
        
        # === MINCE ===
        coin_x = 250
        # Ikona mince
        pygame.draw.circle(self.screen, (255, 215, 0), (coin_x, 25), 8)
        pygame.draw.circle(self.screen, ORANGE, (coin_x, 25), 6)
        
        # Počet mincí
        coins_collected = 0  # Můžeme přidat counter pro mince
        coin_count = self.font_small.render(f"x{coins_collected:02d}", True, WHITE)
        self.screen.blit(coin_count, (coin_x + 15, 18))
        
        # === WORLD (prostředek) ===
        world_label = self.font_small.render("WORLD", True, WHITE)
        world_rect = world_label.get_rect(center=(SCREEN_WIDTH//2, 10))
        self.screen.blit(world_label, world_rect)
        
        # Číslo světa
        world_num = self.font_small.render(f"1-{self.current_level}", True, WHITE)
        world_num_rect = world_num.get_rect(center=(SCREEN_WIDTH//2, 28))
        self.screen.blit(world_num, world_num_rect)
        
        # === TIME (vpravo nahoře) ===
        time_label = self.font_small.render("TIME", True, WHITE)
        time_rect = time_label.get_rect(topright=(SCREEN_WIDTH - 30, 10))
        self.screen.blit(time_label, time_rect)
        
        # Zbývající čas
        time_str = str(max(0, self.time_remaining))
        time_text = self.font_small.render(time_str, True, WHITE)
        time_text_rect = time_text.get_rect(topright=(SCREEN_WIDTH - 30, 28))
        self.screen.blit(time_text, time_text_rect)
        
        # === ŽIVOTY (malé ikony dole v rohu) ===
        lives_x = 30
        lives_y = SCREEN_HEIGHT - 35
        
        # Malé Mario ikony pro životy
        for i in range(self.lives):
            icon_x = lives_x + i * 25
            # Hlava Maria (zjednodušená)
            pygame.draw.circle(self.screen, (255, 180, 150), (icon_x, lives_y), 8)  # Obličej
            # Kšiltovka
            pygame.draw.rect(self.screen, RED, (icon_x - 9, lives_y - 8, 18, 6))
            pygame.draw.circle(self.screen, RED, (icon_x, lives_y - 5), 6)
        
        # === COMBO ZOBRAZENÍ ===
        if self.combo > 1:
            combo_text = self.font_medium.render(f"COMBO x{self.combo}!", True, ORANGE)
            combo_rect = combo_text.get_rect(center=(SCREEN_WIDTH//2, 80))
            
            # Pulzující efekt
            import math
            scale = 1 + math.sin(pygame.time.get_ticks() * 0.01) * 0.1
            scaled_width = int(combo_rect.width * scale)
            scaled_height = int(combo_rect.height * scale)
            scaled_text = pygame.transform.scale(combo_text, (scaled_width, scaled_height))
            scaled_rect = scaled_text.get_rect(center=(SCREEN_WIDTH//2, 80))
            
            # Pozadí pro combo
            bg_rect = pygame.Rect(scaled_rect.x - 10, scaled_rect.y - 5, 
                                 scaled_rect.width + 20, scaled_rect.height + 10)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(200)
            bg_surface.fill((255, 100, 0))
            self.screen.blit(bg_surface, (bg_rect.x, bg_rect.y))
            pygame.draw.rect(self.screen, YELLOW, bg_rect, 3)
            
            self.screen.blit(scaled_text, scaled_rect)
        
        # === SPEED BOOST INDIKÁTOR ===
        if self.player.speed_boost_timer > 0:
            boost_text = self.font_small.render("SPEED!", True, (0, 200, 255))
            boost_rect = boost_text.get_rect(topright=(SCREEN_WIDTH - 30, 60))
            self.screen.blit(boost_text, boost_rect)
            self.screen.blit(bg_surface, (bg_rect.x, bg_rect.y))
            pygame.draw.rect(self.screen, (0, 200, 255), bg_rect, 3)
            
            self.screen.blit(boost_text, boost_rect)
            
            # Timer bar
            timer_width = 200
            timer_height = 10
            timer_x = SCREEN_WIDTH - 20 - timer_width
            timer_y = boost_rect.bottom + 10
            
            pygame.draw.rect(self.screen, (50, 50, 50), 
                           (timer_x, timer_y, timer_width, timer_height))
            
            progress = (self.player.speed_boost_timer / 300) * timer_width
            pygame.draw.rect(self.screen, (0, 200, 255),
                           (timer_x, timer_y, int(progress), timer_height))
            
            pygame.draw.rect(self.screen, WHITE,
                           (timer_x, timer_y, timer_width, timer_height), 2)
    
    def draw_heart(self, x, y):
        """Vykreslí červené srdíčko"""
        heart_color = (255, 0, 0)
        # Levá polovina
        pygame.draw.circle(self.screen, heart_color, (x, y), 8)
        # Pravá polovina
        pygame.draw.circle(self.screen, heart_color, (x + 14, y), 8)
        # Spodní trojúhelník
        points = [(x - 8, y), (x + 22, y), (x + 7, y + 18)]
        pygame.draw.polygon(self.screen, heart_color, points)
        # Lesk
        pygame.draw.circle(self.screen, (255, 100, 100), (x + 3, y - 2), 3)
        # Obrys
        pygame.draw.circle(self.screen, (200, 0, 0), (x, y), 8, 2)
        pygame.draw.circle(self.screen, (200, 0, 0), (x + 14, y), 8, 2)
    
    def draw_empty_heart(self, x, y):
        """Vykreslí prázdné srdíčko (ztracený život)"""
        heart_color = (100, 100, 100)
        # Levá polovina
        pygame.draw.circle(self.screen, heart_color, (x, y), 8, 2)
        # Pravá polovina
        pygame.draw.circle(self.screen, heart_color, (x + 14, y), 8, 2)
        # Spodní trojúhelník
        points = [(x - 8, y), (x + 22, y), (x + 7, y + 18)]
        pygame.draw.polygon(self.screen, heart_color, points, 2)
        
    def draw_level_complete(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Animace pulzování
        import math
        pulse = 1 + math.sin(pygame.time.get_ticks() * 0.005) * 0.1
        
        complete_text = self.font_large.render("LEVEL DOKONČEN!", True, GREEN)
        text_width = int(complete_text.get_width() * pulse)
        text_height = int(complete_text.get_height() * pulse)
        scaled_text = pygame.transform.scale(complete_text, (text_width, text_height))
        complete_rect = scaled_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
        self.screen.blit(scaled_text, complete_rect)
        
        # Hvězdičky kolem textu
        for i in range(8):
            angle = (i / 8) * 2 * math.pi + pygame.time.get_ticks() * 0.002
            x = SCREEN_WIDTH//2 + math.cos(angle) * 150
            y = SCREEN_HEIGHT//2 - 80 + math.sin(angle) * 80
            star_size = 8
            
            points = []
            for j in range(5):
                angle1 = math.pi / 2 + (2 * math.pi * j / 5)
                angle2 = math.pi / 2 + (2 * math.pi * (j + 0.5) / 5)
                
                x1 = x + math.cos(angle1) * star_size
                y1 = y + math.sin(angle1) * star_size
                x2 = x + math.cos(angle2) * (star_size / 2)
                y2 = y + math.sin(angle2) * (star_size / 2)
                
                points.extend([(x1, y1), (x2, y2)])
            
            pygame.draw.polygon(self.screen, YELLOW, points)
        
        score_text = self.font_medium.render(f"Skóre: {self.score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        continue_text = self.font_medium.render("Stiskni ENTER pro pokračování", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        
        # Blikající text
        if int(pygame.time.get_ticks() / 500) % 2 == 0:
            self.screen.blit(continue_text, continue_rect)
        
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_medium.render(f"Finální skóre: {self.score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font_small.render("Stiskni R pro restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_win(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Konfety efekt
        import math
        import random
        random.seed(42)  # Pro konzistentní pozice
        for i in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = (random.randint(0, SCREEN_HEIGHT) + pygame.time.get_ticks() // 10) % SCREEN_HEIGHT
            color = random.choice([RED, YELLOW, GREEN, BLUE, (255, 0, 255)])
            size = random.randint(3, 8)
            pygame.draw.circle(self.screen, color, (x, y), size)
        
        win_text = self.font_large.render("GRATULUJEME!", True, YELLOW)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        
        # Stín textu
        shadow_text = self.font_large.render("GRATULUJEME!", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH//2 + 3, SCREEN_HEIGHT//2 - 97))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(win_text, win_rect)
        
        complete_text = self.font_medium.render("Dokončil jsi všechny levely!", True, GREEN)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        self.screen.blit(complete_text, complete_rect)
        
        score_text = self.font_medium.render(f"Finální skóre: {self.score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        
        # Pulzující skóre
        pulse = 1 + math.sin(pygame.time.get_ticks() * 0.005) * 0.1
        text_width = int(score_text.get_width() * pulse)
        text_height = int(score_text.get_height() * pulse)
        scaled_score = pygame.transform.scale(score_text, (text_width, text_height))
        scaled_rect = scaled_score.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        self.screen.blit(scaled_score, scaled_rect)
        
        restart_text = self.font_small.render("Stiskni R pro restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        
        # Blikající text
        if int(pygame.time.get_ticks() / 500) % 2 == 0:
            self.screen.blit(restart_text, restart_rect)
