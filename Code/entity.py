import math

class Entity():
    x, y = 0,0
    max_health = 0
    current_health = 0
    name = ""
    range_ = 0
    foe = True
    image_postfix = ""
    width = 0
    height = 0
    cooldown_time_left = 0
 

    def __init__(self, position):
        self.status_affects = []
        self.x, self.y = position[0], position[1]
        ## FOR FUTURE: Refactor name to target_list for clarity in boolean checks
        self.target = []

    # FOR FUTURE: Refactor name to "update_targets"
    def acquire_targets(self, entities):
        if entities == []:
            for target in self.target:
                self.target.remove(target)

        else:
            for entity in entities:
                for target in self.target:
                    self.target.remove(target)
                    if entity is target:
                        self.target.append(entity)
            for entity in entities:
                if (self.distance_from(entity) < self.range_) and entity.is_alive():
                    if self.has_target() == False:
                        self.target.append(entity)
                else:
                    for target in self.target:
                        if entity is target:
                            self.target.remove(entity)

    def can_attack(self):
        if self.cooldown_time_left > 0:
            return False
        else: 
            return True

    def has_target(self):
        if self.target == False:
            return False
        else:
            for target in self.target:
                if target.is_alive():
                    return True
            return False

    def attack(self):
        pass

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

    def change_health(self, number):
        pass

    def draw(self):
        return (self.image_postfix, (int(self.x - (self.width/2)) , int(self.y - (self.height/2))))

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