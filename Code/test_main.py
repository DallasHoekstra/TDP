import time

import pytest
import pytest_mock

import gameclock as gc
import main
import entity
import tower
import level


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
    cycle_1 = game_clock.get_current_time()
    cycle_2 = game_clock.get_current_time()
    assert cycle_1 < cycle_2
    
def test_clock_ticks_at_least_cycle_length():
    game_clock = gc.GameClock(60)
    cycle_1 = game_clock.get_current_time()
    game_clock.tick()
    cycle_2 = game_clock.get_current_time()
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




# Tower Tests
def test_entity_uses_proper_GUI_formatting():
    test_entity = entity.Entity((100,200))
    image_path, position = test_entity.draw()
    assert isinstance(image_path, str)
    assert isinstance(position, tuple)
    assert isinstance(position[0], int or float)
    assert isinstance(position[1], int or float)

def test_entity_taret_returns_None_if_no_available_targets():
    test_entities = [entity.Entity((100,100)), entity.Entity((200,200))]
    test_targeting_entity = entity.Entity((800,800))
    assert test_targeting_entity.target(test_entities) is None

def test_entity_targets_first_within_range_by_default():
    nearest = (100, 200)
    position_2 = (100, 400)
    position_3 = (400, 400)

    test_entities = [entity.Entity(nearest), entity.Entity(position_2), entity.Entity(position_3)]
    test_targeting_entity = entity.Entity((150, 250))
    test_targeting_entity.range_ = 100

    target = test_targeting_entity.target(test_entities)
    
    assert isinstance(target, entity.Entity)
    assert target == test_entities[0]

    new_nearest = (115, 215)
    test_entities.append(entity.Entity(new_nearest))

    assert test_targeting_entity.target(test_entities) == test_entities[0]

    test_entities.remove(test_entities[0])
    assert test_targeting_entity.target(test_entities) == test_entities[2]




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


