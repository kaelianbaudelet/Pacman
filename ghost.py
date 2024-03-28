from graph import *
from random import choice
from collections import deque
import pyxel


class Ghost:
    def __init__(self, x, y, labyrinthe, direction=0):
        self.x = x
        self.y = y
        self.labyrinthe = labyrinthe
        self.death = False
        self.vulnerable = False
        self.frame_vulnerable = 0
        self.direction = direction

    def deplacer(self):
        # Déplacement automatique tant que la direction ne change pas
        if self.direction == 0 and not self.labyrinthe.collision(self.x + 1, self.y):
            self.x += 1
        elif self.direction == 1 and not self.labyrinthe.collision(self.x, self.y - 1):
            self.y -= 1
        elif self.direction == 2 and not self.labyrinthe.collision(self.x - 1, self.y):
            self.x -= 1
        elif self.direction == 3 and not self.labyrinthe.collision(self.x, self.y + 1):
            self.y += 1

        if self.x > 26:
            self.x = 0
        elif self.x < 0:
            self.x = 26

    def get_direction(self):
        return self.direction

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_vulnerable(self):
        return self.vulnerable

    def get_death(self):
        return self.death

    def set_direction(self, direction):
        self.direction = direction

    def set_death(self, death):
        self.death = death
        if death:
            self.vulnerable = False

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def set_vulnerable(self, vulnerable):
        self.vulnerable = vulnerable
        if vulnerable:
            self.frame_vulnerable = pyxel.frame_count

    def set_unvulnerable(self):
        if pyxel.frame_count - self.frame_vulnerable > 480:
            self.vulnerable = False

    def affiche(self, col):
        if self.death:
            pyxel.blt(self.x * 8, self.y * 8, 0, 32, 8, 8, 8, 13)
        elif self.vulnerable:
            pyxel.blt(self.x * 8, self.y * 8, 0, 40, 8, 8, 8)
        else:
            pyxel.blt(self.x * 8, self.y * 8, 0, 8*col, 8, 8, 8)

class Blinky(Ghost):
    def __init__(self, labyrinthe, graph, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(11, 13, labyrinthe)
        self.graph = graph
        self.parcours = []
        self.speed = speed

    def deplacer(self, x, y):
        self.ghost.set_unvulnerable()

        if pyxel.frame_count % self.speed == 0:

            if self.ghost.get_x() == x and self.ghost.get_y() == y and self.ghost.get_vulnerable():
                self.ghost.set_death(True)
            if self.ghost.get_x() == 13 and self.ghost.get_y() == 13:
                self.ghost.set_death(False)

            if self.ghost.death:
                # change de direction en fonction du chemin
                chemin = self.graph.parcours_largeur(
                    (self.ghost.get_x(), self.ghost.get_y()), (13, 13))

                # Suivre le chemin
                y, x = chemin[1]
                self.ghost.set_coordinates(x, y)
            else:
                # change de direction en fonction du chemin
                # Calculer le chemin le plus court vers Pac-Man
                grille = self.labyrinthe.get_grille()
                chemin = get_chemin(
                    grille, (self.ghost.get_y(), self.ghost.get_x()), (y, x))

                # Suivre le chemin
                if chemin:
                    y, x = chemin[1]
                    self.ghost.set_coordinates(x, y)

    def can_be_eaten(self):
        self.ghost.set_vulnerable(True)

    def affiche(self):
        self.ghost.affiche(1)

class Inky(Ghost):
    def __init__(self, labyrinthe, graph, speed=10): 
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(13, 13, labyrinthe)
        self.graph = graph
        self.parcours = []
        self.speed = speed
        self.chemin_vulnerable = [] # chemin à suivre pour fuir

    def deplacer(self, x, y):
        self.ghost.set_unvulnerable()

        # le fantome fais ses actions en fonction de sa vitesse
        if pyxel.frame_count % self.speed == 0:

            if self.ghost.get_x() == x and self.ghost.get_y() == y and self.ghost.get_vulnerable():
                # le fantome meurt si il est vulnérable et qu'il est sur Pac man
                self.ghost.set_death(True)
            if self.ghost.get_x() == 13 and self.ghost.get_y() == 13 and self.ghost.get_death():
                # le fantome revient à la vie si il est mort et qu'il est sur la case de départ
                self.ghost.set_death(False)
            if not self.ghost.get_vulnerable():
                # on vide le chemin à suivre pour fuir si le fantome n'est plus vulnérable
                self.chemin_vulnerable = []

            if self.ghost.get_death():
                # change de direction en fonction du chemin
                chemin = self.graph.parcours_largeur(
                    (self.ghost.get_x(), self.ghost.get_y()), (13, 13))

                # Suivre le chemin
                y, x = chemin[1]
                self.ghost.set_coordinates(x, y)
            
            elif self.ghost.get_vulnerable():
                # Si le fantôme est vulnérable, il se déplace en suivant un chemin de parcour en profondeur
                if not self.chemin_vulnerable:
                    self.chemin_vulnerable = self.graph.parcours_profondeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (x, y))
                    self.chemin_vulnerable.pop(0)
                y, x = self.chemin_vulnerable.pop(0)
                self.ghost.set_coordinates(x, y)

            else:
                # change de direction en fonction du chemin
                chemin = self.graph.parcours_largeur(
                    (self.ghost.get_x(), self.ghost.get_y()), (x, y))

                # Suivre le chemin
                y, x = chemin[1]
                self.ghost.set_coordinates(x, y)

    def can_be_eaten(self):
        self.ghost.set_vulnerable(True)

    def affiche(self):
        self.ghost.affiche(0)
        
