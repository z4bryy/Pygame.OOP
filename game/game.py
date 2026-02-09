import pygame
from config import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.last_mouse_pos = (0, 0)  # uložíme poslední známou pozici myši

    def handle_events(self):
        for event in pygame.event.get():
            print(event.type)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                nazev_klavesy = pygame.key.name(event.key)
                # ukončit pouze při ESC
                if event.key == pygame.K_ESCAPE:
                    print(f"Zmáčknutá klávesa: {nazev_klavesy} (kód: {event.key}) -> ukončuji")
                    self.running = False
                else:
                    # pouze vypiš název klávesy a pozici myši, bez ukončení
                    x, y = pygame.mouse.get_pos() or self.last_mouse_pos
                    self.last_mouse_pos = (x, y)
                    print(f"Zmáčknutá klávesa: {nazev_klavesy} (kód: {event.key})")
                    print(f"{x}, {y}")
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                self.last_mouse_pos = (x, y)
                print(f"{x}, {y}")

    def update(self):
        pass

    def draw(self):
        self.screen.fill(SKY_BLUE)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)