# Super Mario Bros - Technical Architecture Documentation

## Game Engine Architecture Overview

This document provides a comprehensive breakdown of the Super Mario Bros (NES style) game engine architecture, focusing on Player and Enemy systems.

---

## 1. PLAYER STRUCTURE (Mario)

### 1.1 Data Structure

The Player class represents Mario's complete state in the game world.

```python
class Player:
    # === PHYSICS & TRANSFORM ===
    position: Vector2D          # World position (x, y)
    velocity: Vector2D          # Current velocity (vx, vy)
    acceleration: Vector2D      # Current acceleration (ax, ay)
    hitbox: Rect               # Collision rectangle (AABB)
    
    # === MOVEMENT STATE ===
    is_grounded: bool          # On solid ground?
    facing_direction: int      # 1 = right, -1 = left
    move_state: MovementState  # Idle, Walking, Running, Jumping, Falling
    
    # === POWER STATE ===
    power_state: PowerState    # Small, Super, Fire
    size: Size                 # Current hitbox dimensions
    invincibility_frames: int  # I-frames after damage
    transform_frames: int      # Transition animation frames
    
    # === ABILITIES ===
    can_shoot: bool            # Fire Mario ability
    fireballs: List[Fireball]  # Active projectiles
    shoot_cooldown: int        # Frames until next shot
    
    # === PHYSICS CONSTANTS ===
    WALK_SPEED = 2.5
    RUN_SPEED = 4.0
    JUMP_FORCE = -12.0
    GRAVITY = 0.6
    FRICTION = 0.8
    AIR_RESISTANCE = 0.95
```

### 1.2 Finite State Machine (FSM)

#### Movement States
```
                    ┌─────────┐
                    │  IDLE   │
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    [Run Input]    [Jump Input]   [Fall Off]
          │              │              │
          ▼              ▼              ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ RUNNING │───→│ JUMPING │───→│ FALLING │
    └─────────┘    └────┬────┘    └────┬────┘
          │             │              │
          └─────────[Land]─────────────┘
                        │
                        ▼
                   ┌─────────┐
                   │  IDLE   │
                   └─────────┘
```

#### Power States
```
┌───────────┐  Mushroom  ┌───────────┐  Fire Flower  ┌───────────┐
│   SMALL   │───────────→│   SUPER   │──────────────→│   FIRE    │
│  (40px)   │            │  (50px)   │               │  (50px)   │
└─────┬─────┘            └─────┬─────┘               └─────┬─────┘
      │                        │                           │
      │         [Damage]       │        [Damage]           │
      │←───────────────────────┴───────────────────────────┘
      │
      └──[Damage]──→ DEATH
```

### 1.3 Physics Implementation

```python
def update_physics(self, delta_time: float):
    """
    Physics update following Euler integration
    Position Verlet would be more accurate but Euler matches NES behavior
    """
    
    # 1. APPLY GRAVITY (constant downward acceleration)
    if not self.is_grounded:
        self.velocity.y += GRAVITY * delta_time
        self.velocity.y = min(self.velocity.y, MAX_FALL_SPEED)
    
    # 2. APPLY FRICTION (ground friction or air resistance)
    if self.is_grounded:
        self.velocity.x *= FRICTION
    else:
        self.velocity.x *= AIR_RESISTANCE
    
    # 3. INTEGRATE VELOCITY
    self.position.x += self.velocity.x * delta_time
    self.position.y += self.velocity.y * delta_time
    
    # 4. UPDATE HITBOX
    self.hitbox.x = self.position.x
    self.hitbox.y = self.position.y
    
    # 5. ANIMATION FRAME
    if abs(self.velocity.x) > 0.1:
        self.animation_frame += abs(self.velocity.x) * 0.1

def handle_input(self, keys):
    """Process player input and update movement state"""
    
    # HORIZONTAL MOVEMENT
    if keys[LEFT]:
        self.acceleration.x = -WALK_SPEED
        self.facing_direction = -1
        self.move_state = MovementState.RUNNING
    elif keys[RIGHT]:
        self.acceleration.x = WALK_SPEED
        self.facing_direction = 1
        self.move_state = MovementState.RUNNING
    else:
        self.acceleration.x = 0
        if self.is_grounded:
            self.move_state = MovementState.IDLE
    
    # Apply acceleration to velocity
    self.velocity.x += self.acceleration.x
    self.velocity.x = clamp(self.velocity.x, -RUN_SPEED, RUN_SPEED)
    
    # JUMP (buffered input for 5 frames)
    if keys[JUMP] and (self.is_grounded or self.coyote_time > 0):
        self.velocity.y = JUMP_FORCE
        self.is_grounded = False
        self.move_state = MovementState.JUMPING
        self.jump_buffer = 0
    
    # VARIABLE JUMP HEIGHT (release early = shorter jump)
    if not keys[JUMP] and self.velocity.y < 0:
        self.velocity.y *= 0.5  # Cut jump short
    
    # SHOOTING (Fire Mario only)
    if keys[SHOOT] and self.power_state == PowerState.FIRE:
        if self.can_shoot and len(self.fireballs) < 2:
            self.shoot_fireball()
```

