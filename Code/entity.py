import math

class Entity():
    x, y = 0,0
    max_health = 0
    current_health = 0
    name = ""
    range_ = 0
    foe = True
    image_path = ""

    def __init__(self, position):
        self.status_affects = []
        self.x, self.y = position[0], position[1]

    def target(self, entities):
        for entity in entities:
            if (math.sqrt(pow((entity.x - self.x), 2) + pow((entity.y - self.y), 2)) < self.range_):
                return entity

    def attack(self):
        pass

    def set_position(self, position):
        pass

    def get_position(self):
        pass

    def move(self):
        pass

    def set_health(self, number):
        pass

    def get_health(self):
        pass

    def change_health(self, number):
        pass

    def draw(self):
        return (self.image_path, (self.x, self.y))

    def spawn(self):
        pass

    def despawn(self):
        pass

    def isFoe(self):
        return self.foe

