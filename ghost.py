from math import e # Importation de la constante e
from graph import * # Importation de la classe Graph
from random import choice # Importation de la fonction choice
from collections import deque # Importation de la classe deque pour la file/la pile
import pyxel # Importation de la bibliothèque Pyxel


class Ghost:
    def __init__(self, x, y, labyrinthe, direction=0):
        """Constructeur de la classe Ghost"""
        self.x = x # Coordonnée x du fantôme
        self.y = y # Coordonnée y du fantôme
        self.labyrinthe = labyrinthe # Labyrinthe du fantôme
        self.death = False # Etat du fantôme (mort ou non)
        self.vulnerable = False # Etat du fantôme (vulnérable ou non)
        self.frame_vulnerable = 0 # Frame de la vulnérabilité
        self.direction = direction # Direction du fantôme

    def deplacer(self):
        """Déplacement du fantôme"""
        # On change la direction du fantôme en fonction de la direction et des collisions
        if self.direction == 0 and not self.labyrinthe.collision(
                self.x + 1, self.y):
            self.x += 1 # Le fantome se déplace à droite
        elif self.direction == 1 and not self.labyrinthe.collision(self.x, self.y - 1):
            self.y -= 1 # Le fantome se déplace en haut
        elif self.direction == 2 and not self.labyrinthe.collision(self.x - 1, self.y):
            self.x -= 1 # Le fantome se déplace à gauche
        elif self.direction == 3 and not self.labyrinthe.collision(self.x, self.y + 1):
            self.y += 1 # Le fantome se déplace en bas

        # On gère les téléportations (sortie de l'écran à gauche et à droite utilisées par Clyde)
        if self.x > 26:
            self.x = 0
        elif self.x < 0:
            self.x = 26

    def get_direction(self):
        """Renvoie la direction du fantôme"""
        return self.direction # Renvoie la direction du fantôme

    def get_x(self):
        """Renvoie la coordonnée x du fantôme"""
        return self.x # Renvoie la coordonnée x du fantôme

    def get_y(self):
        """Renvoie la coordonnée y du fantôme"""
        return self.y # Renvoie la coordonnée y du fantôme

    def get_vulnerable(self):
        """Renvoie si le fantôme est vulnérable ou non"""
        return self.vulnerable # Renvoie si le fantôme est vulnérable ou non

    def get_death(self):
        """Renvoie si le fantôme est mort ou non"""
        return self.death # Renvoie si le fantôme est mort ou non

    def set_direction(self, direction):
        """Définit la direction du fantôme"""
        self.direction = direction # Définit la direction du fantôme

    def set_death(self, death):
        """Définit si le fantôme est mort ou non"""
        self.death = death # Définit si le fantôme est mort ou non
        # Si le fantôme est mort, il n'est plus vulnérable
        if death: # Si le fantôme est mort
            self.vulnerable = False # Le fantôme n'est plus vulnérable

    def set_coordinates(self, x, y):
        """Définit les coordonnées du fantôme"""
        self.x = x # Coordonnée x du fantôme
        self.y = y # Coordonnée y du fantôme

    def set_vulnerable(self, vulnerable):
        """Définit si le fantôme est vulnérable ou non"""
        # On définit la vulnérabilité du fantôme
        self.vulnerable = vulnerable
        # On défini si le fantome est vulnérable ou non
        if vulnerable: # Si le fantôme est vulnérable
            self.frame_vulnerable = pyxel.frame_count # On définit la frame de la vulnérabilité

    def set_unvulnerable(self):
        """Définit le fantôme comme non vulnérable"""
        if pyxel.frame_count - self.frame_vulnerable > 480: # Si le fantôme n'est plus vulnérable
            self.vulnerable = False # Le fantôme n'est plus vulnérable

    def affiche(self, col):
        """Affichage du fantôme"""

        # On affiche le fantôme en fonction de son état
        if self.death: # Si le fantôme est mort
            pyxel.blt(self.x * 8, self.y * 8, 0, 32, 8, 8, 8, 13) # Affichage du fantôme mort
        elif self.vulnerable: # Si le fantôme est vulnérable
            pyxel.blt(self.x * 8, self.y * 8, 0, 40, 8, 8, 8) # Affichage du fantôme vulnérable avec les yeux bleus flottants
        else:
            pyxel.blt(self.x * 8, self.y * 8, 0, 8 * col, 8, 8, 8) # Affichage du fantôme normal


