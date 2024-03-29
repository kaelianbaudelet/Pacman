from math import e
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
        if self.direction == 0 and not self.labyrinthe.collision(
                self.x + 1, self.y):
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
            pyxel.blt(self.x * 8, self.y * 8, 0, 8 * col, 8, 8, 8)


class Blinky(Ghost):
    def __init__(self, labyrinthe, graph, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(13, 14, labyrinthe)
        self.graph = graph
        self.parcours = []
        self.parcours_vulnerable = []
        self.speed = speed
        self.en_attente = True
        self.direction_attente = True

    def arreter_animation_attente(self):
        self.en_attente = False

    def deplacer(self, x, y):
        if self.en_attente:
            # on ignore x et y si le fantome est en attente
            if pyxel.frame_count % self.speed == 0:
                if self.direction_attente:
                    # Monter
                    if self.ghost.get_y() < 15:
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() + 1)
                    else:
                        self.direction_attente = False
                else:
                    # Descendre
                    if self.ghost.get_y() > 13:
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() - 1)
                    else:
                        self.direction_attente = True

        else:
            self.ghost.set_unvulnerable()

            # on tue le fantome si il est vulnérable et sur pac_man
            if self.ghost.get_x() == x and self.ghost.get_y() == y:
                if self.ghost.get_vulnerable():
                    self.ghost.set_death(True)
                elif not self.ghost.get_death():
                    return True

            # on fait revivre le fantome si il est mort et sur la case de
            # départ
            if self.ghost.get_x() == 13 and self.ghost.get_y() == 13:
                self.ghost.set_death(False)

            if pyxel.frame_count % self.speed == 0:

                # on vide le chemin à suivre pour fuir si le fantome n'est plus
                # vulnérable
                if not self.ghost.get_vulnerable():
                    self.parcours_vulnerable = []

                if self.ghost.death:
                    # change de direction en fonction du chemin
                    chemin = self.graph.parcours_largeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (13, 13))  # utilisation du parcours en largeur

                    # Suivre le chemin
                    y, x = chemin[1]
                    self.ghost.set_coordinates(x, y)

                elif self.ghost.get_vulnerable():
                    # Si le fantôme est vulnérable, il se déplace en suivant un
                    # chemin de parcour en profondeur
                    if self.parcours_vulnerable == []:
                        self.parcours_vulnerable = self.graph.parcours_profondeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x, y))  # utilisation du parcours en profondeur
                        self.parcours_vulnerable.pop(0)
                    y, x = self.parcours_vulnerable.pop(0)
                    self.ghost.set_coordinates(x, y)

                else:
                    # change de direction en fonction du chemin
                    # Calculer le chemin le plus court vers Pac-Man
                    grille = self.labyrinthe.get_grille()
                    chemin = get_chemin(
                        grille, (self.ghost.get_y(), self.ghost.get_x()), (y, x))  # utilisation de dijkstra

                    # Suivre le chemin dans si pacman est à portée de vue
                    if len(chemin) > 1:
                        y, x = chemin[1]
                        self.ghost.set_coordinates(x, y)

    def can_be_eaten(self):
        self.ghost.set_vulnerable(True)

    def affiche(self):
        self.ghost.affiche(1)