---

## 2. ENEMY STRUCTURE

### 2.1 Inheritance Hierarchy

```
                    ┌──────────────┐
                    │    Entity    │
                    │ (Abstract)   │
                    └──────┬───────┘
                           │
           ┌───────────────┴───────────────┐
           │                               │
    ┌──────▼───────┐               ┌──────▼──────┐
    │    Player    │               │  BaseEnemy  │
    └──────────────┘               │ (Abstract)  │
                                   └──────┬───────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
             ┌──────▼──────┐       ┌─────▼─────┐       ┌──────▼──────┐
             │   Goomba    │       │   Koopa   │       │   Piranha   │
             │  (Walker)   │       │ (Shelled) │       │   (Static)  │
             └─────────────┘       └───────────┘       └─────────────┘
```

### 2.2 Class Structure

```python
# === BASE ENTITY ===
class Entity:
    """Abstract base for all game entities"""
    def __init__(self, x: float, y: float):
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)
        self.hitbox = Rect(x, y, 0, 0)
        self.is_alive = True
        self.gravity_scale = 1.0
    
    def update(self, delta_time: float):
        """Override in subclasses"""
        raise NotImplementedError
    
    def draw(self, screen, camera_offset):
        """Override in subclasses"""
        raise NotImplementedError
    
    def apply_gravity(self, delta_time: float):
        """Standard gravity for all entities"""
        self.velocity.y += GRAVITY * self.gravity_scale * delta_time
        self.velocity.y = min(self.velocity.y, MAX_FALL_SPEED)

# === BASE ENEMY ===
class BaseEnemy(Entity):
    """Base class for all enemies"""
    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__(x, y)
        self.hitbox = Rect(x, y, width, height)
        self.direction = -1  # -1 = left, 1 = right
        self.patrol_speed = 1.0
        self.is_stomped = False
        self.death_timer = 0
        
    def update(self, delta_time: float, platforms: List[Platform]):
        """Standard enemy update loop"""
        if not self.is_alive:
            self.death_timer += delta_time
            return
        
        # 1. AI Behavior
        self.update_ai()
        
        # 2. Physics
        self.apply_gravity(delta_time)
        self.position.x += self.velocity.x * delta_time
        self.position.y += self.velocity.y * delta_time
        
        # 3. Collision
        self.check_platform_collision(platforms)
        self.check_world_bounds()
        
        # 4. Update hitbox
        self.hitbox.x = self.position.x
        self.hitbox.y = self.position.y
    
    def update_ai(self):
        """Override in subclasses for specific behavior"""
        pass
    
    def on_stomped(self):
        """Called when player jumps on enemy"""
        self.is_alive = False
        self.is_stomped = True
        self.velocity.y = -8  # Bounce effect
    
    def check_edge(self, platforms: List[Platform]) -> bool:
        """Detect if enemy is at edge of platform"""
        # Raycast down from front edge
        check_x = self.position.x + (self.hitbox.width * self.direction)
        check_y = self.position.y + self.hitbox.height + 5
        
        for platform in platforms:
            if platform.hitbox.collidepoint(check_x, check_y):
                return False  # Ground ahead
        return True  # Edge detected!

# === GOOMBA (Simple Walker) ===
class Goomba(BaseEnemy):
    """Basic walking enemy that patrols back and forth"""
    def __init__(self, x: float, y: float):
        super().__init__(x, y, width=32, height=32)
        self.patrol_speed = 1.5
        
    def update_ai(self):
        """Simple patrol behavior"""
        # Move in current direction
        self.velocity.x = self.patrol_speed * self.direction
        
        # Turn at edges (optional based on NES behavior)
        # Original Goombas DON'T turn at edges, they fall!
        # But some implementations add edge detection:
        # if self.check_edge(platforms):
        #     self.direction *= -1
    
    def on_wall_collision(self):
        """Turn around when hitting wall"""
        self.direction *= -1

# === KOOPA TROOPA (Shell Mechanic) ===
class Koopa(BaseEnemy):
    """Enemy that retreats into shell when stomped"""
    def __init__(self, x: float, y: float, color: str = "green"):
        super().__init__(x, y, width=32, height=48)
        self.color = color  # green = walks off edges, red = turns around
        self.in_shell = False
        self.shell_kicked = False
        self.shell_speed = 8.0
        
    def update_ai(self):
        if self.in_shell:
            # Shell behavior
            if self.shell_kicked:
                self.velocity.x = self.shell_speed * self.direction
            else:
                self.velocity.x = 0
        else:
            # Normal walking
            self.velocity.x = self.patrol_speed * self.direction
            
            # Red Koopas turn at edges
            if self.color == "red" and self.check_edge():
                self.direction *= -1
    
    def on_stomped(self):
        """Enter shell mode instead of dying"""
        if not self.in_shell:
            self.in_shell = True
            self.hitbox.height = 32  # Smaller hitbox
            self.velocity.x = 0
        else:
            # Kick shell
            self.shell_kicked = True
            self.direction = 1 if self.player_direction > 0 else -1
```

