from . import stair, vendingMachine


class StaticObjects:
    def __init__(self, data):
        self.data = data
        self.objectList = []
        self.possibilities = 2

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

