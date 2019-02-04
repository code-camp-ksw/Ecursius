from . import base
import random


class Sword(base.Item):
    def __init__(self, data):
        base.Item.__init__(self, "sword")
        self.random_position(data, 4)
        self.name = "basic Sword"
        self.identified_name = "basic Sword"
        self.type = "sword"
        self.damage = random.randint(7, 15)
        self.durability = random.randint(15, 25)
        data.NameRegistry.name_dict[self.id] = self.name

    def groundAttack(self, data, player):
        player.invulnerable = True

    def directionAttack(self, data, direction, player):
        entPos = [player.pos[0] + direction[0], player.pos[1] + direction[1]]

        for i in data.ents:
            if i.pos == entPos:
                i.hp -= self.damage
                self.durability -= 1
                if self.durability <= 0:
                    data.itemList.remove(self)
                    if data.selItem == len(data.itemList) and data.selItem != 0:
                        data.selItem -= 1

    def __call__(self, data):
        return Sword(data)
