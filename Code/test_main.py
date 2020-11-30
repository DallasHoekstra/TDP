import time
import math
from random import randint 

import pytest
import unittest
import pytest_mock as mocker

import pygame
import gameclock as gc
import GUI
import main
import entity
import tower
import level
import creature
from creature import Creature as CRT
import attack

# Lists for use in parametrized tests
creature_types_list = ["Skeleton", "Accelerator"]
levels_list = [1, 2, 3, 4]
tower_type_list = ["Fire_Tower", "Ice_Tower", "Arrow_Tower"]


# Game Clock Tests
def test_initialize_game_clock():
    fps = 60
    game_clock_1 = gc.GameClock(fps)
    assert game_clock_1.get_fps() == fps
    
    fps = 30
    game_clock_2 = gc.GameClock(fps)
    assert game_clock_2.get_fps() == fps

def test_clock_cycles_progress_forward():
    game_clock = gc.GameClock(60)
    cycle_1 = game_clock.get_internal_time()
    cycle_2 = game_clock.get_internal_time()
    assert cycle_1 < cycle_2
    
def test_clock_ticks_at_least_cycle_length():
    game_clock = gc.GameClock(60)
    cycle_1 = game_clock.get_internal_time()
    game_clock.tick()
    cycle_2 = game_clock.get_internal_time()
    assert (cycle_2 - cycle_1) >= game_clock.get_cycle_length()

def test_fps_can_be_changed_multiple_times():
    fps_60 = 60
    fps_30 = 30

    game_clock = gc.GameClock(fps_60)
    assert game_clock.get_fps() == 60
    game_clock.set_fps(fps_30)
    assert game_clock.get_fps() == 30
    game_clock.set_fps(fps_60)
    assert game_clock.get_fps() == 60

def test_clock_converts_current_time_to_seconds():
    clock = gc.GameClock(60)
    time = clock.get_internal_time()
    time_in_seconds = clock.in_seconds(time)
    assert isinstance(time_in_seconds, int)

def test_pause_records_time_paused_at():
    clock = gc.GameClock(60)
    assert clock.paused_time == 0
    before = clock.get_internal_time()
    clock.pause()
    after = clock.get_internal_time()
    assert clock.paused_time >= before
    assert clock.paused_time <= after

def test_pause_ignores_calls_when_clock_is_paused():
    clock = gc.GameClock(60)
    clock.pause()
    original_paused_time = clock.paused_time
    clock.pause()
    assert clock.paused_time == original_paused_time

def test_get_external_time_gives_paused_time_in_seconds_when_paused():
    clock = gc.GameClock(60)

    random_number = randint(0, 10)
    for cycle in range(random_number):
        clock.tick()

    clock.pause()
    assert clock.in_seconds(clock.paused_time) == clock.get_external_time()
    assert isinstance(clock.get_external_time(), int)

def test_is_paused_returns_correct_value():
    clock = gc.GameClock(60)
    assert clock.is_paused() == False
    clock.paused = True
    assert clock.is_paused() == True

def test_resume_resets_paused_status():
    clock = gc.GameClock(60)
    clock.pause()
    assert clock.is_paused() == True
    clock.resume()
    assert clock.is_paused() == False

def test_external_time_ignores_time_passed_while_paused():
    clock = gc.GameClock(60)
    call_delay = round(abs(clock.get_internal_time() - clock.get_external_time()), 5)
    margin_of_error = call_delay + clock.get_cycle_length()/2
    
    clock.pause()
    after_pause = clock.get_internal_time()
    timer_1 = randint(0,10)
    for cycle in range(timer_1):
        clock.tick()
    before_resume = clock.get_internal_time()
    clock.resume()
    delay_time = round(before_resume - after_pause, 5)
    time_offset = round(clock.get_internal_time() - clock.get_external_time(), 5)
    assert time_offset < delay_time + margin_of_error
    assert time_offset + margin_of_error > delay_time

def test_external_time_ignores_time_across_multiple_pause_instances():
    clock = gc.GameClock(60)
    call_delay = round(abs(clock.get_internal_time() - clock.get_external_time()), 5)
    margin_of_error = call_delay + clock.get_cycle_length()/2
    delay_time = 0
    for _ in range(3):
        clock.pause()
        after_pause = clock.get_internal_time()

        timer = randint(0,10)
        for cycle in range(timer):
            clock.tick()
        
        before_resume = clock.get_internal_time()
        clock.resume()
        delay_time += before_resume - after_pause
        time_offset = clock.get_internal_time() - clock.get_external_time()

        assert time_offset < delay_time + margin_of_error
        assert time_offset > delay_time - margin_of_error

def test_resume_ignores_calls_when_clock_is_not_paused():    
    clock = gc.GameClock(60)
    clock.pause()
    clock.resume()
    original_time_offset = clock.time_offset
    clock.resume()
    assert original_time_offset == clock.time_offset

def test_get_external_time_returns_offset_time_when_paused():
    clock = gc.GameClock(60)
    call_delay = round(abs(clock.get_internal_time() - clock.get_external_time()), 5)
    margin_of_error = call_delay + clock.get_cycle_length()/2
    clock.pause()
    clock.resume()
    clock.pause()
    assert clock.get_external_time() < clock.get_external_time() - clock.time_offset + margin_of_error
    assert clock.get_external_time() > clock.get_external_time() - clock.time_offset - margin_of_error

# GUI Tests

@pytest.mark.parametrize("width, height, correct_dimensions", 
                        [(10, 15, (10, 15)), (131, 2050, (131, 2050))])
def test_get_image_dimensions(width, height, correct_dimensions):
    test_gui = GUI.TDDisplay()
    
    image = unittest.mock.MagicMock()
    image.get_width.return_value = width
    image.get_height.return_value = height

    image_dimensions = test_gui.get_image_dimensions(image)

    assert image_dimensions == correct_dimensions

@pytest.mark.parametrize("center_point, width, height, correct_drawpoint", 
                        [((100, 100), 50, 50, (75, 75)), ((500, 400), 120, 120, (440, 340))])
def test_calculate_drawpoint_returns_correct_value(center_point, width, height, correct_drawpoint):
    test_gui = GUI.TDDisplay()
    
    image_center = center_point
    image = unittest.mock.MagicMock()
    image.get_width = unittest.mock.MagicMock(return_value = width)
    image.get_height = unittest.mock.MagicMock(return_value = height)

    response = test_gui.calculate_drawpoint(image, image_center, width, height)

    assert response == correct_drawpoint

@pytest.mark.parametrize("thickness, percent_health, center_point, width", [(3, .5, (100, 100), 20), (10, .1, (200, 153), 15)])
def test_generate_healthbar_generates_healthbar(thickness, percent_health, center_point, width):
    test_gui = GUI.TDDisplay()

    response_object = test_gui.generate_healthbar(thickness, percent_health, center_point, width)
    assert response_object.height == thickness
    assert response_object.width == int(percent_health*width)
    assert response_object.top == center_point[1] - 5
    assert response_object.left == center_point[0]

