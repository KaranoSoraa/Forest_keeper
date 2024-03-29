from utils import rand_bool; from utils import rand_cell; from utils import rand_cell2
from clouds import Clouds;

CELL_TYPES = "🟩🌳🌊💊🧰🔥"
THREE_BONUS = 100
UPGRADE_COST = 5000
LIVE_COST = 1000
class Map:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for i in range(h)]
        self.generate_forest(4, 10)
        self.generate_river(5)
        self.generate_river(6)
        self.generate_upgrade_shop()
        self.generate_hospital()
        self.clouds = Clouds(w, h)
    def check_bounds(self, x, y):
        if (x < 0) or (y < 0) or (x > self.h - 1) or (y > self.w - 1):
            return False
        return True

    def print_map(self, helico):
        print('⬛' * (self.w + 2))
        for ri in range(self.h):
            print('⬛', end='')
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if self.clouds.cells[ri][ci] == 1:
                    print("🌤️", end='')
                elif self.clouds.cells[ri][ci] == 2:
                    print("🌩️", end='')
                elif (helico.x == ri and helico.y == ci):
                    print('🚁', end='')
                elif (cell >= 0) and (cell <= len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end='')
            print('⬛')
        print('⬛' * (self.w + 2))

    def generate_river(self, l):
        rc = rand_cell(self.w, self.h)
        rx, ry = rc[0], rc[1]
        self.cells[rx][ry] = 2
        l -= 1
        while l > 0:
            rc2 = rand_cell2(rx, ry)
            rx2, ry2 = rc2[0], rc2[1]
            if self.check_bounds(rx2, ry2):
                if self.cells[rx2][ry2] == 2 and self.cells[rx2][ry2] == 1:
                    continue
                self.cells[rx2][ry2] = 2
                rx, ry = rx2, ry2
                l -= 1

    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if rand_bool(r, mxr):
                    self.cells[ri][ci] = 1

    def generate_tree(self):
        c = rand_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.cells[cx][cy] == 0):
            self.cells[cx][cy] = 1

    def generate_upgrade_shop(self):
        c = rand_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = 4

    def generate_hospital(self):
        c = rand_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] != 4:
            self.cells[cx][cy] = 3
        else:
            self.generate_hospital()
    def add_fire(self):
        c = rand_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5

    def update_fires(self, helico):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                    self.cells[ri][ci] = 0
                    helico.score -= 100
        for i in range(10):
            self.add_fire()
    def process_helicopter(self, helico, clouds):
        c = self.cells[helico.x][helico.y]
        d = clouds.cells[helico.x][helico.y]
        if c == 2:
            helico.tank = helico.mx_tank
        if (c == 5) and (helico.tank > 0):
            self.cells[helico.x][helico.y] = 1
            helico.score += THREE_BONUS
            helico.tank -= 1
        if (c == 4) and (helico.score >= UPGRADE_COST):
            helico.mx_tank += 1
            helico.score -= UPGRADE_COST
        if (c == 3) and (helico.score >= LIVE_COST):
            helico.lives += 100
            helico.score -= LIVE_COST
        if d == 2:
            helico.lives -= 1
            if helico.lives == 0:
                helico.game_over()
        fin = []
        for i in range(self.h):
            for j in range(self.w):
                fin.append(self.cells[i][j])
        if 1 in fin:
            print()
        else:
            helico.game_over()
    def export_data(self):
        return {"cells": self.cells}

    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.w)] for i in range(self.h)]