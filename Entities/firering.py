from . import base, pathfinder


class FireRing(base.Entity):
    def __init__(self, data):
        base.Entity.__init__(self, "&", 1000000, "firering")
        self.pos2 = self.random_positionList(data, 15)  # middle
        if self.pos2 is not None:
            self.radius = 3
            self.pathPos = 1
            self.path = pathfinder.genCirclePath(self, data)
            self.collide = False
            self.pos = self.path[0]
            self.autoMove = True
        else:
            self.requiresPostProcesses = True

    def move(self, data):
        if self.pathPos < len(self.path) - 1:
            self.pathPos += 1
        else:
            self.pathPos = 0
        self.pos = self.path[self.pathPos]
        if self.pos == data.player.pos:
            data.player.get_attacked(data, 10, self)

    def postProcess(self, data):
        data.ents.remove(self)
        del self

    def __call__(self, data):
        return FireRing(data)
