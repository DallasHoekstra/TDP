import pygame
import entity
import math

class Creature(entity.Entity):
    default_move_speed = 0
    move_speed = default_move_speed
    life_damage = 0
    
    def __init__(self, position, path):
        self.x = position[0]
        self.y = position[1]
        self.status_effects = []

        self.path = path.copy()
        if len(self.path) > 0:
            self.next_point = self.path[-1]
        else:
            self.next_point = None

    def update_next_point(self):
        if len(self.path) > 1:
            self.path.remove(self.path[-1])
            self.next_point = self.path[-1]
        else:
            self.next_point = None

    def has_completed_path(self):
        return self.next_point is None

    def has_reached_next_point(self):
        return self.distance_from(self.next_point) < self.move_speed

    def move(self):

        if self.has_completed_path() == False:
            if self.has_reached_next_point(): 
                self.update_next_point()
            if self.has_completed_path() == True:
                return
            else:
                if self.x > self.next_point[0]:
                    self.x -= self.move_speed
                elif self.x < self.next_point[0]:
                    self.x += self.move_speed
                if self.y > self.next_point[1]:
                    self.y -= self.move_speed
                elif self.y < self.next_point[1]:
                    self.y += self.move_speed
        else: 
            self.die()
    
    def get_life_damage(self):
        return self.life_damage

    def draw(self):
        percent_health = round(self.current_health/self.max_health, 2)
        return (self.image_postfix, (self.x, self.y), percent_health)

        
class Skeleton(Creature):
    max_health = 25
    current_health = max_health
    default_move_speed = 1
    move_speed = default_move_speed
    life_damage = 1
    value = 10
    image_postfix = "L0Skeleton.gif"
    width = 20
    height = 20
#     attack = 5


class Troll(Creature):
    image_postfix = "L0Troll.gif"
    max_health = 500
    current_health = max_health
    default_move_speed = 1
    move_speed = default_move_speed
    life_damage = 10
    value = 100
    width = 20
    height = 40
#     attack = 50

class Accelerator(Creature):
    max_health = 10
    current_health = max_health
    default_move_speed = 1
    move_speed = default_move_speed
    life_damage = 1
    value = 20
    image_postfix = "L0Accelerator.gif"
    acceleration_counter = 0
    width = 5
    height = 5
#     attack = 2

    def accelerate(self, time_passed):
        self.acceleration_counter += time_passed
        if self.acceleration_counter >= 1:
            self.move_speed += 1
            self.acceleration_counter -= 1
 
            

    def tick(self, time_passed):
        self.cooldown_time_left -= time_passed
        self.accelerate(time_passed)

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

