from . import base
import random


class PoisonPotion(base.Item):
    def __init__(self, data):
        super().__init__("potion of poison")
        self.type = "potion"
        self.random_position(data, 4)
        self.identified_name = "Potion of poison"
        self.name = ""
        self.durability = random.randint(1, 4)
        self.strength = random.randint(30, 60)
        self.set_name(data)

    def use_item(self, data, player):
        player.hp -= self.strength
        self.durability -= 1

        data.NameRegistry.name_dict[self.id] = self.identified_name
        data.reload_name_registry()

        if self.durability <= 0:
            del data.itemList[data.selItem]
            if data.selItem != 0:
                data.selItem -= 1

    def lands_on_entity(self, entity, data):
        entity.hp -= self.strength
        data.groundItems.remove(self)
        del self

    @staticmethod
    def get_probability(data):
        return 2

    def __call__(self, data):
        return PoisonPotion(data)

