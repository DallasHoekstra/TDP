import entity
import math

class Tower(entity.Entity):
    cost = 0
    refund_rate = .5
    x, y = 0,0
    max_health = 0
    current_health = 0
    name = ""
    range_ = 0
    foe = False
    image_postfix = ""
    width = 40
    height = 42
    
    def __init__(self, position):
        self.status_affects = []
        self.x, self.y = position[0], position[1]
        self.current_health = self.max_health

    def set_position(self, position):
        pass

    def move(self):
        pass

    def set_health(self, number):
        pass

    def get_health(self):
        pass

    def change_health(self, number):
        pass

    def spawn(self):
        pass

    def despawn(self):
        pass

    def get_value(self):
        return self.cost

class Fire_Tower(Tower):
    cost = 100
    max_health = 100
    name = "FIRE_TOWER"
    image_postfix = "FireTowerL0.gif"
    range_ = 100*math.sqrt(2)
    damage = 1

    def __init__(self, position):
        self.current_health = self.max_health
        self.status_affects = []
        self.x, self.y = position[0], position[1]
        self.target_list = []

    def acquire_targets(self, entities):
        for entity in entities:
            if self.distance_from(entity) <= self.range_ and entity.is_alive():
                self.target_list.append(entity)


    def attack(self):
        for target in self.target_list:
            target.change_health_by(-1*self.damage)
            



class Ice_Tower(Tower):
    cost = 150
    max_health = 100
    name = "Ice_Tower"
    image_postfix = "IceTowerL0.gif"
    range_ = 300

    def __init__(self, position):
        self.current_health = self.max_health
        self.status_affects = []
        self.x, self.y = position[0], position[1]
        

    






class Arrow_Tower(Tower):
    cost = 150
    max_health = 100
    name = "Arrow_Tower"
    image_postfix = "ArrowTowerL0.gif"
    range_ = 500

    def __init__(self, position):
        self.current_health = self.max_health
        self.status_affects = []
        self.x, self.y = position[0], position[1]