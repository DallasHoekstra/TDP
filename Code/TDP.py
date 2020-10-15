import pygame
import tower as twr
import creature as crt

framerate = 60

# FOR FUTURE: Create functionality that dynamically adjusts to playing screen size and full/partial window
window_width = 1000
window_height = 800

# FOR FUTURE: Adjust tower size to playing screen size
# Set to be equal to the .gif files for more accurate placement
tower_width = 42
tower_height = 40


# FOR FUTURE: Create functionality to set path dynamically based on install or relative to files
base_path = "c:/Users/Anonymous/Desktop/PythonProjects/TowerDefenseProject/"
image_path = base_path + "Assets/Images/"
audio_path = base_path + "Assets/Audio/"

# For Future: Replace with images
tower_graphic_list = {"Fire":(255,0,0), "Ice":(0,0,255), "Arrow":(100,100,0), "Wall":(100,100,100)}

# Create the game screen
window = pygame.display.set_mode((window_width, window_height))

pygame.font.init()

# global variable for managing the fact that it needs to be changed by multiple functions. 
# FOR FUTURE: Figure out a more elegant way to handle this. The Gold variable doesn't make sense outside of a level context
global gold
gold = 0

def draw_interface():
    pass

def purchase_Tower(kind, existing_Towers, position, gold):
    for tower in existing_Towers:
        if (abs(tower.x - position[0]) < (tower_width + 1)) and (abs(tower.y - position[1]) < (tower_height + 1)):
            # play_sound("collision")
            return (kind, gold)
    # FOR FUTURE: Create loop instead of extended if-elif block?
    if kind == "Fire":
        if gold >= twr.Fire_Tower.value:            
            gold -= twr.Fire_Tower.value
            new_Tower = twr.Fire_Tower(position[0], position[1])
            existing_Towers.append(new_Tower)
        else:
            # play_sound("poverty")
            return (kind, gold)
            
    elif kind == "Ice":
        if gold >= twr.Ice_Tower.value:
            gold -= twr.Ice_Tower.value
            new_Tower = twr.Ice_Tower(position[0], position[1])
            existing_Towers.append(new_Tower)
        else:
            # play_sound("poverty")
            return (kind, gold)

    elif kind == "Arrow":
        if gold >= twr.Arrow_Tower.value:
            gold -= twr.Arrow_Tower.value
            new_Tower = twr.Arrow_Tower(position[0], position[1])
            existing_Towers.append(new_Tower)
        else:
            # play_sound("poverty")
            return (kind, gold)

    elif kind == "Wall":
        if gold >= twr.Wall.value:
            gold -= twr.Wall.value
            new_Tower = twr.Wall(position[0], position[1])
            existing_Towers.append(new_Tower)
        else:
            # play_sound("poverty")
            return (kind, gold)
    return ("", gold)

def spawn_Creatures(kind, quantity, spawn_center, existing_Creatures):
    if kind == "Skeleton":
        for _ in range(quantity):
            spawn_x, spawn_y = spawn_center[0] + _, spawn_center[1] + _
            skeleton = crt.Skeleton(spawn_x, spawn_y)
            existing_Creatures.append(skeleton)

def create_combat_interface(): 
    # The list to store the interface objects: buttons, etc
    fire_tower_button = (pygame.Rect(0, 50, tower_width, tower_height), (255, 0, 0), "Fire")
    ice_tower_button = (pygame.Rect(100, 50, tower_width, tower_height), (0, 0, 255), "Ice")
    arrow_tower_button = (pygame.Rect(200, 50, tower_width, tower_height), (100, 100, 0), "Arrow")
    wall_button = (pygame.Rect(300, 50, tower_width, tower_height), (100, 100, 100), "Wall")
    return (fire_tower_button, ice_tower_button, arrow_tower_button, wall_button)


def main(window):
    run = True
    in_combat = True
    interface_created = False
    combat_interface = create_combat_interface()
    prospective_Tower = ""
    interface_font = pygame.font.SysFont("comicsans", 40, bold=True)
    game_paused = False

    # Per-Level properties. 
    # FOR FUTURE: Create separate class to contain these properties? 
    starting_gold = 500
    enemy_path_1 = []
    enemy_path_2 = []
    enemy_list = [("Skeleton", 1, (500,500))]
    wave_timer = [5]
    # backgroundImage = 
    wave = 0
    time_past = 0

    global gold
    gold = starting_gold



    # A list to hold the purchased tower objects 
    # FOR FUTURE: Is there a better way to manage this? Needs to be on a level by level basis
    existing_Towers = []

    # A list to hold the existing creatures
    # FOR FUTURE: Is there a better way to manage this? Needs to be on a level by level basis
    existing_Creatures = []

    window.fill((0,0,0))
    while run:
        clock = pygame.time.Clock()
        clock.tick(framerate)

        if not game_paused:
            time_past += 1
        if wave < len(enemy_list):
            if wave_timer[wave]*framerate < time_past:
    
                wave_makeup = enemy_list[wave]
                spawn_Creatures(wave_makeup[0], wave_makeup[1], wave_makeup[2], existing_Creatures) 
                wave += 1

        # Window drawing. 
        # FOR FUTURE move to seperate method

        # Draw background onto the screen
        window.fill((0,0,0))

        # Draw the combat interface
        for button, color, kind in combat_interface:
            pygame.draw.rect(window, color, button)
        
        # Draw gold quantity
        gold_amount_text = interface_font.render("Gold: " + str(gold), 1, (255, 255, 0))
        window.blit(gold_amount_text, (600, 100))
        time_past_text = interface_font.render("Time: " + str(time_past//60), 1, (255,255,255))
        window.blit(time_past_text, (600, 150))

        # Draw the towers
        for tower in existing_Towers:
            tower.draw_tower(window)

        # Draw the creatures
        for creature in existing_Creatures:
            creature.draw_creature(window)
        
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
                    tower_position = (event.pos[0] - tower_width//2, event.pos[1] - tower_height//2)
                    prospective_Tower, gold = purchase_Tower(prospective_Tower, existing_Towers, tower_position, gold)

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