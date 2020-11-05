import pygame
import time

class TDDisplay():

    def __init__(self):
        # FOR FUTURE: add option to alter the framerate? Reasons?
        self.framerate = 60

        # FOR FUTURE: Create functionality that dynamically adjusts to playing screen size and full/partial window
        self.window_width = 1000
        self.window_height = 800

        # FOR FUTURE: Adjust tower size to playing screen size
        # Set to be equal to the .gif files for more accurate placement
        self.tower_width = 42
        self.tower_height = 40

        # FOR FUTURE: Create functionality to set path dynamically based on install or relative to files
        self.base_path = "c:/Users/Anonymous/Desktop/PythonProjects/TowerDefenseProject/"
        self.image_path = self.base_path + "Assets/Images/"
        self.audio_path = self.base_path + "Assets/Audio/"

        # For Future: Replace with images
        self.tower_graphic_list = {"Fire":(255,0,0), "Ice":(0,0,255), "Arrow":(100,100,0), "Wall":(100,100,100), "Sell":(100, 100, 0)}

        # Create the game screen
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # Fonts
        pygame.font.init()
        self.combat_interface_font = pygame.font.SysFont("comicsans", 20, bold=True)
        self.game_end_font = pygame.font.SysFont("comicsans", 80, bold=True)
        self.settings_menu_font = pygame.font.SysFont("comicsans", 40, bold=True)
        self.main_menu_font = pygame.font.SysFont("comicsans", 50, bold=True)

        # Purchase Container, Wave Info Container, Play/Pause Container, Health Container
        # (start_x, start_y, %window_width_to_right, %window_height_down)
        # Combat interface container dimensions percentage
        self.container_dimensions_percent = [(0, 0, .1, .33), (.25, 0, .5, .05), (.95, 0, .05, .05), (.5, .95, .1, .05)]

        self.combat_interface = self.create_combat_interface()
        self.main_menu = self.create_main_menu()
        #self.settings_menu = self.create_settings_menu()

    def return_user_input(self, caller):
        # Event triggers
        for event in pygame.event.get():
            if caller == "level":
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = event.pos
                    for button, _, tower_name in self.combat_interface[3]:
                        if button.collidepoint(mouse_position):
                            return tower_name
            elif caller == "main":
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = event.pos
                    for button_tuple in self.main_menu:
                        if button_tuple[0].collidepoint(mouse_position):
                            print(button_tuple[2])
                            return button_tuple[2]
                    return mouse_position

            
            # MOUSE BUTTON events
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_position = event.pos
        
                # Check to see if player is using combat interface
                # for button, _, kind in combat_interface[3]:
                #     if button.collidepoint(mouse_position):
                        # call attempting to purchase

                # Check to see if player is using game control interface
                # for button, _, kind in combat_interface[2]:
                #     if button.collidepoint(mouse_position):
                #         if kind == "PLAY":
                #             # call game play
                #         elif kind == "PAUSE":
                #             # call game pause
                #         if kind == "CallWave":
                #             if wave <= (len(waves) - 1):
                #             # call next wave
            # KEYBOARD events  
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         # Call open menu
    # Call when window is resized to adjust 

    def create_combat_interface(self): 

        self.window_width, self.window_height = self.window.get_size()

        container_dimensions = []
        for container in self.container_dimensions_percent:
            container_dimensions.append((container[0]*self.window_width, container[1]*self.window_height, container[2]*self.window_width, container[3]*self.window_height))

        # Tower purchasing buttons
        tower_start = container_dimensions[0]
        fire_tower_image = pygame.image.load(self.image_path + "FireTowerL0.gif")
        fire_tower_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 10, fire_tower_image.get_width(), fire_tower_image.get_height()), fire_tower_image, "Fire")

        ice_tower_image = pygame.image.load(self.image_path + "IceTowerL0.gif")
        ice_tower_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 60, ice_tower_image.get_width(), ice_tower_image.get_height()), ice_tower_image, "Ice")

        arrow_tower_image = pygame.image.load(self.image_path + "ArrowTowerL0.gif")
        arrow_tower_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 110, arrow_tower_image.get_width(), arrow_tower_image.get_height()), arrow_tower_image, "Arrow")

        sell_image = pygame.image.load(self.image_path + "Sell.gif")
        sell_button = (pygame.Rect(tower_start[0] + 10, tower_start[1] + 160, self.tower_width, self.tower_height), sell_image, "Sell")

        purchase_Container = [fire_tower_button, ice_tower_button, arrow_tower_button, sell_button]

        # Level data
        data_start = container_dimensions[1]
        text_Positions = [(data_start[0] + 10, data_start[1] + 10), (data_start[0] + int(data_start[2]*.33), data_start[1] + 10), 
                            (data_start[0] + int(data_start[2]*.66), data_start[1] + 10)]
        text_Values = ["Gold: ", "Time: ", "Wave: "]
        text_Colors = [(255,255,0), (255,255,255), (255,255,255)]


        text_Container = []
        for counter in range(len(text_Positions)):
            text_Container.append((text_Positions[counter], text_Values[counter], text_Colors[counter]))

        # Game flow control container
        control_start = container_dimensions[2]

        play_image = pygame.image.load(self.image_path + "PlayButton.gif")
        play_button = (pygame.Rect(control_start[0] + 10, control_start[1] + 10, play_image.get_width(), play_image.get_height()), play_image, "PLAY")

        pause_image = pygame.image.load(self.image_path + "PauseButton.gif")
        pause_button = (pygame.Rect(control_start[0] + 10, control_start[1] + 60, pause_image.get_width(), pause_image.get_height()), pause_image, "PAUSE")

        call_wave_image = pygame.image.load(self.image_path + "CallWave.gif")
        call_wave_button = (pygame.Rect(control_start[0] + 10, control_start[1] + 110, pause_image.get_width(), pause_image.get_height()), call_wave_image, "CallWave")

        control_Container = (play_button, pause_button, call_wave_button)

        # Health container
        health_start = container_dimensions[3]
        health_Container = [((health_start[0] + 10, health_start[1] + 10), "Health: ", (255, 0, 0))]

        return (self.combat_interface_font, text_Container, control_Container, purchase_Container, health_Container)

    def create_main_menu(self):
    
        play_level_one = self.main_menu_font.render("Play Level One", 1, (255,255,255))
        level_one_text = (play_level_one, (200,250))
        level_one_button = pygame.Rect(150, 250, 300, 250)
        
        play_level_two = self.main_menu_font.render("Play Level Two", 1, (255, 255, 255))
        level_two_text = (play_level_two, (550, 250))
        level_two_button = pygame.Rect(500, 250, 300, 250)

        play_level_three = self.main_menu_font.render("Play Level Three", 1, (255, 255, 255))
        level_three_text = (play_level_three, (200, 550))
        level_three_button = pygame.Rect(150, 550, 300, 250)
        
        return [(level_one_button, level_one_text, 1), (level_two_button, level_two_text, 2), (level_three_button, level_three_text, 3)]


    def draw_screen(self):

        # background_image = # background image from level

        # Draw the tower purchase container
        
        for button, image, kind in self.combat_interface[3]:
            pygame.draw.rect(self.window, (0,0,0), button)
            self.window.blit(image, (button[0], button[1]))
        
        # Draw the wave data container
        #wave_data = # Call gold, time_past, wave (gold, time_past//framerate, wave)
        i = 0
        #for position, text, color in self.combat_interface[1]:
            # text = self.combat_interface_font.render(text + str(wave_data[i]), 1, color)
            # self.window.blit(text, position)
            # i += 1

        # Draw the game control container
        for button, image, kind in self.combat_interface[2]:
            pygame.draw.rect(self.window, (0,0,0), button)
            self.window.blit(image, (button[0], button[1]))

        # Draw the health container
        for position, text, color in self.combat_interface[4]:
            fulltext = text + str(20) # Call health
            displaytext = self.combat_interface_font.render(fulltext, 1, color)
            self.window.blit(displaytext, position)



        pygame.display.update()

    def draw_settings_menu(self):
        # Open the settings menu
        # Create the settings menu buttons
        return_to_main_menu_button = self.settings_menu_font.render("Main Menu", 1, (255, 255, 255))
        return_to_game_button = self.settings_menu_font.render("Return to Game", 1, (255, 255, 255))

        # Create the text
        return_to_main_menu_text = self.settings_menu_font.render("Main Menu", 1, (255, 255, 255))
        return_to_game_text = self.settings_menu_font.render("Return to Game", 1, (255, 255, 255))

        # Draw the buttons
        pygame.draw.rect(self.window, (50, 0, 0), return_to_main_menu_button)
        pygame.draw.rect(self.window, (0, 50, 0), return_to_game_button)
        self.window.blit(return_to_main_menu_text, (175, 380))
        self.window.blit(return_to_game_text, (525, 380))
        
        # if return_to_game_button.collidepoint(mouse_position):
        #     # return control to level
        # elif return_to_main_menu_button.collidepoint(mouse_position):
        #     # return control to main menu

    def draw_main_menu(self):
        self.window.fill((0,0,0))
        for _, text, _ in self.main_menu:
            self.window.blit(text[0], text[1])
        pygame.display.update()

    def draw_image(self, image_data):
        image_filepath_postfix, image_position = image_data
        image = pygame.image.load(self.image_path + image_filepath_postfix)
        self.window.blit(image, image_position)