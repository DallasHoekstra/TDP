import entity

class SpellBolt(entity.Entity):
    damage = 0
    element = ""
    default_move_speed = 0
    move_speed = 0
    image_postfix = "Ice_Shard.gif"
    inflicts_status_effect = False

    def __init__(self, position, targets):
        self.x = position[0]
        self.y = position[1]
        self.target_list = targets.copy()

    def remove_invalid_targets(self, entities):
        for entity in entities:
            for target in self.target_list:
                self.target_list.remove(target)
                if entity is target:
                    if entity.is_alive():
                        self.target_list.append(entity)
                break

    def is_alive(self):
        if len(self.target_list) > 0:
            return True
        else:
            return False

    def can_attack(self):
        if self.target_list != []:
            for target in self.target_list:
                if self.collision(target):
                    return True
            return False
        else:
            return False
        # else:
        #     return False

    def attack(self):
        target = self.target_list[0]
        target.change_health_by(-1*self.damage)
        if self.inflicts_status_effect:
            status_effect = self.generate_status_effect()
            target.add_status_effect(status_effect[0], status_effect[1], status_effect[2])
        self.target_list.remove(target)

    def generate_status_effect(self):
        return [False, False, False]

    def move(self):
        if self.x > self.target_list[0].x:
            self.x -= 1
        elif self.x < self.target_list[0].x:
            self.x += 1
        if self.y > self.target_list[0].y:
            self.y -= 1
        elif self.y < self.target_list[0].y:
            self.y += 1

class IceBolt(SpellBolt):
    damage = 10
    element = "Ice"
    duration = 5
    severity = 2
    inflicts_status_effect = True
    image_postfix = "Ice_Shard.gif"
    default_move_speed = 5
    move_speed = default_move_speed
    width = 5
    height = 5

    def generate_status_effect(self):
        return [self.element, self.duration, self.severity]

class ArrowBolt(SpellBolt):
    damage = 2
    element = "Piercing"
    image_postfix = "Arrow.gif"
    default_move_speed = 5
    move_speed = default_move_speed
    width = 5
    height = 5




