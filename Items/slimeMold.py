from . import base


class SlimeMold(base.Food):
    def __init__(self, data):
        super().__init__(data, "slime_mold")
        self.name = "Slime mold"
        self.base_price = 20
        self.nutrition = 1000



