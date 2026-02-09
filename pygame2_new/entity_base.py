"""
Entity Base Classes
Provides foundation for all game entities (Player, Enemies, Items)
"""
import pygame
from config import GRAVITY, SCREEN_HEIGHT, GROUND_HEIGHT
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Vector2D:
    """2D Vector for position and velocity"""
    x: float = 0.0
    y: float = 0.0
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar: float):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector2D(self.x / mag, self.y / mag)
        return Vector2D(0, 0)


class Entity:
    """
    Abstract base class for all game entities
    Provides common physics and collision properties
    """
    def __init__(self, x: float, y: float, width: int, height: int):
        # Transform
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)
        self.acceleration = Vector2D(0, 0)
        
        # Collision
        self.rect = pygame.Rect(int(x), int(y), width, height)
        self.hitbox_offset = Vector2D(0, 0)  # For sprite vs hitbox offset
        
        # State
        self.is_alive = True
        self.is_active = True  # For off-screen culling
        
        # Physics properties
        self.gravity_scale = 1.0
        self.friction = 0.8
        
    def apply_gravity(self, delta_time: float = 1.0):
        """Apply gravity to entity"""
        self.velocity.y += GRAVITY * self.gravity_scale * delta_time
        self.velocity.y = min(self.velocity.y, 20)  # Terminal velocity
    
    def apply_friction(self):
        """Apply friction to horizontal movement"""
        self.velocity.x *= self.friction
    
    def update_position(self, delta_time: float = 1.0):
        """Update position based on velocity"""
        self.position.x += self.velocity.x * delta_time
        self.position.y += self.velocity.y * delta_time
        
        # Sync rect with position
        self.rect.x = int(self.position.x + self.hitbox_offset.x)
        self.rect.y = int(self.position.y + self.hitbox_offset.y)
    
    def update(self, delta_time: float = 1.0):
        """Override in subclasses"""
        raise NotImplementedError("Subclasses must implement update()")
    
    def draw(self, screen: pygame.Surface, camera_x: float):
        """Override in subclasses"""
        raise NotImplementedError("Subclasses must implement draw()")
    
    def check_ground_collision(self, platforms: List) -> bool:
        """Check if entity is on ground"""
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        
        # Check game floor
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.position.y = self.rect.y - self.hitbox_offset.y
            self.velocity.y = 0
            return True
        
        # Check platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0 and self.rect.bottom - self.velocity.y <= platform.rect.top + 5:
                    self.rect.bottom = platform.rect.top
                    self.position.y = self.rect.y - self.hitbox_offset.y
                    self.velocity.y = 0
                    return True
        
        return False


class BaseEnemy(Entity):
    """
    Base class for all enemy types
    Implements common enemy behavior patterns
    """
    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__(x, y, width, height)
        
        # Movement
        self.direction = -1  # -1 = left, 1 = right
        self.move_speed = 1.5
        self.start_x = x
        self.patrol_range = 100
        
        # State
        self.is_stomped = False
        self.death_timer = 0
        self.death_animation_duration = 30  # frames
        
        # AI
        self.ai_state = "patrol"  # patrol, chase, idle
        self.turn_at_edges = False  # Goomba=False, Red Koopa=True
    
    def update(self, delta_time: float, platforms: List):
        """Standard enemy update loop"""
        if not self.is_alive:
            self.death_timer += 1
            if self.death_timer > self.death_animation_duration:
                self.is_active = False
            return
        
        # AI Behavior
        self.update_ai()
        
        # Physics
        self.apply_gravity(delta_time)
        self.update_position(delta_time)
        
        # Collision
        self.check_ground_collision(platforms)
        self.check_world_bounds()
    
    def update_ai(self):
        """Basic patrol AI - override for specific behavior"""
        if self.ai_state == "patrol":
            self.velocity.x = self.move_speed * self.direction
            
            # Simple patrol range
            if self.rect.x > self.start_x + self.patrol_range:
                self.direction = -1
            elif self.rect.x < self.start_x - self.patrol_range:
                self.direction = 1
    
    def on_stomped(self):
        """Called when player jumps on enemy"""
        self.is_alive = False
        self.is_stomped = True
        self.velocity.y = -8  # Bounce effect for visual feedback
        self.velocity.x = 0
    
    def on_wall_collision(self):
        """Called when enemy hits wall"""
        self.direction *= -1
        self.velocity.x = 0
    
    def check_edge(self, platforms: List) -> bool:
        """
        Detect if enemy is about to walk off edge
        Used by Red Koopa and other edge-aware enemies
        """
        # Check position ahead of enemy
        check_x = self.rect.x + (self.rect.width * self.direction)
        check_y = self.rect.bottom + 5  # Slightly below feet
        
        # Check ground
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        if check_y >= ground_y:
            return False
        
        # Check platforms
        for platform in platforms:
            if platform.rect.collidepoint(check_x, check_y):
                return False
        
        return True  # No ground ahead = edge!
    
    def check_world_bounds(self):
        """Prevent enemies from going out of bounds"""
        if self.rect.bottom > SCREEN_HEIGHT + 100:
            self.is_alive = False
            self.is_active = False


