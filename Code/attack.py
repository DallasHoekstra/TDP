import entity

class SpellBolt(entity.Entity):
    damage = 0
    element = ""
    default_move_speed = 0
    move_speed = 0

    def __init__(self, position, target):
        self.x = position[0]
        self.y = position[1]
        self.targets = [target]


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


