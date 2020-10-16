import pygame

# FOR FUTURE: Create functionality to set path dynamically based on install or relative to files
base_path = "c:/Users/Anonymous/Desktop/PythonProjects/TowerDefenseProject/"
image_path = base_path + "Assets/Images/"
audio_path = base_path + "Assets/Audio/"

class Creature():
    L0_Path = ""
    L0_Image = ""
    x = 0
    y = 0
    health = 0
    attack = 0
    speed = 0
    foe = False
    path = []
    width = 0
    height = 0
    visible = False
    
    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord
        if self.L0_Path != "":
            self.L0_Image = pygame.image.load(self.L0_Path)
            self.width, self.height = self.L0_Image.get_rect().size

    def draw_creature(self, window):
        
        if not self.visible:
            window_dimensions = window.get_size()        
            if self.x > 0 and self.x < window_dimensions[0]:
                if self.y > 0 and self.y < window_dimensions[1]:
                    self.visible = True
        else:
            if self.L0_Image != "":
                window.blit(self.L0_Image, (self.x, self.y))
            

    def draw_attack(self):
        pass

    def set_path(self, path):
        self.path = path

    def move(self):
        pass

class Skeleton(Creature):
    L0_Path = image_path + "L0Skeleton.gif"
    health = 25
    attack = 5
    speed = 10
    foe = True
    life_damage = 1

        