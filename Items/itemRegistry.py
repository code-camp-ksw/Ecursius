from . import sword, telepotion, pickaxe, healthpotion, gold, poison, greater_health_potion, waterbottle, slimeMold


class Items():
    def __init__(self, data):
        self.data = data
        self.ItemList = []
        self.possibilities = 2

    def appendToItemlist(self, object, count):
        for i in range(count):
            self.ItemList.append(object)

    def genItems(self):
        self.ItemList = []
        # adds to entities which are possible: class object, weight
        self.appendToItemlist(poison.PoisonPotion, 2)
        self.appendToItemlist(sword.Sword, 2)
        self.appendToItemlist(telepotion.TelePotion, 2)
        self.appendToItemlist(pickaxe.Pickaxe, pickaxe.Pickaxe.get_probability(self.data))
        self.appendToItemlist(healthpotion.HealthPotion, 2)
        self.appendToItemlist(gold.Gold, 5)
        self.appendToItemlist(greater_health_potion.GreaterHealthPotion, greater_health_potion.GreaterHealthPotion.get_probability(self.data))
        self.appendToItemlist(waterbottle.WaterBottle, waterbottle.WaterBottle.get_probability(self.data))
        self.appendToItemlist(slimeMold.SlimeMold, slimeMold.SlimeMold.get_probability(self.data))

    def getItems(self):
        self.genItems()
        return self.ItemList
