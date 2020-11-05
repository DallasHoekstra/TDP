# import tower as twr
# import creature as crt
import math
import time
import level as lvl
import GUI
import gameclock as gc
import tower



def play_level(level_number, display):
    run = True
    fps = 60
    level = lvl.Level(level_number)
    clock = gc.GameClock(fps)
    score = 0
    game_paused = False
    tower_purchase_selection = ""
    tower_names = ["Fire_Tower", "Ice_Tower", "Arrow_Tower"]
    selection_location = (0,0)
    wave = 0

    
    while run:

        clock.tick()
    
        if game_paused == False:
            pass
        #   is it time to spawn a wave
        #       if so, spawn wave
        #   check if creatures are alive
        #       move creatures
        #       collision check creatures and the village
        #       manage creature attacks
        #           draw creature attacks
        # 
        #   process tower attacks
        #       draw tower attacks
        #   move bullets
        #       collision check bullets and creatures
        #           remove expended bullet
        # 
        
        # draw combat interface

        time = clock.in_seconds(clock.get_current_time())
        update_screen(level, display, time, wave)

        user_input = get_user_input(display, "level")
        if user_input == False:
            return False
        if user_input in tower_names:
            tower_purchase_selection = user_input
        if isinstance(user_input, tuple):
            selection_location = user_input
            if tower_purchase_selection != "":
                purchase_tower(level, tower_purchase_selection, selection_location)
                tower_purchase_selection = ""
    return (score)




def purchase_tower(level, kind, position):
    new_tower = None
    if kind == "Fire_Tower":
        new_tower = tower.Fire_Tower(position)
    elif kind == "Ice_Tower":
        new_tower = tower.Ice_Tower(position)
    elif kind == "Arrow_Tower":
        new_tower = tower.Arrow_Tower(position)

    if level.get_current_gold() >= new_tower.get_value():
        level.reduce_gold_by(new_tower.get_value())
    else:
        new_tower = None

    if len(level.existing_towers) > 0:
            for existing_tower in level.existing_towers:
                if existing_tower.collision(new_tower):
                    new_tower = None
    if new_tower is not None:
        level.existing_towers.append(new_tower)

def sell_tower(level):
    pass




def update_screen(level, display, time, wave):
    
    display.draw_image(level.draw_background())
    display.draw_screen()
    display.draw_image(level.draw_village(display.window_width, display.window_height))

    for creature in level.existing_creatures:
        display.draw_image(creature.draw())
    for tower in level.existing_towers:
        display.draw_image(tower.draw())
    for attack in level.existing_attacks:
        display.draw_image(attack.draw())

    gold = level.get_current_gold()
    display.update_level_data_container(gold, time, wave)

    # Call for creature attacks
    # Call for creature deaths

    # Draw prospective purchased tower


    # if # game is over
    #     if # ended in victory:
    #         win_text = self.game_end_font.render("Victory", 1, (0, 255, 0))
    #         self.window.blit(win_text, (int(self.window_width/2 - win_text.get_width()/2), int(self.window_height/2 - win_text.get_height()/2) ))
    #     else: # ended in defeat
    #         loss_text = self.game_end_font.render("Your village has fallen!", 1, (255, 0, 0))
    #         self.window.blit(loss_text, (150, int(window_height/2) - 50))
















def get_user_input(display, caller):
    if caller == "level":
        user_input = display.return_user_input("level")
        if user_input == "QUIT":
            return exit_to_os(display)
        else:
            return user_input

    if caller == "main":
        user_input = display.return_user_input("main")
        if user_input == "Quit":
            return exit_to_os(display)
        else:
            return user_input

def exit_to_os(display):
    return False

def main():
    run = True
    display = GUI.TDDisplay()

    while run:
        result = ""
        user_input = ""
        user_input = get_user_input(display, "main")

        if user_input == "QUIT":
            run = False
        else:
            display.draw_main_menu()
            if user_input != None:
                result = play_level(user_input, display)
                user_input = None

        if result == False:
            run = False
        else:
            score = result
            # save the score to a file


main()