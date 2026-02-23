class Player(pygame.sprite.Sprite)
        def update(self, platforms):
            
            if keys[pygame.K_SPACE] and self.on.ground:
                  self.velocity_y = JUMP_POWER
                  self.on_ground = False

            self.velocity_y += GRAVITY
            if self.velocity_y > 15
             self.velocity_y = 15
            
        self.rect.x += self.velocity_x
        if self.rect.left < 0:
             self.rect.left = 0
        if self.rect.right = SCREEN_WIDTH:
             self.rect.right = SCREEN_WIDTH

        self.rect.y += self.velocity_y

        self.on_ground = Falsee

        for platform in platform
            if self.rect.colliderect(platform.rect)
                if self.velocity_y = 0:
                    self.on_ground = True
                elif self.velocity_y < 0
                   self.rect.top = platform.rect.button
                   self.velocity_y = 0

        if self.rect.top > SCREEN_HEIGHT:
            return True
        return False