class Blinky(Ghost):
    """Classe du fantôme Blinky"""

    def __init__(self, labyrinthe, graph, speed=10):
        """Constructeur de la classe Blinky"""
        self.labyrinthe = labyrinthe # Labyrinthe du fantôme
        self.ghost = Ghost(13, 14, labyrinthe) # Fantôme Blinky
        self.graph = graph # Graphe du labyrinthe
        self.parcours = [] # Parcours du fantôme
        self.parcours_vulnerable = [] # Parcours du fantôme vulnérable
        self.speed = speed # Vitesse du fantôme
        self.en_attente = True # Etat du fantôme (en attente ou non)
        self.direction_attente = True # Direction du fantôme en attente

    def arreter_animation_attente(self):
        """Arrête l'animation d'attente du fantôme"""
        self.en_attente = False # Le fantôme n'est plus en attente

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

            # On tue le fantome si il est vulnérable et sur pac_man
            if self.ghost.get_x() == x and self.ghost.get_y() == y:
                if self.ghost.get_vulnerable():
                    self.ghost.set_death(True)
                elif not self.ghost.get_death():
                    return True

            # On fait revivre le fantome si il est mort et sur la case de départ
            if self.ghost.get_x() == 13 and self.ghost.get_y() == 13:
                self.ghost.set_death(False)

            if pyxel.frame_count % self.speed == 0:

                # On vide le chemin à suivre pour fuir si le fantome n'est plus vulnérable
                if not self.ghost.get_vulnerable():
                    self.parcours_vulnerable = []

                if self.ghost.death:
                    # Change de direction en fonction du chemin
                    chemin = self.graph.parcours_largeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (13, 13))  # utilisation du parcours en largeur

                    # Suivre le chemin
                    y, x = chemin[1]
                    self.ghost.set_coordinates(x, y)

                elif self.ghost.get_vulnerable():
                    # Si le fantôme est vulnérable, il se déplace en suivant un chemin de parcour en profondeur
                    if self.parcours_vulnerable == []:
                        self.parcours_vulnerable = self.graph.parcours_profondeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x, y))  # utilisation du parcours en profondeur
                        self.parcours_vulnerable.pop(0)
                    y, x = self.parcours_vulnerable.pop(0)
                    self.ghost.set_coordinates(x, y)

                else:
                    # Change de direction en fonction du chemin 
                    grille = self.labyrinthe.get_grille()
                    chemin = get_chemin(
                        grille, (self.ghost.get_y(), self.ghost.get_x()), (y, x))  # utilisation de dijkstra

                    # Suivre le chemin dans si pacman est à portée de vue
                    if len(chemin) > 1:
                        y, x = chemin[1]
                        self.ghost.set_coordinates(x, y)

    def can_be_eaten(self):
        """Rend le fantôme vulnérable"""
        self.ghost.set_vulnerable(True) # Rend le fantôme vulnérable

    def affiche_chemin(self, x, y):
        """Affiche le chemin du fantôme en mode développeur"""
        if self.ghost.get_vulnerable(): # Si le fantôme est vulnérable on affiche le chemin par rapport à Pacman
            chemin = self.graph.parcours_largeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x,y))
            for i in chemin:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 8)
        elif self.ghost.get_death(): # Si le fantôme est mort on affiche le chemin par rapport à la case de départ
            for i in self.parcours_vulnerable:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 8)
        else: # Sinon on affiche le chemin par rapport à Pacman
            chemin = self.graph.parcours_profondeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x,y))
            for i in chemin:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 8)

    def affiche(self):
        """Affiche le fantôme"""
        self.ghost.affiche(1) # Affiche le fantôme


