from . import base
import random


class Pickaxe(base.Item):
    def __init__(self, data):
        base.Item.__init__(self, "pickaxe")
        self.random_position(data, 4)
        self.name = "pickaxe"
        self.identified_name = "pickaxe"
        self.type = "pickaxe"
        self.durability = random.randint(10, 15)
        self.damage = random.randint(2, 4)
        data.NameRegistry.name_dict[self.id] = self.name

    def groundAttack(self, data, player):
        pass

    def directionAttack(self, data, direction, player):
        entPos = [player.pos[0] + direction[0], player.pos[1] + direction[1]]

        for i in data.ents:
            if i.pos == entPos:
                if i.name == "rock":
                    i.hp -= random.randint(40000, 70000)
                else:
                    i.hp -= self.damage
                self.durability -= 1
                if self.durability <= 0:
                    data.itemList.remove(self)
                    if data.selItem == len(data.itemList) and data.selItem != 0:
                        data.selItem -= 1

    def __call__(self, data):
        return Pickaxe(data)
