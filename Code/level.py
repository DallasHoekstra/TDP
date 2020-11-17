class Level():
    health = 20
    background_image = ""
    starting_gold = 0
    current_gold = 0
    level_width = 1000
    level_height = 800
    village_postfix = "L0_Village.jpg"
    village = [.5*level_width, .875*level_height, 50, 50]
    village_relative = [.5, .875, 50, 50]
    background_image = "L1_Background.png"
    def __init__(self, level_number):
        self.existing_towers = []
        self.existing_creatures = []
        self.existing_attacks = []
        self.spellbolts = []
        if level_number == 1:
            self.starting_gold = 2000
            self.spawn_points = [(720, 10), (140, 10)]
            self.enemy_paths = [[(int(self.village[0] + 25), int(self.village[1] + 25)), (475, 660), (450, 625), (425, 590), 
                                    (400, 540), (445, 520), (490, 490), (565, 430), (650, 360), (775, 285), (700, 285), (615, 255), (585,225), (585,155), (725, 130)], 
                                [(int(self.village[0] + 25), int(self.village[1] + 25)), (475, 660), (450, 625), (425, 590), 
                                    (400, 540), (330, 515), (260, 500), (190, 490), (120, 470), (130, 330), (370, 330), (370, 240), (240, 240), (140, 160)] 
                                ]
            self.waves = [(5, "Skeleton", 10, self.spawn_points[1], self.enemy_paths[1]), (15, "Skeleton", 10, self.spawn_points[0], self.enemy_paths[0]), 
                                (30, "Skeleton", 20, self.spawn_points[0], self.enemy_paths[0]), (40, "Skeleton", 20, self.spawn_points[1], self.enemy_paths[1])]
        elif level_number == 2:
            self.starting_gold = 3000
            self.spawn_points = [(720, 10), (140, 10)]
            self.enemy_paths = [[(int(self.village[0] + 25), int(self.village[1] + 25)), (475, 660), (450, 625), (425, 590), 
                                        (400, 540), (445, 520), (490, 490), (565, 430), (650, 360), (775, 285), (700, 285), (615, 255), (585,225), (585,155), (725, 130)], 
                                [(int(self.village[0] + 25), int(self.village[1] + 25)), (475, 660), (450, 625), (425, 590), 
                                        (400, 540), (330, 515), (260, 500), (190, 490), (120, 470), (130, 330), (370, 330), (370, 240), (240, 240), (140, 160)] 
                                ]
            self.waves = [(5, "Accelerator", 10, self.spawn_points[1], self.enemy_paths[1]), (15, "Skeleton", 10, self.spawn_points[0], self.enemy_paths[0]), 
                                (20, "Skeleton", 20, self.spawn_points[0], self.enemy_paths[0]), (30, "Skeleton", 40, self.spawn_points[1], self.enemy_paths[1]),
                                (35, "Skeleton", 40, self.spawn_points[1], self.enemy_paths[1])]
        elif level_number == 3:
            self.starting_gold = 3000
            self.spawn_points = [(720, 10), (140, 10)]
            self.enemy_paths = [[(int(self.village[0] + 100), int(self.village[1] + 100)), (475, 660), (450, 625), (425, 590), 
                                        (400, 540), (445, 520), (490, 490), (565, 430), (650, 360), (775, 285), (700, 285), (615, 255), (585,225), (585,155), (725, 130)], 
                                [(int(self.village[0] + 100), int(self.village[1] + 100)), (475, 660), (450, 625), (425, 590), 
                                        (400, 540), (330, 515), (260, 500), (190, 490), (120, 470), (130, 330), (370, 330), (370, 240), (240, 240), (140, 160)] 
                                ]
            self.waves = [(5, "Skeleton", 10, self.spawn_points[1], self.enemy_paths[1]), (1, "Troll", 2, self.spawn_points[0], self.enemy_paths[0]), 
                                (20, "Skeleton", 20, self.spawn_points[0], self.enemy_paths[0]), (30, "Skeleton", 40, self.spawn_points[1], self.enemy_paths[1]),
                                (35, "Skeleton", 40, self.spawn_points[1], self.enemy_paths[1]), (45, "Troll", 10, self.spawn_points[0], self.enemy_paths[0])]
        self.current_gold = self.starting_gold

    def draw_background(self):
        return (self.background_image, (0,0))
    
    def draw_village(self, window_width, window_height):
        return(self.village_postfix, (self.village_relative[0]*window_width, self.village_relative[1]*window_height))

    def get_current_gold(self):
        return self.current_gold

    def decrease_gold_by(self, quantity):
        self.current_gold -= quantity

    def increase_gold_by(self, quantity):
        self.current_gold += quantity

    def lower_health_by(self, quantity):
        if quantity < 0:
            return
        if self.health - quantity >= 0:
            self.health -= quantity
        else:
            self.health = 0