@pytest.mark.parametrize("position, width, height, image_center, perc_health, color, postfix",
                        [((90, 90), 20, 20, (100, 100), .5, (200, 0, 0), "L0IceTower")])
@unittest.mock.patch('pygame.image.load')
@unittest.mock.patch('pygame.draw.rect')
@unittest.mock.patch('GUI.TDDisplay.generate_healthbar')
def test_draw_handles_drawing_a_creature(mock_generate_healthbar, mock_draw_rect, 
                                        mock_image_load, position, width, height, 
                                        image_center, perc_health, color, postfix ):
    test_gui = GUI.TDDisplay()

    image = unittest.mock.MagicMock()
    image.get_width = unittest.mock.MagicMock(return_value=width)
    image.get_height = unittest.mock.MagicMock(return_value=height)
    mock_image_load.return_value = image
    
    health_bar = unittest.mock.MagicMock()
    mock_generate_healthbar.return_value = health_bar

    test_gui.window = unittest.mock.MagicMock()
    test_gui.window.blit = unittest.mock.MagicMock()
    

    test_gui.draw((postfix, image_center, perc_health))


    mock_image_load.assert_called_with(str(test_gui.image_path) + str(postfix))
    mock_draw_rect.assert_called_with(test_gui.window, color, health_bar, 0)
    test_gui.window.blit.assert_called_with(image, position)

@pytest.mark.parametrize("position, width, height, image_center, postfix",
                            [((90, 90), 20, 20, (100, 100), "L0IceTower"),
                            ((60, 60), 100, 100, (110, 110), "L0FireTower")])
@unittest.mock.patch('pygame.image.load')
def test_draw_handles_drawing_an_image(mock_image_load, position, width, height,
                                        image_center, postfix):
    test_gui = GUI.TDDisplay()

    image = unittest.mock.MagicMock()
    image.get_width = unittest.mock.MagicMock(return_value=width)
    image.get_height = unittest.mock.MagicMock(return_value=height)
    mock_image_load.return_value = image

    test_gui.window = unittest.mock.MagicMock()
    test_gui.window.blit = unittest.mock.MagicMock()
    

    test_gui.draw((postfix, image_center))

    mock_image_load.assert_called_with(str(test_gui.image_path) + str(postfix))
    test_gui.window.blit.assert_called_with(image, position)

# Entity Tests
def test_entity_initializes_correctly():
    entity_position = (7, 7)
    test_entity = entity.Entity(entity_position)
    assert test_entity.x == entity_position[0]
    assert test_entity.y == entity_position[1]
    assert test_entity.max_health == 0
    assert test_entity.current_health == 0
    assert test_entity.name == ""
    assert test_entity.range_ == 0
    assert test_entity.foe == True
    assert test_entity.image_postfix == ""
    assert test_entity.attack_image_postfix == ""
    assert test_entity.width == 0
    assert test_entity.height == 0
    assert test_entity.fire_rate == 1
    assert test_entity.cooldown_time == round(1/test_entity.fire_rate, 5)
    assert test_entity.cooldown_time_left == 0
    assert test_entity.attack_draw_duration == 0
    assert test_entity.status_effects == []
    assert test_entity.target_list == []

def test_change_health_adds_number_to_health():
    test_entity = entity.Entity((0,0))
    test_entity.current_health = 10
    test_entity.max_health = 25
    original_health = test_entity.current_health

    test_entity.change_health_by(10)
    assert test_entity.current_health == original_health + 10
    original_health_2 = test_entity.current_health

    test_entity.change_health_by(-10)
    assert test_entity.current_health == original_health_2 - 10

def test_change_health_cannot_exceed_max_health():
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_entity.current_health = test_entity.max_health

    test_entity.change_health_by(1)
    assert test_entity.current_health == test_entity.max_health

def test_change_health_cannot_lower_health_below_zero():
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_entity.current_health = 0

    test_entity.change_health_by(-1)

    assert test_entity.current_health == 0

def test_change_health_by_sets_health_to_zero_if_excess_damage_done():
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_entity.max_health = 10
    test_entity.current_health = test_entity.max_health

    test_entity.change_health_by(-15)

    assert test_entity.current_health == 0

def test_entity_collides_with_entity():
    position_1 = (100, 100)
    position_2 = (125, 100)
    position_3 = (100, 125)
    position_4 = (150, 150)
    position_5 = (300, 100)
    position_6 = (100, 300)

    test_entity_1 = entity.Entity(position_1)
    test_entity_2 = entity.Entity(position_2)
    test_entity_3 = entity.Entity(position_3)
    test_entity_4 = entity.Entity(position_4)
    test_entity_5 = entity.Entity(position_5)
    test_entity_6 = entity.Entity(position_6)

    test_entity_1.width = 40
    test_entity_1.height = 40
    test_entity_2.width = 40
    test_entity_2.height = 40
    test_entity_3.width = 40
    test_entity_3.height = 40
    test_entity_4.width = 40
    test_entity_4.height = 40
    test_entity_5.width = 40
    test_entity_5.height = 40
    test_entity_6.width = 40
    test_entity_6.height = 40

    assert test_entity_1.collision(test_entity_2) == True
    assert test_entity_2.collision(test_entity_1) == True
    assert test_entity_1.collision(test_entity_3) == True
    assert test_entity_3.collision(test_entity_1) == True
    assert test_entity_2.collision(test_entity_3) == True
    assert test_entity_3.collision(test_entity_2) == True

    assert test_entity_1.collision(test_entity_4) == False
    assert test_entity_4.collision(test_entity_1) == False
    assert test_entity_2.collision(test_entity_4) == False
    assert test_entity_4.collision(test_entity_2) == False
    assert test_entity_3.collision(test_entity_4) == False
    assert test_entity_4.collision(test_entity_3) == False

    assert test_entity_1.collision(test_entity_5) == False
    assert test_entity_2.collision(test_entity_5) == False
    assert test_entity_3.collision(test_entity_5) == False
    assert test_entity_4.collision(test_entity_5) == False
    assert test_entity_6.collision(test_entity_5) == False

    assert test_entity_1.collision(test_entity_6) == False
    assert test_entity_2.collision(test_entity_6) == False
    assert test_entity_3.collision(test_entity_6) == False
    assert test_entity_4.collision(test_entity_6) == False
    assert test_entity_5.collision(test_entity_6) == False

@pytest.mark.parametrize("collision_point, result", [((301, 301), True), ((299, 299), False), ((300, 300), True)])
def test_entity_collision_with_point(collision_point, result):
    test_entity_position = (300, 300)
    test_entity = entity.Entity(test_entity_position)
    test_entity.width = 40
    test_entity.height = 40

    assert test_entity.collision(collision_point) == result

@pytest.mark.parametrize("position_1, point, position_2", [((0,0),(0,0),(0,0)), ((0,0), (100,100),(100,100)),
                                                        ((0,0),(100,100),(152,312)), ((0,0),(200,200),(312,0))])
