from . import rock, firering, orc, cat


class Ents():
    def __init__(self, data):
        self.data = data
        self.possibilities = 2

    def appendToEntlist(self, object, count):
        for i in range(count):
            self.entList.append(object)

    def genEnts(self):
        self.entList = []
        self.appendToEntlist(rock.Rock, 3)
        self.appendToEntlist(firering.FireRing, 2)
        self.appendToEntlist(orc.Orc, 2)
        self.appendToEntlist(cat.Cat, 1)

    def getEnts(self):
        self.genEnts()
        return self.entList
