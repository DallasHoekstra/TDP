import pygame
import tower as twr
import creature as crt
import math

# FOR FUTURE: add option to alter the framerate? Reasons?
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

def spawn_Creatures(kind, quantity, spawn_center, path, existing_Creatures):
    if kind == "Skeleton":
        for counter in range(quantity):
            # FOR FUTURE: edit offsets to use the dimensions of the creatures image
            x_offset = 18
            if (counter % 2) == 1:
                x_offset = x_offset * -1
            y_offset = 22

            spawn_x, spawn_y = spawn_center[0], spawn_center[1]
            skeleton = crt.Skeleton(spawn_x + x_offset, spawn_y - y_offset*counter)
            skeleton.set_path(path)
            existing_Creatures.append(skeleton)

def create_combat_interface(): 
    combat_interface_font = pygame.font.SysFont("comicsans", 20, bold=True)

    # FOR FUTURE: this won't re-create the window height and width if the size changes. Add dynamic functionality
    window_width, window_height = window.get_size()
    # Purchase Container, Wave Info Container, Play/Pause Container, Health Container
    # (start_x, start_y, %window_width_to_right, %window_height_down)
    container_dimensions_percent = [(0, 0, .1, .33), (.25, 0, .5, .05), (.95, 0, .05, .05), (.5, .95, .1, .05)]
    container_dimensions = []
    for container in container_dimensions_percent:
        container_dimensions.append((container[0]*window_width, container[1]* window_height, container[2]*window_width, container[3]*window_height))
            

    
    # The list to store the interface objects: buttons, etc

    # Tower purchasing buttons
    tower_start = container_dimensions[0]
    fire_tower_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 10, tower_width, tower_height), (255, 0, 0), "Fire")
    ice_tower_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 60, tower_width, tower_height), (0, 0, 255), "Ice")
    arrow_tower_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 110, tower_width, tower_height), (100, 100, 0), "Arrow")
    wall_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 160, tower_width, tower_height), (100, 100, 100), "Wall")
    purchase_Container = [fire_tower_button, ice_tower_button, arrow_tower_button, wall_button]

    # Level data
    data_start = container_dimensions[1]
    # gold_amount_text = combat_interface_font.render("Gold: 0", 1, (255, 255, 0))
    # time_past_text = combat_interface_font.render("Time: 0", 1, (255,255,255))
    # current_wave_text = combat_interface_font.render("Wave: 0", 1, (255,255,255))
    text_Positions = [(data_start[0] + 10, data_start[1] + 10), (data_start[0] + int(data_start[2]*.33), data_start[1] + 10), 
                        (data_start[0] + int(data_start[2]*.66), data_start[1] + 10)]
    text_Values = ["Gold: ", "Time: ", "Wave: "]
    text_Colors = [(255,255,0), (255,255,255), (255,255,255)]


    text_Container = []
    for counter in range(len(text_Positions)):
        text_Container.append((text_Positions[counter], text_Values[counter], text_Colors[counter]))

    # Game flow control container
    control_start = container_dimensions[2]
    play_button = (pygame.Rect(control_start[0] + 10, control_start[1] + 10, tower_width, tower_height), (255, 125, 125), "PLAY")
    pause_button = (pygame.Rect(control_start[0] + 10, control_start[1] + 60, tower_width, tower_height), (125, 125, 255), "PAUSE")
    control_Container = (play_button, pause_button)

    # Health container
    health_start = container_dimensions[3]
    health_Container = [((health_start[0] + 10, health_start[1] + 10), "Health: ", (255, 0, 0))]

    return (combat_interface_font, text_Container, control_Container, purchase_Container, health_Container)








