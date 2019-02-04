from . import base
import random


class Stair(base.Object):
    def __init__(self, data):
        super().__init__("stair", "")
        self.variant = None
        self.random_position(data, 6)
        self.setVariant()

    def setVariant(self):
        self.variant = random.choice(["up", "down", "up"])
        if self.variant == "up":
            self.chr = "↗"
            self.name = "a stair going up"
        else:
            self.chr = "↘"
            self.name = "a stair going down"

    def onPlayerMovesOnMe(self, app):
        pass

    def on_player_walks_me(self, app):
        if self.variant == "up":
            app.data.level += 1
            app.data.score += 5

            if app.data.level == 0:
                app.labeltext += "You finished the game by escaping.\nDon't think you really won! "
                app.finish()
            else:
                app.data.generate_map()

        else:
            app.data.level -= 1
            app.data.score += 5
            if app.data.level < app.data.maxLevel:
                app.data.maxLevel -= 1
            app.data.generate_map()
            app.labeltext += "This stair went down. "

    def __call__(self, data):
        return Stair(data)

