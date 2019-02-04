from . import base
import random


class Rock(base.Entity):
    def __init__(self, data):
        base.Entity.__init__(self, "#", 100000, "rock")
        self.draw_in_back = False
        self.child = False
        self.canMove = False
        self.random_position(data, 4)
        self.requiresPostProcesses = True

    def postProcess(self, data):
        if not self.child:
            self.genStructure(data)
        self.requiresPostProcesses = False

    def genStructure(self, data):
        for i in range(0, 3):
            for j in range(0, 3):
                pos = [self.pos[0] + i - 1, self.pos[1] + j - 1]
                if data.position_in_world(pos) and random.choice([True, False]):
                    a = Rock(data)
                    a.child = True
                    a.pos = pos
                    data.ents.append(a)

    def __call__(self, data):
        return Rock(data)
