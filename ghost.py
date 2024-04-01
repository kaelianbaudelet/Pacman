from math import e  # Importation de la constante e
from graph import *  # Importation de la classe Graph
from random import choice  # Importation de la fonction choice
from collections import deque  # Importation de la classe deque pour la file/la pile
import pyxel  # Importation de la bibliothèque Pyxel


class Ghost:
    """Classe du fantôme"""

    def __init__(self, x, y, labyrinthe, direction=0):
        """Constructeur de la classe Ghost"""
        self.x = x  # Coordonnée x du fantôme
        self.y = y  # Coordonnée y du fantôme
        self.labyrinthe = labyrinthe  # Labyrinthe du fantôme
        self.death = False  # Etat du fantôme (mort ou non)
        self.vulnerable = False  # Etat du fantôme (vulnérable ou non)
        self.frame_vulnerable = 0  # Frame de la vulnérabilité
        self.direction = direction  # Direction du fantôme

    def deplacer(self):
        """Déplacement du fantôme"""
        # On change la direction du fantôme en fonction de la direction et des
        # collisions
        if self.direction == 0 and not self.labyrinthe.collision(
                self.x + 1, self.y):
            self.x += 1  # Le fantome se déplace à droite
        elif self.direction == 1 and not self.labyrinthe.collision(self.x, self.y - 1):
            self.y -= 1  # Le fantome se déplace en haut
        elif self.direction == 2 and not self.labyrinthe.collision(self.x - 1, self.y):
            self.x -= 1  # Le fantome se déplace à gauche
        elif self.direction == 3 and not self.labyrinthe.collision(self.x, self.y + 1):
            self.y += 1  # Le fantome se déplace en bas

        # On gère les téléportations (sortie de l'écran à gauche et à droite
        # utilisées par Clyde)
        if self.x > 26:
            self.x = 0
        elif self.x < 0:
            self.x = 26

    def get_direction(self):
        """Renvoie la direction du fantôme"""
        return self.direction  # Renvoie la direction du fantôme

    def get_x(self):
        """Renvoie la coordonnée x du fantôme"""
        return self.x  # Renvoie la coordonnée x du fantôme

    def get_y(self):
        """Renvoie la coordonnée y du fantôme"""
        return self.y  # Renvoie la coordonnée y du fantôme

    def get_vulnerable(self):
        """Renvoie si le fantôme est vulnérable ou non"""
        return self.vulnerable  # Renvoie si le fantôme est vulnérable ou non

    def get_death(self):
        """Renvoie si le fantôme est mort ou non"""
        return self.death  # Renvoie si le fantôme est mort ou non

    def set_direction(self, direction):
        """Définit la direction du fantôme"""
        self.direction = direction  # Définit la direction du fantôme

    def set_death(self, death):
        """Définit si le fantôme est mort ou non"""
        self.death = death  # Définit si le fantôme est mort ou non
        # Si le fantôme est mort, il n'est plus vulnérable
        if death:  # Si le fantôme est mort
            pyxel.play(2, 13)
            self.vulnerable = False  # Le fantôme n'est plus vulnérable

    def set_coordinates(self, x, y):
        """Définit les coordonnées du fantôme"""
        self.x = x  # Coordonnée x du fantôme
        self.y = y  # Coordonnée y du fantôme

    def set_vulnerable(self, vulnerable):
        """Définit si le fantôme est vulnérable ou non"""
        # On définit la vulnérabilité du fantôme
        self.vulnerable = vulnerable
        # On défini si le fantome est vulnérable ou non
        if vulnerable:  # Si le fantôme est vulnérable
            # On définit la frame de la vulnérabilité
            self.frame_vulnerable = pyxel.frame_count

    def set_unvulnerable(self):
        """Définit le fantôme comme non vulnérable"""
        if pyxel.frame_count - self.frame_vulnerable > 480:  # Si le fantôme n'est plus vulnérable
            self.vulnerable = False  # Le fantôme n'est plus vulnérable

    def affiche(self, col):
        """Affichage du fantôme"""

        # On affiche le fantôme en fonction de son état
        if self.death:  # Si le fantôme est mort
            pyxel.blt(self.x * 8, self.y * 8, 0, 32, 8, 8,
                      8, 13)  # Affichage du fantôme mort
        elif self.vulnerable:  # Si le fantôme est vulnérable
            # Affichage du fantôme vulnérable avec les yeux bleus flottants
            pyxel.blt(self.x * 8, self.y * 8, 0, 40, 8, 8, 8)
        else:
            pyxel.blt(self.x * 8, self.y * 8, 0, 8 * col, 8,
                      8, 8)  # Affichage du fantôme normal


