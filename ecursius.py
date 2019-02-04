# -*- coding: utf-8 -*-

import tkinter as tk
import os
import logging
import random
from PIL import Image, ImageTk

from Entities import entRegistry
from Items import itemRegistry, NameRegistry, FoodRegistry
from Objects import objectRegistry, door


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game = Game(master=self)
        self.menu = Menu(master=self)
        self.settings = Settings(master=self)
        self.help = Help(master=self)
        self.help.withdraw()
        self.menu.pack()
        self.bind_all("<Control-KeyPress-q>", self.quit_event)

    def quit_event(self, e):
        self.quit()

    def start_game(self):
        self.menu.pack_forget()
        self.game.pack()
        self.game.start()

    def open_settings(self):
        self.menu.pack_forget()
        self.settings.pack()


class Help(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.mode = tk.Menu(self, relief=tk.FLAT)
        self.mode.add_command(label="hide", command=self.withdraw)
        self.mode.add_command(label="Buttons", command=self.show_button_text)
        self.config(menu=self.mode)
        self.text = tk.Label(self, width=40, anchor=tk.NW, justify=tk.LEFT, bg="#efefef")
        self.text.grid(row=2, column=0)
        self.show_button_text()

    def show_button_text(self):
        self.text.configure(text="""    uio\tkeypad to move/attack
    jkl\telse: numpad
    m,.\tswitch mode with F1
    >\tmove up stair (↗)
    <\tmove down stair (↘)
    
    ↓\tmove selection down
    ↑\tmove selection up
    ←\tswitch inventory side / move selection
    →\tswitch inventory side / move selection
    z\topen/close inventory
    -\tdrop selected item
    n\tpick up Item
    """)


class Settings(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=500, height=560)
        self.back = tk.Button(self, text="Back to Menu", command=self.exit_to_menu)
        self.back.grid(row=1, column=0)
        self.numpad = tk.Button(self, text="Numpad mode: OFF", command=self.toggle_numpad)
        self.numpad.grid(row=0, column=0)

    def exit_to_menu(self):
        self.pack_forget()
        self.master.menu.pack()

    def toggle_numpad(self):
        if self.master.game.data.numpadmode:
            self.master.game.data.numpadmode = False
            self.numpad.configure(text="Numpad mode: OFF")
        else:
            self.master.game.data.numpadmode = True
            self.numpad.configure(text="Numpad mode: ON")


class Menu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=500, height=560)
        self.grid_propagate(0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.background = ImageTk.PhotoImage(Image.open("Menu.png"))
        self.background_label = tk.Label(self, image=self.background)
        self.background_label.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)
        self.start_button = tk.Button(self, text="START!", command=master.start_game, anchor=tk.CENTER, relief=tk.FLAT)
        self.start_button.grid(row=0, column=1, pady=(150, 10))
        self.settings_button = tk.Button(self, text="Settings", command=master.open_settings, anchor=tk.CENTER, relief=tk.FLAT)
        self.settings_button.grid(row=1, column=1, pady=(10, 10))
        self.quit_button = tk.Button(self, text="Quit", command=self.quit, anchor=tk.CENTER, relief=tk.FLAT)
        self.quit_button.grid(row=2, column=1, pady=(10, 10))