class Inky(Ghost):
    def __init__(self, labyrinthe, graph, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(15, 14, labyrinthe)
        self.graph = graph
        self.parcours = []
        self.speed = speed
        self.chemin_vulnerable = []  # chemin à suivre pour fuir
        self.en_attente = True
        self.direction_attente = True

    def arreter_animation_attente(self):
        self.en_attente = False

    def deplacer(self, x, y):
        if self.en_attente:
            # on ignore x et y si le fantome est en attente
            if pyxel.frame_count % self.speed == 0:
                if self.direction_attente:
                    # Monter
                    if self.ghost.get_y() < 15:
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() + 1)
                    else:
                        self.direction_attente = False
                else:
                    # Descendre
                    if self.ghost.get_y() > 13:
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() - 1)
                    else:
                        self.direction_attente = True

        else:
            self.ghost.set_unvulnerable()

            if self.ghost.get_x() == x and self.ghost.get_y() == y:
                # le fantome meurt si il est vulnérable et qu'il est sur Pac
                # man
                if self.ghost.get_vulnerable():
                    self.ghost.set_death(True)
                elif not self.ghost.get_death():
                    return True

            if self.ghost.get_x() == 13 and self.ghost.get_y() == 13 and self.ghost.get_death():
                # le fantome revient à la vie si il est mort et qu'il est sur
                # la case de départ
                self.ghost.set_death(False)

            # le fantome fais ses actions en fonction de sa vitesse
            if pyxel.frame_count % self.speed == 0:

                if not self.ghost.get_vulnerable():
                    # on vide le chemin à suivre pour fuir si le fantome n'est
                    # plus vulnérable
                    self.chemin_vulnerable = []

                if self.ghost.get_death():
                    # change de direction en fonction du chemin
                    chemin = self.graph.parcours_largeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (13, 13))

                    # Suivre le chemin
                    y, x = chemin[1]
                    self.ghost.set_coordinates(x, y)

                elif self.ghost.get_vulnerable():
                    # Si le fantôme est vulnérable, il se déplace en suivant un
                    # chemin de parcour en profondeur
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
                    if len(chemin) > 1:
                        y, x = chemin[1]
                        self.ghost.set_coordinates(x, y)

    def can_be_eaten(self):
        self.ghost.set_vulnerable(True)

    def affiche(self):
        self.ghost.affiche(0)

    def get_x(self):
        return self.ghost.get_x()

    def get_y(self):
        return self.ghost.get_y()


class Pinky(Ghost):
    def __init__(self, labyrinthe, graph, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(14, 13, labyrinthe)
        self.graph = graph
        self.speed = speed
        self.chemin_vulnerable = []  # chemin à suivre pour fuir
        self.en_attente = True
        self.direction_attente = True

    def arreter_animation_attente(self):
        self.en_attente = False

    def deplacer(self, x, y):
        if self.en_attente:
            # on ignore x et y si le fantome est en attente
            if pyxel.frame_count % self.speed == 0:
                if self.direction_attente:
                    # Monter
                    if self.ghost.get_y() < 15:
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() + 1)
                    else:
                        self.direction_attente = False
                else:
                    # Descendre
                    if self.ghost.get_y() > 13:
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() - 1)
                    else:
                        self.direction_attente = True

        else:
            self.ghost.set_unvulnerable()

            if self.ghost.get_x() == x and self.ghost.get_y() == y:
                if self.ghost.get_vulnerable():
                    self.ghost.set_death(True)
                elif not self.ghost.get_death():
                    return True

            if self.ghost.get_x() == 13 and self.ghost.get_y() == 13:
                self.ghost.set_death(False)

            if pyxel.frame_count % self.speed == 0:

                if not self.ghost.get_vulnerable():
                    self.chemin_vulnerable = []

                if self.ghost.get_death():
                    # change de direction en fonction du chemin
                    chemin = self.graph.parcours_largeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (13, 13))

                    # Suivre le chemin
                    if len(chemin) > 1:
                        y, x = chemin[1]
                        self.ghost.set_coordinates(x, y)

                elif self.ghost.get_vulnerable():
                    # Si le fantôme est vulnérable, il se déplace en suivant un
                    # chemin de parcour en profondeur
                    if self.chemin_vulnerable == []:
                        self.chemin_vulnerable = self.graph.parcours_profondeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x, y))
                        self.chemin_vulnerable.pop(0)
                    y, x = self.chemin_vulnerable.pop(0)
                    self.ghost.set_coordinates(x, y)

                else:
                    chemin = self.graph.parcours_largeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (x, y))

                    # Suivre le chemin
                    if len(chemin) > 1:
                        y, x = chemin[1]
                        self.ghost.set_coordinates(x, y)

    def can_be_eaten(self):
        self.ghost.set_vulnerable(True)

    def affiche(self):
        self.ghost.affiche(2)

    def get_x(self):
        return self.ghost.get_x()

    def get_y(self):
        return self.ghost.get_y()


