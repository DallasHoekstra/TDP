class Level():
    background_image = ""
    starting_gold = 0
    def __init__(self):
        self.starting_gold = 2000
        self.spawn_points = [(720, 10), (140, 10)]
        self.village = [.5, .875, 50, 50]
        self.enemy_paths = [[(int(self.village[0] + 25), int(self.village[1] + 25)), (475, 660), (450, 625), (425, 590), 
                                    (400, 540), (445, 520), (490, 490), (565, 430), (650, 360), (775, 285), (700, 285), (615, 255), (585,225), (585,155), (725, 130)], 
                            [(int(self.village[0] + 25), int(self.village[1] + 25)), (475, 660), (450, 625), (425, 590), 
                                    (400, 540), (330, 515), (260, 500), (190, 490), (120, 470), (130, 330), (370, 330), (370, 240), (240, 240), (140, 160)] 
                            ]
        self.waves = [(5, "Skeleton", 10, self.spawn_points[1], self.enemy_paths[1]), (15, "Skeleton", 10, self.spawn_points[0], self.enemy_paths[0]), 
                        (30, "Skeleton", 20, self.spawn_points[0], self.enemy_paths[0]), (40, "Skeleton", 20, self.spawn_points[1], self.enemy_paths[1])]
    
