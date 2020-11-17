import creature as crt
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
    cycle_time = clock.get_cycle_length()

    score = 0

    
    selection_stage_one = ""
    tower_names = ["Fire_Tower", "Ice_Tower", "Arrow_Tower"]
    selection_location = (0,0)
    wave = 0

    
    while run:

        clock.tick()
        
    
        if clock.is_paused() == False:
            game_tick(level, cycle_time)


            if wave < len(level.waves):
                if clock.get_external_time() > level.waves[wave][0]:
                    spawn_wave_number(level, wave)
                    wave += 1

            for creature in level.existing_creatures:
                if not creature.is_alive():
                    level.existing_creatures.remove(creature)
                else:
                    creature.move()           
                    if creature.has_completed_path():
                        level.lower_health_by(creature.get_life_damage())
                    #       manage creature attacks
                    #           draw creature attacks
            for bolt in level.spellbolts:
                if bolt.is_alive():
                    bolt.move()
            for bolt in level.spellbolts:
                if bolt.can_attack():
                    bolt.attack()
                bolt.update_targets(bolt.target_list)
                if not bolt.is_alive():
                    level.spellbolts.remove(bolt)

            for tower in level.existing_towers:
                if tower.can_attack():
                    tower.update_targets(level.existing_creatures)
                    if tower.has_target():
                        spellbolts_holder = tower.attack()
                        if len(spellbolts_holder) > 0:
                            for bolt in spellbolts_holder:
                                level.spellbolts.append(bolt)

        #       draw tower attacks

        time = clock.get_external_time()
        update_screen(level, display, time, wave)

        user_input = get_user_input(display, "level")
        if user_input == False:
            return False
        elif user_input in tower_names:
            selection_stage_one = user_input
        elif user_input == "SELL":
            selection_stage_one = user_input
        elif user_input == "PAUSE":
            clock.pause()
        elif user_input == "PLAY":
            clock.resume()
        elif isinstance(user_input, tuple):
            selection_location = user_input
            if selection_stage_one in tower_names:
                purchase_tower(level, selection_stage_one, selection_location)
                selection_stage_one = ""
            elif selection_stage_one == "SELL":
                for tower in level.existing_towers:
                    if tower.collision(selection_location):
                        sell_tower(level, tower)
    return (score)

def game_tick(level, cycle_time):
    for creature in level.existing_creatures:
        creature.tick(cycle_time)
    for tower in level.existing_towers:
        tower.tick(cycle_time)


def spawn_wave_number(level, wave):
    creature_type = level.waves[wave][1]
    spawn_point = level.waves[wave][3]
    path = level.waves[wave][4].copy()
    for _ in range(level.waves[wave][2]):
        new_creature = getattr(crt, creature_type)(spawn_point, path)
        level.existing_creatures.append(new_creature)
        new_creature = None

def purchase_tower(level, kind, position):
    new_tower = None
    if kind == "Fire_Tower":
        new_tower = tower.Fire_Tower(position)
    elif kind == "Ice_Tower":
        new_tower = tower.Ice_Tower(position)
    elif kind == "Arrow_Tower":
        new_tower = tower.Arrow_Tower(position)

    if level.get_current_gold() >= new_tower.get_value():
        level.decrease_gold_by(new_tower.get_value())
    else:
        new_tower = None

    if len(level.existing_towers) > 0:
            for existing_tower in level.existing_towers:
                if existing_tower.collision(new_tower):
                    new_tower = None
    if new_tower is not None:
        level.existing_towers.append(new_tower)

def sell_tower(level, tower):
    level.increase_gold_by(int(tower.get_value()*tower.refund_rate))
    level.existing_towers.remove(tower)

def update_screen(level, display, time, wave):
    
    display.draw_image(level.draw_background())

    gold = level.get_current_gold()
    display.update_level_data_container(gold, time, wave)
    display.draw_interface()
    display.draw_image(level.draw_village(display.window_width, display.window_height))

    for creature in level.existing_creatures:
        display.draw_creature(creature.draw())
    for tower in level.existing_towers:
        display.draw_image(tower.draw())
    for bolt in level.spellbolts:
        display.draw_image(bolt.draw())

    display.show_updated_screen_to_user()

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