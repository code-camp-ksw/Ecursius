from . import base
import random


class GreaterHealthPotion(base.Item):
    def __init__(self, data):
        super().__init__("greater_health_potion")
        self.type = "potion"
        self.random_position(data, 4)
        self.identified_name = "Greater healing potion"
        self.durability = random.randint(1, 3)
        self.strength = random.randint(15, 25)

        self.set_name(data)

    def use_item(self, data, player):
        player.hp += self.strength
        if player.hp > player.max_hp:
            player.hp = player.max_hp
        self.durability -= 1

        data.NameRegistry.name_dict[self.id] = self.identified_name
        data.reload_name_registry()

        if self.durability <= 0:
            del data.itemList[data.selItem]
            if data.selItem != 0:
                data.selItem -= 1

    """def __call__(self, data):
        return GreaterHealthPotion(data)"""


