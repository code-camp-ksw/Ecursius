from . import rock, firering, orc, cat

entity_list = [rock.Rock, firering.FireRing, orc.Orc, cat.Cat]


class Ents():
    def __init__(self, data):
        self.data = data
        self.possibilities = 2

        for i in entity_list:
            if i.get_color_tag() is not None:
                data.tagRegistry.add(i.get_color_tag()[0], i.get_color_tag()[1])

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