def level_one(window):
    run = True
    in_combat = True
    combat_interface = create_combat_interface()
    combat_interface_font = combat_interface[0]
    prospective_Tower = ""

    # FOR FUTURE: clean up attack handling so that orphaned attacks don't occur. Relevant once a sell feature is created
    orphaned_attacks = []

    # FOR FUTURE: possibly add skills that alter health level-to-level. Add a get/set method in that case?
    health = 20
    game_paused = True

    # Per-Level properties. 
    # FOR FUTURE: Create separate class to contain these properties? 
    starting_gold = 500

    # Spawn points:
    spawn_point_1 = (800, 10)
    spawn_point_2 = (200, 200)


    # Add background image including background terrain, paths, etc
    # backgroundImage = 
    wave = 0
    time_past = 0
    village_position = (window_width//2, window_height - 100)
    village = pygame.Rect(village_position[0], village_position[1], 50, 50)
    # Paths consist of a list of coordinate tuples. Enemies move from one to the next until they reach the end of the path.
    # Begin with the end so that creature.move() can use pop to progress between nodes
    enemy_path_1 = [(int(village_position[0] + 25), int(village_position[1] + 25)), (700, 350), (650, 400), (700, 150), (800, 100)]
    enemy_path_2 = []
    enemy_list = [("Skeleton", 10, spawn_point_1, enemy_path_1)]
    wave_timer = [5]

    # FOR FUTURE: Clean up the way that gold is handled and possibly move it to the tower purchase container
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

        # Draw background onto the screen
        window.fill((0,0,0))
        clock = pygame.time.Clock()

        # If the game is paused, then the drawing functions should continue but movement/projectiles/etc should not
        if not game_paused:
            time_past += 1
            clock.tick(framerate)

            for creature in existing_Creatures:
                if creature.health <= 0:
                    # FOR FUTURE: add functionality for creature death: death animations, gold increase, etc
                    # creature.die()
                    # gold += creature.value
                    # etc
                    existing_Creatures.remove(creature)
                    continue     
                creature.move()
                if village.collidepoint((creature.x, creature.y)) and creature.foe == True:
                    health -= creature.life_damage

            # Handle tower firing and attack movement
            for tower in existing_Towers:
                if len(tower.attack_objects) > 0:
                    for attack in tower.attack_objects:
                        attack.move()
                if tower.can_attack(math.floor(time_past/2)):
                    tower.attack(existing_Creatures, math.floor(time_past/2))
                    if tower.last_attack == math.floor(time_past/2):
                        tower.draw_attack(window)

            if wave < len(enemy_list):
                if wave_timer[wave]*framerate < time_past:
        
                    wave_makeup = enemy_list[wave]
                    spawn_Creatures(wave_makeup[0], wave_makeup[1], wave_makeup[2], wave_makeup[3], existing_Creatures) 
                    wave += 1

        # Window drawing. 
        # FOR FUTURE move to seperate method



        # Draw the combat interface
        # Draw the tower purchase container
        for button, color, kind in combat_interface[3]:
            pygame.draw.rect(window, color, button)
        
        # Draw the wave data container
        wave_data = (gold, time_past//framerate, wave)
        i = 0
        for position, text, color in combat_interface[1]:
            text = combat_interface_font.render(text + str(wave_data[i]), 1, color)
            window.blit(text, position)
            i += 1

        # Draw the game control container
        for button, color, kind in combat_interface[2]:
            pygame.draw.rect(window, color, button)

        # Draw the health container
        for position, text, color in combat_interface[4]:
            fulltext = text + str(health)
            displaytext = combat_interface_font.render(fulltext, 1, color)
            window.blit(displaytext, position)

        # Draw the towers and the projectiles/attacks
        for tower in existing_Towers:
            tower.draw_tower(window)
            if len(tower.attack_objects) > 0:
                for attack in tower.attack_objects:
                    attack.draw(window)
                    if attack.remove_attack == True:
                        tower.attack_objects.remove(attack)

        # Draw the village
        pygame.draw.rect(window, (128,128,128), village)

        # Draw the creatures
        for creature in existing_Creatures:
            creature.draw_creature(window)

        # Draw prospective purchased tower
        if prospective_Tower != "":
            mouse_position = pygame.mouse.get_pos()
            pygame.draw.rect(window, tower_graphic_list[prospective_Tower], (mouse_position[0] - tower_width//2, mouse_position[1] - tower_height//2, tower_width, tower_height))

        # Draw waypoints for debugging
        # for waypoint in enemy_path_1:
        #     pygame.draw.rect(window, (255,0,0), (waypoint[0], waypoint[1], 30, 30))


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
                    for button, _, kind in combat_interface[3]:
                        if button.collidepoint(mouse_position):
                            prospective_Tower = kind
                    for button, _, kind in combat_interface[2]:
                        
                        if button.collidepoint(mouse_position):
                            if kind == "PLAY":
                                game_paused = False
                            elif kind == "PAUSE":
                                game_paused = True
                    


                    # FOR FUTURE: 
                    # Check if player is selecting a hero
                    # Check if player is selecting a tower
                    # Check if player is selecting an enemy 
                    # Check if player is selecting something else
                            
                        





        pygame.display.update()

    pygame.display.quit()

def main():
    run = True
    while run:
        main_menu_font = pygame.font.SysFont("comicsans", 100, bold=True)
        play_level_one = main_menu_font.render("Play Level One", 1, (255,255,255))
        window.blit(play_level_one, (250,250))

        level_one_button = pygame.Rect(250, 250, 500, 250)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = event.pos
                if level_one_button.collidepoint(mouse_position):
                    level_one(window) 
                    
main()
