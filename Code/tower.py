import pygame
import math
import random

# FOR FUTURE: Create functionality to set path dynamically based on install or relative to files
base_path = "c:/Users/Anonymous/Desktop/PythonProjects/TowerDefenseProject/"
image_path = base_path + "Assets/Images/"
audio_path = base_path + "Assets/Audio/"

class Tower():
    # Tower properties
    x, y = 0, 0
    kind = ""
    value = 0
    damage = 0
    damage_type = ""
    range_ = 0
    

    # Last attack should assume a 30 fps rate
    last_attack = 0
    attack_rate = 0

    
    def __init__(self, x_ord, y_ord, kind):
        self.attack_objects = []
        pass
        
    # FOR FUTURE: Move generalized draw_tower here.
    def draw_tower(self):
        pass

    def draw_attack(self, window):
        pass

    # FOR FUTURE: add status affects (frozen, etc) that prevent towers from firing to this method
    def can_attack(self, timestamp):
        # timestamp should be in 30ths of a second. if framerate = 60, timestamp = framerate//2, etc)
        if self.attack_rate > 0:
            return (timestamp - self.last_attack)/self.attack_rate > 1
        else:
            return False

    def attack(self, timestamp):
        pass

class Fire_Tower(Tower):
    # FOR FUTURE: future tower level branches will allow for Fire_Attack objects to attach themselves to a target
    # and move with the target dealing damage as they go. 
    
    L0_path = image_path + "FireTowerL0.gif"
    L0_tower_image = pygame.image.load(L0_path)
    value = 100
    damage = 1
    damage_type = "Fire"
    range_ = 100
    attack_rate = 15
    kind = "Fire"
    dimension = (L0_tower_image.get_width(), L0_tower_image.get_height())

    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord
        self.targets = []
        self.attack_objects = []

    def draw_tower(self, window):
        L0_tower_image = pygame.image.load(self.L0_path)
        window.blit(L0_tower_image, (self.x, self.y))
        
    # Draw the attack animation, not the attack object
    def draw_attack(self, window):
        if len(self.attack_objects) > 0:
            for attack_object in self.attack_objects:
                attack_object.draw(window)

    # Attack objects are centered on the tower and the attack functionality is carried out by the tower
    def attack(self, existing_Creatures, timestamp):
        if len(existing_Creatures) > 0:            
            for creature in existing_Creatures:
                if math.sqrt(math.pow((creature.x - self.x), 2) + math.pow((creature.y - self.y), 2)) < self.range_:                    
                    self.attack_objects.append(Fire_Attack(self.x, self.y, self.range_, self.damage, self.damage_type))
                    for attack in self.attack_objects:
                        attack.hit(creature)
                        attack.remove_attack = True
                    self.last_attack = timestamp
                
class Ice_Tower(Tower):
    L0_path = image_path + "IceTowerL0.gif"
    range_ = 500
    attack_rate = 150
    slow_affect = 2
    value = 150
    kind = "Ice"

    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord
        self.attack_objects = []

    def draw_tower(self, window):
        L0_tower_image = pygame.image.load(self.L0_path)
        window.blit(L0_tower_image, (self.x, self.y))

    def attack(self, existing_Creatures, timestamp):
        if len(existing_Creatures) > 0:
            for creature in existing_Creatures:
                if abs(creature.x - self.x) and abs(creature.y - self.y) < self.range_:                    
                    self.attack_objects.append(Ice_Attack(self.x, self.y, [creature]))
                    self.last_attack = timestamp
                    break

    def draw_attack(self, window):
        pass

class Arrow_Tower(Tower):
    L0_path = image_path + "ArrowTowerL0.gif"
    range_ = 600
    attack_rate = 30
    value = 200
    kind = "Arrow"

    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord
        self.attack_objects = []

    def draw_tower(self, window):
        L0_tower_image = pygame.image.load(self.L0_path)
        window.blit(L0_tower_image, (self.x, self.y))

    def draw_attack(self, window):
        pass

    def attack(self, existing_Creatures, timestamp):
        if len(existing_Creatures) > 0:
            for creature in existing_Creatures:
                if abs(creature.x - self.x) and abs(creature.y - self.y) < self.range_:                    
                    self.attack_objects.append(Arrow_Attack(self.x, self.y, [creature]))
                    self.last_attack = timestamp
                    break

