import random


class NameRegistry:
    def __init__(self):
        self.name_dict = {}
        self.potion_possibilities = ["Bottle of yellow liquid", "Green liquid", "Oily liquid", "Wine?", "Fizzy potion",
                                     "Milky potion", "Smoky potion", "Clear potion"]
        self.sword_possibilities = ["Shining stick", "Stick", "Sticky thingy", "Crude blade", "Light blade",
                                    "Green blade"]
        self.pickaxe_possibilities = ["Iron pickaxe", "Great pickaxe", "Hammer"]
        self.scroll_possibilities = ["Scroll named ???", "Paper with letters", "Red parchment", "Scroll named VAZKII",
                                     "Scroll named IV HARK", "Scroll named HE|q"]
        self.spellbook_possibilities = ["Green spellbook", "Yellow spellbook", "Cyan spellbook", "Strange spellbook",
                                        "Purple spellbook"]

    def request_name(self, id, type):
        if id in self.name_dict:
            return self.name_dict[id]
        else:
            if type == "potion":
                self.name_dict[id] = self.new_potion_name()
            elif type == "sword":
                self.name_dict[id] = self.new_sword_name()
            elif type == "pickaxe":
                self.name_dict[id] = self.new_pickaxe_name()
            elif type == "scroll":
                self.name_dict[id] = self.new_scroll_name()
            elif type == "spellbook":
                self.name_dict[id] = self.new_spellbook_name()
            return self.name_dict[id]

    def new_potion_name(self):
        return self.potion_possibilities.pop(random.randint(0, len(self.potion_possibilities) - 1))

    def new_sword_name(self):
        return self.sword_possibilities.pop(random.randint(0, len(self.sword_possibilities) - 1))

    def new_pickaxe_name(self):
        return self.pickaxe_possibilities.pop(random.randint(0, len(self.pickaxe_possibilities) - 1))

    def new_scroll_name(self):
        return self.scroll_possibilities.pop(random.randint(0, len(self.scroll_possibilities) - 1))

    def new_spellbook_name(self):
        return self.spellbook_possibilities.pop(random.randint(0, len(self.spellbook_possibilities) - 1))