class Blinky(Ghost):
    """Classe du fantôme Blinky"""

    def __init__(self, labyrinthe, graph, speed=10):
        """Constructeur de la classe Blinky"""
        self.labyrinthe = labyrinthe  # Labyrinthe du fantôme
        self.ghost = Ghost(13, 14, labyrinthe)  # Fantôme Blinky
        self.graph = graph  # Graphe du labyrinthe
        self.parcours = []  # Parcours du fantôme
        self.parcours_vulnerable = []  # Parcours du fantôme vulnérable
        self.speed = speed  # Vitesse du fantôme
        self.en_attente = True  # Etat du fantôme (en attente ou non)
        self.direction_attente = True  # Direction du fantôme en attente

    def arreter_animation_attente(self):
        """Arrête l'animation d'attente du fantôme"""
        self.en_attente = False  # Le fantôme n'est plus en attente

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

            # On fait revivre le fantome si il est mort et sur la case de
            # départ
            if self.ghost.get_x() == 13 and self.ghost.get_y() == 13:
                self.ghost.set_death(False)

            if pyxel.frame_count % self.speed == 0:

                # On vide le chemin à suivre pour fuir si le fantome n'est plus
                # vulnérable
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
                    # Si le fantôme est vulnérable, il se déplace en suivant un
                    # chemin de parcour en profondeur
                    if self.parcours_vulnerable == []:
                        self.parcours_vulnerable = self.graph.parcours_profondeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x, y))  # utilisation du parcours en profondeur
                        self.parcours_vulnerable.pop(0)
                    y, x = self.parcours_vulnerable.pop(0)
                    self.ghost.set_coordinates(x, y)

                else:
                    # Change de direction en fonction du chemin
                    grille = self.labyrinthe.get_grille()
                    # utilisation de dijkstra
                    chemin = get_chemin(
                        grille, (self.ghost.get_y(), self.ghost.get_x()), (y, x))

                    # Suivre le chemin dans si pacman est à portée de vue
                    if len(chemin) > 1:
                        y, x = chemin[1]
                        self.ghost.set_coordinates(x, y)

    def can_be_eaten(self):
        """Rend le fantôme vulnérable"""
        self.ghost.set_vulnerable(True)  # Rend le fantôme vulnérable

    def affiche_chemin(self, x, y):
        """Affiche le chemin du fantôme en mode développeur"""
        if self.ghost.get_vulnerable(
        ):  # Si le fantôme est vulnérable on affiche le chemin par rapport à Pacman
            chemin = self.graph.parcours_largeur(
                (self.ghost.get_x(), self.ghost.get_y()), (x, y))
            for i in chemin:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 8)
        elif self.ghost.get_death():  # Si le fantôme est mort on affiche le chemin par rapport à la case de départ
            for i in self.parcours_vulnerable:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 8)
        else:  # Sinon on affiche le chemin par rapport à Pacman
            chemin = self.graph.parcours_profondeur(
                (self.ghost.get_x(), self.ghost.get_y()), (x, y))
            for i in chemin:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 8)

    def affiche(self):
        """Affiche le fantôme"""
        self.ghost.affiche(1)  # Affiche le fantôme


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
        self.en_attente = False  # Le fantôme n'est plus en attente

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
                    # Si le fantôme est vulnérable, il se déplace en suivant un
                    # chemin de parcour en profondeur
                    if not self.chemin_vulnerable:
                        self.chemin_vulnerable = self.graph.parcours_profondeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x, y))
                        self.chemin_vulnerable.pop(0)
                    y, x = self.chemin_vulnerable.pop(0)
                    self.ghost.set_coordinates(x, y)

                else:
                    # Change de direction en fonction du chemin
                    chemin = self.graph.parcours_largeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (x, y))  # Utilisation du parcours en largeur

                    # Suivre le chemin
                    if len(chemin) > 1:  # Si le chemin n'est pas vide
                        y, x = chemin[1]  # On prend la prochaine case
                        self.ghost.set_coordinates(
                            x, y)  # On déplace le fantome

    def can_be_eaten(self):
        """Rend le fantôme vulnérable"""
        self.ghost.set_vulnerable(True)  # Rend le fantôme vulnérable

    def affiche_chemin(self, x, y):
        """Affiche le chemin du fantôme en mode développeur"""
        if self.ghost.get_vulnerable(
        ):  # Si le fantôme est vulnérable on affiche le chemin par rapport à Pacman
            chemin = self.graph.parcours_largeur(
                (self.ghost.get_x(), self.ghost.get_y()), (x, y))
            for i in chemin:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 12)
        elif self.ghost.get_death():  # Si le fantôme est mort on affiche le chemin par rapport à la case de départ
            for i in self.chemin_vulnerable:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 12)
        else:  # Sinon on affiche le chemin par rapport à Pacman
            chemin = self.graph.parcours_profondeur(
                (self.ghost.get_x(), self.ghost.get_y()), (x, y))
            for i in chemin:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 12)

    def affiche(self):
        """Affiche le fantôme"""
        self.ghost.affiche(0)  # Affiche le fantôme

    def get_x(self):
        """Renvoie la coordonnée x du fantôme"""
        return self.ghost.get_x()  # Renvoie la coordonnée x du fantôme

    def get_y(self):
        """Renvoie la coordonnée y du fantôme"""
        return self.ghost.get_y()  # Renvoie la coordonnée y du fantôme


