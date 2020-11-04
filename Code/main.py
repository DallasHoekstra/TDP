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
    return (score)

def update_screen(level, display):
    display.draw_image(level.draw_background())
    display.draw_image(level.draw_village())
        # draw entities: creatures, towers, bullets, heroes, etc


        

def main():
    run = True
    display = GUI.TDDisplay()

    while run:
        selection = display.draw_main_menu()
        score = play_level(selection, display)
        # save the score to a file


main()