import pyxel
import random
from labyrinthe import *


class Pac_man:
    def __init__(self, labyrinthe):
        self.labyrinthe = labyrinthe
        self.x = 1  # Position initiale en x
        self.y = 1  # Position initiale en y
        self.direction = 0  # 0: droite, 1: haut, 2: gauche, 3: bas
        # Prochaine direction si le joueur appuie sur une touche directionnelle
        # pendant le déplacement
        self.next_direction = 0
        self.speed = 10
        self.sprite = True

    def deplacer(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.next_direction = 0
        elif pyxel.btn(pyxel.KEY_UP):
            self.next_direction = 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.next_direction = 2
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.next_direction = 3

        if pyxel.btn(pyxel.KEY_RIGHT) and not self.x == 27 and not self.labyrinthe.collision(
                self.x + 1, self.y):
            self.direction = 0
        elif pyxel.btn(pyxel.KEY_UP) and not self.labyrinthe.collision(self.x, self.y - 1):
            self.direction = 1
        elif pyxel.btn(pyxel.KEY_LEFT) and not self.labyrinthe.collision(self.x - 1, self.y):
            self.direction = 2
        elif pyxel.btn(pyxel.KEY_DOWN) and not self.labyrinthe.collision(self.x, self.y + 1):
            self.direction = 3

        if pyxel.frame_count % self.speed == 0:
            # Déplacement automatique tant que la direction ne change pas
            if self.direction == 0 and not self.x == 27 and not self.labyrinthe.collision(
                    self.x + 1, self.y):
                self.x += 1
            elif self.direction == 1 and not self.labyrinthe.collision(self.x, self.y - 1):
                self.y -= 1
            elif self.direction == 2 and not self.labyrinthe.collision(self.x - 1, self.y):
                self.x -= 1
            elif self.direction == 3 and not self.labyrinthe.collision(self.x, self.y + 1):
                self.y += 1

            if self.x > 26:
                self.x = 2
            elif self.x < 1:
                self.x = 26

            # Vérification de la prochaine direction
            if self.next_direction == 0 and not self.x == 27 and not self.labyrinthe.collision(
                    self.x + 1, self.y):
                self.direction = 0
            elif self.next_direction == 1 and not self.labyrinthe.collision(self.x, self.y - 1):
                self.direction = 1
            elif self.next_direction == 2 and not self.labyrinthe.collision(self.x - 1, self.y):
                self.direction = 2
            elif self.next_direction == 3 and not self.labyrinthe.collision(self.x, self.y + 1):
                self.direction = 3

    def afficher(self):
        if pyxel.frame_count % (self.speed / 2) == 0:
            self.sprite = not self.sprite

        if self.sprite:
            if self.direction == 0:
                pyxel.blt(self.x * 8, self.y * 8, 0, 8, 0, 8, 8, 0)
            elif self.direction == 1:
                pyxel.blt(self.x * 8, self.y * 8, 0, 32, 0, 8, 8, 0)
            elif self.direction == 2:
                pyxel.blt(self.x * 8, self.y * 8, 0, 24, 0, 8, 8, 0)
            elif self.direction == 3:
                pyxel.blt(self.x * 8, self.y * 8, 0, 16, 0, 8, 8, 0)
        else:
            pyxel.blt(self.x * 8, self.y * 8, 0, 0, 0, 8, 8, 0)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