class Pinky(Ghost):
    def __init__(self, labyrinthe, graph, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(15, 13, labyrinthe)
        self.graph = graph
        self.speed = speed

    def deplacer(self, x, y):
        self.ghost.set_unvulnerable()

        if pyxel.frame_count % self.speed == 0:

            if self.ghost.get_x() == x and self.ghost.get_y() == y and self.ghost.get_vulnerable():
                self.ghost.set_death(True)
            if self.ghost.get_x() == 13 and self.ghost.get_y() == 13:
                self.ghost.set_death(False)

            if self.ghost.get_death():
                # change de direction en fonction du chemin
                chemin = self.graph.parcours_largeur(
                (self.ghost.get_x(), self.ghost.get_y()), (13, 13))

                # Suivre le chemin
                y, x = chemin[1]
                self.ghost.set_coordinates(x, y)
                
            else:
                chemin = self.graph.parcours_largeur(
                    (self.ghost.get_x(), self.ghost.get_y()), (x, y))

                # Suivre le chemin
                y, x = chemin[1]
                self.ghost.set_coordinates(x, y)

    def can_be_eaten(self):
        self.ghost.set_vulnerable(True)

    def affiche(self):
        self.ghost.affiche(2)

class Clyde(Ghost):
    def __init__(self, labyrinthe, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(17, 13, labyrinthe)
        self.speed = speed

    def deplacer(self):
        self.ghost.set_unvulnerable()

        if pyxel.frame_count % self.speed == 0:
            # on créé une liste de tous les chemins
            L_dir = []

            if not self.labyrinthe.collision(self.ghost.get_x() + 1, self.ghost.get_y()) and self.ghost.get_direction() != 2:
                L_dir.append(0)
            if not self.labyrinthe.collision(self.ghost.get_x(), self.ghost.get_y() - 1) and self.ghost.get_direction() != 3:
                L_dir.append(1)
            if not self.labyrinthe.collision(self.ghost.get_x() - 1, self.ghost.get_y()) and self.ghost.get_direction() != 0:
                L_dir.append(2)
            if not self.labyrinthe.collision(self.ghost.get_x(), self.ghost.get_y() + 1) and self.ghost.get_direction() != 1:
                L_dir.append(3)

            if len(L_dir) >= 1:
                self.ghost.set_direction(choice(L_dir))

            self.ghost.deplacer()

    def can_be_eaten(self):
        self.ghost.set_vulnerable(True)

    def affiche(self):
        self.ghost.affiche(3)
        
    