import pygame

framerate = 60

# FOR FUTURE: Create functionality that dynamically adjusts to playing screen size and full/partial window
window_width = 1000
window_height = 800

# FOR FUTURE: Create functionality to set path dynamically based on install or relative to files
base_path = "C:/Users/Anonymous/Desktop/PythonProjects/TowerDefenseGame"
image_path = base_path + "/Assets/Images"
audio_path = base_path + "Assets/Audio"


# Create the game screen
window = pygame.display.set_mode((window_width, window_height))

class Creature():
    x = 0
    y = 0

    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord

class Tower():
    # Tower properties
    x, y = 0, 0
    tower_kind_list = ["Fire", "Ice", "Arrow", "Wall"]
    tower_value_dict = {"Fire":100, "Ice":150, "Arrow":200, "Wall":10}
    tower_kind = ""
    value = 0
    damage = 0
    range_ = 0
    last_attack = 0
    attack_rate = 0.0
    
    def __init__(self, x_ord, y_ord, kind):
        self.x = x_ord
        self.y = y_ord
        self.tower_kind = kind
        self.value = self.tower_value_dict[kind]
        
    def draw_tower(self):
        pass

    def draw_attack(self):
        pass



class Fire_Tower(Tower):
    L0_path = image_path + "FireTowerL0.gif"


    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord
        self.damage = 1
        self.range_ = 200
        self.attack_rate = .5


    def draw_tower(self, window):
        L0_tower_image = pygame.image.load(self.L0_path)
        window.blit(L0_tower_image, (self.x, self.y))
        
    
    def draw_attack(self):
        pass

def draw_interface():
    pass

def create_combat_interface(): 
    # The list to store the interface objects: buttons, etc
    fire_tower_button = (pygame.Rect(0, 50, 50, 50), (255, 0, 0))
    ice_tower_button = (pygame.Rect(100, 50, 50, 50), (0, 0, 255))
    return (fire_tower_button, ice_tower_button)


def main(window):
    run = True
    in_combat = True
    interface_created = False
    combat_interface = create_combat_interface()
    window.fill((0,0,0))
    while run:
        clock = pygame.time.Clock()
        clock.tick(framerate)

        # Window drawing. FOR FUTURE move to seperate method

        # Draw the combat interface
        for button, color in combat_interface:
            pygame.draw.rect(window, color, button)
        

        # Draw the red circle
        red_circle_path = "C:/Users/Anonymous/Desktop/PythonProjects/TowerDefenseProject/Assets/Images/RedCircle.jpg"
        red_circle = pygame.image.load(red_circle_path)
        window.blit(red_circle, (0,0))

        # Event triggers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False





        pygame.display.update()

    pygame.display.quit()


main(window) 