class Clyde(Ghost):
    def __init__(self, labyrinthe, graph, speed=10):
        self.labyrinthe = labyrinthe
        self.graph = graph
        self.ghost = Ghost(12, 14, labyrinthe)
        self.speed = speed
        self.en_attente = True
        self.direction_attente = True
        self.omniscience_temporaire = True

    def arreter_animation_attente(self):
        self.en_attente = False

    def deplacer(self, x, y):
        if self.en_attente:
            # on ignore x et y si le fantome est en attente
            if pyxel.frame_count % self.speed == 0:
                if self.direction_attente:
                    # Monter
                    if self.ghost.get_y() < 15:
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() + 1)
                    else:
                        self.direction_attente = False
                else:
                    # Descendre
                    if self.ghost.get_y() > 13:
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() - 1)
                    else:
                        self.direction_attente = True

        else:

            if self.ghost.get_x() == x and self.ghost.get_y() == y:
                if self.ghost.get_vulnerable():
                    self.ghost.set_death(True)
                elif not self.ghost.get_death():
                    return True
                
            if pyxel.frame_count % self.speed == 0:
                if self.omniscience_temporaire:
                    # permet temporairment a clyde de sortir de la maison de
                    # force sans qu'il fasse n'imprte quoi et reste bloqué
                    # dedans

                    # dijkstra avec get_chemin

                    chemin = get_chemin(
                        self.labyrinthe.get_grille(), (self.ghost.get_y(), self.ghost.get_x()), (y, x))

                    # Suivre le chemin
                    if len(chemin) > 1:
                        y, x = chemin[1]
                        self.ghost.set_coordinates(x, y)

                    # on desactive l'omniscience de clyde après 4 secondes
                    if pyxel.frame_count % 13 == 0:
                        self.omniscience_temporaire = False

                else:

                    self.ghost.set_unvulnerable()

                    # on créé une liste de tous les chemins

                    if self.ghost.get_x() == 12 and self.ghost.get_y() == 14:
                        self.ghost.set_death(False)
                        self.omniscience_temporaire = True

                    if not self.ghost.get_vulnerable():
                        self.chemin_vulnerable = []

                    if self.ghost.get_death():
                        # change de direction en fonction du chemin
                        chemin = self.graph.parcours_largeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (12, 14))

                        # Suivre le chemin
                        if len(chemin) > 1:
                            y, x = chemin[1]
                            self.ghost.set_coordinates(x, y)

                    else:
                        L_dir = []

                        if not self.labyrinthe.collision(self.ghost.get_x(
                        ) + 1, self.ghost.get_y()) and self.ghost.get_direction() != 2:
                            L_dir.append(0)
                        if not self.labyrinthe.collision(self.ghost.get_x(
                        ), self.ghost.get_y() - 1) and self.ghost.get_direction() != 3:
                            L_dir.append(1)
                        if not self.labyrinthe.collision(self.ghost.get_x(
                        ) - 1, self.ghost.get_y()) and self.ghost.get_direction() != 0:
                            L_dir.append(2)
                        if not self.labyrinthe.collision(self.ghost.get_x(
                        ), self.ghost.get_y() + 1) and self.ghost.get_direction() != 1:
                            L_dir.append(3)

                        if len(L_dir) >= 1:
                            self.ghost.set_direction(choice(L_dir))

                        self.ghost.deplacer()

    def can_be_eaten(self):
        self.ghost.set_vulnerable(True)

    def affiche(self):
        self.ghost.affiche(3)
