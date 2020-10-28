import pygame
import tower as twr
import creature as crt
import math
import time
import level as lvl
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
tower_graphic_list = {"Fire":(255,0,0), "Ice":(0,0,255), "Arrow":(100,100,0), "Wall":(100,100,100), "Sell":(100, 100, 0)}

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
    for tower, tower_rect in existing_Towers:
        if (abs(tower.x - position[0]) < (tower_width + 1)) and (abs(tower.y - position[1]) < (tower_height + 1)):
            # play_sound("collision")
            return (kind, gold)
    # FOR FUTURE: Create loop instead of extended if-elif block?
    
    if kind == "Fire":
        if gold >= twr.Fire_Tower.value:            
            gold -= twr.Fire_Tower.value
            new_Tower = twr.Fire_Tower(position[0], position[1])
            tower_Rect = pygame.Rect(position[0], position[1], tower_width, tower_height)
            existing_Towers.append((new_Tower, tower_Rect))
        else:
            # play_sound("poverty")
            return (kind, gold)
            
    elif kind == "Ice":
        if gold >= twr.Ice_Tower.value:
            gold -= twr.Ice_Tower.value
            new_Tower = twr.Ice_Tower(position[0], position[1])
            tower_Rect = pygame.Rect(position[0], position[1], tower_width, tower_height)
            existing_Towers.append((new_Tower, tower_Rect))
        else:
            # play_sound("poverty")
            return (kind, gold)

    elif kind == "Arrow":
        if gold >= twr.Arrow_Tower.value:
            gold -= twr.Arrow_Tower.value
            new_Tower = twr.Arrow_Tower(position[0], position[1])
            tower_Rect = pygame.Rect(position[0], position[1], tower_width, tower_height)
            existing_Towers.append((new_Tower, tower_Rect))
        else:
            # play_sound("poverty")
            return (kind, gold)

    elif kind == "Wall":
        if gold >= twr.Wall.value:
            gold -= twr.Wall.value
            new_Tower = twr.Wall(position[0], position[1])
            tower_Rect = pygame.Rect(position[0], position[1], tower_width, tower_height)
            existing_Towers.append((new_Tower, tower_Rect))
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
    fire_tower_image = pygame.image.load(image_path + "FireTowerL0.gif")
    fire_tower_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 10, fire_tower_image.get_width(), fire_tower_image.get_height()), fire_tower_image, "Fire")

    ice_tower_image = pygame.image.load(image_path + "IceTowerL0.gif")
    ice_tower_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 60, ice_tower_image.get_width(), ice_tower_image.get_height()), ice_tower_image, "Ice")

    arrow_tower_image = pygame.image.load(image_path + "ArrowTowerL0.gif")
    arrow_tower_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 110, arrow_tower_image.get_width(), arrow_tower_image.get_height()), arrow_tower_image, "Arrow")

    sell_image = pygame.image.load(image_path + "Sell.gif")
    sell_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 160, tower_width, tower_height), sell_image, "Sell")

    purchase_Container = [fire_tower_button, ice_tower_button, arrow_tower_button, sell_button]

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

    play_image = pygame.image.load(image_path + "PlayButton.gif")
    play_button = (pygame.Rect(control_start[0] + 10, control_start[1] + 10, play_image.get_width(), play_image.get_height()), play_image, "PLAY")

    pause_image = pygame.image.load(image_path + "PauseButton.gif")
    pause_button = (pygame.Rect(control_start[0] + 10, control_start[1] + 60, pause_image.get_width(), pause_image.get_height()), pause_image, "PAUSE")
    control_Container = (play_button, pause_button)

    # Health container
    health_start = container_dimensions[3]
    health_Container = [((health_start[0] + 10, health_start[1] + 10), "Health: ", (255, 0, 0))]

    return (combat_interface_font, text_Container, control_Container, purchase_Container, health_Container)








