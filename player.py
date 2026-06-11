from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SHOOT_SPEED, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from circleshape import CircleShape
import pygame
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y,):
        super().__init__(x, y, PLAYER_RADIUS)

        #load main sprite and convert alpha
        self.sprite_sheet = pygame.image.load("assets/spaceships.png").convert_alpha()
        temp_sheet = pygame.image.load ("assets/thruster.png").convert_alpha()
        self.thruster_sheet = []
        #getting frames from thruster sprite sheet
        for i in range(5):
            raw_frame = temp_sheet.subsurface(pygame.Rect(i * 8, 0, 8, 8))
            #scale it to 24x24
            scaled_frame = pygame.transform.scale(raw_frame, (24, 24))
            self.thruster_sheet.append(scaled_frame)
        #extract specefic sprite from the sprite sheet
        self.ship_image = self.sprite_sheet.subsurface(pygame.Rect(0, 0, 48, 48))
        self.rotation = 0
        self.cooldown = 0
        self.thruster_index = 0
        self.animation_timer = 0
        
        
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c] 

    def draw(self, screen):
        ##rotate ship image
        rotated_ship = pygame.transform.rotate(self.ship_image, -self.rotation)
        #get rectangle for rotated image and center it on the player position
        ship_rect = rotated_ship.get_rect(center=self.position)
        
        #thrusters
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            current_frame = self.thruster_sheet[self.thruster_index]
            #rotate thruster frame to match ship rotation
            rotated_thruster = pygame.transform.rotate(current_frame, -self.rotation + 180)
            # put thruster slightly behind ship
            thruster_offset = pygame.Vector2(0, -24).rotate(self.rotation)
            thruster_rect = rotated_thruster.get_rect(center=self.position + thruster_offset)
            #draw thruster
            screen.blit(rotated_thruster, thruster_rect)
            #draw ship
        screen.blit(rotated_ship, ship_rect)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        #animation timer for thrusters
        self.animation_timer += dt
        if self.animation_timer > 0.1: #swap frames every 0.1 seconds
            self.thruster_index = (self.thruster_index + 1) % len(self.thruster_sheet)
            self.animation_timer = 0

        self.cooldown -= dt

        if keys[pygame.K_SPACE]:
            shot = self.shoot()
        
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.cooldown > 0:
            return None
        self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = forward * PLAYER_SHOOT_SPEED
        self.shoot_sound.play()
        return Shot(self.position.x, self.position.y, velocity)
        