def test_distance_from_calculates_distance_between_two_entities_or_points(position_1, point, position_2):
    entity_1 = entity.Entity(position_1)
    entity_2 = entity.Entity(position_2)
    distance_1p = math.sqrt(math.pow(abs(entity_1.x - point[0]), 2) + 
                            math.pow(abs(entity_1.y - point[1]), 2))
    distance_1_2 = math.sqrt(math.pow(abs(entity_1.x - entity_2.x), 2) + 
                            math.pow(abs(entity_1.y - entity_2.y), 2))

    assert entity_1.distance_from(point) == distance_1p
    assert entity_1.distance_from(entity_2) == distance_1_2
    assert entity_2.distance_from(entity_1) == distance_1_2

def test_entity_target_returns_None_if_no_available_targets():
    test_entities = [entity.Entity((100,100)), entity.Entity((200,200))]
    test_targeting_entity = entity.Entity((800,800))
    assert test_targeting_entity.update_targets(test_entities) is None

def test_entity_update_targets_removes_targets_out_of_range():
    target_position = (150, 150)
    targeter_position = (200, 200)
    test_target = entity.Entity(target_position)
    test_target.current_health = 1
    test_targeter = entity.Entity(targeter_position)
    possible_target_list = [test_target]

    test_targeter.target_list.append(test_target)

    assert test_targeter.has_target() == True
    test_target.x = 301
    test_target.y = 301
    test_targeter.update_targets(possible_target_list)
    assert test_targeter.has_target() == False

def test_entity_update_targets_handles_disappearing_target():
    targeter_position = (100, 100)
    targeted_position = (150, 150)
    
    test_targeter = entity.Entity(targeter_position)
    test_targeted = entity.Entity(targeted_position)
    test_targeted.current_health = 1

    test_targeter.target_lsit = [test_targeted]

    possible_target_list_without_current_target = []
    test_targeter.update_targets(possible_target_list_without_current_target)

    assert test_targeter.has_target() == False

def test_entity_update_targets_removes_dead_targets():
    targeter_position = (100, 100)
    targeted_position = (150, 150)
    
    test_targeter = entity.Entity(targeter_position)
    test_targeted = entity.Entity(targeted_position)
    test_targeted.current_health = 1
    test_targeter.range_ = 100

    test_targeter.update_targets([test_targeted])
    assert test_targeter.has_target() == True
    test_targeted.current_health = 0
    test_targeter.update_targets([test_targeted])
    assert test_targeter.has_target() == False

def test_entity_attack_returns_empty_list_by_default():
    position = (0,0)
    test_entity = entity.Entity(position)

    return_value = test_entity.attack()
    assert return_value == []

# FOR FUTURE: Update this behavior to "nearest to village" once pathing distance is implemented
def test_entity_targets_first_nearest_by_default():
    nearest = (100, 200)
    position_2 = (100, 400)
    position_3 = (400, 400)

    test_targeted = [entity.Entity(nearest), entity.Entity(position_2), entity.Entity(position_3)]
    print()
    print(test_targeted)
    for target in test_targeted:
        target.current_health = 1

    test_targeter = entity.Entity((150, 250))

    test_targeter.range_ = 400

    test_targeter.update_targets(test_targeted)
    assert isinstance(test_targeter.target_list[0], entity.Entity)
    assert test_targeter.target_list[0] == test_targeted[0]

    new_nearest = (115, 215)
    test_targeted.append(entity.Entity(new_nearest))
    test_targeter.update_targets(test_targeted)
    

    assert test_targeter.target_list[0] == test_targeted[0]
    test_targeted.remove(test_targeted[0])
    test_targeter.update_targets(test_targeted)
    assert test_targeter.target_list[0] == test_targeted[0]

def test_entity_can_only_attack_if_cooldown_complete():
    test_entity = entity.Entity((100, 100))
    assert test_entity.can_attack() == True
    test_entity.cooldown_time_left = 1
    assert test_entity.can_attack() == False

def test_entity_attack_resets_cooldown():
    position = (100, 100)
    test_entity = entity.Entity(position)
    
    test_entity.attack()
    assert test_entity.cooldown_time_left == test_entity.cooldown_time

def test_entity_tick_reduces_cooldown_time_left():
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_entity.cooldown_time_left = 1
    time_passed = .016
    test_entity.tick(time_passed)

    assert test_entity.cooldown_time_left == 1 - time_passed

@pytest.mark.parametrize("time_passed", [1, 4])
def test_entity_tick_reduces_duration_of_one_effect(time_passed):
    position = (100, 100)
    test_entity = entity.Entity(position)
    duration = 10

    test_entity.add_status_effect("Ice", duration, 2)
    test_entity.tick(time_passed)
    duration_remaining = test_entity.status_effects[0][1]
    assert duration_remaining == duration - time_passed

def test_entity_tick_reduces_duration_of_multiple_effects():
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_entity.add_status_effect("Ice", 10, 2)
    test_entity.add_status_effect("Fire", 5, 15)

    test_entity.tick(1)

    assert test_entity.status_effects[0][1] == 9
    assert test_entity.status_effects[1][1] == 4

@pytest.mark.parametrize("time_passed", [5, 2])
def test_entity_tick_removes_an_expired_effect(time_passed):
    position = (200, 200)
    test_entity = entity.Entity(position)
    test_entity.add_status_effect("Ice", 2, 2)
    
    test_entity.tick(time_passed)

    assert test_entity.status_effects == []

def test_entity_tick_removes_expired_effects_but_not_nonexpired_ones():
    position = (314, 159)
    test_entity = entity.Entity(position)
    test_entity.add_status_effect("Ice", 5, 1)
    test_entity.add_status_effect("Fire", 2, .5)

    test_entity.tick(3)

    assert test_entity.status_effects == [["Ice", 2, 1]]

def test_entity_tick_removes_multiple_expired_effects():
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_entity.add_status_effect("Fire", 2, 3)
    test_entity.add_status_effect("Ice", 1, 15)

    test_entity.tick(2)

    assert test_entity.status_effects == []

def test_entity_tick_applies_status_effects():
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_entity.status_effects = [["Ice", 5, 2], ["Fire", 5, .1]]
    test_entity.apply_status_effect = unittest.mock.MagicMock(name="apply status")

    test_entity.tick(1)

    test_entity.apply_status_effect.assert_any_call("Ice", 4, 2)
    test_entity.apply_status_effect.assert_any_call("Fire", 4, .1)
    
def test_entity_has_target_only_if_target_list_is_not_empty():
    test_entity_targeter = entity.Entity((100, 100))
    test_entity_targeted = entity.Entity((50,50))
    test_entity_targeted.current_health = 1

    assert test_entity_targeter.has_target() == False
    
    test_entity_targeter.target_list = [test_entity_targeted]

    assert test_entity_targeter.has_target() == True