class CollisionSystem:
    """
    Static class for collision detection and resolution
    Uses AABB (Axis-Aligned Bounding Box) collision
    """
    
    @staticmethod
    def check_aabb(rect_a: pygame.Rect, rect_b: pygame.Rect) -> bool:
        """Basic AABB collision check"""
        return rect_a.colliderect(rect_b)
    
    @staticmethod
    def get_overlap(rect_a: pygame.Rect, rect_b: pygame.Rect) -> Tuple[float, float]:
        """
        Calculate overlap on each axis
        Returns (overlap_x, overlap_y)
        """
        dx = rect_a.centerx - rect_b.centerx
        dy = rect_a.centery - rect_b.centery
        
        overlap_x = (rect_a.width + rect_b.width) / 2 - abs(dx)
        overlap_y = (rect_a.height + rect_b.height) / 2 - abs(dy)
        
        return (overlap_x, overlap_y)
    
    @staticmethod
    def get_collision_normal(rect_a: pygame.Rect, rect_b: pygame.Rect) -> Vector2D:
        """
        Determine collision direction
        Returns normalized vector pointing from B to A
        """
        dx = rect_a.centerx - rect_b.centerx
        dy = rect_a.centery - rect_b.centery
        
        overlap_x, overlap_y = CollisionSystem.get_overlap(rect_a, rect_b)
        
        # Return normal on axis with LEAST penetration
        if overlap_x < overlap_y:
            return Vector2D(1 if dx > 0 else -1, 0)
        else:
            return Vector2D(0, 1 if dy > 0 else -1)
    
    @staticmethod
    def is_stomp(player_rect: pygame.Rect, player_velocity_y: float, 
                 enemy_rect: pygame.Rect) -> bool:
        """
        Determine if player is stomping enemy (jumping on top)
        
        Conditions:
        1. Player moving downward
        2. Player's bottom above enemy's center
        3. Collision from above
        """
        if player_velocity_y <= 0:
            return False
        
        # Player's feet must be above enemy's center
        if player_rect.bottom > enemy_rect.centery + 5:
            return False
        
        return True
    
    @staticmethod
    def resolve_platform_collision(entity: Entity, platform_rect: pygame.Rect):
        """
        Resolve collision between entity and platform
        Pushes entity out of platform on shortest axis
        """
        if not entity.rect.colliderect(platform_rect):
            return
        
        dx = entity.rect.centerx - platform_rect.centerx
        dy = entity.rect.centery - platform_rect.centery
        
        overlap_x, overlap_y = CollisionSystem.get_overlap(entity.rect, platform_rect)
        
        if overlap_x < overlap_y:
            # Horizontal collision
            if dx > 0:
                entity.rect.x += overlap_x
                entity.position.x = entity.rect.x
            else:
                entity.rect.x -= overlap_x
                entity.position.x = entity.rect.x
            entity.velocity.x = 0
            
            # Enemy wall behavior
            if isinstance(entity, BaseEnemy):
                entity.on_wall_collision()
        else:
            # Vertical collision
            if dy > 0:
                # Landing on top
                entity.rect.y += overlap_y
                entity.position.y = entity.rect.y
                entity.velocity.y = 0
            else:
                # Hitting from below
                entity.rect.y -= overlap_y
                entity.position.y = entity.rect.y
                entity.velocity.y = 0


# Export classes
__all__ = ['Entity', 'BaseEnemy', 'CollisionSystem', 'Vector2D']
