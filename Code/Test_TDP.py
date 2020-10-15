import pytest
import TDP as TDP
import tower as twr
import creature as crt


def test_window():
    pass

def test_creature_class():
    x_ord = 10
    y_ord = 15
    creature = crt.Creature(x_ord, y_ord)
    assert creature.x == 10
    assert creature.y == 15
    assert creature.attack == 0
    assert creature.speed == 0
    assert creature.health == 0

    x_ord = 15
    y_ord = 20
    test_skeleton = crt.Skeleton(x_ord, y_ord)
    assert test_skeleton.x == x_ord
    assert test_skeleton.y == y_ord
    assert test_skeleton.health == 25
    assert test_skeleton.attack == 5
    assert test_skeleton.speed == 10
    



def test_tower_class():
    x_ord = 10
    y_ord = 15

    # Create a fire tower object to test
    test_tower_1 = twr.Fire_Tower(x_ord, y_ord)

    # Test tower initialization
    assert test_tower_1.x == 10
    assert test_tower_1.y == 15
    assert test_tower_1.kind == "Fire"
    assert test_tower_1.value == 100

def test_fire_tower_class():
    x_ord = 20
    y_ord = 22
    
    test_fire_tower = twr.Fire_Tower(x_ord, y_ord)
    
    assert test_fire_tower.x == 20
    assert test_fire_tower.y == 22
    assert test_fire_tower.damage == 1
    assert test_fire_tower.range_ == 200
    assert test_fire_tower.attack_rate == .5

def test_purchase_tower():
    gold = 10000
    existing_test_towers = []
    test_fire_tower_1 = twr.Fire_Tower(100, 100)
    existing_test_towers.append(test_fire_tower_1)

    assert existing_test_towers[0] is test_fire_tower_1

    # Create the towers
    TDP.purchase_Tower("Fire", existing_test_towers, (200,200), gold)
    TDP.purchase_Tower("Ice", existing_test_towers, (300,300), gold)
    TDP.purchase_Tower("Arrow", existing_test_towers, (400,400), gold)
    TDP.purchase_Tower("Wall", existing_test_towers, (500,500), gold)

    # Test typing and initialization
    assert isinstance(existing_test_towers[1], twr.Tower)
    assert isinstance(existing_test_towers[1], twr.Fire_Tower)
    assert existing_test_towers[1].x == 200
    assert existing_test_towers[1].y == 200

    assert isinstance(existing_test_towers[2], twr.Tower)
    assert isinstance(existing_test_towers[2], twr.Ice_Tower)
    assert existing_test_towers[2].x == 300
    assert existing_test_towers[2].y == 300

    assert isinstance(existing_test_towers[3], twr.Tower)
    assert isinstance(existing_test_towers[3], twr.Arrow_Tower)
    assert existing_test_towers[3].x == 400
    assert existing_test_towers[3].y == 400

    assert isinstance(existing_test_towers[4], twr.Tower)
    assert isinstance(existing_test_towers[4], twr.Wall)
    assert existing_test_towers[4].x == 500
    assert existing_test_towers[4].y == 500

    # Test collision detection for tower placement
    assert TDP.purchase_Tower("Ice", existing_test_towers, (200, 200), gold) == ("Ice", gold)

    # Test for purchasing towers with insufficient funds
    assert TDP.purchase_Tower("Fire", existing_test_towers, (600,600), 50) == ("Fire", 50)
    assert TDP.purchase_Tower("Fire", existing_test_towers, (600,600), 100) == ("", 0)



    


