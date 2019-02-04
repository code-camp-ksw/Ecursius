from . import base
import random


class Gold(base.Item):
    def __init__(self, data):
        super().__init__("gold")
        self.amount = random.randint(1, 6)
        self.char = "g"
        self.name = "some gold"
        self.random_position(data, 2)

    def pickup(self, data):
        data.player.gold += self.amount
        data.groundItems.remove(self)

    def __call__(self, data):
        return Gold(data)