def test_entity_has_target_only_if_target_is_alive():
    test_entity_targeter = entity.Entity((0,0))
    test_entity_targeted = entity.Entity((0,0))
    test_entity_targeted.current_health = 1

    test_entity_targeter.target_list = [test_entity_targeted]
    assert test_entity_targeter.has_target() == True
    test_entity_targeted.die()
    assert test_entity_targeter.has_target() == False

def test_entity_has_target_handles_multitarget_lists():
    test_entity_targeter = entity.Entity((0,0))
    test_entity_targeted = []
    for _ in range(5):
        test_entity_targeted.append(entity.Entity((_,_)))
        test_entity_targeted[_].current_health = 1
    test_entity_targeter.target_list = test_entity_targeted.copy()

    assert test_entity_targeter.has_target() == True

def test_add_status_effect_adds_status_to_list_by_default():
    position = (100, 100)
    test_entity = entity.Entity(position)

    test_entity.add_status_effect("Ice", 10, 2)
    assert test_entity.status_effects == [["Ice", 10, 2]]

def test_add_status_effect_allows_adding_subsequent_effects():
    position = (121, 122)
    test_entity = entity.Entity(position)

    test_entity.add_status_effect("Ice", 10, 2)
    test_entity.add_status_effect("Fire", 5, 5)

    assert test_entity.status_effects == [["Ice", 10, 2], ["Fire", 5, 5]]

@pytest.mark.parametrize("move_speed, severity", [(4, 2), (8, 3)])
def test_apply_status_effect_ice_divides_entity_speed_by_severity(move_speed, severity):
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_entity.default_move_speed = move_speed
    test_entity.move_speed = move_speed

    test_entity.apply_status_effect("Ice", 10, severity)

    assert test_entity.move_speed == move_speed/severity

def test_apply_status_effect_ice_uses_exactly_most_severe_effect():
    position = (100, 100)
    move_speed = 4
    duration = 10
    less_severe = 2 
    more_severe = 4
    test_entity = entity.Entity(position)
    test_entity.default_move_speed = move_speed
    test_entity.move_speed = move_speed


    test_entity.apply_status_effect("Ice", duration, less_severe)
    test_entity.apply_status_effect("Ice", duration, more_severe)

    assert test_entity.move_speed == move_speed/more_severe

@pytest.mark.parametrize("severity", [.01, .005])
def test_apply_status_effect_fire_damages_entity_by_severity(severity):
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_entity.current_health = 10

    test_entity.apply_status_effect("Fire", 10, severity)

    assert test_entity.current_health == 10 - severity

def test_end_status_effect_ice_returns_move_speed_to_normal():
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_entity.default_move_speed = 4
    test_entity.move_speed = 4

    test_entity.apply_status_effect("Ice", 1, 2)
    test_entity.end_status_effect("Ice", 0, 2)

    assert test_entity.move_speed == test_entity.default_move_speed


# Tower Tests
@pytest.mark.parametrize("tower_position", [(100, 100), (145, 230)])
def test_tower_draw_attack_returns_correct_data(tower_position):
    test_tower = tower.Tower(tower_position)

    draw_data = test_tower.draw_attack()
    assert isinstance(draw_data[1], tuple)
    assert draw_data[1][0] == test_tower.x
    assert draw_data[1][1] == test_tower.y
    assert draw_data[0] == test_tower.attack_image_postfix

def test_entity_draw_uses_proper_GUI_formatting():
    test_entity = entity.Entity((100,200))
    image_path, position = test_entity.draw()
    assert isinstance(image_path, str)
    assert isinstance(position, tuple)
    assert isinstance(position[0], int or float)
    assert isinstance(position[1], int or float)

def test_Fire_Tower_initializes_correctly():
    tower_position = (100, 100)
    test_tower = tower.Fire_Tower(tower_position)

    assert test_tower.x == tower_position[0]
    assert test_tower.y == tower_position[1]
    assert isinstance(test_tower, tower.Fire_Tower) == True
    assert test_tower.status_effects == []
    assert test_tower.target_list == []
    assert test_tower.cost == 100
    assert test_tower.name == "FIRE_TOWER"
    assert test_tower.image_postfix == "FireTowerL0.gif"
    assert test_tower.attack_image_postfix == "Fire_Attack.gif"
    assert test_tower.attack_draw_duration == .2
    assert test_tower.fire_rate == 2
    assert test_tower.cooldown_time == round(1/test_tower.fire_rate, 5)
    assert test_tower.cooldown_time_left == 0
    assert test_tower.range_ == 100*math.sqrt(2)
    assert test_tower.damage == 1

def test_Ice_Tower_initializes_correctly():
    tower_position = (100, 100)
    test_tower = tower.Ice_Tower(tower_position)

    assert test_tower.x == tower_position[0]
    assert test_tower.y == tower_position[1]
    assert isinstance(test_tower, tower.Ice_Tower) == True
    assert test_tower.status_effects == []
    assert test_tower.target_list == []
    assert test_tower.cost == 150
    assert test_tower.name == "ICE_TOWER"
    assert test_tower.image_postfix == "IceTowerL0.gif"
    assert test_tower.attack_image_postfix == "Ice_Shard.gif"
    assert test_tower.attack_draw_duration == 1
    assert test_tower.fire_rate == .5
    assert test_tower.cooldown_time == round(1/test_tower.fire_rate, 5)
    assert test_tower.cooldown_time_left == 0
    assert test_tower.range_ == 300*math.sqrt(2)
    assert test_tower.damage == 5

def test_Arrow_Tower_initializes_correctly():
    tower_position = (100, 100)
    test_tower = tower.Arrow_Tower(tower_position)

    assert test_tower.x == tower_position[0]
    assert test_tower.y == tower_position[1]
    assert isinstance(test_tower, tower.Arrow_Tower) == True
    assert test_tower.status_effects == []
    assert test_tower.target_list == []
    assert test_tower.cost == 150
    assert test_tower.name == "ARROW_TOWER"
    assert test_tower.image_postfix == "ArrowTowerL0.gif"
    assert test_tower.attack_image_postfix == "Arrow.gif"
    assert test_tower.attack_draw_duration == 1
    assert test_tower.fire_rate == .5
    assert test_tower.cooldown_time == round(1/test_tower.fire_rate, 5)
    assert test_tower.cooldown_time_left == 0
    assert test_tower.range_ == 500*math.sqrt(2)
    assert test_tower.damage == 5

def test_tower_should_draw_attack_returns_True_if_has_attacked_recently():
    tower_position = (100, 100)
    test_tower = tower.Fire_Tower(tower_position)

    test_tower.cooldown_time_left = test_tower.cooldown_time - test_tower.attack_draw_duration

    assert test_tower.should_draw_attack() == True

def test_tower_should_draw_attack_returns_False_if_has_not_attacked_recently():
    tower_position = (100, 100)
    test_tower = tower.Fire_Tower(tower_position)

    test_tower.cooldown_time_left = test_tower.cooldown_time - (test_tower.attack_draw_duration + 1)

    assert test_tower.should_draw_attack() == False

