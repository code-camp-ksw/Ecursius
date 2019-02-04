from . import base


class WaterBottle(base.Drink):
    def __init__(self, data):
        super().__init__(data, "water_bottle")
        self.base_price = 1
        self.name = "Bottle of Water"

    @staticmethod
    def get_base_price():
        return 1



