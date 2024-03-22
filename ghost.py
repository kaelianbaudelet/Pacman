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
        self.direction = direction

    def get_death(self):
        return self.death
          
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
    
    def set_direction(self, direction):
        self.direction = direction

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y
        
    def affiche(self, col):
        pyxel.rect(self.x * 8 + 1, self.y * 8 + 1, 6, 6, col)

class Blinky(Ghost):
    def __init__(self, labyrinthe, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(11, 13, labyrinthe)
        self.parcours = []
        self.speed = speed

    def deplacer(self, x, y):
        # si on a trouver pacman on tue le fantome
        if self.ghost.get_x() == x and self.ghost.get_y() == y:
            self.ghost.death = True

        if pyxel.frame_count % self.speed == 0:
            # change de direction en fonction du chemin
            if self.ghost.get_death(): # retour a la base
                self.ghost.deplacer_vers(11, 13)
                if self.ghost.get_x() == 11 and self.ghost.get_y() == 13:
                    self.ghost.death = False
            else:
                self.ghost.deplacer_vers(x, y)

    def affiche(self):
        self.ghost.affiche(8)

class Inky(Ghost):
    def __init__(self, labyrinthe, graph, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(13, 13, labyrinthe)
        self.graph = graph
        self.parcours = []
        self.speed = speed

    def deplacer(self, x, y):
        if self.ghost.get_x() == x and self.ghost.get_y() == y:
            self.ghost.death = True

        if pyxel.frame_count % self.speed == 0:
            # change de direction en fonction du chemin
            if self.ghost.get_death(): # retour a la base
                chemin = self.graph.parcours_largeur((self.ghost.get_x(), self.ghost.get_y()), (13, 13))
                if self.ghost.get_x() == 13 and self.ghost.get_y() == 13:
                    self.ghost.death = False
            else:
                chemin = self.graph.parcours_largeur((self.ghost.get_x(), self.ghost.get_y()), (x, y))

            # Suivre le chemin
            y, x = chemin[1]
            self.ghost.set_coordinates(x, y)

    def affiche(self):
        self.ghost.affiche(12)
        
class Pinky(Ghost):
    def __init__(self, labyrinthe, graph, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(15, 13, labyrinthe)
        self.graph = graph
        self.speed = speed

    def deplacer(self, x, y):
        # si au meme coordonnées que pacman, on met a mort
        if self.ghost.get_x() == x and self.ghost.get_y() == y:
            self.ghost.death = True

        if pyxel.frame_count % self.speed == 0:
            chemin = self.graph.parcours_profondeur((self.ghost.get_x(), self.ghost.get_y()), (x, y))

            # Suivre le chemin
            y, x = chemin[1]
            self.ghost.set_coordinates(x, y)

    def affiche(self):
        self.ghost.affiche(14)

class Clyde(Ghost):
    def __init__(self, labyrinthe, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(17, 13, labyrinthe)
        self.speed = speed
        
    def deplacer(self, x, y):
        # si au meme coordonnées que pacman, on met a mort
        if self.ghost.get_x() == x and self.ghost.get_y() == y:
            self.ghost.death = True

        if pyxel.frame_count % self.speed == 0:
            # on créé une liste de tous les chemins
            if self.ghost.get_death(): # retour a la base
                chemin = self.graph.parcours_largeur((self.ghost.get_x(), self.ghost.get_y()), (17, 13))
                if self.ghost.get_x() == 17 and self.ghost.get_y() == 13:
                    self.ghost.death = False
            else:
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
            
    def affiche(self):
        self.ghost.affiche(9)
        
    