@pytest.mark.parametrize("tower_type", tower_type_list)
def test_tower_get_position_returns_correct_position(tower_type):
    tower_position = (0, 0)
    test_tower = getattr(tower, tower_type)(tower_position)
    position = test_tower.get_position()
    assert position[0] == tower_position[0]
    assert position[1] == tower_position[1]

def test_Fire_Tower_update_targets_acquires_all_viable_targets():
    fire_tower_position = (400, 400)
    test_fire_tower = tower.Fire_Tower(fire_tower_position)
    viable_target_positions = [(300, 300), (400, 400), (500, 500), (500, 300), (300, 500)]
    viable_target_entities = []
    for position in viable_target_positions:
        temp_entity = entity.Entity(position)
        temp_entity.current_health = 10
        viable_target_entities.append(temp_entity)
        
    test_fire_tower.update_targets(viable_target_entities)

    counter = 0
    for viable_entity in viable_target_entities:
        for target in test_fire_tower.target_list:
            if viable_entity is target:
                viable_target_entities[counter] = None
                counter += 1
                break
    for viable_entity in viable_target_entities:
        assert viable_entity is None 

def test_Fire_Tower_attack_deals_damage():
    Fire_Tower_position = (400, 400)
    test_Fire_Tower = tower.Fire_Tower(Fire_Tower_position)
    
    skeleton_1_position = (299, 299)
    path = [(299, 299), (350, 350), (401, 401)]
    skeleton_1 = creature.Skeleton(skeleton_1_position, path)
    skeleton_original_health = skeleton_1.current_health

    test_Fire_Tower.target_list = [skeleton_1]
    test_Fire_Tower.attack()

    assert skeleton_1.current_health == skeleton_original_health - test_Fire_Tower.damage

@pytest.mark.parametrize("tower_type", tower_type_list)
def test_tower_attacks_reset_cooldown_when_tower_has_targets(tower_type):
    entity_position = (50, 50)
    test_entity = entity.Entity(entity_position)

    tower_position = (100, 100)
    test_tower = getattr(tower, tower_type)(tower_position)
    test_tower.target_list = [test_entity]


    test_tower.attack()
    assert test_tower.cooldown_time_left == test_tower.cooldown_time

def test_Fire_Tower_attacks_all_targets():
    mock_entities_positions = [(80, 80), (90, 90), (110, 110), (120, 120)]
    mock_entities = []

    for position in mock_entities_positions:
        temp_mock_entity = entity.Entity(position)
        temp_mock_entity.change_health_by = unittest.mock.MagicMock(name='change_health_by')
        mock_entities.append(temp_mock_entity)

    fire_tower_position = (100, 100)
    test_fire_tower = tower.Fire_Tower(fire_tower_position)

    test_fire_tower.target_list = mock_entities.copy()
    test_fire_tower.attack()

    for mock_entity in mock_entities:
        mock_entity.change_health_by.assert_called()

def test_Fire_Tower_attack_returns_empty_list():
    fire_tower_position = (100, 100)
    test_fire_tower = tower.Fire_Tower(fire_tower_position)

    entity_position = (130, 130)
    test_entity = entity.Entity(entity_position)
    test_entity.current_health = 1

    test_fire_tower.target_list = [test_entity]
    return_value = test_fire_tower.attack()

    assert return_value == []

def test_Ice_Tower_attack_without_targets_returns_empty_list():
    tower_positon = (100, 100)
    test_ice_tower = tower.Ice_Tower(tower_positon)
    test_ice_tower.update_targets([])

    spellbolt = test_ice_tower.attack()
    assert spellbolt == []    

def test_Ice_Tower_attack_with_targets_returns_Ice_bolt():
    tower_positon = (100, 100)
    test_ice_tower = tower.Ice_Tower(tower_positon)
    
    entity_position = (200, 200)
    test_entity = entity.Entity(entity_position)
    test_entity.current_health = 1

    test_ice_tower.update_targets([test_entity])
    spellbolt = test_ice_tower.attack()
    print(spellbolt)
    assert len(spellbolt) > 0
    assert isinstance(spellbolt[0], attack.IceBolt)

def test_Arrow_Tower_attack_without_targets_returns_empty_list():
    tower_position = (400, 400)
    test_tower = tower.Arrow_Tower(tower_position)
    return_value = test_tower.attack()

    assert return_value == []

def test_Arrow_Tower_attack_with_targets_returns_Arrow_bolt():
    entity_position = (100, 100)
    test_entity = entity.Entity(entity_position)
    test_entity.current_health = 1

    tower_position = (400, 400)
    test_tower = tower.Arrow_Tower(tower_position)
    test_tower.target_list = [test_entity]
    return_value = test_tower.attack()
    assert isinstance(return_value[0], attack.ArrowBolt) == True

#Attack Class Tests

@pytest.mark.parametrize("position, target_position, target_path, target_type", 
                                        [((100, 100), (500, 500), [(550, 550)], "Skeleton"), ((0, 0), (600, 600), [(300, 300)], "Accelerator"),
                                         ((400, 400), (100, 300), [(200, 800)], "Skeleton")])
def test_spellbolt_initializes_correctly(position, target_position, target_path, target_type):
    test_target = [getattr(creature, target_type)(target_position, target_path)]

    test_spellbolt = attack.SpellBolt(position, test_target)

    assert isinstance(test_spellbolt, entity.Entity)
    assert isinstance(test_spellbolt, attack.SpellBolt)
    assert test_spellbolt.x == position[0]
    assert test_spellbolt.y == position[1]
    assert test_spellbolt.target_list == test_target
    assert test_spellbolt.damage == 0
    assert test_spellbolt.element == ""
    assert test_spellbolt.default_move_speed == 0
    assert test_spellbolt.move_speed == 0

def test_bolt_is_alive_returns_false_without_targets():
    position = (100, 100)
    test_spellbolt = attack.SpellBolt(position, [])

    assert test_spellbolt.is_alive() == False

def test_bolt_is_alive_returns_true_if_bolt_has_targets():
    entity_position = (100, 100)
    test_entity = entity.Entity(entity_position)
    test_entity.current_health = 1

    spellbolt_position = (200, 200)
    test_spellbolt = attack.SpellBolt(spellbolt_position, [test_entity])

    assert test_spellbolt.is_alive() == True

@pytest.mark.parametrize("creature_type", creature_types_list)
def test_spellbolt_handles_multiple_targets(creature_type):
    position = (100, 100)
    path = [(500, 500)]
    test_target_list = []
    for _ in range(5):
        temp_creature = getattr(creature, creature_type)(position, path)
        test_target_list.append(temp_creature)
        position = (position[0] + 10, position[1] + 10)
        path[0] = (path[0][1] + 10, path[0][1] + 10)

    test_spellbolt = attack.SpellBolt(position, test_target_list)
    assert isinstance(test_spellbolt, entity.Entity)
    assert isinstance(test_spellbolt, attack.SpellBolt)
    assert test_spellbolt.x == position[0]
    assert test_spellbolt.y == position[1]
    assert test_spellbolt.target_list == test_target_list
    assert test_spellbolt.damage == 0
    assert test_spellbolt.element == ""
    assert test_spellbolt.default_move_speed == 0
    assert test_spellbolt.move_speed == 0