---

## 3. INTERACTION & COLLISION SYSTEM

### 3.1 AABB Collision Detection

```python
class CollisionSystem:
    """Handles all collision detection and resolution"""
    
    @staticmethod
    def check_aabb(rect_a: Rect, rect_b: Rect) -> bool:
        """
        Axis-Aligned Bounding Box collision check
        Returns True if rectangles overlap
        """
        return (rect_a.x < rect_b.x + rect_b.width and
                rect_a.x + rect_a.width > rect_b.x and
                rect_a.y < rect_b.y + rect_b.height and
                rect_a.y + rect_a.height > rect_b.y)
    
    @staticmethod
    def get_collision_normal(player: Player, enemy: BaseEnemy) -> Vector2D:
        """
        Determine collision direction (where player hit enemy)
        Returns normalized vector of collision
        """
        # Calculate overlap on each axis
        dx = (player.hitbox.centerx - enemy.hitbox.centerx)
        dy = (player.hitbox.centery - enemy.hitbox.centery)
        
        # Calculate penetration depth
        overlap_x = (player.hitbox.width + enemy.hitbox.width) / 2 - abs(dx)
        overlap_y = (player.hitbox.height + enemy.hitbox.height) / 2 - abs(dy)
        
        # Collision from the side with LEAST penetration
        if overlap_x < overlap_y:
            # Horizontal collision (side touch)
            return Vector2D(1 if dx > 0 else -1, 0)
        else:
            # Vertical collision (top/bottom)
            return Vector2D(0, 1 if dy > 0 else -1)
    
    @staticmethod
    def resolve_player_enemy_collision(player: Player, enemy: BaseEnemy):
        """
        Main collision resolution logic
        Determines if player stomps enemy or takes damage
        """
        if not CollisionSystem.check_aabb(player.hitbox, enemy.hitbox):
            return  # No collision
        
        if not enemy.is_alive:
            return  # Dead enemies don't collide
        
        # Get collision direction
        normal = CollisionSystem.get_collision_normal(player, enemy)
        
        # === STOMP CHECK ===
        # Player must be:
        # 1. Moving downward (velocity.y > 0)
        # 2. Collision from above (normal.y < 0)
        # 3. Player's bottom edge above enemy's center
        if (player.velocity.y > 0 and 
            normal.y < 0 and 
            player.hitbox.bottom < enemy.hitbox.centery + 5):
            
            # STOMP SUCCESSFUL
            enemy.on_stomped()
            player.velocity.y = -10  # Bounce player up
            player.combo_counter += 1
            
            # Award points based on combo
            points = 100 * player.combo_counter
            Game.add_score(points)
            
        else:
            # === DAMAGE PLAYER ===
            if player.invincibility_frames <= 0:
                player.take_damage()
```

