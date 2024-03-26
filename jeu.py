import pyxel

from ghost import *
from pac_man import *
from labyrinthe import *
from graph import *


class Jeu:

    def __init__(self, laby):

        pyxel.init(224, 264, title="Pac-man", fps=60)
        pyxel.load("res.pyxres")

        # création du labyrinthe
        self.L = Lab(laby)
        # et du graphe
        self.G = Graph(laby)

        # creation de Pac Man
        self.pac_man = Pac_man(self.L)

        # création des fantomes
        self.clyde = Clyde(self.L, speed=14)
        self.blinky = Blinky(self.L, speed=14)
        self.pinky = Pinky(self.L, self.G, speed=14)
        self.inky = Inky(self.L, self.G, speed=14)

        self.powertime = False
        self.game_started = False

        self.pac_man_bouche_compteur = 0
        self.pac_man_ecrant_titre_x = -10

        # score
        self.score = 0

        # Lancement du jeu
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_started:
            
            # deplacement des fantomes
            self.clyde.deplacer()
            self.blinky.deplacer(self.pac_man.get_x(), self.pac_man.get_y())
            self.pinky.deplacer(self.pac_man.get_x(), self.pac_man.get_y())
            self.inky.deplacer(self.pac_man.get_x(), self.pac_man.get_y())

            # deplacement de pac-man
            self.pac_man.deplacer()
            
            self.score += self.L.detection_gomme(self.pac_man.get_x(), self.pac_man.get_y())
            self.L.detection_powergum(self.pac_man.get_x(), self.pac_man.get_y())

        # Bouton de démarrage du jeu
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.game_started = True

        self.pac_man_bouche_compteur += 1

        if self.pac_man_ecrant_titre_x >= 30:
            self.pac_man_ecrant_titre_x = 0

        # Vérifier si le compteur a atteint l'intervalle défini
        if self.pac_man_bouche_compteur >= 20:
            self.pac_man_bouche_compteur = 0  # Réinitialiser le compteur
            self.pac_man_ecrant_titre_x += 1  # Dé

    def draw(self):

        pyxel.cls(0)

        if self.game_started:
            # affichage du labyrinthe
            self.L.affiche()
            
            # affihage des fantomes
            self.clyde.affiche()
            self.blinky.affiche()
            self.inky.affiche()
            self.pinky.affiche()

            # affichage de pacman
            self.pac_man.afficher()

            # affichage du score
            pyxel.text(8, 250, "SCORE: " + str(self.score), 7)
        else:
            # Bouton de démarrage du jeu
            pyxel.rect(80, 120, 64, 16, 7)
            pyxel.text(103, 125, "START", 0)

            pyxel.blt(60, 48, 0, 0, 32, 116, 28, 0)

            if self.pac_man_ecrant_titre_x > 28:
                self.pac_man_ecrant_titre_x = -8

            if self.pac_man_bouche_compteur < 20 // 2:
                pyxel.blt(8*self.pac_man_ecrant_titre_x+40, 8,
                          0, 0, 0, 8, 8, 0)  # Bouche fermée
            else:
                pyxel.blt(8*self.pac_man_ecrant_titre_x+40,
                          8, 0, 8, 0, 8, 8, 0)

            # fantomes 3

            pyxel.blt(8*self.pac_man_ecrant_titre_x, 8, 0, 0, 8, 32, 8, 0)


laby = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1,
        2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 1, 0, 0, 1, 2, 1, 0, 0, 0, 1, 2, 1, 1,
        2, 1, 0, 0, 0, 1, 2, 1, 0, 0, 1, 3, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1,
        2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1,
        1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1,
        1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1,
        2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1,
        0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1,
        0, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 0, 0, 0,
        0, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0,
        0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0,
        0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1,
        1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1,
        1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1,
        1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1,
        2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1,
        2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0,
        2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1,
        1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1,
        1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1,
        2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1,
        2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1,
        2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


Jeu(laby)
