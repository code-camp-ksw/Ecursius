from . import base, slimeMold, waterbottle, fish
import random


class FoodRegistry:
    def __init__(self, data):
        self.data = data
        self.food = []
        self.drinks = []

    def add_to_list(self, list, object, amount):
        for i in range(amount):
            list.append(object)

    def gen_food_list(self):
        self.add_to_list(self.food, slimeMold.SlimeMold, slimeMold.SlimeMold.get_probability(self.data))
        self.add_to_list(self.food, fish.Fish, fish.Fish.get_probability(self.data))

    def gen_drink_list(self):
        self.add_to_list(self.drinks, waterbottle.WaterBottle, waterbottle.WaterBottle.get_probability(self.data))

    def get_food_list(self):
        self.gen_food_list()
        return self.food[:]

    def get_random_food(self, count):
        f = self.get_food_list()
        for i in range(count):
            yield random.choice(f)

    def get_drinks_list(self):
        self.gen_drink_list()
        return self.drinks[:]

    def get_random_drink(self, count):
        d = self.get_drinks_list()
        for i in range(count):
            yield random.choice(d)

