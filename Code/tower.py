import entity
import attack
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
    width = 40
    height = 42
    
    def __init__(self, position):
        self.status_affects = []
        self.x, self.y = position[0], position[1]
        self.current_health = self.max_health
        self.target_list = []

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

    def draw_attack(self):
        position = (self.x, self.y)
        return [self.attack_image_postfix, position]
    

class Fire_Tower(Tower):
    cost = 100
    max_health = 100
    name = "FIRE_TOWER"
    image_postfix = "FireTowerL0.gif"
    attack_image_postfix = "Fire_Attack.gif"
    attack_draw_duration = .2
    fire_rate = 2
    cooldown_time = round(1/fire_rate, 5)
    cooldown_time_left = 0
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
        self.cooldown_time_left = self.cooldown_time
        return []
            


class Ice_Tower(Tower):
    cost = 150
    max_health = 100
    name = "ICE_TOWER"
    image_postfix = "IceTowerL0.gif"
    attack_image_postfix = "Ice_Shard.gif"
    attack_draw_duration = 1
    damage = 5
    fire_rate = .5
    cooldown_time = round(1/fire_rate, 5)
    cooldown_time_left = 0
    range_ = 300*math.sqrt(2)

    def __init__(self, position):
        self.current_health = self.max_health
        self.status_affects = []
        self.x, self.y = position[0], position[1]
        self.target_list = []
        
    def attack(self):
        if len(self.target_list) > 0:
            bolt_position = self.x, self.y
            bolt_target = [self.target_list[0]]
            Ice_Bolt = [attack.IceBolt(bolt_position, bolt_target)]
            self.cooldown_time_left = self.cooldown_time
            return Ice_Bolt
        else:
            return []
    
class Arrow_Tower(Tower):
    cost = 150
    max_health = 100
    name = "ARROW_TOWER"
    image_postfix = "ArrowTowerL0.gif"
    attack_image_postfix = "Arrow.gif"
    attack_draw_duration = 1
    damage = 5
    fire_rate = .5
    cooldown_time = round(1/fire_rate, 5)
    cooldown_time_left = 0
    range_ = 500*math.sqrt(2)
    

    def __init__(self, position):
        self.current_health = self.max_health
        self.status_affects = []
        self.x, self.y = position[0], position[1]
        self.target_list = []

    def attack(self):
        if len(self.target_list) > 0:
            bolt_position = self.x, self.y
            bolt_target = [self.target_list[0]]
            ArrowBolt = [attack.ArrowBolt(bolt_position, bolt_target)]
            self.cooldown_time_left = self.cooldown_time
            return ArrowBolt
        else:
            return []