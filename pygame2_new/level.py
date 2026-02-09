import pygame
from config import *
from platform import Platform
from enemy import Enemy
from coin import Coin
from flag import Flag
from powerup import PowerUp
from mario_blocks import Block, Pipe, Mushroom, FireFlower

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.platforms = []
        self.enemies = []
        self.coins = []
        self.powerups = []
        self.blocks = []
        self.pipes = []
        self.mushrooms = []
        self.flowers = []
        self.flag = None
        
        # Načtení levelu podle čísla
        if level_number == 1:
            self.create_level_1()
        elif level_number == 2:
            self.create_level_2()
        elif level_number == 3:
            self.create_level_3()
            
    def create_level_1(self):
        """Jednoduchý úvodní level"""
        # Platformy
        self.platforms.append(Platform(300, 450, 150, 20))
        self.platforms.append(Platform(500, 400, 100, 20))
        self.platforms.append(Platform(650, 350, 120, 20))
        self.platforms.append(Platform(850, 300, 150, 20))
        self.platforms.append(Platform(1050, 400, 100, 20))
        self.platforms.append(Platform(1200, 450, 200, 20))
        
        # Otázníkové bloky s obsahem
        self.blocks.append(Block(350, 370, "question", "coin"))
        self.blocks.append(Block(390, 370, "question", "powerup"))  # Mushroom pro Small, Flower pro Super
        self.blocks.append(Block(430, 370, "question", "coin"))
        
        self.blocks.append(Block(700, 270, "question", "coin"))
        self.blocks.append(Block(900, 220, "question", "powerup"))  # Mushroom pro Small, Flower pro Super
        
        # Cihlové bloky
        self.blocks.append(Block(540, 320, "brick"))
        self.blocks.append(Block(580, 320, "brick"))
        self.blocks.append(Block(620, 320, "brick"))
        
        # Roury
        self.pipes.append(Pipe(600, 510, 2))
        self.pipes.append(Pipe(1100, 470, 3))
        
        # Mince
        self.coins.append(Coin(530, 350))
        self.coins.append(Coin(1080, 350))
        self.coins.append(Coin(1250, 400))
        self.coins.append(Coin(1300, 400))
        
        # Nepřátelé
        self.enemies.append(Enemy(550, 350, 80))
        self.enemies.append(Enemy(900, 250, 100))
        self.enemies.append(Enemy(1250, 400, 120))
        
        # Power-upy (stará verze - extra životy)
        self.powerups.append(PowerUp(1100, 350, "extra_life"))
        
        # Vlajka (cíl)
        self.flag = Flag(1450, SCREEN_HEIGHT - GROUND_HEIGHT - FLAG_HEIGHT)
        
    def create_level_2(self):
        """Středně těžký level s více skoky"""
        # Platformy - více vertikálních skoků
        self.platforms.append(Platform(250, 450, 100, 20))
        self.platforms.append(Platform(400, 400, 80, 20))
        self.platforms.append(Platform(550, 350, 80, 20))
        self.platforms.append(Platform(400, 280, 100, 20))
        self.platforms.append(Platform(600, 230, 120, 20))
        self.platforms.append(Platform(800, 280, 100, 20))
        self.platforms.append(Platform(950, 350, 100, 20))
        self.platforms.append(Platform(1100, 300, 150, 20))
        self.platforms.append(Platform(1300, 400, 100, 20))
        self.platforms.append(Platform(1450, 450, 120, 20))
        
        # Otázníkové bloky
        self.blocks.append(Block(280, 370, "question", "coin"))
        self.blocks.append(Block(430, 320, "question", "powerup"))  # Adaptivní power-up
        self.blocks.append(Block(580, 270, "question", "coin"))
        self.blocks.append(Block(650, 150, "question", "powerup"))  # Adaptivní power-up
        self.blocks.append(Block(830, 200, "question", "coin"))
        self.blocks.append(Block(1150, 220, "question", "powerup"))  # Adaptivní power-up
        
        # Cihlové bloky
        self.blocks.append(Block(470, 320, "brick"))
        self.blocks.append(Block(510, 320, "brick"))
        self.blocks.append(Block(870, 200, "brick"))
        self.blocks.append(Block(910, 200, "brick"))
        
        # Roury
        self.pipes.append(Pipe(500, 490, 2))
        self.pipes.append(Pipe(750, 470, 3))
        self.pipes.append(Pipe(1350, 450, 4))
        
        # Mince
        self.coins.append(Coin(430, 350))
        self.coins.append(Coin(580, 300))
        self.coins.append(Coin(980, 300))
        self.coins.append(Coin(1330, 350))
        
        # Více nepřátel
        self.enemies.append(Enemy(280, 400, 70))
        self.enemies.append(Enemy(600, 180, 90))
        self.enemies.append(Enemy(850, 230, 80))
        self.enemies.append(Enemy(1150, 250, 100))
        self.enemies.append(Enemy(1350, 350, 70))
        
        # Power-upy
        self.powerups.append(PowerUp(1000, 300, "extra_life"))
        
        # Vlajka
        self.flag = Flag(1650, SCREEN_HEIGHT - GROUND_HEIGHT - FLAG_HEIGHT)
        
    def create_level_3(self):
        """Nejtěžší level s přesnými skoky a více nepřáteli"""
        # Náročnější platformy
        self.platforms.append(Platform(200, 480, 80, 20))
        self.platforms.append(Platform(350, 420, 70, 20))
        self.platforms.append(Platform(500, 360, 70, 20))
        self.platforms.append(Platform(650, 300, 80, 20))
        self.platforms.append(Platform(500, 240, 70, 20))
        self.platforms.append(Platform(350, 180, 80, 20))
        self.platforms.append(Platform(550, 180, 80, 20))
        self.platforms.append(Platform(750, 240, 100, 20))
        self.platforms.append(Platform(900, 300, 80, 20))
        self.platforms.append(Platform(1050, 250, 100, 20))
        self.platforms.append(Platform(1200, 320, 80, 20))
        self.platforms.append(Platform(1350, 380, 100, 20))
        self.platforms.append(Platform(1500, 440, 120, 20))
        self.platforms.append(Platform(1670, 380, 100, 20))
        
        # Mnoho otázníkových bloků
        self.blocks.append(Block(220, 400, "question", "coin"))
        self.blocks.append(Block(380, 340, "question", "powerup"))  # Adaptivní
        self.blocks.append(Block(530, 280, "question", "coin"))
        self.blocks.append(Block(680, 220, "question", "powerup"))  # Adaptivní
        self.blocks.append(Block(530, 160, "question", "coin"))
        self.blocks.append(Block(380, 100, "question", "powerup"))  # Adaptivní
        self.blocks.append(Block(780, 160, "question", "coin"))
        self.blocks.append(Block(1080, 170, "question", "powerup"))  # Adaptivní
        self.blocks.append(Block(1230, 240, "question", "coin"))
        self.blocks.append(Block(1380, 300, "question", "powerup"))  # Adaptivní
        
        # Hodně cihlových bloků
        self.blocks.append(Block(260, 400, "brick"))
        self.blocks.append(Block(420, 340, "brick"))
        self.blocks.append(Block(460, 340, "brick"))
        self.blocks.append(Block(720, 220, "brick"))
        self.blocks.append(Block(820, 160, "brick"))
        self.blocks.append(Block(860, 160, "brick"))
        
        # Roury
        self.pipes.append(Pipe(300, 490, 2))
        self.pipes.append(Pipe(800, 450, 4))
        self.pipes.append(Pipe(1150, 430, 5))
        self.pipes.append(Pipe(1700, 470, 3))
        
        # Mince
        self.coins.append(Coin(380, 370))
        self.coins.append(Coin(530, 310))
        self.coins.append(Coin(930, 250))
        self.coins.append(Coin(1230, 270))
        self.coins.append(Coin(1530, 390))
        
        # Hodně nepřátel
        self.enemies.append(Enemy(230, 430, 50))
        self.enemies.append(Enemy(380, 370, 60))
        self.enemies.append(Enemy(680, 250, 70))
        self.enemies.append(Enemy(800, 190, 70))
        self.enemies.append(Enemy(1100, 200, 80))
        self.enemies.append(Enemy(1240, 270, 60))
        self.enemies.append(Enemy(1530, 390, 90))
        self.enemies.append(Enemy(1710, 330, 60))
        
        # Power-upy
        self.powerups.append(PowerUp(1350, 330, "extra_life"))
        
        # Vlajka
        self.flag = Flag(1850, SCREEN_HEIGHT - GROUND_HEIGHT - FLAG_HEIGHT)
