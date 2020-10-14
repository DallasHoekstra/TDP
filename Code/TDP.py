import pygame

framerate = 60

# FOR FUTURE: Create functionality that dynamically adjusts to playing screen size and full/partial window
window_width = 1000
window_height = 800

# FOR FUTURE: Adjust tower size to playing screen size
tower_width = 50
tower_height = 50


# FOR FUTURE: Create functionality to set path dynamically based on install or relative to files
base_path = "c:/Users/Anonymous/Desktop/PythonProjects/TowerDefenseProject/"
image_path = base_path + "Assets/Images/"
audio_path = base_path + "Assets/Audio/"

# For Future: Replace with images
tower_graphic_list = {"Fire":(255,0,0), "Ice":(0,0,255)}

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

class Ice_Tower(Tower):
    L0_path = image_path + "IceTowerL0.gif"

    def __init__(self, x_ord, y_ord):
        self.x = x_ord
        self.y = y_ord
        self.damage = 2
        self.range = 500
        self.attack_rate = 5
        self.slow_affect = 2
    
    def draw_tower(self, window):
        L0_tower_image = pygame.image.load(self.L0_path)
        window.blit(L0_tower_image, (self.x, self.y))

    def draw_attack(self):
        pass

def draw_interface():
    pass

def purchase_Tower(kind, existing_Towers, position):
    if kind == "Fire":
        new_Tower = Fire_Tower(position[0], position[1])
        existing_Towers.append(new_Tower)
    elif kind == "Ice":
        new_Tower = Ice_Tower(position[0], position[1])
        existing_Towers.append(new_Tower)
    return ""

def create_combat_interface(): 
    # The list to store the interface objects: buttons, etc
    fire_tower_button = (pygame.Rect(0, 50, 50, 50), (255, 0, 0), "Fire")
    ice_tower_button = (pygame.Rect(100, 50, 50, 50), (0, 0, 255), "Ice")
    return (fire_tower_button, ice_tower_button)


def main(window):
    run = True
    in_combat = True
    interface_created = False
    combat_interface = create_combat_interface()
    prospective_Tower = ""

    # A list to hold the purchased tower objects FOR FUTURE: Is there a better way to manage this? Needs to be on a level by level basis
    existing_Towers = []

    window.fill((0,0,0))
    while run:
        clock = pygame.time.Clock()
        clock.tick(framerate)

        # Window drawing. FOR FUTURE move to seperate method

        # Draw background onto the screen
        window.fill((0,0,0))

        # Draw the combat interface
        for button, color, kind in combat_interface:
            pygame.draw.rect(window, color, button)

        # Draw the towers
        for tower in existing_Towers:
            tower.draw_tower(window)
        
        # Draw prospective purchased tower
        if prospective_Tower != "":
            mouse_position = pygame.mouse.get_pos()
            pygame.draw.rect(window, tower_graphic_list[prospective_Tower], (mouse_position[0] - tower_width//2, mouse_position[1] - tower_height//2, tower_width, tower_height))


        # Draw the red circle
        red_circle_path = "C:/Users/Anonymous/Desktop/PythonProjects/TowerDefenseProject/Assets/Images/RedCircle.jpg"
        red_circle = pygame.image.load(red_circle_path)
        window.blit(red_circle, (0,0))

        # Event triggers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Player trying to place a tower
                if prospective_Tower != "":
                    prospective_Tower = purchase_Tower(prospective_Tower, existing_Towers, event.pos)

                else:
                    mouse_position = event.pos

                    # Check to see if player is using combat interface
                    for button, _, kind in combat_interface:
                        if button.collidepoint(mouse_position):
                            prospective_Tower = kind

                    # FOR FUTURE: 
                    # Check if player is selecting a hero
                    # Check if player is selecting a tower
                    # Check if player is selecting an enemy 
                    # Check if player is selecting something else
                            
                        





        pygame.display.update()

    pygame.display.quit()


main(window) 