class Pinky(Ghost):
    """Classe du fantôme Pinky"""

    def __init__(self, labyrinthe, graph, speed=10):
        """Constructeur de la classe Pinky"""
        self.labyrinthe = labyrinthe  # Labyrinthe du fantôme
        self.ghost = Ghost(14, 14, labyrinthe)  # Fantôme Pinky
        self.graph = graph  # Graphe du labyrinthe
        self.speed = speed  # Vitesse du fantôme
        self.chemin_vulnerable = []  # chemin à suivre pour fuir
        self.en_attente = True  # Etat du fantôme (en attente ou non)
        self.direction_attente = True  # Direction du fantôme en attente

    def arreter_animation_attente(self):
        """Arrête l'animation d'attente du fantôme"""
        self.en_attente = False  # Le fantôme n'est plus en attente

    def deplacer(self, x, y):
        """Déplacement du fantôme Pinky"""
        # Si le fantôme est en attente
        if self.en_attente:
            # Vitesse du fantôme
            if pyxel.frame_count % self.speed == 0:

                # Si le fantôme est en attente, il se déplace de haut en bas
                if self.direction_attente:
                    # Si le fantôme est en haut, il descend
                    if self.ghost.get_y() < 15:  # Si le fantôme est en haut
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() + 1)  # Le fantôme descend
                    else:
                        self.direction_attente = False  # Le fantôme ne monte plus
                else:  # Sinon le fantôme monte
                    # Descendre
                    if self.ghost.get_y() > 13:  # Si le fantôme est en bas
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() - 1)  # Le fantôme monte
                    else:
                        self.direction_attente = True  # Le fantôme ne descend plus

        else:
            self.ghost.set_unvulnerable()  # Le fantôme n'est plus vulnérable

            if self.ghost.get_x() == x and self.ghost.get_y(
            ) == y:  # Si le fantôme est sur Pacman
                if self.ghost.get_vulnerable():  # Si le fantôme est vulnérable
                    self.ghost.set_death(True)  # Le fantôme meurt
                elif not self.ghost.get_death():  # Si le fantôme n'est pas mort
                    return True  # On renvoie True

            if self.ghost.get_x() == 14 and self.ghost.get_y(
            ) == 14:  # Si le fantôme est sur la case de départ
                self.ghost.set_death(False)  # Le fantôme n'est plus mort

            # Vitese du fantôme
            if pyxel.frame_count % self.speed == 0:

                # On vide le chemin à suivre pour fuir si le fantôme n'est plus
                # vulnérable
                if not self.ghost.get_vulnerable():
                    self.chemin_vulnerable = []  # On vide le chemin à suivre pour fuir

                # Si le fantôme est mort
                if self.ghost.get_death():

                    chemin = self.graph.parcours_largeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (14, 14))  # Utilisation du parcours en largeur

                    # Suivre le chemin
                    if len(chemin) > 1:
                        y, x = chemin[1]  # On prend la prochaine case
                        self.ghost.set_coordinates(
                            x, y)  # On déplace le fantôme

                elif self.ghost.get_vulnerable():
                    # Si le fantôme est vulnérable, il se déplace en suivant un
                    # chemin de parcour en profondeur
                    if self.chemin_vulnerable == []:
                        # On définit le chemin à suivre pour fuir
                        self.chemin_vulnerable = self.graph.parcours_profondeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (x, y))
                        # On enlève la première case
                        self.chemin_vulnerable.pop(0)
                    y, x = self.chemin_vulnerable.pop(
                        0)  # On prend la prochaine case
                    self.ghost.set_coordinates(x, y)  # On déplace le fantôme

                else:
                    chemin = self.graph.parcours_largeur(
                        (self.ghost.get_x(), self.ghost.get_y()), (x, y))  # Utilisation du parcours en largeur

                    # Suivre le chemin
                    if len(chemin) > 1:  # Si le chemin n'est pas vide
                        y, x = chemin[1]  # On prend la prochaine case
                        self.ghost.set_coordinates(
                            x, y)  # On déplace le fantôme

    def can_be_eaten(self):
        """Rend le fantôme vulnérable"""
        self.ghost.set_vulnerable(True)  # Rend le fantôme vulnérable

    def affiche_chemin(self, x, y):
        """Affiche le chemin du fantôme en mode développeur"""
        if self.ghost.get_vulnerable():  # Si le fantôme est vulnérable
            chemin = self.graph.parcours_largeur(
                (self.ghost.get_x(), self.ghost.get_y()), (x, y))  # Utilisation du parcours en largeur
            for i in chemin:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 13)
        elif self.ghost.get_death():  # Si le fantôme est mort
            # On affiche le chemin en fonction de la case de départ
            for i in self.chemin_vulnerable:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 13)
        else:  # Sinon
            chemin = self.graph.parcours_profondeur((self.ghost.get_x(
            ), self.ghost.get_y()), (x, y))  # Utilisation du parcours en profondeur
            # On affiche le chemin en fonction de la position de Pacman
            for i in chemin:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 13)

    def affiche(self):
        """Affiche le fantôme"""
        self.ghost.affiche(2)  # Affiche le fantôme

    def get_x(self):
        """Renvoie la coordonnée x du fantôme"""
        return self.ghost.get_x()  # Renvoie la coordonnée x du fantôme

    def get_y(self):
        """Renvoie la coordonnée y du fantôme"""
        return self.ghost.get_y()  # Renvoie la coordonnée y du fantôme


