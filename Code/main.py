# import tower as twr
# import creature as crt
import math
import time
import level as lvl
import GUI
import gameclock as gc




def play_level(level_number, display):
    run = True
    fps = 60
    level = lvl.Level(level_number)
    clock = gc.GameClock(fps)
    score = 0
    game_paused = False

    
    while run:
        
        clock.tick()
        update_screen(level, display)

        


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
        display.draw_screen()

        user_input = get_user_input(display, "level")
        if user_input == False:
            return False

    return (score)

def update_screen(level, display):
    display.draw_image(level.draw_background())
    display.draw_image(level.draw_village())

    for creature in level.existing_creatures:
        creature.draw()
    for tower in level.existing_towers:
        tower.draw()
    for attack in level.existing_attacks:
        attack.draw()
    

def get_user_input(display, caller):
    if caller == "level":
        user_input = display.return_user_input("level")
        if user_input == "QUIT":
            return exit_to_os(display)
        #elif user_input == :

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