import random


class Entity():
    def __init__(self, char, health, name):
        self.name = name
        self.pos = []
        self.isItem = False
        self.char = char
        self.hp = health
        self.collide = True
        self.canMove = True
        self.requiresPostProcesses = False
        self.draw_in_back = True
        self.autoMove = False
        self.playerMove = False
        self.ticks_until_turn = 100
        self.ticks_remaining = self.ticks_until_turn
        self.movetime = 1

    def set_position(self, y, x):
        self.pos = [int(y), int(x)]

    def chr(self):
        return self.char

    def random_position(self, data, tries):
        for i in range(tries):
            pos = [random.randint(5, 25), random.randint(5, 45)]
            if data.position_in_world(pos):
                self.set_position(pos[0], pos[1])

    def random_positionList(self, data, tries):
        new_pos = None
        for i in range(tries):
            pos = [random.randint(5, 25), random.randint(5, 45)]
            if data.position_in_world(pos):
                new_pos = [pos[0], pos[1]]
        return new_pos

    def set_movement_delay(self, time, no_reset=False):
        self.ticks_until_turn = time
        if not no_reset:
            self.ticks_remaining = time


def copyList(list1, list2):
    list1 = list2[:]