class Clyde(Ghost):
    """Classe du fantôme Clyde"""

    def __init__(self, labyrinthe, graph, speed=10):
        """Constructeur de la classe Clyde"""
        self.labyrinthe = labyrinthe  # Labyrinthe du fantôme
        self.graph = graph  # Graphe du labyrinthe
        self.ghost = Ghost(12, 14, labyrinthe)  # Fantôme Clyde
        self.speed = speed  # Vitesse du fantôme
        self.en_attente = True  # Etat du fantôme (en attente ou non)
        self.direction_attente = True  # Direction du fantôme en attente
        self.omniscience_temporaire = True  # Omniscience temporaire de Clyde

    def arreter_animation_attente(self):
        """Arrête l'animation d'attente du fantôme"""
        self.en_attente = False  # Le fantôme n'est plus en attente

    def deplacer(self, x, y):
        """Déplacement du fantôme Clyde"""
        # Si le fantôme est en attente
        if self.en_attente:
            # Vitesse du fantôme
            if pyxel.frame_count % self.speed == 0:
                # Si le fantôme est en attente, il se déplace de haut en bas
                if self.direction_attente:
                    # Si le fantôme est en haut, il descend
                    if self.ghost.get_y() < 15:  # Si le fantôme est en haut
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() + 1)  # Le fantôme descend
                    else:
                        # Le fantôme ne monte plus
                        self.direction_attente = False  # Le fantôme ne monte plus
                else:
                    # S'il est en bas, il monte
                    if self.ghost.get_y() > 13:  # Si le fantôme est en bas
                        self.ghost.set_coordinates(
                            self.ghost.get_x(), self.ghost.get_y() - 1)  # Le fantôme monte
                    else:
                        # Le fantôme ne descend plus
                        self.direction_attente = True  # Le fantôme ne descend plus

        else:
            # Le fantôme n'est plus vulnérable
            if self.ghost.get_x() == x and self.ghost.get_y(
            ) == y:  # Si le fantôme est sur Pacman
                if self.ghost.get_vulnerable():  # Si le fantôme est vulnérable
                    self.ghost.set_death(True)  # Le fantôme meurt
                elif not self.ghost.get_death():  # Si le fantôme n'est pas mort
                    return True  # On renvoie True

            if pyxel.frame_count % self.speed == 0:
                # Permet de rendre le fantôme omniscient pendant 4 secondes
                # pour le force à fuir
                if self.omniscience_temporaire:
                    # On créé une liste de tous les chemins vers Pacman
                    chemin = get_chemin(
                        self.labyrinthe.get_grille(), (self.ghost.get_y(), self.ghost.get_x()), (y, x))

                    # Suivre le chemin
                    if len(chemin) > 1:  # Si le chemin n'est pas vide
                        y, x = chemin[1]  # On prend la prochaine case
                        self.ghost.set_coordinates(
                            x, y)  # On déplace le fantôme

                    # On rend le fantôme omniscient pendant 4 secondes
                    if pyxel.frame_count % 13 == 0:  # Si le temps est un multiple de 13
                        # On rend le fantôme omniscient pendant 4 secondes
                        self.omniscience_temporaire = False

                else:
                    # Le fantôme n'est plus vulnérable
                    self.ghost.set_unvulnerable()

                    if self.ghost.get_x() == 12 and self.ghost.get_y(
                    ) == 14:  # Si le fantôme est sur la case de départ
                        # Le fantôme n'est plus mort
                        self.ghost.set_death(False)
                        self.omniscience_temporaire = True  # On rend le fantôme omniscient

                    if not self.ghost.get_vulnerable():  # Si le fantôme n'est plus vulnérable
                        self.chemin_vulnerable = []  # On vide le chemin à suivre pour fuir

                    if self.ghost.get_death():
                        # Change de direction en fonction du chemin
                        chemin = self.graph.parcours_largeur(
                            (self.ghost.get_x(), self.ghost.get_y()), (12, 14))  # Utilisation du parcours en largeur

                        # Suivre le chemin
                        if len(chemin) > 1:  # Si le chemin n'est pas vide
                            y, x = chemin[1]  # On prend la prochaine case
                            self.ghost.set_coordinates(
                                x, y)  # On déplace le fantôme

                    else:
                        # Change de direction en fonction du chemin
                        L_dir = []  # Liste des directions possibles

                        if not self.labyrinthe.collision(
                                self.ghost.get_x() + 1,
                                self.ghost.get_y()) and self.ghost.get_direction() != 2:  # Si le fantôme peut aller à droite
                            L_dir.append(0)  # On ajoute la direction droite
                        if not self.labyrinthe.collision(self.ghost.get_x(), self.ghost.get_y(
                        ) - 1) and self.ghost.get_direction() != 3:  # Si le fantôme peut aller en haut
                            L_dir.append(1)  # On ajoute la direction haut
                        if not self.labyrinthe.collision(
                                self.ghost.get_x() - 1,
                                self.ghost.get_y()) and self.ghost.get_direction() != 0:  # Si le fantôme peut aller à gauche
                            L_dir.append(2)  # On ajoute la direction gauche
                        if not self.labyrinthe.collision(self.ghost.get_x(), self.ghost.get_y(
                        ) + 1) and self.ghost.get_direction() != 1:  # Si le fantôme peut aller en bas
                            L_dir.append(3)  # On ajoute la direction bas

                        if len(
                                L_dir) >= 1:  # Si la liste des directions possibles est supérieure ou égale à 1
                            # On choisit une direction aléatoire
                            self.ghost.set_direction(choice(L_dir))

                        self.ghost.deplacer()  # On déplace le fantôme

    def can_be_eaten(self):
        """Rend le fantôme vulnérable"""
        self.ghost.set_vulnerable(True)  # Rend le fantôme vulnérable

    def affiche_chemin(self, x, y):
        """Affiche le chemin du fantôme en mode développeur"""

        if self.ghost.get_vulnerable(
        ):  # Si le fantôme est vulnérable, on affiche le chemin en fonction de Pacman
            chemin = self.graph.parcours_largeur(
                (self.ghost.get_x(), self.ghost.get_y()), (x, y))  # Utilisation du parcours en largeur
            # On affiche le chemin
            for i in chemin:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 9)
        elif self.ghost.get_death():  # Si le fantôme est mort, on affiche le chemin en fonction de la case de départ
            chemin = self.graph.parcours_largeur(
                (self.ghost.get_x(),
                 self.ghost.get_y()),
                (12,
                 14))  # Utilisation du parcours en largeur
            for i in chemin:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 9)  # On affiche le chemin
        else:  # Sinon, on affiche le chemin en fonction de la position de Pacman
            chemin = self.graph.parcours_profondeur((self.ghost.get_x(
            ), self.ghost.get_y()), (x, y))  # Utilisation du parcours en profondeur
            # On affiche le chemin
            for i in chemin:
                pyxel.rect(i[1] * 8, i[0] * 8, 8, 8, 9)  # On affiche le chemin

    def affiche(self):
        """Affiche le fantôme"""
        self.ghost.affiche(3)  # Affiche le fantôme
