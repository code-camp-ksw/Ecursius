from . import base, pathfinder
import random


class Orc(base.Entity):
    def __init__(self, data):
        hp = random.randint(8, 12)
        base.Entity.__init__(self, "o", hp, "orc")
        self.random_position(data, 4)
        self.playerMove = True
        self.movetime = 2

    def move(self, data):
        if data.move % self.movetime == 0:
            prevpos = []
            base.copyList(prevpos, self.pos)
            direction = pathfinder.normalMoveDir(self.pos, data.player.pos, data)
            self.pos = [int(self.pos[0] + direction[0]), int(self.pos[1] + direction[1])]
            for i in data.ents:
                if self.pos == i.pos:
                    base.copyList(self.pos, prevpos)

            if self.pos == data.player.pos:
                data.player.get_attacked(5)
                base.copyList(self.pos, prevpos)


