import pygame

# FOR FUTURE: Create functionality to set path dynamically based on install or relative to files
base_path = "c:/Users/Anonymous/Desktop/PythonProjects/TowerDefenseProject/"
image_path = base_path + "Assets/Images/"
audio_path = base_path + "Assets/Audio/"

class Creature():
    x = 0
    y = 0
    health = 0
    attack = 0
    speed = 0
    
    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord

    def draw_creature(self, window):
        pass

    def draw_attack(self):
        pass

class Skeleton(Creature):
    L0_path = image_path + "L0Skeleton.gif"
    health = 25
    attack = 5
    speed = 10

    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord
        
    def draw_creature(self, window):
        L0_skeleton_image = pygame.image.load(self.L0_path)
        window.blit(L0_skeleton_image, (self.x, self.y))