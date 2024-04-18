import pygame
from math import atan2, degrees

class miner(pygame.sprite.Sprite): #Creates a movable player
    def __init__(self, x, y, velocity, size): #Initializes the player
        super().__init__()
        self.idleAnimations = ["Textures/Characters/Miner/miner_idle_1.png", "Textures/Characters/Miner/miner_idle_2.png"]
        self.flippedAnimations = ["Textures/Characters/Miner/miner_idle_1_flip.png", "Textures/Characters/Miner/miner_idle_2_flip.png"]
        self.animations = [self.flippedAnimations, self.idleAnimations]
        self.velocity = velocity
        self.facingDirection = 1 #1 = Facing to Right, 0 = Facing to Left
        self.currentAnimation = 0
        self.size = size
        self.image = pygame.image.load(self.animations[self.facingDirection][self.currentAnimation]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60 * size, 60 * size))
        self.rect = self.image.get_rect(center = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 3

    def update(self, dx, dy): #Allows the player to move
        self.rect.x += dx * self.velocity
        self.rect.y -= dy * self.velocity
        
    def animation(self, dx, dy, time, flip): #Sorts out animations
        if dx < 0 and self.facingDirection == 1 and flip:
            self.facingDirection = 0

        if dx > 0 and self.facingDirection == 0 and flip:
            self.facingDirection = 1

        if (abs(dx) + abs(dy) == 0 and time == 30) or (abs(dx) + abs(dy) != 0 and time % 5 == 1):
            if self.currentAnimation == 0:
                self.currentAnimation = 1
            else:
                self.currentAnimation = 0

        self.image = pygame.image.load(self.animations[self.facingDirection][self.currentAnimation]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60 * self.size, 60 * self.size))
        self.mask = pygame.mask.from_surface(self.image)

    def collide(self):
        if self.facingDirection:
            self.rect.x += self.velocity
            self.rect.y += 1
        else:
            self.rect.x -= self.velocity
            self.rect.y += 1

class Drill(pygame.sprite.Sprite):
  def __init__(self, x, y):
    self.originalImage = pygame.image.load("Textures/Characters/Miner/Drill_1.png").convert_alpha() #Create an image to rotate from
    self.image = self.originalImage #General initializing stuff
    self.pos = (x, y)
    self.rect = self.image.get_rect(center = self.pos)

  def update(self, targetPos):
    xDist = targetPos[0] - self.rect.x #Calculate difference in x
    yDist = -(targetPos[1] - self.rect.y) #Calculate difference in y
    angle = degrees(atan2(yDist, xDist)) #Calculate angle between targetPos and drill

    self.image = pygame.transform.rotate(self.originalImage, angle - 180) #Rotates around the center
    self.rect = self.image.get_rect(center = self.pos)