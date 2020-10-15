import pygame

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
    range_ = 0
    last_attack = 0
    attack_rate = 0.0
    
    def __init__(self, x_ord, y_ord, kind):
        pass
        
    # FOR FUTURE: Move generalized draw_tower here.
    def draw_tower(self):
        pass

    def draw_attack(self):
        pass

class Fire_Tower(Tower):
    L0_path = image_path + "FireTowerL0.gif"
    value = 100
    damage = 1
    range_ = 200
    attack_rate = .5
    kind = "Fire"

    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord

    def draw_tower(self, window):
        L0_tower_image = pygame.image.load(self.L0_path)
        window.blit(L0_tower_image, (self.x, self.y))
        
    
    def draw_attack(self):
        pass

class Ice_Tower(Tower):
    L0_path = image_path + "IceTowerL0.gif"
    damage = 2
    range = 500
    attack_rate = 5
    slow_affect = 2
    value = 150
    kind = "Ice"

    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord

    def draw_tower(self, window):
        L0_tower_image = pygame.image.load(self.L0_path)
        window.blit(L0_tower_image, (self.x, self.y))

    def draw_attack(self):
        pass

class Arrow_Tower(Tower):
    L0_path = image_path + "ArrowTowerL0.gif"
    damage = 5
    range = 600
    attack_rate = 2
    crit_chance = .05
    value = 200
    kind = "Arrow"

    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord


    def draw_tower(self, window):
        L0_tower_image = pygame.image.load(self.L0_path)
        window.blit(L0_tower_image, (self.x, self.y))

    def draw_attack(self):
        pass

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