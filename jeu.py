import pyxel

from ghost import *
from pac_man import *
from labyrinthe import *
from graph import *


class Jeu:

    def __init__(self, laby):

        pyxel.init(224, 272, title="Pac-man", fps=60)
        pyxel.load("res.pyxres")
        
        # création du labyrinthe
        self.laby_initial = laby[:]

        # Création du labyrinthe
        self.L = Lab(list(self.laby_initial))
        self.G = Graph(list(self.laby_initial))

        # creation de Pac Man
        self.pac_man = Pac_man(self.L)

        # création des fantomes
        self.clyde = Clyde(self.L, self.G, speed=14)
        self.blinky = Blinky(self.L, self.G, speed=13)
        self.pinky = Pinky(self.L, self.G, speed=15)
        self.inky = Inky(self.L, self.G, speed=14)

        self.powertime = False
        self.game_started = False
        self.depart_fantomes = 0

        self.pac_man_bouche_compteur = 0
        self.pac_man_ecrant_titre_x = -10

        # score
        self.score = 0
        self.vie = 3

        # TODO : faire les musiques

        # Lancement du jeu
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_started:

            if pyxel.btn(pyxel.KEY_K):
                self.L.total_pagomme = 0


            # PASSAGE NIVEAU SUIVANT
            if self.L.total_pagomme <= 0:
                # recréation du labyrinthe avec les gommes
                self.L = Lab(list(self.laby_initial))

                # Retéléportation des fantomes
                print('Niveau suivant')

                self.clyde = Clyde(self.L, self.G, speed=14)
                self.blinky = Blinky(self.L, self.G, speed=13)
                self.pinky = Pinky(self.L, self.G, speed=15)
                self.inky = Inky(self.L, self.G, speed=14)

                self.pac_man = Pac_man(self.L)

                self.depart_fantomes = 0

            # deplacement des fantomes

            # incrementation du compteur de depart des fantomes toute les 60 frames, toutes les 60 frames un fantome part

            if pyxel.frame_count % 300 == 0 and self.depart_fantomes < 5:
                self.depart_fantomes += 1

            if self.depart_fantomes >= 1:
                self.clyde.arreter_animation_attente()
                
            if self.depart_fantomes >= 2:
                self.pinky.arreter_animation_attente()
                
            if self.depart_fantomes >= 3:
                self.blinky.arreter_animation_attente()
                
            if self.depart_fantomes >= 4:
                self.inky.arreter_animation_attente()

            liste_mort = []
            liste_mort.append(self.inky.deplacer(self.pac_man.get_x(), self.pac_man.get_y()))
            liste_mort.append(self.blinky.deplacer(self.pac_man.get_x(), self.pac_man.get_y()))
            liste_mort.append(self.pinky.deplacer(self.pac_man.get_x(), self.pac_man.get_y()))
            liste_mort.append(self.clyde.deplacer(self.pac_man.get_x(), self.pac_man.get_y()))

            if True in liste_mort:
                self.vie -= 1
                print('mort pacman')

                # Retéléportation des fantomes
                self.clyde = Clyde(self.L, self.G, speed=14)
                self.blinky = Blinky(self.L, self.G, speed=13)
                self.pinky = Pinky(self.L, self.G, speed=15)
                self.inky = Inky(self.L, self.G, speed=14)

                self.pac_man = Pac_man(self.L)

                self.depart_fantomes = 0
                
            
            # deplacement de pac-man
            self.pac_man.deplacer()
            
            self.score += self.L.detection_gomme(self.pac_man.get_x(), self.pac_man.get_y())
            tmp_pg = self.L.detection_powergum(self.pac_man.get_x(), self.pac_man.get_y())
            self.score += tmp_pg
            if tmp_pg > 0:
                self.clyde.can_be_eaten()
                self.blinky.can_be_eaten()
                self.pinky.can_be_eaten()
                self.inky.can_be_eaten()

        else:
            # Bouton de démarrage du jeu
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.game_started = True

            self.pac_man_bouche_compteur += 1

            if self.pac_man_ecrant_titre_x >= 30:
                self.pac_man_ecrant_titre_x = 0

            # Vérifier si le compteur a atteint l'intervalle défini
            if self.pac_man_bouche_compteur >= 20:
                self.pac_man_bouche_compteur = 0  # Réinitialiser le compteur
                self.pac_man_ecrant_titre_x += 1  # Déplacer le sprite de la bouche

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

            # affichage du score et des vies
            pyxel.text(4, 252, "SCORE: " + str(self.score), 7)
            pyxel.text(4, 262, "HI-SCORE: " + str(self.score), 7)
            pyxel.text(130, 252, "1UP", 7)
            pyxel.text(180, 252, "CREDITS: 3", 7)
            pyxel.blt(98, 251, 0, 8, 0, 8, 8, 0)
            pyxel.blt(108, 251, 0, 8, 0, 8, 8, 0)
            pyxel.blt(118, 251, 0, 8, 0, 8, 8, 0)
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
    [1, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1,
        1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0,
        0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 0,
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


Jeu(list(laby))
