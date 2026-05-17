import pygame
from pygame.math import Vector2

pygame.init()

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, size, textures: tuple , speed: int):
        super().__init__()
        self.image = pygame.Surface(size)
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.speed = speed
    
    def update(self):
        pass
        
        
class Player(Entity):
        def __init__(self):
            super().__init__()
            
        
class Object(pygame.sprite.Sprite):
    def __init__(self, texture, size: tuple, position: tuple):
        super().__init__()
        self.texture = texture
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        
        
class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self,entity):
        return entity.rect.move(self.rect.topleft)
        
    def draw(self, screen_h, screen_w,target):
        x = target.rect.centerx - screen_w // 2
        y = target.rect.centery - screen_h // 2
        self.rect.topleft = (x, y)
        
        
class Interface(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, size: tuple):
        super().__init__()
        self.x = x
        self.y = y
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect()
        
    def event(self, position: tuple) -> bool:
         return self.rect.collidepoint(position)
         

class Joystick:
    def __init__(self, base_radius, color):
        self.base_radius = base_radius
        self.knob_radius = base_radius // 2
        self.base_pos = Vector2(0,0)
        self.knob_pos = Vector2(0,0)
        self.direction = Vector2(0,0)
        self.finger_id = None
        
        self.base = pygame.Surface((base_radius * 2,base_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.base,color,(base_radius,base_radius),base_radius)
        
        self.knob = pygame.Surface((base_radius, base_radius),pygame.SRCALPHA)
        pygame.draw.circle(self.knob,color,(self.knob_radius,self.knob_radius),self.knob_radius)
        
    def event(self, event, screen_width,screen_height):
        if event.type == pygame.FINGERDOWN and self.finger_id is None:
            if event.x < 0.5:
                self.finger_id = event.finger_id
                self.base_pos = Vector2(event.x * screen_width, event.y * screen_height)
                self.knob_pos = self.base_pos
                
        elif event.type == pygame.FINGERMOTION:
            if event.finger_id == self.finger_id:
                self.direction = Vector2(event.x *screen_width, event.y * screen_height) - self.base_pos
                
                #мертвая зона
            if self.direction.length() < self.knob_radius // 4:
                self.direction *= 0
                    
               #ограничиваем стик радиусом
            elif self.direction.length() > self.base_radius:
                self.direction = self.direction.scale_to_length(self.base_radius)
                self.knob_pos = self.direction
                 
            else:
               self.knob_pos = self.direction + self.base_pos
                    
        elif event.type == pygame.FINGERUP:
             if event.finger_id == self.finger_id:
                self.finger_id = None
                self.base_pos = Vector2(0,0)
                self.knob_pos = Vector2(0,0)
            
    def draw(self, surface, position):
        if self.finger_id is not None:
            surface.blit(self.base, self.base_pos - Vector2(self.base_radius))
            surface.blit(self.knob, self.knob_pos - Vector2(self.knob_radius))
        

# служебные функции
def converter(images):
    for image in images:
        images[image] = images[image].convert_alpha()