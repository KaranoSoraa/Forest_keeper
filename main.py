# 🌳 🌊 🚁 🟩 🔥 💊 ❤️ 🧺 🧰 🌤️ 🌩️ 🏆
from map import Map
import time
import os
from helicopter import Helicopter as Helico
from pynput import keyboard
from clouds import Clouds
import json
def clear():
    os.system('cls')

TICK_SLEEP = 0.2
THREE_UPDATE = 50
CLOUDS_UPDATE = 30
FIRE_UPDATE = 75
MAP_W, MAP_H = 20, 10

field = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
heli = Helico(MAP_W, MAP_H)
tick = 1

MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}

def process_key(key):
    global heli, tick, clouds, field
    c = key.char.lower()
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        heli.move(dx, dy)
    elif c == 'f':
        data = {"helicopter": heli.export_data(),
                "clouds": field.clouds.export_data(),
                "field": field.export_data(),
                "tick": tick}
        with open("level.json", 'w') as lvl:
            json.dump(data, lvl)
    elif c == "g":
        with open("level.json", 'r') as lvl:
            data = json.load(lvl)
            heli.import_date(data["helicopter"])
            tick = data["tick"] or 1
            field.import_data(data["field"])
            field.clouds.import_data(data["clouds"])

listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()



while True:
    clear() # почему-то не работает.

    field.process_helicopter(heli, field.clouds)
    heli.print_stats()
    field.print_map(heli)
    print("TICK", tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if tick % THREE_UPDATE == 0:
        field.generate_tree()
    if tick % FIRE_UPDATE == 0:
        field.update_fires()
    if tick % CLOUDS_UPDATE == 0:
        field.clouds.update()


