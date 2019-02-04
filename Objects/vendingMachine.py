from . import base
import random


class VendingMachine(base.Object):
    def __init__(self, data):
        super().__init__("vending_machine", "£")
        self.variant = None
        self.set_variant()
        self.recipe = []
        self.set_recipe(data)
        self.random_position(data, 4)
        self.free_objects = random.randint(0, 3)

    def set_variant(self):
        self.variant = random.choice(["snacks", "drinks"])

    def set_recipe(self, data):
        if self.variant == "snacks":
            self.recipe.append(data.FoodRegistry.get_random_food(1).__next__()(data))
            self.recipe.append(self.recipe[0].base_price +
                               random.randint(int(self.recipe[0].base_price * 0.2), int(self.recipe[0].base_price * 0.8)))
        elif self.variant == "drinks":
            self.recipe.append(data.FoodRegistry.get_random_drink(1).__next__()(data))
            self.recipe.append(self.recipe[0].base_price +
                               random.randint(int(self.recipe[0].base_price * 0.2), int(self.recipe[0].base_price * 0.8)))

    def use(self, app):
        if app.data.player.gold >= self.recipe[1]:
            app.data.player.gold -= self.recipe[1]
            app.data.groundItems.append(self.recipe[0])
            app.data.groundItems[len(app.data.groundItems) - 1].set_position(self.pos[0], self.pos[1])
            self.set_recipe(app.data)
        else:
            app.data.player.gold = 0
            if random.randint(0, 99) > 95 and self.free_objects > 0:  # 1:25
                self.free_objects -= 1
                app.labeltext += "The vending machine shakes..."
                app.data.groundItems.append(self.recipe[0])
                app.data.groundItems[len(app.data.groundItems) - 1].set_position(self.pos[0], self.pos[1])
                self.set_recipe(app.data)
            else:
                app.labeltext += "The vending machine took all your gold. "

    def onPlayerMovesOnMe(self, app):
        pass

    def get_label_text(self):
        return "a vending machine selling {} for {} gold".format(self.recipe[0].name, self.recipe[1])