def level_one(window):
    run = True
    settings_menu_open = False
    victory = False
    combat_interface = create_combat_interface()
    combat_interface_font = combat_interface[0]
    prospective_Tower = ""
    background_image = pygame.image.load(image_path + "L1_Background.png")
    game_end_font = pygame.font.SysFont("comicsans", 80, bold=True)
    settings_menu_font = pygame.font.SysFont("comicsans", 40, bold=True)
    # FOR FUTURE: clean up attack handling so that orphaned attacks don't occur. Relevant once a sell feature is created
    orphaned_attacks = []

    # FOR FUTURE: possibly add skills that alter health level-to-level. Add a get/set method in that case?
    health = 20
    game_paused = True

    level = lvl.Level()
    wave = 0
    global gold
    time_past = 0

    gold = level.starting_gold
    village = pygame.Rect(level.village[0]*window_width, level.village[1]*window_height, level.village[2], level.village[3])
    waves = level.waves.copy()

    existing_Towers = []
    existing_Creatures = []

    while run:

        # Draw background onto the screen
        window.blit(background_image, (0,0))
        clock = pygame.time.Clock()

        # If the game is paused, then the drawing functions should continue but movement/projectiles/etc should not
        if not game_paused:
            time_past += 1
            clock.tick(framerate)

            # Manage creature functions: death, movement, attacking village
            for creature in existing_Creatures:
                if creature.health <= 0:
                    # FOR FUTURE: add functionality for creature death: death animations, gold increase, etc
                    # creature.die()
                    gold += creature.value
                    existing_Creatures.remove(creature)
                    continue     
                creature.move()
                if village.collidepoint((creature.x, creature.y)) and creature.foe == True:
                    health -= creature.life_damage
                    existing_Creatures.remove(creature)

            if health == 0:
                run = False

            # Handle tower firing and attack movement
            for tower, tower_rect in existing_Towers:
                if len(tower.attack_objects) > 0:
                    for attack in tower.attack_objects:
                        attack.move()
                if tower.can_attack(math.floor(time_past/2)):
                    tower.attack(existing_Creatures, math.floor(time_past/2))
                    if tower.last_attack == math.floor(time_past/2):
                        tower.draw_attack(window)
            for attack in orphaned_attacks:
                attack.move()

            # Handle wave spawning
            if wave <= (len(waves) - 1):
                if waves[wave][0]*framerate < time_past:
                    spawn_Creatures(waves[wave][1], waves[wave][2], waves[wave][3], waves[wave][4], existing_Creatures) 
                    wave += 1
            elif len(existing_Creatures) <= 0 and health > 0:
                victory = True
                run = False




        # Window drawing. 
        # FOR FUTURE move to seperate GUI Class
        # Draw the combat interface
        # Draw the tower purchase container
        if settings_menu_open == False:
            for button, image, kind in combat_interface[3]:
                pygame.draw.rect(window, (0,0,0), button)
                window.blit(image, (button[0], button[1]))
            
            # Draw the wave data container
            wave_data = (gold, time_past//framerate, wave)
            i = 0
            for position, text, color in combat_interface[1]:
                text = combat_interface_font.render(text + str(wave_data[i]), 1, color)
                window.blit(text, position)
                i += 1

            # Draw the game control container
            for button, image, kind in combat_interface[2]:
                pygame.draw.rect(window, (0,0,0), button)
                window.blit(image, (button[0], button[1]))

            # Draw the health container
            for position, text, color in combat_interface[4]:
                fulltext = text + str(health)
                displaytext = combat_interface_font.render(fulltext, 1, color)
                window.blit(displaytext, position)

            # Draw the towers and the projectiles/attacks
            for tower, tower_rect in existing_Towers:
                pygame.draw.rect(window, (0,0,0), tower_rect)
                tower.draw_tower(window)
                if len(tower.attack_objects) > 0:
                    for attack in tower.attack_objects:
                        attack.draw(window)
                        if attack.remove_attack == True:
                            tower.attack_objects.remove(attack)
            for attack in orphaned_attacks:
                attack.draw(window)
                if attack.remove_attack == True:
                    orphaned_attacks.remove(attack)

            # Draw the village
            pygame.draw.rect(window, (128,128,128), village)

            # Draw the creatures
            for creature in existing_Creatures:
                creature.draw_creature(window)

            # Draw prospective purchased tower
            if prospective_Tower != "":
                mouse_position = pygame.mouse.get_pos()
                pygame.draw.rect(window, tower_graphic_list[prospective_Tower], (mouse_position[0] - tower_width//2, mouse_position[1] - tower_height//2, tower_width, tower_height))
        
        else:
            # Open the settings menu
            # FOR FUTURE: automate centering and export to GUI?
            window.fill((0,0,0))

            # Create the buttons
            return_to_main_menu_button = pygame.Rect(100, 300, 300, 200)
            return_to_game_button = pygame.Rect(500, 300, 300, 200)
            
            # Create the text
            return_to_main_menu_text = settings_menu_font.render("Main Menu", 1, (255, 255, 255))
            return_to_game_text = settings_menu_font.render("Return to Game", 1, (255, 255, 255))

            # Draw the buttons
            pygame.draw.rect(window, (50, 0, 0), return_to_main_menu_button)
            pygame.draw.rect(window, (0, 50, 0), return_to_game_button)
            window.blit(return_to_main_menu_text, (175, 380))
            window.blit(return_to_game_text, (525, 380))



        # Event triggers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = event.pos
                if settings_menu_open == False:  
                    # Player trying to place a tower
                    if prospective_Tower != "" and prospective_Tower != "Sell":
                        tower_position = (event.pos[0] - tower_width//2, event.pos[1] - tower_height//2)
                        prospective_Tower, gold = purchase_Tower(prospective_Tower, existing_Towers, tower_position, gold)
                    elif prospective_Tower == "Sell":
                        for tower, tower_rect in existing_Towers:
                            if tower_rect.collidepoint(mouse_position):
                                gold += int(tower.value/2)
                                orphaned_attacks.extend(tower.attack_objects)
                                existing_Towers.remove((tower, tower_rect))
                                prospective_Tower = ""   
                    else:
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
                elif settings_menu_open == True:
                    if return_to_game_button.collidepoint(mouse_position):
                        settings_menu_open = False
                    elif return_to_main_menu_button.collidepoint(mouse_position):
                        run = False
                
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings_menu_open = True
                    pass
                    


                    # FOR FUTURE: 
                    # Check if player is selecting a hero
                    # Check if player is selecting a tower
                    # Check if player is selecting an enemy 
                    # Check if player is selecting something else
        pygame.display.update()

    
    if victory:
        win_text = game_end_font.render("Victory", 1, (0, 255, 0))
        window.blit(win_text, (int(window_width/2 - win_text.get_width()/2), int(window_height/2 - win_text.get_height()/2) ))
    else:
        loss_text = game_end_font.render("Your village has fallen!", 1, (255, 0, 0))
        window.blit(loss_text, (150, int(window_height/2) - 50))
    pygame.display.update()
    time.sleep(5)
    return()

def main():
    run = True
    while run:
        window.fill((0,0,0))
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
