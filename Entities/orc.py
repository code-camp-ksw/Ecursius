from . import base, pathfinder
import random


class Orc(base.Entity):
    def __init__(self, data):
        hp = random.randint(8, 12)
        base.Entity.__init__(self, "o", hp, "orc")
        self.random_position(data, 4)
        self.playerMove = True
        self.movetime = 2
        self.failed_move = False

    def move(self, data):
        if data.move % self.movetime == 0 and pathfinder.calc_distance(self.pos, data.player.pos) <= 10:
            prevpos = self.pos[:]
            direction = pathfinder.normal_moving_direction(self.pos, data.player.pos, data)
            self.pos = [int(self.pos[0] + direction[0]), int(self.pos[1] + direction[1])]
            for i in data.ents:
                if i is not self and self.pos == i.pos:
                    print(i)
                    self.pos = prevpos

            if self.pos == data.player.pos:
                data.player.get_attacked(5)
                self.pos = prevpos

