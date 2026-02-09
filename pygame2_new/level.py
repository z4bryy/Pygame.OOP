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
        
        if level_number == 1:
            self.create_level_1()
        elif level_number == 2:
            self.create_level_2()
        elif level_number == 3:
            self.create_level_3()
            
    def create_level_1(self):
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.platforms.append(Platform(0, ground_y, 400, GROUND_HEIGHT))
        self.platforms.append(Platform(400, ground_y, 200, GROUND_HEIGHT))
        self.platforms.append(Platform(650, ground_y, 250, GROUND_HEIGHT))
        self.platforms.append(Platform(950, ground_y, 350, GROUND_HEIGHT))
        self.platforms.append(Platform(1350, ground_y, 400, GROUND_HEIGHT))
        self.platforms.append(Platform(1800, ground_y, 600, GROUND_HEIGHT))
        self.platforms.append(Platform(500, 370, 80, 20))
        self.platforms.append(Platform(650, 320, 80, 20))
        self.platforms.append(Platform(1100, 380, 100, 20))
        self.blocks.append(Block(320, 370, "question", "coin"))
        self.blocks.append(Block(360, 370, "question", "powerup"))
        self.blocks.append(Block(400, 370, "brick"))
        self.blocks.append(Block(440, 370, "question", "coin"))
        self.blocks.append(Block(560, 320, "question", "coin"))
        self.blocks.append(Block(700, 270, "question", "powerup"))
        self.blocks.append(Block(900, 370, "brick"))
        self.blocks.append(Block(940, 370, "brick"))
        self.blocks.append(Block(980, 370, "brick"))
        self.blocks.append(Block(1020, 370, "question", "coin"))
        self.blocks.append(Block(1060, 370, "brick"))
        for i in range(8):
            self.blocks.append(Block(1200 + i*40, 320, "brick"))
        self.blocks.append(Block(1360, 320, "question", "powerup"))
        self.pipes.append(Pipe(450, ground_y - 80, 2))
        self.pipes.append(Pipe(750, ground_y - 120, 3))
        self.pipes.append(Pipe(1150, ground_y - 160, 4))
        self.pipes.append(Pipe(1600, ground_y - 120, 3))
        self.enemies.append(Enemy(380, ground_y - 40))
        self.enemies.append(Enemy(420, ground_y - 40))
        self.enemies.append(Enemy(800, ground_y - 40))
        self.enemies.append(Enemy(950, ground_y - 40))
        self.enemies.append(Enemy(1000, ground_y - 40))
        self.enemies.append(Enemy(1400, ground_y - 40))
        self.enemies.append(Enemy(1500, ground_y - 40))
        for i in range(5):
            self.coins.append(Coin(600 + i*30, 350))
        for i in range(4):
            self.coins.append(Coin(1110 + i*30, 320))
        self.flag = Flag(2200, SCREEN_HEIGHT - GROUND_HEIGHT - 180)
        
    def create_level_2(self):
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.platforms.append(Platform(0, ground_y, 2500, GROUND_HEIGHT))
        for i in range(5):
            width = 60 + i*20
            self.platforms.append(Platform(300 + i*100, ground_y - 60 - i*50, width, 20))
        self.platforms.append(Platform(900, ground_y - 150, 200, 20))
        self.platforms.append(Platform(1200, ground_y - 200, 150, 20))
        self.pipes.append(Pipe(200, ground_y - 80, 2))
        self.pipes.append(Pipe(500, ground_y - 120, 3))
        self.pipes.append(Pipe(800, ground_y - 160, 4))
        self.pipes.append(Pipe(1100, ground_y - 120, 3))
        self.pipes.append(Pipe(1500, ground_y - 160, 4))
        self.pipes.append(Pipe(1800, ground_y - 200, 5))
        self.pipes.append(Pipe(2100, ground_y - 120, 3))
        for i in range(12):
            self.blocks.append(Block(400 + i*40, 300, "brick"))
        self.blocks.append(Block(600, 300, "question", "coin"))
        self.blocks.append(Block(720, 300, "question", "powerup"))
        for height in range(5):
            self.blocks.append(Block(1000, ground_y - 80 - height*40, "brick"))
            self.blocks.append(Block(1040, ground_y - 80 - height*40, "brick"))
        self.blocks.append(Block(1300, 250, "question", "coin"))
        self.blocks.append(Block(1600, 200, "question", "powerup"))
        self.enemies.append(Enemy(350, ground_y - 40))
        self.enemies.append(Enemy(600, ground_y - 40))
        self.enemies.append(Enemy(650, ground_y - 40))
        self.enemies.append(Enemy(1200, ground_y - 40))
        self.enemies.append(Enemy(1400, ground_y - 40))
        self.enemies.append(Enemy(1900, ground_y - 40))
        for i in range(10):
            self.coins.append(Coin(950 + i*30, ground_y - 100))
        for i in range(6):
            self.coins.append(Coin(1250 + i*30, 220))
        self.flag = Flag(2300, SCREEN_HEIGHT - GROUND_HEIGHT - 180)
        
    def create_level_3(self):
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.platforms.append(Platform(0, ground_y, 200, GROUND_HEIGHT))
        self.platforms.append(Platform(1800, ground_y, 600, GROUND_HEIGHT))
        platforms_config = [(200, 480, 80), (350, 420, 70), (500, 360, 70), (650, 300, 80), (500, 240, 70), (350, 180, 80), (550, 180, 80), (750, 240, 100), (900, 300, 80), (1050, 250, 100), (1200, 320, 80), (1350, 380, 100), (1500, 440, 120), (1670, 380, 100)]
        for x, y, width in platforms_config:
            self.platforms.append(Platform(x, y, width, 20))
        blocks_config = [(220, 400, "question", "coin"), (380, 340, "question", "powerup"), (530, 280, "question", "coin"), (680, 220, "question", "powerup"), (530, 160, "question", "coin"), (780, 160, "question", "coin"), (1080, 170, "question", "powerup"), (1230, 240, "question", "coin"), (1380, 300, "question", "powerup")]
        for x, y, block_type, content in blocks_config:
            self.blocks.append(Block(x, y, block_type, content))
        brick_positions = [(260, 400), (420, 340), (460, 340), (720, 220), (820, 160), (860, 160)]
        for x, y in brick_positions:
            self.blocks.append(Block(x, y, "brick"))
        self.pipes.append(Pipe(300, 460, 2))
        self.pipes.append(Pipe(800, 420, 3))
        self.pipes.append(Pipe(1700, 470, 3))
        enemies_config = [(230, 430), (380, 370), (680, 250), (800, 190), (1100, 200), (1240, 270), (1530, 390), (1710, 330)]
        for x, y in enemies_config:
            self.enemies.append(Enemy(x, y))
        coin_positions = [(380, 370), (530, 310), (930, 250), (1230, 270), (1530, 390)]
        for x, y in coin_positions:
            self.coins.append(Coin(x, y))
        self.flag = Flag(2200, SCREEN_HEIGHT - GROUND_HEIGHT - 180)
