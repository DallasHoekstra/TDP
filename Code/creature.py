import pygame
import entity

class Creature(entity.Entity):
#     L0_Path = ""
#     L0_Image = ""
#     x = 0
#     y = 0
#     maxhealth = 0
#     health = 0
#     attack = 0
#     default_move_speed = 0
#     move_speed = 0
#     foe = False
#     path = []
#     width = 0
#     height = 0
#     visible = False
    
    def __init__(self, x_ord, y_ord, path):
        self.x = x_ord
        self.y = y_ord
        self.conditions = []
        self.path = path.copy()
#         if self.L0_Path != "":
#             self.L0_Image = pygame.image.load(self.L0_Path)
#             self.width, self.height = self.L0_Image.get_rect().size

#     def draw_creature(self, window):
        
#         if not self.visible:
#             window_dimensions = window.get_size()        
#             if self.x > 0 and self.x < window_dimensions[0]:
#                 if self.y > 0 and self.y < window_dimensions[1]:
#                     self.visible = True
#         else:
#             if self.L0_Image != "":
#                 window.blit(self.L0_Image, (self.x, self.y))
#                 pygame.draw.rect(window, (255,0,0), (self.x, self.y - 5, int((self.width/self.maxhealth)*self.health) + 1, 5))
                        
#     def set_path(self, path):
#         self.path = path.copy() 

#     def draw_attack(self):
#         pass

#     def move(self):
#         if len(self.path) > 0:
#             x_diff = self.path[-1][0] - self.x
#             y_diff = self.path[-1][1] - self.y
#             if abs(x_diff) > self.move_speed or abs(y_diff) > self.move_speed:
#                 if abs(x_diff) > self.move_speed:
#                     if x_diff > 0:
#                         self.x += self.move_speed
#                     else:
#                         self.x -= self.move_speed
#                 else:
#                     self.x = self.path[-1][0]
#                 if abs(y_diff) > self.move_speed:
#                     if y_diff > 0:
#                         self.y += self.move_speed
#                     else:
#                         self.y -= self.move_speed
#                 else:
#                     self.y = self.path[-1][1]
#             else:
#                 self.x = self.path[-1][0]
#                 self.y = self.path[-1][1]
#                 self.path.pop()

#     def apply_status(self, statusType, duration, severity):
#         self.statuses[statusType][0] = True
#         self.statuses[statusType][1] = duration
#         self.statuses[statusType][2] = severity 

#     def tick_status(self):
#         for status in self.statuses:
#             isActive = self.statuses[status][0]
#             timeLeft = self.statuses[status][1]
#             severity = self.statuses[status][2]
#             if isActive == True:
#                 if timeLeft > 0:
#                     timeLeft -= 1
#                 else:
#                     isActive = False

#                 # SWITCH based on status
#                 # FOR FUTURE: find a way to do this without a SWITCH STYLE
#                 if status == "Chilled":
#                     self.move_speed = self.default_move_speed*severity

        
class Skeleton(Creature):
    max_health = 25
    health = max_health
    default_move_speed = 1
    move_speed = default_move_speed
    life_damage = 1
    value = 10
    image_postfix = "L0Skeleton.gif"
#     attack = 5


# class Troll(Creature):
#     L0_Path = image_path + "L0Troll.gif"
#     maxhealth = 500
#     health = 500
#     attack = 50
#     default_move_speed = 1
#     move_speed = default_move_speed
#     foe = True
#     life_damage = 10
#     value = 100

class Accelerator(Creature):
    max_health = 10
    health = max_health
    default_move_speed = 1
    move_speed = default_move_speed
    life_damage = 1
    value = 20
    image_postfix = "L0Accelerator.gif"
    acceleration_counter = 0

#     attack = 2


#     def move(self):
#         self.acceleration_counter += 1
#         if len(self.path) > 0:
#             x_diff = self.path[-1][0] - self.x
#             y_diff = self.path[-1][1] - self.y
            
#             if abs(x_diff) > self.move_speed or abs(y_diff) > self.move_speed:
#                 if abs(x_diff) > self.move_speed:
#                     if x_diff > 0:
#                         self.x += self.move_speed
#                     else:
#                         self.x -= self.move_speed
#                 else:
#                     self.x = self.path[-1][0]
#                 if abs(y_diff) > self.move_speed:
#                     if y_diff > 0:
#                         self.y += self.move_speed
#                     else:
#                         self.y -= self.move_speed
#                 else:
#                     self.y = self.path[-1][1]
                
#             else:
#                 self.x = self.path[-1][0]
#                 self.y = self.path[-1][1]
#                 self.path.pop()