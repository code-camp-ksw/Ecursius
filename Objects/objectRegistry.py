from . import stair, vendingMachine

object_list = [stair.Stair, vendingMachine.VendingMachine]


class StaticObjects:
    def __init__(self, data):
        self.data = data
        self.objectList = []
        self.possibilities = 2

        for i in object_list:
            if i.get_color_tag() is not None:
                data.tagRegistry.add(i.get_color_tag()[0], i.get_color_tag()[1])

    def appendToObjectList(self, object, count):
        for i in range(count):
            self.objectList.append(object)

    def genObjects(self):
        self.objectList = []

        self.appendToObjectList(stair.Stair, 2)
        self.appendToObjectList(vendingMachine.VendingMachine, vendingMachine.VendingMachine.get_probability(self.data))

    def getObjects(self):
        self.genObjects()
        return self.objectList

