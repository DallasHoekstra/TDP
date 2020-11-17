import entity

class SpellBolt(entity.Entity):
    damage = 0
    element = ""
    default_move_speed = 0
    move_speed = 0
    image_postfix = "Ice_Shard.gif"

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
        self.target_list.remove(target)

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
    image_postfix = "Ice_Shard.gif"
    default_move_speed = 2
    move_speed = default_move_speed
    width = 5
    height = 5

class ArrowBolt(SpellBolt):
    damage = 2
    element = "Piercing"
    image_postfix = "Arrow.gif"
    default_move_speed = 2
    move_speed = default_move_speed
    width = 5
    height = 5

# class Fire_Attack(Attack):
#     range_ = tower.Fire_Tower.range_
#     image_path = image_path + "Fire_Attack.gif"
#     attack_image = pygame.image.load(image_path)
#     attack_image.set_alpha(100)

#     def __init__(self, x_ord, y_ord):
#         self.x = x_ord
#         self.y = y_ord
#         self.damage = tower.Fire_Tower.damage
#         self.damage_Type = tower.Fire_Tower.damage_type
#         self.move_Speed = 0
    
#     def hit(self, creature):
#         # FOR FUTURE: possibly add on-hit animation that is different from the attack animation?
    
#         # apply damage 
#         # FOR FUTURE: work out how to handle vulnerabilities, resistances, immunities, etc
#         creature.health -= self.damage

#     def draw(self, window):
#         window.blit(self.attack_image, (self.x, self.y))


