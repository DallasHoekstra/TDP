import entity

class Tower(entity.Entity):

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

    def spawn(self):
        pass

    def despawn(self):
        pass


class Fire_Tower(Tower):
    max_health = 100
    name = "FIRE_TOWER"
    range_ = 100

    def __init__(self, position):
        self.current_health = self.max_health
        self.status_affects = []
        self.x, self.y = position[0], position[1]

class Ice_Tower(Tower):
    max_health = 100
    name = "Ice_Tower"
    range_ = 300

    def __init__(self, position):
        self.current_health = self.max_health
        self.status_affects = []
        self.x, self.y = position[0], position[1]

class Arrow_Tower(Tower):
    max_health = 100
    name = "Arrow_Tower"
    range_ = 500

    def __init__(self, position):
        self.current_health = self.max_health
        self.status_affects = []
        self.x, self.y = position[0], position[1]