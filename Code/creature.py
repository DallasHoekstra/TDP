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
    maxhealth = 0
    health = 0
    attack = 0
    move_speed = 0
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
                pygame.draw.rect(window, (255,0,0), (self.x, self.y - 5, int((self.width/self.maxhealth)*self.health) + 1, 5))
                        
    def set_path(self, path):
        self.path = path.copy() 

    def draw_attack(self):
        pass

    def move(self):
        if len(self.path) > 0:
            x_diff = self.path[-1][0] - self.x
            y_diff = self.path[-1][1] - self.y
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
                self.path.pop()
        
class Skeleton(Creature):
    L0_Path = image_path + "L0Skeleton.gif"
    maxhealth = 25
    health = 25
    attack = 5
    move_speed = 1
    foe = True
    life_damage = 1
    value = 10

        