class Wall(Tower):
    L0_path = image_path + "WallL0.gif"
    damage = 0
    range = 0
    attack_rate = 0
    value = 10
    kind = "Wall"

    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord

    def draw_tower(self, window):
        L0_tower_image = pygame.image.load(self.L0_path)
        window.blit(L0_tower_image, (self.x, self.y))

# ----------------- Attack Class -------------------------------------------------------------------
class Attack():
    # FOR FUTURE: maybe create a class for all objects that use assets? Some other way of inserting 
    # the base file paths other than manually adding it to each code file?
    image_path = image_path + "Default_Attack.gif"
    attack_image = pygame.image.load(image_path)
    dimension = (attack_image.get_width, attack_image.get_height)
    x = 0
    y = 0
    damage = 0
    damage_Type = ""
    move_speed = 0
    remove_attack = False

    # FOR FUTURE: add animations/gifs for when attacks hit the target
    # impact_animation

    def __init__(self):
        self.targets = []

    def move(self):
        pass

    def draw(self, window):
        window.blit(self.attack_image, (self.x - math.floor(self.dimension[0]/2), self.y - math.floor(self.dimension[1]/2)))

    def hit(self):
        pass

class Fire_Attack(Attack):
    range_ = 0
    image_path = image_path + "Fire_Attack.gif"
    attack_image = pygame.image.load(image_path)
    dimension = (attack_image.get_width(), attack_image.get_height())
    attack_image.set_alpha(100)

    def __init__(self, x_ord, y_ord, range_, damage, damage_type):
        self.x = x_ord
        self.y = y_ord
        self.range_ = range_
        self.damage = damage
        self.damage_Type = damage_type
        self.move_Speed = 0

    def hit(self, creature):
        # FOR FUTURE: possibly add on-hit animation that is different from the attack animation?
    
        # apply damage 
        # FOR FUTURE: work out how to handle vulnerabilities, resistances, immunities, etc
        creature.health -= self.damage

class Ice_Attack(Attack):
    image_path = image_path + "Ice_Shard.gif"
    attack_image = pygame.image.load(image_path)
    dimension = (attack_image.get_width(), attack_image.get_height())
    attack_image.set_alpha(255)
    damage = 5
    damage_Type = "Ice"
    move_speed = 15

    # Leaving target in the plural for future implementation of bouncing attacks
    # Interpret as target(s)
    def __init__(self, x_ord, y_ord, targets):
        self.x = x_ord
        self.y = y_ord
        self.targets = targets

    def move(self):
        if len(self.targets) > 0:
            x_diff = self.targets[-1].x - self.x
            y_diff = self.targets[-1].y - self.y
            if abs(x_diff) > self.move_speed or abs(y_diff) > self.move_speed:
                if x_diff > 0:
                    self.x += self.move_speed
                else:
                    self.x -= self.move_speed
                if y_diff > 0:
                    self.y += self.move_speed
                else:
                    self.y -= self. move_speed
            else:
                self.x, self.y = self.targets[-1].x, self.targets[-1].y
                self.hit()
                self.targets.pop()
                if len(self.targets) == 0:
                    self.remove_attack = True

    def hit(self):
        self.targets[-1].health -= self.damage
        #self.targets[-1].status

class Arrow_Attack(Attack):
    image_path = image_path + "Arrow.gif"
    attack_image = pygame.image.load(image_path)
    dimension = (attack_image.get_width(), attack_image.get_height())
    attack_image.set_alpha(255)
    damage = 5
    crit_chance = .05
    damage_Type = "Ice"
    move_speed = 20
    crit_multiplier = 2

    def __init__(self, x_ord, y_ord, target):
        self.x = x_ord
        self.y = y_ord
        self.targets = target

    def move(self):
        if len(self.targets) > 0:
            x_diff = self.targets[-1].x - self.x
            y_diff = self.targets[-1].y - self.y
            if abs(x_diff) > self.move_speed or abs(y_diff) > self.move_speed:
                if x_diff > 0:
                    self.x += self.move_speed
                else:
                    self.x -= self.move_speed
                if y_diff > 0:
                    self.y += self.move_speed
                else:
                    self.y -= self. move_speed
            else:
                self.x, self.y = self.targets[-1].x, self.targets[-1].y
                self.hit()
                self.targets.pop()
                if len(self.targets) == 0:
                    self.remove_attack = True

    def hit(self):
        if math.floor(self.crit_chance * random.randrange(1, 20, 1) >= 1):
            self.targets[-1].health -= self.crit_multiplier*self.damage
        else:
            self.targets[-1].health -= self.damage
