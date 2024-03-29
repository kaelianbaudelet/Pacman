import pyxel

from ghost import *
from pac_man import *
from labyrinthe import *
from graph import *


class Jeu:

    def __init__(self, laby):

        pyxel.init(224, 272, title="Pac-man", fps=60)
        pyxel.load("res.pyxres")

        pyxel.colors[0] = 0x000000
        pyxel.colors[1] = 0x0000FF
        pyxel.colors[2] = 0xFF0000
        pyxel.colors[3] = 0x00FF00
        pyxel.colors[4] = 0xFFFF00
        pyxel.colors[5] = 0x5B59BC
        pyxel.colors[6] = 0x00FFFF
        pyxel.colors[7] = 0xFFFFFF
        pyxel.colors[8] = 0xFC5506
        pyxel.colors[9] = 0xFFA308
        pyxel.colors[10] = 0xFFFB4F
        pyxel.colors[11] = 0x7FFFFF
        pyxel.colors[12] = 0x0BA8F9
        pyxel.colors[13] = 0xFF7FFF
        pyxel.colors[15] = 0xf5fcc6
        pyxel.colors[14] = 0xF8A6FB

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
        self.dev_mode = False

        # score
        self.score = 0
        self.vie = 3

        # Importe le highsore depuis le fichier ou le crée (highscore.txt)
        try:
            with open("highscore.txt", "r") as f:
                self.highscore = int(f.read())
        except FileNotFoundError:
            with open("highscore.txt", "w") as f:
                f.write("0")
            self.highscore = 0

        

        # lancement de la musique
        pyxel.playm(0, loop=True)

        # Lancement du jeu

        pyxel.run(self.update, self.draw)

    def update(self):

        if pyxel.btnp(pyxel.KEY_F9):
            self.dev_mode = not self.dev_mode
            # reinitialisation de la vitesse des fantomes
            self.clyde.speed = 14
            self.blinky.speed = 13
            self.pinky.speed = 15
            self.inky.speed = 14

        if self.dev_mode:
            # Freeze les fantomes
            if pyxel.btnp(pyxel.KEY_F1):
                # arreter les fantomes
                self.clyde.speed = inf
                self.blinky.speed = inf
                self.pinky.speed = inf
                self.inky.speed = inf

            if pyxel.btnp(pyxel.KEY_F2):
                # donner des vies
                self.vie += 1

                

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

            # mort définitive
            if self.vie < 0:

                # sauvagarde du highscore si il est battu
                if self.score > self.highscore:
                    with open("highscore.txt", "w") as f:
                        f.write(str(self.score))

                # recréation du labyrinthe avec les gommes
                self.L = Lab(list(self.laby_initial))
                self.score = 0
                self.vie = 3
                self.game_started = False

                # Retéléportation des fantomes
                print('fin du jeu')

                self.clyde = Clyde(self.L, self.G, speed=14)
                self.blinky = Blinky(self.L, self.G, speed=13)
                self.pinky = Pinky(self.L, self.G, speed=15)
                self.inky = Inky(self.L, self.G, speed=14)

                self.pac_man = Pac_man(self.L)

                self.depart_fantomes = 0

            # incrementation du compteur de depart des fantomes toute les 60
            # frames, toutes les 60 frames un fantome part

            if pyxel.frame_count % 300 == 0 and self.depart_fantomes < 5:
                self.depart_fantomes += 1

            if self.depart_fantomes >= 0:
                self.clyde.arreter_animation_attente()
                
            if self.depart_fantomes >= 1:
                self.pinky.arreter_animation_attente()
                
            if self.depart_fantomes >= 2:
                self.blinky.arreter_animation_attente()
                
            if self.depart_fantomes >= 3:
                self.inky.arreter_animation_attente()

            liste_mort = []
            liste_mort.append(
                self.inky.deplacer(
                    self.pac_man.get_x(),
                    self.pac_man.get_y()))
            liste_mort.append(
                self.blinky.deplacer(
                    self.pac_man.get_x(),
                    self.pac_man.get_y()))
            liste_mort.append(
                self.pinky.deplacer(
                    self.pac_man.get_x(),
                    self.pac_man.get_y()))
            liste_mort.append(
                self.clyde.deplacer(
                    self.pac_man.get_x(),
                    self.pac_man.get_y()))

            if True in liste_mort:
                self.vie -= 1

                # Retéléportation des fantomes
                self.clyde = Clyde(self.L, self.G, speed=14)
                self.blinky = Blinky(self.L, self.G, speed=13)
                self.pinky = Pinky(self.L, self.G, speed=15)
                self.inky = Inky(self.L, self.G, speed=14)

                self.pac_man = Pac_man(self.L)

                self.depart_fantomes = 0

            # deplacement de pac-man
            self.pac_man.deplacer()

            self.score += self.L.detection_gomme(
                self.pac_man.get_x(), self.pac_man.get_y())
            tmp_pg = self.L.detection_powergum(
                self.pac_man.get_x(), self.pac_man.get_y())
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
            pyxel.text(4, 262, "HI-SCORE: " + str(self.highscore), 7)
            pyxel.text(130, 252, "1UP", 7)
            pyxel.text(180, 252, "CREDITS: 3", 7)

            for i in range(self.vie):
                pyxel.blt(98+i*10, 260, 0, 8, 0, 8, 8, 0)

        else:
            # Bouton de démarrage du jeu
            pyxel.rect(80, 120, 64, 16, 7)
            pyxel.text(103, 125, "START", 0)

            pyxel.blt(60, 48, 0, 0, 32, 116, 28, 0)

            if self.pac_man_ecrant_titre_x > 28:
                self.pac_man_ecrant_titre_x = -8

            if self.pac_man_bouche_compteur < 20 // 2:
                pyxel.blt(8 * self.pac_man_ecrant_titre_x + 40, 8,
                          0, 0, 0, 8, 8, 0)  # Bouche fermée
            else:
                pyxel.blt(8 * self.pac_man_ecrant_titre_x + 40,
                          8, 0, 8, 0, 8, 8, 0)

            # fantomes 3

            pyxel.blt(8 * self.pac_man_ecrant_titre_x, 8, 0, 0, 8, 32, 8, 0)

        if self.dev_mode:
            pyxel.text(4, 4, "DEV MODE", 2)
            # Informations debug



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
