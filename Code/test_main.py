import time
import math


import pytest
import pytest_mock

import gameclock as gc
import main
import entity
import tower
import level
import creature

# List of creatures. Used in parametrized tests
creature_types_list = ["Skeleton", "Accelerator"]


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

def test_clock_converts_current_time_to_seconds():
    clock = gc.GameClock(60)
    time = clock.get_current_time()
    time_in_seconds = clock.in_seconds(time)
    assert isinstance(time_in_seconds, int)


# Entity Tests
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


#Level Tests
def test_gold_can_be_increased():
    test_level = level.Level(1)
    initial_gold = test_level.get_current_gold()
    test_level.increase_gold_by(100)
    new_gold = test_level.get_current_gold()

    assert new_gold == initial_gold + 100

def test_gold_can_be_decreased():
    test_level = level.Level(1)
    initial_gold = test_level.get_current_gold()
    test_level.decrease_gold_by(100)
    new_gold = test_level.get_current_gold()

    assert new_gold == initial_gold - 100

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


# Creature Tests
def test_creatures_initializes_correctly():
    x_ord, y_ord = 0, 0
    test_path = [(100,100), (200,200)]
    test_creature = creature.Creature(x_ord, y_ord, test_path)

    assert isinstance(test_creature, entity.Entity)
    assert test_creature.x == x_ord
    assert test_creature.y == y_ord
    assert len(test_creature.conditions) == 0
    assert test_creature.path == test_path
    test_path.append((300,300))
    assert test_creature.path != test_path

def test_skeleton_initializes_correctly():
    x_ord, y_ord = 0, 0
    test_path = [(100,100), (200,200)]
    test_skeleton = creature.Skeleton(x_ord,y_ord, test_path)

    assert test_skeleton.x == x_ord
    assert test_skeleton.y == y_ord
    assert len(test_skeleton.conditions) == 0

    assert test_skeleton.max_health == 25
    assert test_skeleton.health == test_skeleton.max_health
    assert test_skeleton.default_move_speed == 1
    assert test_skeleton.move_speed == test_skeleton.default_move_speed
    assert test_skeleton.foe == True
    assert test_skeleton.life_damage == 1
    assert test_skeleton.value == 10
    assert test_skeleton.image_postfix != ""
    assert test_skeleton.path == test_path

def test_accelerator_initializes_correctly():
    x_ord, y_ord = 0,0
    test_path = [(100,100), (200,200)]
    test_accelerator = creature.Accelerator(x_ord, y_ord, test_path)

    assert test_accelerator.x == x_ord
    assert test_accelerator.y == y_ord
    assert len(test_accelerator.conditions) == 0

    assert test_accelerator.max_health == 10
    assert test_accelerator.health == test_accelerator.max_health
    assert test_accelerator.default_move_speed == 1
    assert test_accelerator.move_speed == test_accelerator.default_move_speed
    assert test_accelerator.foe == True
    assert test_accelerator.life_damage == 1
    assert test_accelerator.value == 20
    assert test_accelerator.image_postfix != ""
    assert test_accelerator.path == test_path
    assert test_accelerator.acceleration_counter == 0

@pytest.mark.parametrize("creature_type", creature_types_list)
def test_creature_is_alive_returns_true_when_it_should(creature_type):
    x_ord, y_ord, test_path = 0, 0, []

    test_creature = getattr(creature, creature_type)(x_ord, y_ord, test_path)
    assert test_creature.is_alive() == True

    test_creature.die()
    assert test_creature.is_alive() == False

@pytest.mark.parametrize("creature_type", creature_types_list)
def test_creature_moves_toward_next_point_in_path(creature_type):
    x_ord, y_ord, test_path = 0, 0, [(100, 100)]

    test_creature = getattr(creature, creature_type)(x_ord, y_ord, test_path)
    
    test_creature.move()

    assert test_creature.x > 0
    assert test_creature.y > 0