class Game(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#eaeaea")
        self.running = False
        self.master.title("Ecursius")
        self.master.configure(bg="#eaeaea")
        self.game_text = tk.StringVar()
        self.field = tk.Label(self, width=60, height=30, bg="#eaeaea", font="TkFixedFont", textvariable=self.game_text)
        self.expire_turns = 1
        self.itemscore = tk.Label(self, height=30, width=35, bg="#eaeaea", anchor=tk.NW, justify=tk.LEFT)
        self.stats = tk.Label(self, height=3, bg="#eaeaea")
        self.label = tk.Label(self, height=5, bg="#eaeaea")
        self.separator = tk.Label(self, height=30, text="", bg="#eaeaea")

        t = "|"
        for i in range(29):
            t += "\n|"
        self.separator.configure(text=t)

        self.field.grid(row=1, column=0)
        self.separator.grid(row=1, column=1)
        self.itemscore.grid(row=1, column=2)
        self.stats.grid(row=2, column=0, columnspan=3)
        self.label.grid(row=0, columnspan=3)

        self.labeltext = ""
        self.data = GameDataHolder()

    def exit_to_menu(self, e):
        self.pack_forget()
        self.master.menu.pack()

    def write_to_label(self, text, expires=False):
        self.label.configure(text=text)
        if expires == False:
            self.expire_turns = -1
        else:
            self.expire_turns = expires
        self.running = False

    def entity_automove(self):
        if self.running:
            for i in self.data.ents:
                if i.autoMove:
                    i.ticks_remaining -= 1
                    if i.ticks_remaining == 0:
                        i.move(self.data)
                        i.ticks_remaining = i.ticks_until_turn

            self.draw()

            if self.data.player.hp < 1:
                logging.info("player died.")
                self.labeltext += "Game Over\nyou died. "
                self.label.configure(bg="#ea2222")
                self.finish()

        self.after(10, func=self.entity_automove)

    def draw(self):
        screen = []
        for i in range(len(self.data.game)):
            line = []
            for j in self.data.game[i]:
                line.append(j)
            screen.append(line)

        for i in self.data.doorList:
            screen[i.pos[0]][i.pos[1]] = i.chr

        for i in self.data.staticObjects:
            screen[i.pos[0]][i.pos[1]] = i.chr

        for i in self.data.groundItems:
            screen[i.pos[0]][i.pos[1]] = i.chr()
        for i in self.data.ents:
            if not i.draw_in_back:
                if screen[i.pos[0]][i.pos[1]] == " ":
                    screen[i.pos[0]][i.pos[1]] = i.chr()
            else:
                screen[i.pos[0]][i.pos[1]] = i.chr()

        screen[self.data.player.pos[0]][self.data.player.pos[1]] = "@"
        for i in range(len(screen)):
            screen[i] = "".join(screen[i])
        self.game_text.set("\n".join(screen))

        self.draw_stats()
        self.draw_itemscore()

    def draw_stats(self):
        new_text = "~" * 95
        new_text += "\n"
        new_text += "health: {}/{}\tgold: {}\t{}".format(self.data.player.hp, self.data.player.max_hp, self.data.player.gold, ", ".join(self.data.player.statuslist))
        new_text += "\n"
        new_text += "score: {}\tlevel: {}\tdeepest level: {}".format(
            self.data.score, self.data.level, self.data.maxLevel)
        self.stats.configure(text=new_text)

    def draw_itemscore(self):
        new_text = ""

        if self.data.showInventory:
            if ((self.data.inventorySide + 1) * 30) - 1 >= len(self.data.itemList):
                last_item = len(self.data.itemList)
            else:
                last_item = ((self.data.inventorySide + 1) * 30)

            for i in range(self.data.inventorySide * 30, last_item):
                item = self.data.itemList[i]
                if self.data.itemList[self.data.selItem] == item:
                    new_text += "[ {}: {} ]\n".format(item.name, item.durability)
                else:
                    new_text += "- {}: {}\n".format(item.name, item.durability)

        self.itemscore.configure(text=new_text)

    def start(self):
        self.running = True
        self.unbind_all("<KeyPress-q>")
        self.bind_all("<KeyPress>", func=self.input_handler)
        self.data.reset_inventory()
        self.data.generate_map()
        self.data.player.reset_stats()
        self.entity_automove()
        self.label.configure(bg="#eaeaea", text="Press any button to start. \"h\" will give you help. ")
        self.draw()

    def finish(self):
        self.running = False
        self.unbind_all("<KeyPress>")
        self.bind_all("<KeyPress-q>", func=self.exit_to_menu)

    def input_handler(self, event):
        self.running = True
        self.expire_turns -= 1
        self.data.no_move = False
        self.labeltext = ""

        if self.expire_turns == 0:
            self.write_to_label(" ")

        if self.data.player.invulnerable:
            self.data.player.invulnerable = False

        if event.keysym == "h":
            self.master.help.deiconify()

        elif event.keysym == "q":
            self.labeltext += "Game Over! "
            logging.info("Player pressed q")
            self.finish()

        elif event.keysym == "w":
            self.data.selItem -= 1
            if self.data.selItem < 0:
                self.data.selItem = len(self.data.itemList) - 1

        elif event.keysym == "s":
            self.data.selItem += 1
            if self.data.selItem > len(self.data.itemList) - 1:
                self.data.selItem = 0

        elif event.keysym == "a":
            self.data.inventorySide -= 1
            if self.data.inventorySide < 0:
                self.data.inventorySide = self.data.get_needed_inv_sides() - 1

        elif event.keysym == "d":
            self.data.inventorySide += 1
            if self.data.inventorySide >= self.data.get_needed_inv_sides():
                self.data.inventorySide = 0

        elif event.keysym == "minus":
            if self.data.itemList:
                self.data.itemList[self.data.selItem].drop(self.data)

        elif event.keysym == "f":
            self.data.generate_map()
            self.data.player.random_position(self.data)
            logging.info("generating new game, ")

        elif event.keysym == "z":
            if self.data.showInventory:
                self.data.showInventory = False
            else:
                self.data.showInventory = True

        elif event.keysym == "n":
            for i in self.data.groundItems:
                if i.pos == self.data.player.pos:
                    i.pickup(self.data)

        elif event.keysym == "F1":
            if self.data.numpadmode:
                self.data.numpadmode = False
            else:
                self.data.numpadmode = True

        elif event.keysym_num == 73:  # I
            for i in self.data.staticObjects:
                if i.pos == self.data.player.pos:
                    i.use(self)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.data.numpadmode:
                    if event.keysym == self.data.numpad[i][j]:
                        self.data.player.move([i - 1, j - 1], self.data)
                else:
                    if event.keysym == self.data.keypad[i][j] and event.state == 0x0000:
                        self.data.player.move([i - 1, j - 1], self.data)

        for i in self.data.ents:
            if i.hp < 1:
                self.data.ents.remove(i)

        if self.data.player.hp < 1:
            logging.info("player died.")
            self.labeltext += "Game Over\nyou died."
            self.label.configure(bg="#ea2222")
            self.finish()

        for i in self.data.groundItems:
            if i.pickupDelay > 0:
                i.pickupDelay -= 1
            if i.pos == self.data.player.pos:
                if "You see here: " not in self.labeltext:
                    self.labeltext += "You see here: "
                self.labeltext += i.name + ", "

        for i in self.data.doorList:
            if i.pos == self.data.player.pos:
                i.onPlayerMovesOnMe(self)

        for i in self.data.staticObjects:
            if self.data.player.pos == i.pos:
                i.onPlayerMovesOnMe(self)
                if i.id == "stair" and ((i.variant == "down" and event.keysym == "greater") or (i.variant == "up" and event.keysym == "less")):
                    i.on_player_walks_me(self)
                else:
                    if "You see here: " not in self.labeltext:
                        self.labeltext += "You see here: "
                    self.labeltext += i.get_label_text()

        if not self.data.no_move:
            self.data.move += 1
            for i in self.data.ents:
                if i.playerMove:
                    i.move(self.data)

        self.data.player.saturation -= 1
        self.data.player.water -= 1

        self.label.configure(text=self.labeltext)
        self.draw()


class GameDataHolder:
    def __init__(self):
        self.no_move = False
        self.numpadmode = False

        self.numpad = [["KP_7", "KP_8", "KP_9"], ["KP_4", "KP_5", "KP_6"], ["KP_1", "KP_2", "KP_3"]]

        self.keypad = [["u", "i", "o"],
                       ["j", "k", "l"],
                       ["m", "comma", "period"]]
        self.selItem = 0
        self.inventorySide = 0
        self.showInventory = True
        self.itemList = []

        self.groundItems = []
        self.ents = []

        self.entRegistry = None
        self.itemRegistry = None
        self.objectRegistry = None
        self.NameRegistry = None
        self.FoodRegistry = None

        self.rooms = []
        self.game = []
        self.maxLevel = -1
        self.level = -1
        self.score = 0
        self.move = 0

        self.player = Player()
        self.staticObjects = []
        self.doorList = []

        self.registry_setup()

    def registry_setup(self):
        self.entRegistry = entRegistry.Ents(self)
        self.itemRegistry = itemRegistry.Items(self)
        self.objectRegistry = objectRegistry.StaticObjects(self)
        self.NameRegistry = NameRegistry.NameRegistry()
        self.FoodRegistry = FoodRegistry.FoodRegistry(self)

    def reload_name_registry(self):
        for i in self.itemList:
            if not (i.already_known or i.identified):
                i.name = self.NameRegistry.request_name(i.id, i.type)
                if i.name == i.identified_name:
                    i.identified = True

    def get_needed_inv_sides(self):
        i = 0
        while i * 30 <= len(self.itemList):
            i += 1

        return i

    def reset_inventory(self):
        self.inventorySide = 0
        self.itemList = []
        self.showInventory = True
        self.selItem = 0

    def entity_creation(self):
        self.spawn_entity_creation()
        for i in self.ents:
            if i.requiresPostProcesses:
                i.postProcess(self)

    def spawn_entity_creation(self):
        enttypes = []
        enttypes.extend(self.itemRegistry.getItems())
        enttypes.extend(self.entRegistry.getEnts())
        self.ents = []
        self.groundItems = []

        for j in range(random.randint(0, self.itemRegistry.possibilities + self.entRegistry.possibilities)):
            e = enttypes.pop(random.randint(0, len(enttypes) - 1))
            i = e(self)

            if i.isItem:
                self.groundItems.append(i)
            else:
                self.ents.append(i)

            if not i.pos:
                i.random_position(self, 4)

            if not i.pos and i in self.ents:
                self.ents.remove(i)
            elif not i.pos and i in self.groundItems:
                self.groundItems.remove(i)

    def static_object_creation(self):
        self.staticObjects = []
        objectlist = self.objectRegistry.getObjects()
        for i in range(random.randint(0, self.objectRegistry.possibilities)):
            o = objectlist.pop(random.randint(0, len(objectlist) - 1))
            obj = o(self)
            if obj.pos:
                self.staticObjects.append(obj)

    def generate_map(self):
        self.game = []

        self.doorList = []
        self.rooms = []
        for i in range(random.randint(1, 3)):
            self.rooms.append(Room(
                [random.randint(2, 20), random.randint(2, 55)]))

        for y in range(30):
            line = []
            for x in range(60):
                s = self.position_on_wall([y, x])
                if s is not None:
                    if random.randint(0, 100) > 97:
                        d = door.Door([y, x])
                        d.side = s
                        self.doorList.append(d)
                    line.append("#")
                else:
                    line.append(" ")
            self.game.append(line)

        self.entity_creation()
        self.static_object_creation()
        self.player.random_position_next_wall(self)

    def position_in_world(self, pos):
        for i in self.rooms:
            if i.position_in_room(pos):
                return True
        return False

    def position_on_wall(self, pos):
        r = None
        position_in_room = False
        for i in self.rooms:
            if i.position_in_room(pos):
                position_in_room = True
                r = None
            j = i.position_on_wall(pos)
            if j is not None and not position_in_room:
                r = j
        return r


class Room:
    def __init__(self, pos):
        self.upper = pos[0]
        self.left = pos[0]

        self.lower = random.randint(self.upper + 2, 28)
        self.right = random.randint(self.left + 2, 58)

    def __repr__(self):
        return str(self.upper) + "/" + str(self.left) + "  " + str(self.lower) + "/" + str(self.right)

    def position_in_room(self, pos):
        if self.upper < pos[0] < self.lower:
            if self.left < pos[1] < self.right:
                return True

        return False

    def position_on_wall(self, pos):
        if self.upper == pos[0] and self.left <= pos[1] <= self.right:
            return "upper"
        elif self.lower == pos[0] and self.left <= pos[1] <= self.right:
            return "lower"
        elif self.left == pos[1] and self.upper <= pos[0] <= self.lower:
            return "left"
        elif self.right == pos[1] and self.upper <= pos[0] <= self.lower:
            return "right"
        else:
            return None


class Player:
    def __init__(self):
        self.cursor_mode = False
        self.cursor_pos = []
        self.pos = []
        self.hp = 50
        self.max_hp = 50
        self.experience = 0
        self.invulnerable = False
        self.prevPos = []
        self.gold = 0
        self.saturation = 0
        self.water = 0
        self.statuslist = []

    def set_position(self, posy, posx):
        self.pos = [int(posy), int(posx)]

    def get_attacked(self, damage):
        if not self.invulnerable:
            self.hp -= damage

    def reset_stats(self):
        self.saturation = 5000
        self.water = 1000

    def move(self, direction, data):
        self.statuslist = []
        self.prevPos = self.pos[:]
        possible = False

        self.pos[0] += direction[0]
        self.pos[1] += direction[1]

        if direction == [0, 0] and data.itemList != []:
            if data.itemList[data.selItem].type in ["potion", "food", "drink"]:
                data.itemList[data.selItem].use_item(data, self)

        for i in data.ents:
            if self.pos == i.pos:
                logging.debug(str(i.pos))
                if i.collide:
                    self.pos = self.prevPos[:]
                if data.itemList != [] and data.itemList[data.selItem].type in "sword":
                    self.attack(direction, data)

        for i in data.doorList:
            if i.pos == self.pos:
                possible = True

        if not data.position_in_world(self.pos) and not possible:
            self.pos = self.prevPos[:]

        if 0 < self.water < 400:
            self.statuslist.append("Thirsty")
        elif self.water <= 0:
            if self.water < data.level * 20:
                self.statuslist.append("Dehydrated")
                self.hp = 0
            else:
                self.statuslist.append("Dehydrating")

        if self.saturation > 10000:
            self.statuslist.append("Saturated")
        elif 200 < self.saturation < 2000:
            self.statuslist.append("Hungry")
        elif 0 < self.saturation <= 750:
            self.statuslist.append("Weak")
        elif self.saturation <= 0:
            if self.saturation < data.level * 50:
                self.statuslist.append("Biting dust")
            else:
                self.statuslist.append("Fainting")

    def attack(self, direction, data):
        if direction == [0, 0] and data.itemList != []:
            data.itemList[data.selItem].groundAttack(data, self)
        elif data.itemList:
            data.itemList[data.selItem].directionAttack(data, direction, self)

    def random_position(self, data):
        self.pos = []
        while not self.pos:
            pos = [random.randint(5, 25), random.randint(5, 45)]
            if data.position_in_world(pos):
                self.set_position(pos[0], pos[1])

    def random_position_next_wall(self, data):
        self.pos = []
        while not self.pos:
            pos = [random.randint(5, 25), random.randint(5, 45)]
            s = data.position_on_wall(pos)
            doorpos = pos
            player_position = pos
            if s == "upper":
                player_position = [doorpos[0] + 1, doorpos[1]]
                if not data.position_in_world(player_position):
                    doorpos = [pos[0], pos[1] - 1]
                    player_position = [doorpos[0] + 1, doorpos[1]]
                    if not data.position_in_world(player_position):
                        doorpos = [pos[0], pos[1] + 1]
                        player_position = [doorpos[0] + 1, doorpos[1]]
            elif s == "lower":
                player_position = [doorpos[0] - 1, doorpos[1]]
                if not data.position_in_world(player_position):
                    doorpos = [pos[0], pos[1] - 1]
                    player_position = [doorpos[0] - 1, doorpos[1]]
                    if not data.position_in_world(player_position):
                        doorpos = [pos[0], pos[1] + 1]
                        player_position = [doorpos[0] - 1, doorpos[1]]
            elif s == "left":
                player_position = [doorpos[0], doorpos[1] + 1]
                if not data.position_in_world(player_position):
                    doorpos = [pos[0] - 1, pos[1]]
                    player_position = [doorpos[0], doorpos[1] + 1]
                    if not data.position_in_world(player_position):
                        doorpos = [pos[0] + 1, pos[1]]
                        player_position = [doorpos[0], doorpos[1] + 1]
            elif s == "right":
                player_position = [doorpos[0], doorpos[1] - 1]
                if not data.position_in_world(player_position):
                    doorpos = [pos[0] - 1, pos[1]]
                    player_position = [doorpos[0], doorpos[1] - 1]
                    if not data.position_in_world(player_position):
                        doorpos = [pos[0] + 1, pos[1]]
                        player_position = [doorpos[0], doorpos[1] - 1]

            if s is not None:
                d = door.Door([doorpos[0], pos[1]])
                d.side = s
                data.doorList.append(d)

                self.set_position(player_position[0], player_position[1])


if __name__ == '__main__':
    logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), "log.txt"), level=logging.DEBUG,
                        filemode="w")
    logging.debug(os.path.realpath(__file__))

    App = Window()
    App.mainloop()

    logging.info("game closed")
    logging.info("points:\t\t%d" % App.game.data.score)
    logging.info("maxlevel:\t\t%d" % App.game.data.maxLevel)