class Inky(Ghost):
    """Classe du fantôme Inky"""
    def __init__(self, labyrinthe, graph, speed=10):
        """Constructeur de la classe Inky"""
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(15, 14, labyrinthe)
        self.graph = graph
        self.parcours = []
        self.speed = speed
        self.chemin_vulnerable = []  # chemin à suivre pour fuir
        self.en_attente = True
        self.direction_attente = True

    def arreter_animation_attente(self):
        """Arrête l'animation d'attente du fantôme"""
        self.en_attente = False # Le fantôme n'est plus en attente

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

            if self.ghost.get_x() == 15 and self.ghost.get_y() == 13 and self.ghost.get_death():
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
                        (self.ghost.get_x(), self.ghost.get_y()), (15, 13))

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
                    # Change de direction en fonction du chemin
                    chemin = self.graph.parcours_largeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (x, y)) # Utilisation du parcours en largeur

                    # Suivre le chemin
                    if len(chemin) > 1: # Si le chemin n'est pas vide
                        y, x = chemin[1] # On prend la prochaine case
                        self.ghost.set_coordinates(x, y) # On déplace le fantome

    def can_be_eaten(self):
        """Rend le fantôme vulnérable"""
        self.ghost.set_vulnerable(True) # Rend le fantôme vulnérable

    def affiche_chemin(self, x, y):
        """Affiche le chemin du fantôme en mode développeur"""
        if self.ghost.get_vulnerable(): # Si le fantôme est vulnérable on affiche le chemin par rapport à Pacman
            chemin = self.graph.parcours_largeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x,y))
            for i in chemin:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 12)
        elif self.ghost.get_death(): # Si le fantôme est mort on affiche le chemin par rapport à la case de départ
            for i in self.chemin_vulnerable:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 12)
        else: # Sinon on affiche le chemin par rapport à Pacman
            chemin = self.graph.parcours_profondeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x,y))
            for i in chemin:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 12)

    def affiche(self): # Affiche le fantôme
        self.ghost.affiche(0) # Affiche le fantôme

    def get_x(self): # Renvoie la coordonnée x du fantôme
        return self.ghost.get_x() # Renvoie la coordonnée x du fantôme

    def get_y(self): # Renvoie la coordonnée y du fantôme
        return self.ghost.get_y() # Renvoie la coordonnée y du fantôme


class Pinky(Ghost):
    def __init__(self, labyrinthe, graph, speed=10):
        self.labyrinthe = labyrinthe
        self.ghost = Ghost(14, 14, labyrinthe)
        self.graph = graph
        self.speed = speed
        self.chemin_vulnerable = []  # chemin à suivre pour fuir
        self.en_attente = True
        self.direction_attente = True

    def arreter_animation_attente(self):
        """Arrête l'animation d'attente du fantôme"""
        self.en_attente = False # Le fantôme n'est plus en attente

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

            if self.ghost.get_x() == 14 and self.ghost.get_y() == 14:
                self.ghost.set_death(False)

            if pyxel.frame_count % self.speed == 0:

                if not self.ghost.get_vulnerable():
                    self.chemin_vulnerable = []

                if self.ghost.get_death():
                    # change de direction en fonction du chemin
                    chemin = self.graph.parcours_largeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (14, 14))

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
        """Rend le fantôme vulnérable"""
        self.ghost.set_vulnerable(True) # Rend le fantôme vulnérable


    def affiche_chemin(self, x, y):
        """Affiche le chemin du fantôme en mode développeur"""
        if self.ghost.get_vulnerable():
            chemin = self.graph.parcours_largeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x,y))
            for i in chemin:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 13)
        elif self.ghost.get_death():
            for i in self.chemin_vulnerable:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 13)
        else:
            chemin = self.graph.parcours_profondeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x,y))
            for i in chemin:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 13)

    def affiche(self):
        self.ghost.affiche(2)

    def get_x(self):
        return self.ghost.get_x()

    def get_y(self): # Renvoie la coordonnée y du fantôme
        return self.ghost.get_y() # Renvoie la coordonnée y du fantôme


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
        """Arrête l'animation d'attente du fantôme"""
        self.en_attente = False # Le fantôme n'est plus en attente

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
        """Rend le fantôme vulnérable"""
        self.ghost.set_vulnerable(True) # Rend le fantôme vulnérable

    def affiche_chemin(self, x, y):
        """Affiche le chemin du fantôme en mode développeur"""
        
        if self.ghost.get_vulnerable(): # Si le fantôme est vulnérable, on affiche le chemin en fonction de Pacman
            chemin = self.graph.parcours_largeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x,y))
            for i in chemin:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 9)
        elif self.ghost.get_death(): # Si le fantôme est mort, on affiche le chemin en fonction de la case de départ
            chemin = self.graph.parcours_largeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (12, 14))
            for i in chemin:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 9)
        else: # Sinon, on affiche le chemin en fonction de la position de Pacman
            chemin = self.graph.parcours_profondeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x,y))
            for i in chemin:
                pyxel.rect(i[1]*8, i[0]*8, 8, 8, 9)

    def affiche(self):
        self.ghost.affiche(3)
