import random


class Item:
    def __init__(self, id):
        self.pos = []
        self.isItem = True
        self.inInventory = False
        self.id = id
        self.name = ""
        self.char = "I"
        self.collide = False
        self.type = "sword"
        self.pickupDelay = 0
        self.identified = False
        self.base_price = 100
        self.already_known = False
        self.color_tag = None

    def set_position(self, y, x):
        self.pos = [int(y), int(x)]

    def random_position(self, data, tries):
        for i in range(tries):
            pos = [random.randint(5, 25), random.randint(5, 45)]
            if data.position_in_world(pos):
                self.set_position(pos[0], pos[1])

    def pickup(self, data):
        if self.pickupDelay == 0:
            self.inInventory = True
            data.itemList.append(self)
            data.groundItems.remove(self)

    def drop(self, data):
        self.inInventory = False
        data.groundItems.append(self)
        data.itemList.remove(self)
        self.set_position(data.player.pos[0], data.player.pos[1])
        self.pickupDelay = 3
        if data.selItem == len(data.itemList):
            data.selItem -= 1

    def set_name(self, data):
        self.name = data.NameRegistry.request_name(self.id, self.type)

    @staticmethod
    def get_probability(data):
        return 1

    @staticmethod
    def get_color_tag():  # override with tuple (tagName, color)
        return None

    def chr(self):
        return self.char


class Food(Item):
    def __init__(self, data, id):
        super().__init__(id)
        self.type = "food"
        self.base_price = 20
        self.saturation = 500
        self.water = 0
        self.durability = 1
        self.already_known = True

    def use_item(self, data, player):
        player.water += self.water
        player.saturation += self.saturation

    @staticmethod
    def get_base_price():
        return 20


class Drink(Item):
    def __init__(self, data, id):
        super().__init__(id)
        self.type = "drink"
        self.base_price = 5
        self.saturation = 0
        self.water = 100
        self.durability = 1
        self.already_known = True

    def use_item(self, data, player):
        player.water += self.water
        player.saturation += self.saturation

    @staticmethod
    def get_base_price():
        return 5