### 3.2 Collision Resolution Detail

```python
def resolve_platform_collision(entity: Entity, platforms: List[Platform]):
    """
    Resolve entity collision with platforms
    Uses swept AABB for continuous collision detection
    """
    for platform in platforms:
        if not CollisionSystem.check_aabb(entity.hitbox, platform.hitbox):
            continue
        
        # Calculate overlap
        dx = entity.hitbox.centerx - platform.hitbox.centerx
        dy = entity.hitbox.centery - platform.hitbox.centery
        
        overlap_x = (entity.hitbox.width + platform.hitbox.width) / 2 - abs(dx)
        overlap_y = (entity.hitbox.height + platform.hitbox.height) / 2 - abs(dy)
        
        # Resolve on axis with LEAST penetration
        if overlap_x < overlap_y:
            # Horizontal collision
            if dx > 0:
                entity.position.x += overlap_x
            else:
                entity.position.x -= overlap_x
            entity.velocity.x = 0
            
            # Enemy wall collision
            if isinstance(entity, BaseEnemy):
                entity.on_wall_collision()
        else:
            # Vertical collision
            if dy > 0:
                # Hit from above (landing on platform)
                entity.position.y += overlap_y
                entity.velocity.y = 0
                entity.is_grounded = True
            else:
                # Hit from below (bonking head)
                entity.position.y -= overlap_y
                entity.velocity.y = 0
```

---

## 4. GAME LOOP ARCHITECTURE

```python
class Game:
    """Main game loop"""
    
    def __init__(self):
        self.player = Player(100, 400)
        self.enemies = []
        self.platforms = []
        self.delta_time = 0
        self.clock = pygame.time.Clock()
        
    def run(self):
        """Main game loop"""
        running = True
        while running:
            # 1. TIMING
            self.delta_time = self.clock.tick(60) / 1000.0  # 60 FPS
            
            # 2. INPUT
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            
            # 3. UPDATE
            self.player.update(self.delta_time)
            
            for enemy in self.enemies:
                enemy.update(self.delta_time, self.platforms)
            
            # 4. COLLISION
            for enemy in self.enemies:
                CollisionSystem.resolve_player_enemy_collision(
                    self.player, enemy
                )
            
            # 5. RENDER
            self.draw()
            
    def draw(self):
        """Render all game objects"""
        self.screen.fill(SKY_BLUE)
        
        camera_offset = self.calculate_camera()
        
        for platform in self.platforms:
            platform.draw(self.screen, camera_offset)
        
        for enemy in self.enemies:
            enemy.draw(self.screen, camera_offset)
        
        self.player.draw(self.screen, camera_offset)
        
        pygame.display.flip()
```

---

## 5. PERFORMANCE CONSIDERATIONS

### Spatial Partitioning
For levels with many entities, use quad-tree or grid-based spatial partitioning:

```python
class SpatialGrid:
    """Grid-based spatial partitioning for efficient collision detection"""
    def __init__(self, cell_size=128):
        self.cell_size = cell_size
        self.grid = {}
    
    def insert(self, entity: Entity):
        """Insert entity into grid cells it occupies"""
        cells = self.get_cells(entity.hitbox)
        for cell in cells:
            if cell not in self.grid:
                self.grid[cell] = []
            self.grid[cell].append(entity)
    
    def query(self, rect: Rect) -> List[Entity]:
        """Get all entities in cells overlapping rect"""
        cells = self.get_cells(rect)
        results = set()
        for cell in cells:
            if cell in self.grid:
                results.update(self.grid[cell])
        return list(results)
```

---

## 6. KEY TAKEAWAYS

1. **Separation of Concerns**: Physics, AI, and rendering are separate
2. **Inheritance Hierarchy**: Base classes reduce code duplication
3. **Collision Precision**: AABB with penetration resolution
4. **Fixed Timestep**: 60 FPS for consistent physics
5. **State Machines**: Clear state transitions for player and enemies

This architecture provides a solid foundation for a NES-style platformer with room for expansion.
