from . import base


class Fish(base.Food):
    def __init__(self, data):
        super().__init__(data, "fish")
        self.name = "Fish"
        self.base_price = 13
        self.saturation = 300

