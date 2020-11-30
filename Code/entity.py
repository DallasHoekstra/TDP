import math

class Entity():
    x, y = 0,0
    default_move_speed = 0
    move_speed = 0
    max_health = 0
    current_health = 0
    name = ""
    range_ = 0
    foe = True
    image_postfix = ""
    attack_image_postfix = ""
    attack_draw_duration = 0
    width = 0
    height = 0
    fire_rate = 1
    cooldown_time = round(1/fire_rate, 5)
    cooldown_time_left = 0
    
 

    def __init__(self, position):
        self.status_effects = []
        self.x, self.y = position[0], position[1]
        self.target_list = []
    
    def update_targets(self, entities):
        if entities == []:
            for target in self.target_list:
                self.target_list.remove(target)
        else:
            self.remove_invalid_targets(entities)
            self.acquire_targets(entities)

    def acquire_targets(self, entities):
        for entity in entities:
            if self.distance_from(entity) < self.range_ and entity.is_alive():
                if self.has_target() == False:
                    self.target_list.append(entity)

    def remove_invalid_targets(self, entities):
        for entity in entities:
            for target in self.target_list:
                self.target_list.remove(target)
                if entity is target:
                    if (self.distance_from(entity) < self.range_) and entity.is_alive():
                        self.target_list.append(entity)
                break
            
    def can_attack(self):
        if self.cooldown_time_left > 0:
            return False
        else: 
            return True

    def has_target(self):
        if self.target_list == False:
            return False
        else:
            for target in self.target_list:
                if target.is_alive():
                    return True
            return False

    def attack(self):
        spell_bolts = []
        self.cooldown_time_left = self.cooldown_time
        return spell_bolts

    # FOR FUTURE: consider implementing with dictionary to have named keys instead of numbers
    # FOR FUTURE: alternately, consider creating status class to manage more complex effects
    def add_status_effect(self, effect_type, duration, severity):
        self.status_effects.append([str(effect_type), duration, severity])

    def apply_status_effect(self, effect_type, duration, severity):
        if effect_type == "Ice":
            new_slow_speed = self.default_move_speed/severity
            if self.move_speed > new_slow_speed:
                self.move_speed = new_slow_speed
        else: 
            self.change_health_by(-1*severity)

    def end_status_effect(self, effect_type, duration, severity):
        self.move_speed = self.default_move_speed

    def set_position(self, position):
        pass

    def get_position(self):
        return (self.x, self.y)

    def move(self):
        pass

    def set_health(self, number):
        pass

    def get_health(self):
        pass

    def change_health_by(self, number):
        if number < 0:
            if self.current_health + number >= 0:
                    self.current_health += number
            else:
                self.current_health = 0
        elif self.current_health + number < self.max_health:
            self.current_health += number

    def draw(self):
        return (self.image_postfix, (self.x, self.y))
    
    def should_draw_attack(self):
        if self.cooldown_time_left >= self.cooldown_time - self.attack_draw_duration:
            return True
        else: 
            return False

    def spawn(self):
        pass

    def despawn(self):
        pass

    def collision(self, collidee):
        if isinstance(collidee, Entity):
            x_diff = abs(self.x - collidee.x)
            y_diff = abs(self.y - collidee.y)
            if min(self.width, collidee.width) > x_diff and min(self.height, collidee.height) > y_diff:
                return True
            else:
                return False
        elif isinstance(collidee, tuple):
            point_x, point_y = collidee
            if (point_x >= self.x and point_x <= self.x + self.width) and (point_y >= self.y and point_y <= self.y + self.height):
                return True
            else:
                return False

    def tick(self, time_passed):
        self.cooldown_time_left -= time_passed

        # FOR FUTURE: Is this pythonic?
        counter = 0
        while (counter < len(self.status_effects)):
            effect = self.status_effects[counter]
            effect[1] -= time_passed
            if effect[1] > 0:
                self.apply_status_effect(effect[0], effect[1], effect[2])
                counter += 1
            else:
                self.status_effects.remove(effect)

    def is_foe(self):
        return self.foe

    def is_alive(self):
        return self.current_health > 0

    def die(self):
        self.current_health = 0

    def distance_from(self, point):
        if isinstance(point, Entity):
            return math.sqrt(math.pow(abs(self.x - point.x), 2) + math.pow(abs(self.y - point.y), 2))
        else:
            return math.sqrt(math.pow(abs(self.x - point[0]), 2) + math.pow(abs(self.y - point[1]), 2))