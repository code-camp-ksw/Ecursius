import random


class Object:
    def __init__(self, id, chr):
        self.id = id
        self.pos = []
        self.char = chr
        self.walkable = True
        self.name = ""
        self.messages = True
        self.color_tag = None

    def set_position(self, posy, posx):
        self.pos = [int(posy), int(posx)]

    def random_position(self, data, tries):
        for i in range(tries):
            pos = [random.randint(5, 25), random.randint(5, 45)]
            if data.position_in_world(pos):
                self.set_position(pos[0], pos[1])

    def onPlayerMovesOnMe(self, app):
        pass

    def get_label_text(self):
        return self.name

    @staticmethod
    def get_probability(data):
        return 1

    def use(self, app):
        pass

    def chr(self):
        return self.char

    @staticmethod
    def get_color_tag():  # override with tuple (tagName, color)
        return None

