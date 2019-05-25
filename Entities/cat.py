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
        prevpos = []
        base.copyList(prevpos, self.pos)
        direction = pathfinder.move_to_nearest_of_list(self.pos, data.groundItems, data)
        print(direction)
        if direction == [0, 0] and len(data.groundItems) == 0:
            direction = pathfinder.normal_moving_direction(self.pos, data.player.pos, data)
        print(direction)
        self.pos = [int(self.pos[0] + direction[0]), int(self.pos[1] + direction[1])]
        for i in data.ents:
            if self.pos == i.pos:
                base.copyList(self.pos, prevpos)

        if self.pos == data.player.pos:
            data.player.get_attacked(self.strength)
            self.pos = prevpos[:]

    def __call__(self, data):
        return Cat(data)

