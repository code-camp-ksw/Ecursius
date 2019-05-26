from . import base, pathfinder
import random


class Cat(base.Entity):
    def __init__(self, data):
        hp = random.randint(4, 8)
        super().__init__("c", hp, "cat")
        self.random_position(data, 4)
        self.autoMove = True
        self.set_movement_delay(50)
        self.strength = random.randint(3, 8)

    def move(self, data):
        prevpos = self.pos[:]
        target = None
        for i in data.groundItems:
            if i.id == "fish":
                target = i
        if target is not None:
            direction = pathfinder.a_star(data, self.pos, target.pos, diagonal_allowed=True)
            print(direction)
        else:
            direction = pathfinder.move_to_nearest_of_list(self.pos, data.groundItems, data)
        if direction == [0, 0] and len(data.groundItems) == 0:
            direction = pathfinder.a_star(data, self.pos, data.player.pos)
        if direction != [0, 0] and len(direction) > 1:
            self.pos = list(direction[1])
        for i in data.ents:
            if i is not self and self.pos == i.pos:
                self.pos = prevpos

        if self.pos == data.player.pos:
            data.player.get_attacked(data, self.strength, self)
            self.pos = prevpos

    def __call__(self, data):
        return Cat(data)