def test_Ice_Bolt_initializes_correctly():
    bolt_position = (100, 100)
    target_position = (500, 500)
    test_target = [entity.Entity(target_position)]
    test_bolt = attack.IceBolt(bolt_position, test_target)

    assert isinstance(test_bolt, attack.IceBolt)
    assert isinstance(test_bolt, attack.SpellBolt) 
    assert test_bolt.damage == 10
    assert test_bolt.element == "Ice"
    assert test_bolt.duration == 5
    assert test_bolt.severity == 2
    assert test_bolt.default_move_speed == 5
    assert test_bolt.move_speed == test_bolt.default_move_speed

def test_Arrow_Bolt_initializes_correctly():
    entity_position = (200, 200)
    test_entity = entity.Entity(entity_position)

    bolt_position = (100, 100)
    test_bolt = attack.ArrowBolt(bolt_position, [test_entity])

    assert test_bolt.x == 100
    assert test_bolt.y == 100
    assert len(test_bolt.target_list) == 1
    assert test_bolt.target_list[0] == test_entity
    assert test_bolt.damage == 2
    assert test_bolt.default_move_speed == 5
    assert test_bolt.move_speed == test_bolt.default_move_speed

def test_SpellBolt_remove_invalid_targets_does_not_consider_range():
    entity_position = (100, 100)
    test_entity = entity.Entity(entity_position)
    test_entity.current_health = 1

    bolt_position = (200, 200)
    test_bolt = attack.SpellBolt(bolt_position, [test_entity])
    test_entity.remove_invalid_targets([test_entity])

    assert test_bolt.target_list == [test_entity]
    
def test_SpellBolt_cannot_attack_without_a_target():
    spellbolt_position = (100, 100)
    test_spellbolt = attack.SpellBolt(spellbolt_position, [])
    test_spellbolt.width = 5
    test_spellbolt.height = 5

    assert test_spellbolt.can_attack() == False  

def test_SpellBolt_cannot_attack_without_collision():
    entity_position = (200, 200)
    test_entity = [entity.Entity(entity_position)]
    test_entity[0].current_health = 1
    test_entity[0].width = 5
    test_entity[0].height = 5

    spellbolt_position = (100, 100)
    test_spellbolt = attack.SpellBolt(spellbolt_position, test_entity)
    test_spellbolt.width = 5
    test_spellbolt.height = 5

    assert test_spellbolt.can_attack() == False    

def test_SpellBolt_can_attack_on_collision():
    entity_position = (100, 100)
    test_entity = [entity.Entity(entity_position)]
    test_entity[0].current_health = 1
    test_entity[0].width = 5
    test_entity[0].height = 5

    spellbolt_position = (100, 100)
    test_spellbolt = attack.SpellBolt(spellbolt_position, test_entity)
    test_spellbolt.width = 5
    test_spellbolt.height = 5

    assert test_spellbolt.can_attack() == True

def test_SpellBolt_attack_attempts_to_damage_target():
    mock_position = (100, 100)
    temp_mock_entity = entity.Entity(mock_position)
    temp_mock_entity.change_health_by = unittest.mock.MagicMock(name='change_health_by')
    temp_mock_entity.current_health = 1
    temp_mock_entity.width = 5
    temp_mock_entity.height = 5

    spellbolt_position = (100, 100)
    test_spellbolt = attack.SpellBolt(spellbolt_position, [temp_mock_entity])
    test_spellbolt.width = 5
    test_spellbolt.height = 5

    test_spellbolt.attack()
    temp_mock_entity.change_health_by.assert_called()

    attack_damage = test_spellbolt.damage
    
    temp_mock_entity.change_health_by.assert_called_with(-attack_damage)

def test_spellBolt_removes_target_after_attacking_it():
    entity_position = (100, 100)
    test_entity = [entity.Entity(entity_position)]
    test_entity[0].current_health = 10
    test_entity[0].width = 5
    test_entity[0].height = 5

    spellbolt_position = (100, 100)
    test_spellbolt = attack.SpellBolt(spellbolt_position, test_entity)
    test_spellbolt.damage = 5
    test_spellbolt.width = 5
    test_spellbolt.height = 5

    test_spellbolt.attack()
    assert test_spellbolt.target_list == []

def test_Ice_Bolt_attack_applies_ice_status_effect():
    position = (100, 100)
    test_entity = entity.Entity(position)
    target = [test_entity]
    test_Ice_Bolt = attack.IceBolt(position, target)

    test_Ice_Bolt.attack()

    assert len(test_entity.status_effects) > 0
    assert test_entity.status_effects[0][0] == "Ice"

def test_Ice_Bolt_generate_status_effect_returns_formatted_status_effect():
    position = (100, 100)
    test_entity = entity.Entity(position)
    test_Ice_Bolt = attack.IceBolt(position, [test_entity])

    status_effect = test_Ice_Bolt.generate_status_effect()

    assert status_effect[0] == "Ice"
    assert status_effect[1] == test_Ice_Bolt.duration
    assert status_effect[2] == test_Ice_Bolt.severity

@pytest.mark.parametrize("entity_position", [(100, 100), (300, 300), (200, 100), (200, 300), (200, 200)])
def test_SpellBolt_moves_toward_target(entity_position):
    test_entity = entity.Entity(entity_position)

    spellbolt_position = (200, 200)
    test_spellbolt = attack.SpellBolt(spellbolt_position, [test_entity])
    original_distance = test_spellbolt.distance_from(test_spellbolt.target_list[0])

    test_spellbolt.move()
    new_distance = test_spellbolt.distance_from(test_spellbolt.target_list[0])

    assert original_distance >= new_distance


#Level Tests
def test_level_draw_background_returns_postfix_and_centerpoint():
    level_number = 1
    test_level = level.Level(level_number)
    centerpoint = (int(test_level.width/2), int(test_level.height/2))

    return_value = test_level.draw_background()
    assert return_value[0] == test_level.background_postfix
    assert return_value[1] == centerpoint
    

    test_level.width = 100
    test_level.height = 100
    new_centerpoint = (int(test_level.width/2), int(test_level.height/2))
    new_return_value = test_level.draw_background()
    assert return_value[0] == test_level.background_postfix
    assert new_return_value[1] == new_centerpoint

@pytest.mark.parametrize("level_number", levels_list)
def test_gold_can_be_increased(level_number):
    test_level = level.Level(level_number)
    initial_gold = test_level.get_current_gold()
    test_level.increase_gold_by(100)
    new_gold = test_level.get_current_gold()

    assert new_gold == initial_gold + 100

