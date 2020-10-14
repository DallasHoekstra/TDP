import pytest
import Code.TDP as TDP

@pytest.fixture
def test_window():
    pass

def test_creature_class():
    x_ord = 10
    y_ord = 15
    creature = TDP.Creature(x_ord, y_ord)
    assert creature.x == 10
    assert creature.y == 15

def test_tower_class():
    x_ord = 10
    y_ord = 15

    # Create a fire tower object to test
    test_tower_1 = TDP.Tower(x_ord, y_ord, "Fire")

    # Test tower initialization
    assert test_tower_1.x == 10
    assert test_tower_1.y == 15
    assert test_tower_1.tower_kind == "Fire"
    assert test_tower_1.value == 100

def test_fire_tower_class():
    x_ord = 20
    y_ord = 22
    
    test_fire_tower = TDP.Fire_Tower(x_ord, y_ord)
    
    assert test_fire_tower.x == 20
    assert test_fire_tower.y == 22
    assert test_fire_tower.damage == 1
    assert test_fire_tower.range_ == 200
    assert test_fire_tower.attack_rate == .5

def test_purchase_tower():
    existing_test_towers = []
    test_fire_tower_1 = TDP.Fire_Tower(100, 100)
    existing_test_towers.append(test_fire_tower_1)

    assert existing_test_towers[0] is test_fire_tower_1

    TDP.purchase_Tower("Fire", existing_test_towers, (200,200))
    TDP.purchase_Tower("Ice", existing_test_towers, (300,300))

    assert isinstance(existing_test_towers[1], TDP.Tower)
    assert isinstance(existing_test_towers[1], TDP.Fire_Tower)
    assert existing_test_towers[1].x == 200
    assert existing_test_towers[1].y == 200

    assert isinstance(existing_test_towers[2], TDP.Tower)
    assert isinstance(existing_test_towers[2], TDP.Ice_Tower)
    assert existing_test_towers[2].x == 300
    assert existing_test_towers[2].y == 300


    pass

    


