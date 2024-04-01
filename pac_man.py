import pyxel # Importation de la bibliothèque Pyxel
import random # Importation de la bibliothèque Random
from labyrinthe import * # Importation de la classe Lab


class Pac_man:
    def __init__(self, labyrinthe):
        """Constructeur de la classe Pac_man"""
        self.labyrinthe = labyrinthe # Labyrinthe
        self.x = 15  # Coordonnée initiale en x de Pacman
        self.y = 23  # Coordonnée initiale en y de Pacman
        self.direction = 0  # Direction de Pacman (0: droite, 1: haut, 2: gauche, 3: bas)
        self.next_direction = 0 # Prochaine direction si le joueur appuie sur une touche directionnelle pendant le déplacement
        self.speed = 10 # Vitesse de déplacement de Pacman
        self.sprite = True # Sprite de Pacman (True: bouche ouverte, False: bouche fermée)

    # Déplacement de Pacman
    def deplacer(self):
        """Déplacement de Pacman"""
        if pyxel.btn(pyxel.KEY_RIGHT): # Si le joueur appuie sur la touche directionnelle droite
            self.next_direction = 0 # la prochaine direction enregistrée est la droite
        elif pyxel.btn(pyxel.KEY_UP): # Si le joueur appuie sur la touche directionnelle haut
            self.next_direction = 1 # la prochaine direction enregistrée est le haut
        elif pyxel.btn(pyxel.KEY_LEFT): # Si le joueur appuie sur la touche directionnelle gauche
            self.next_direction = 2 # la prochaine direction enregistrée est la gauche
        elif pyxel.btn(pyxel.KEY_DOWN): # Si le joueur appuie sur la touche directionnelle bas
            self.next_direction = 3 # la prochaine direction enregistrée est le bas

        if pyxel.btn(pyxel.KEY_RIGHT) and not self.x == 27 and not self.labyrinthe.collision(
                self.x + 1, self.y): # Si le joueur appuie sur la touche directionnelle droite et qu'il n'y a pas de collision
            self.direction = 0 # la direction de Pacman est la droite
        elif pyxel.btn(pyxel.KEY_UP) and not self.labyrinthe.collision(self.x, self.y - 1): # Si le joueur appuie sur la touche directionnelle haut et qu'il n'y a pas de collision
            self.direction = 1 # la direction de Pacman est le haut
        elif pyxel.btn(pyxel.KEY_LEFT) and not self.labyrinthe.collision(self.x - 1, self.y): # Si le joueur appuie sur la touche directionnelle gauche et qu'il n'y a pas de collision
            self.direction = 2 # la direction de Pacman est la gauche
        elif pyxel.btn(pyxel.KEY_DOWN) and not self.labyrinthe.collision(self.x, self.y + 1): # Si le joueur appuie sur la touche directionnelle bas et qu'il n'y a pas de collision
            self.direction = 3 # la direction de Pacman est le bas

        if pyxel.frame_count % self.speed == 0:
            # Déplacement automatique tant que la direction ne change pas
            if self.direction == 0 and not self.x == 27 and not self.labyrinthe.collision(
                    self.x + 1, self.y): # Si la direction est la droite et qu'il n'y a pas de collision
                self.x += 1 # Pacman se déplace à droite
            elif self.direction == 1 and not self.labyrinthe.collision(self.x, self.y - 1): # Si la direction est le haut et qu'il n'y a pas de collision
                self.y -= 1 # Pacman se déplace en haut
            elif self.direction == 2 and not self.labyrinthe.collision(self.x - 1, self.y): # Si la direction est la gauche et qu'il n'y a pas de collision
                self.x -= 1 # Pacman se déplace à gauche
            elif self.direction == 3 and not self.labyrinthe.collision(self.x, self.y + 1): # Si la direction est le bas et qu'il n'y a pas de collision
                self.y += 1 # Pacman se déplace en bas

            if self.x > 26: # Si Pacman dépasse la limite de l'écran à droite
                self.x = 2 # On le replace à gauche de l'écran
            elif self.x < 1: # Si Pacman dépasse la limite de l'écran à gauche
                self.x = 26 # On le replace à droite de l'écran

            # Vérification de la prochaine direction
            
            if self.next_direction == 0 and not self.x == 27 and not self.labyrinthe.collision(
                    self.x + 1, self.y): # Si la prochaine direction est la droite et qu'il n'y a pas de collision
                self.direction = 0 # la direction de Pacman est la droite
            elif self.next_direction == 1 and not self.labyrinthe.collision(self.x, self.y - 1): # Si la prochaine direction est le haut et qu'il n'y a pas de collision
                self.direction = 1 # la direction de Pacman est le haut
            elif self.next_direction == 2 and not self.labyrinthe.collision(self.x - 1, self.y): # Si la prochaine direction est la gauche et qu'il n'y a pas de collision
                self.direction = 2 # la direction de Pacman est la gauche
            elif self.next_direction == 3 and not self.labyrinthe.collision(self.x, self.y + 1): # Si la prochaine direction est le bas et qu'il n'y a pas de collision
                self.direction = 3 # la direction de Pacman est le bas

    def afficher(self):
        """Affichage de Pacman"""

        # Animation de Pacman
        if pyxel.frame_count % (self.speed / 2) == 0: # Variation du sprite de Pacman.
            self.sprite = not self.sprite # Changement de sprite de Pacman (bouche ouverte ou fermée)

        # Affichage de Pacman
        if self.sprite:
            # Affichage de Pacman en fonction de sa direction
            if self.direction == 0: # Si la direction est la droite
                pyxel.blt(self.x * 8, self.y * 8, 0, 8, 0, 8, 8, 0) # Affichage de Pacman à droite
            elif self.direction == 1: # Si la direction est le haut
                pyxel.blt(self.x * 8, self.y * 8, 0, 32, 0, 8, 8, 0) # Affichage de Pacman en haut
            elif self.direction == 2: # Si la direction est la gauche
                pyxel.blt(self.x * 8, self.y * 8, 0, 24, 0, 8, 8, 0) # Affichage de Pacman à gauche
            elif self.direction == 3: # Si la direction est le bas
                pyxel.blt(self.x * 8, self.y * 8, 0, 16, 0, 8, 8, 0) # Affichage de Pacman en bas
        else:
            pyxel.blt(self.x * 8, self.y * 8, 0, 0, 0, 8, 8, 0) # Affichage de Pacman avec la bouche fermée

    def get_x(self):
        """Renvoie la coordonnée x de Pacman"""
        return self.x # Renvoie la coordonnée x de Pacman

    def get_y(self):
        """Renvoie la coordonnée y de Pacman"""
        return self.y # Renvoie la coordonnée y de Pacman