@pytest.mark.parametrize("level_number", levels_list)
def test_gold_can_be_decreased(level_number):
    test_level = level.Level(level_number)
    initial_gold = test_level.get_current_gold()
    test_level.decrease_gold_by(100)
    new_gold = test_level.get_current_gold()

    assert new_gold == initial_gold - 100

@pytest.mark.parametrize("level_number", levels_list)
def test_lower_health_by_lowers_health(level_number):
    test_level = level.Level(level_number)

    original_health = test_level.health
    test_level.lower_health_by(5)
    assert test_level.health == original_health - 5
    test_level.lower_health_by(1)
    assert test_level.health == original_health - 6

@pytest.mark.parametrize("level_number", levels_list)
def test_lower_health_by_bottoms_at_zero(level_number):
    test_level = level.Level(level_number)
    original_health = test_level.health
    test_level.lower_health_by(original_health + 1)
    assert test_level.health == 0
    
@pytest.mark.parametrize("level_number", levels_list)
def test_lower_health_by_cannot_increase_health(level_number):
    test_level = level.Level(level_number)
    original_health = test_level.health
    test_level.lower_health_by(-1)
    assert original_health >= test_level.health


# Main Tests
@pytest.mark.parametrize("kind, position, type_", [("Fire_Tower", (100, 100), tower.Fire_Tower), 
                                                    ("Ice_Tower", (200, 200), tower.Ice_Tower),
                                                     ("Arrow_Tower", (300, 300), tower.Arrow_Tower)])
def test_purchase_tower_type_creates_tower_type(kind, position, type_):
    test_level = level.Level(1)

    main.purchase_tower(test_level, kind, position)
    assert isinstance(test_level.existing_towers[0], type_)

def test_purchase_tower_type_prevents_colliding_tower_placement():
    test_level = level.Level(1)
    
    kind = "Fire_Tower"
    position = (100, 100)
    main.purchase_tower(test_level, kind, position)

    kind = "Ice_Tower"
    position = (120, 120)
    main.purchase_tower(test_level, kind, position)

    kind = "Arrow_Tower"
    position = (120, 400)
    main.purchase_tower(test_level, kind, position)

    assert len(test_level.existing_towers) == 2

def test_level_loads_correct_amount_of_gold():
    test_level_1 = level.Level(1)
    test_level_2 = level.Level(2)
    
    assert test_level_1.get_current_gold() == 2000
    assert test_level_2.get_current_gold() == 3000

@pytest.mark.parametrize("kind, position", [("Fire_Tower", (100, 100)), ("Ice_Tower", (200, 200)),
                                                     ("Arrow_Tower", (300, 300))])
def test_cannot_purchase_without_gold(kind, position):
    test_level = level.Level(1)
    test_level.current_gold = 0

    main.purchase_tower(test_level, kind, position)
    assert len(test_level.existing_towers) == 0

@pytest.mark.parametrize("kind, position", [("Fire_Tower", (100, 100)), ("Ice_Tower", (200, 200)),
                                                     ("Arrow_Tower", (300, 300))])
def test_purchase_reduces_player_gold_by_tower_cost(kind, position):
    test_level = level.Level(1)
    gold_before_purchase = test_level.get_current_gold()

    main.purchase_tower(test_level, kind, position)

    gold_after_purchase = test_level.get_current_gold()
    assert gold_before_purchase == gold_after_purchase + test_level.existing_towers[0].get_value()

def test_sell_tower_removes_tower():
    test_level = level.Level(1)
    
    kind = "Fire_Tower"
    position = (100, 100)
    main.purchase_tower(test_level, kind, position)
    main.sell_tower(test_level, test_level.existing_towers[0])
    assert len(test_level.existing_towers) == 0

def test_sell_refunds_partial_and_only_partial_value_of_tower():
    test_level = level.Level(1)
    gold_before_purchase = test_level.get_current_gold()

    kind = "Fire_Tower"
    position = (100, 100)
    main.purchase_tower(test_level, kind, position)
    gold_after_purchase = test_level.get_current_gold()

    test_tower = test_level.existing_towers[0]
    main.sell_tower(test_level, test_tower)
    gold_after_sale = test_level.get_current_gold()

    assert gold_after_sale > gold_after_purchase
    assert gold_after_sale < gold_before_purchase

def test_spawn_wave_adds_creatures_to_existing_creatures():
    test_level_1 = level.Level(1)

    number = 1
    main.spawn_wave_number(test_level_1, number)
    assert len(test_level_1.existing_creatures) == test_level_1.waves[0][2]
    
    number = 3
    main.spawn_wave_number(test_level_1, number)
    assert len(test_level_1.existing_creatures) == test_level_1.waves[0][2] + test_level_1.waves[2][2]

    for test_creature in test_level_1.existing_creatures:
        assert isinstance(test_creature, creature.Skeleton)

    test_level_2 = level.Level(2)
    
    number = 0
    main.spawn_wave_number(test_level_2, number)

def test_spawn_spreads_creatures_out():
    spread = 20

    test_level = level.Level(1)

    number = 1
    main.spawn_wave_number(test_level, number)
    for counter in range(len(test_level.existing_creatures) - 1):
        if counter < 0:
            counter = 0
        creature_1 = test_level.existing_creatures[counter]
        creature_2 = test_level.existing_creatures[counter + 1]
        assert creature_1.distance_from(creature_2) >= spread

def test_game_tick_calls_tick_on_entities_with_cycle_time():
    mock_creatures_positions = [(80, 80), (90, 90), (110, 110), (120, 120)]
    mock_creatures = []   
    for position in mock_creatures_positions:
        temp_mock_creature = entity.Entity(position)
        temp_mock_creature.tick = unittest.mock.MagicMock(name='tick')
        mock_creatures.append(temp_mock_creature)


    mock_towers_positions = [(85, 80), (95, 90), (115, 110), (125, 120)]
    mock_towers = []
    for position in mock_towers_positions:
        temp_mock_tower = entity.Entity(position)
        temp_mock_tower.tick = unittest.mock.MagicMock(name='tick')
        mock_towers.append(temp_mock_tower)

    mock_level = level.Level(1)
    mock_level.existing_creatures = mock_creatures
    mock_level.existing_towers = mock_towers


    cycle_time = .016

    main.game_tick(mock_level, cycle_time)

    for mock_creature in mock_creatures:
        mock_creature.tick.assert_called_with(cycle_time)
    for mock_tower in mock_towers:
        mock_tower.tick.assert_called_with(cycle_time)

# Creature Tests
def test_creature_initializes_correctly():
    position = (0, 0)
    test_path = [(100,100), (200,200)]
    test_creature = creature.Creature(position, test_path)

    assert isinstance(test_creature, entity.Entity)
    assert test_creature.x == position[0]
    assert test_creature.y == position[1]
    assert len(test_creature.status_effects) == 0
    assert test_creature.path == test_path
    test_path.append((300,300))
    assert test_creature.path != test_path

