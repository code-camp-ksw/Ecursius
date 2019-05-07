from . import base


class Door(base.Object):
    def __init__(self, pos):
        super().__init__("door", "O")
        self.set_position(pos[0], pos[1])
        self.side = None  # "upper", "lower", "left", "right"
        self.messages = False

    def onPlayerMovesOnMe(self, app):
        app.data.score += 1
        app.data.generate_map()