def test_skeleton_initializes_correctly():
    position = (0, 0)
    test_path = [(100,100), (200,200)]
    test_skeleton = creature.Skeleton(position, test_path)

    assert test_skeleton.x == position[0]
    assert test_skeleton.y == position[1]
    assert len(test_skeleton.status_effects) == 0

    assert test_skeleton.max_health == 25
    assert test_skeleton.current_health == test_skeleton.max_health
    assert test_skeleton.default_move_speed == 1
    assert test_skeleton.move_speed == test_skeleton.default_move_speed
    assert test_skeleton.foe == True
    assert test_skeleton.life_damage == 1
    assert test_skeleton.value == 10
    assert test_skeleton.image_postfix != ""
    assert test_skeleton.path == test_path

def test_accelerator_initializes_correctly():
    position = (0,0)
    test_path = [(100,100), (200,200)]
    test_accelerator = creature.Accelerator(position, test_path)

    assert test_accelerator.x == position[0]
    assert test_accelerator.y == position[1]
    assert len(test_accelerator.status_effects) == 0

    assert test_accelerator.max_health == 10
    assert test_accelerator.current_health == test_accelerator.max_health
    assert test_accelerator.default_move_speed == 1
    assert test_accelerator.move_speed == test_accelerator.default_move_speed
    assert test_accelerator.foe == True
    assert test_accelerator.life_damage == 1
    assert test_accelerator.value == 20
    assert test_accelerator.image_postfix != ""
    assert test_accelerator.path == test_path
    assert test_accelerator.acceleration_counter == 0

    assert test_accelerator.width == 5
    assert test_accelerator.height == 5

def test_accelerator_tick_calls_accelerate_with_time_passed():
    position = (100, 100)
    path = [(200, 200)]
    test_accelerator = creature.Accelerator(position, path)
    test_accelerator.accelerate = unittest.mock.MagicMock(name="accelerate")

    test_accelerator.tick(1)

    test_accelerator.accelerate.assert_called_with(1)
    
def test_acclerator_accelerate_waits_one_second_to_increase_move_speed():
    position = (100, 100)
    path = [(200, 200)]
    test_accelerator = creature.Accelerator(position, path)
    test_accelerator.move_speed = 1
    original_move_speed = test_accelerator.move_speed

    test_accelerator.accelerate(1-.00000001)

    assert test_accelerator.move_speed == original_move_speed

def test_accelerator_accelerate_increases_move_speed_every_second():
    position = (100, 100)
    path = [(200, 200)]
    test_accelerator = creature.Accelerator(position, path)
    test_accelerator.move_speed = 1

    test_accelerator.accelerate(1)

    assert test_accelerator.move_speed == 2

def test_accelerator_accelerate_accumulates_fractions_of_seconds():
    position = (100, 100)
    path = [(200, 200)]
    test_accelerator = creature.Accelerator(position, path)
    test_accelerator.move_speed = 1
    original_move_speed = test_accelerator.move_speed

    test_accelerator.tick(.2)
    test_accelerator.tick(.2)
    test_accelerator.tick(.2)
    test_accelerator.tick(.2)
    test_accelerator.tick(.2)

    assert test_accelerator.move_speed > original_move_speed

def test_accelerator_accelerate_resets_accumulation_after_increasing_speed():
    position = (100, 100)
    path = [(200, 200)]
    test_accelerator = creature.Accelerator(position, path)
    test_accelerator.move_speed = 1

    test_accelerator.accelerate(1)
    modified_speed = test_accelerator.move_speed

    test_accelerator.accelerate(.2)

    assert test_accelerator.move_speed == modified_speed
    

def test_troll_initializes_correctly():
    position = (150, 200)
    test_path = [(300, 300)]
    test_troll = creature.Troll(position, test_path)

    assert test_troll.x == position[0]
    assert test_troll.y == position[1]
    assert len(test_troll.status_effects) == 0
    assert test_troll.foe == True

    assert test_troll.max_health == 500
    assert test_troll.current_health == test_troll.max_health
    assert test_troll.default_move_speed == 1
    assert test_troll.move_speed == test_troll.default_move_speed
    assert test_troll.life_damage == 10
    assert test_troll.value == 100
    assert test_troll.image_postfix != ""
    assert test_troll.path == test_path

    assert test_troll.width == 20
    assert test_troll.height == 40

@pytest.mark.parametrize("creature_type", creature_types_list)
def test_creature_is_alive_returns_False_after_death(creature_type):
    position, test_path = (0, 0), []

    test_creature = getattr(creature, creature_type)(position, test_path)
    assert test_creature.is_alive() == True

    test_creature.die()
    assert test_creature.is_alive() == False

def test_get_next_point_returns_next_point():
    test_path = [(-100, -100), (0, 200), (100, 100)]
    test_creature = creature.Creature((0, 0), test_path)
    assert test_creature.next_point == (100,100)
    test_creature.update_next_point()
    assert test_creature.next_point == (0, 200)
    test_creature.update_next_point()
    assert test_creature.next_point == (-100, -100)
    test_creature.update_next_point()
    assert test_creature.next_point is None

@pytest.mark.parametrize("creature_type", creature_types_list)
def test_creature_moves_toward_next_point_in_path(creature_type):
    position, test_path = (0, 0), [(-100, -100), (0, 200), (100, 100)]

    test_creature = getattr(creature, creature_type)(position, test_path)
    while test_creature.next_point != None:        
        original_distance = test_creature.distance_from(test_creature.next_point)
        test_creature.move()
        assert test_creature.distance_from(test_creature.next_point) < original_distance
        test_creature.update_next_point()

@pytest.mark.parametrize("creature_type", creature_types_list)
def test_creature_updates_point_when_next_point_is_reached(creature_type):
    position, test_path = (100, 100), [(0,0), (121, 300), (200,200), (100, 100)]

    test_creature = getattr(creature, creature_type)(position, test_path)

    test_creature.move()
    assert test_creature.next_point == (200, 200)

    test_creature.x, test_creature.y = 200, 200
    test_creature.move()
    assert test_creature.next_point == (121, 300)

    test_creature.x, test_creature.y = (121 + (.5*test_creature.move_speed)), (300 - (.5*test_creature.move_speed))
    test_creature.move()
    assert test_creature.next_point == (0,0)

@pytest.mark.parametrize("creature_type", creature_types_list)
def test_creature_stops_moving_when_path_ends(creature_type):
    position, test_path = (100, 100), [(100, 100)]

    test_creature = getattr(creature, creature_type)(position, test_path)
    assert test_creature.next_point == (100, 100)
    test_creature.move()
    assert test_creature.next_point is None
    test_creature.move()

# Test with base class only and do not parametrize: some creatures may not 
# die at end of path
def test_Creature_dies_when_path_ends():
    test_creature = creature.Creature((0, 0), [])
    test_creature.current_health = 10
    test_creature.move()

    assert test_creature.is_alive() == False


