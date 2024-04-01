import pyxel # Importation de la bibliothèque Pyxel

from ghost import * # Importation des classes des fantomes
from pac_man import * # Importation de la classe de Pacman
from labyrinthe import * # Importation de la classe du labyrinthe
from graph import * # Importation de la classe du graphe

class Jeu:
    """ Classe principale du jeu """

    def __init__(self, laby):
        """ Constructeur de la classe Jeu """

        pyxel.init(224, 272, title="Pac-man", fps=60) # Initialisation de la fenêtre Pyxel
        pyxel.load("res.pyxres") # Chargement des ressources du jeu depuis le fichier res.pyxres

        pyxel.colors[0] = 0x000000 # Couleur noire
        pyxel.colors[1] = 0x0000FF # Couleur bleu violet
        pyxel.colors[2] = 0xFF0000 # Couleur rouge
        pyxel.colors[3] = 0x00FF00 # Couleur verte
        pyxel.colors[4] = 0xFFFF00 # Couleur jaune
        pyxel.colors[5] = 0x5B59BC # Couleur violet
        pyxel.colors[6] = 0x00FFFF # Couleur cyan
        pyxel.colors[7] = 0xFFFFFF # Couleur blanche
        pyxel.colors[8] = 0xFC5506 # Couleur jaune foncé
        pyxel.colors[9] = 0xFFA308 # Couleur orange clair
        pyxel.colors[10] = 0xFFFB4F # Couleur jaune clair
        pyxel.colors[11] = 0x7FFFFF # Couleur bleu clair
        pyxel.colors[12] = 0x0BA8F9 # Couleur bleu foncé
        pyxel.colors[13] = 0xFF7FFF # Couleur rose clair
        pyxel.colors[15] = 0xf5fcc6 # Couleur beige
        pyxel.colors[14] = 0xF8A6FB # Couleur rose

        # Création du labyrinthe initial pour le reset du labyrinthe
        self.laby_initial : list = laby[:]

        # Création du labyrinthe et du graphe 
        self.L : Lab = Lab(list(self.laby_initial))
        self.G : Graph = Graph(list(self.laby_initial))

        # Creation de Pac Man
        self.pac_man : Pac_man = Pac_man(self.L)

        # Création des fantomes
        self.clyde : Clyde = Clyde(self.L, self.G, speed=14)
        self.blinky : Blinky= Blinky(self.L, self.G, speed=13)
        self.pinky : Pinky = Pinky(self.L, self.G, speed=15)
        self.inky : Inky = Inky(self.L, self.G, speed=14)

        # Variables de jeu
        self.game_started : bool = False # Booléen pour savoir si le jeu a commencé
        self.depart_fantomes : int = 0 # Compteur pour le départ différé des fantomes
        self.pac_man_bouche_compteur : int = 0 # Utilisé pour l'animation de la bouche de Pacman sur l'écran titre
        self.pac_man_ecrant_titre_x : int = -10 # Utilisé pour l'animation de Pacman sur l'écran titre
        self.dev_mode : bool = False # Booléen pour activer le mode développeur
        self.path_finding : int = 0 # Variable pour afficher le chemin des fantomes dans le mode développeur
        self.score : int = 0 # Variable pour le score du joueur
        self.vie : int = 3 # Variable pour le nombre de vies du joueur
        # Importe le highsore depuis le fichier ou le crée (highscore.txt)
        try:
            with open("highscore.txt", "r") as f: # Ouverture du fichier highscore.txt
                self.highscore = int(f.read()) # Lecture du highscore
        except FileNotFoundError:
            with open("highscore.txt", "w") as f: # Création du fichier highscore.txt si il n'existe pas
                f.write("0")
            self.highscore = 0 # Si le fichier n'existe pas, le highscore est 0

        # Lancement de la musique
        pyxel.playm(0, loop=True)

        # Lancement du jeu
        pyxel.run(self.update, self.draw)

    def update(self):
        """ Fonction de mise à jour du jeu """

        # Si bouton H appuyé, activer/désactiver le mode développeur
        if pyxel.btnp(pyxel.KEY_H):
            self.dev_mode = not self.dev_mode # Inversion du statut du mode développeur

            # Vitesse des fantomes remise à la normale si le mode développeur est activé puis désactivé.
            self.clyde.speed = 14
            self.blinky.speed = 13
            self.pinky.speed = 15
            self.inky.speed = 14

        # Si le mode développeur est activé
        if self.dev_mode: 
            # Si bouton J appuyé, arrêter les fantomes
            if pyxel.btnp(pyxel.KEY_J):
                self.clyde.speed = inf # Vitesse infinie pour arrêter le fantome
                self.blinky.speed = inf # Vitesse infinie pour arrêter le fantome
                self.pinky.speed = inf # Vitesse infinie pour arrêter le fantome
                self.inky.speed = inf # Vitesse infinie pour arrêter le fantome

            # Si bouton K appuyé, ajouter une vie
            if pyxel.btnp(pyxel.KEY_K):
                # Ajoute une vie
                self.vie += 1

            # Si bouton L appuyé, changer le chemin pour afficher le chemin d'un autre fantome
            if pyxel.btnp(pyxel.KEY_L):
                # Incrémente la variable path_finding pour afficher le chemin d'un autre fantome
                self.path_finding += 1

            # Si la variable path_finding est supérieure à 5, la remettre à 1 pour afficher le chemin de chaque fantome
            if self.path_finding > 5:
                # Remise à 1 pour afficher le chemin du premier fantome
                self.path_finding = 1


        # Si le jeu a commencé

        if self.game_started:

            # Si toutes les gommes sont mangées, on recrée le labyrinthe
            if self.L.total_pagomme <= 0:
                # Recréation du labyrinthe avec les gommes et reinitialise la position des fantomes et de Pacman
                self.L : Lab = Lab(list(self.laby_initial)) # Recréation du labyrinthe
                self.clyde : Clyde = Clyde(self.L, self.G, speed=14) # Recréation de Clyde
                self.blinky : Blinky = Blinky(self.L, self.G, speed=13) # Recréation de Blinky
                self.pinky : Pinky = Pinky(self.L, self.G, speed=15) # Recréation de Pinky
                self.inky : Inky = Inky(self.L, self.G, speed=14) # Recréation de Inky
                self.pac_man = Pac_man(self.L) # Recréation de Pacman
                self.depart_fantomes = 0 # Réinitialisation du compteur de départ des fantomes

            # Si le joueur n'a plus de vie
            if self.vie < 0:

                # Si le score est supérieur au highscore, on met à jour le highscore dans le fichier highscore.txt
                if self.score > self.highscore:
                    with open("highscore.txt", "w") as f:
                        f.write(str(self.score))

                # Recréation du labyrinthe avec les gommes et reinitialise la position des fantomes et de Pacman
                self.L : Lab = Lab(list(self.laby_initial)) # Recréation du labyrinthe
                self.score = 0 # Réinitialisation du score
                self.vie = 3 # Réinitialisation du nombre de vies
                self.game_started = False # Arrêt du jeu pour revenir à l'écran titre

                self.clyde : Clyde = Clyde(self.L, self.G, speed=14) # Recréation de Clyde
                self.blinky : Blinky = Blinky(self.L, self.G, speed=13) # Recréation de Blinky
                self.pinky : Pinky = Pinky(self.L, self.G, speed=15) # Recréation de Pinky
                self.inky : Inky = Inky(self.L, self.G, speed=14) # Recréation de Inky
                self.pac_man = Pac_man(self.L) # Recréation de Pacman
                self.depart_fantomes = 0 # Réinitialisation du compteur de départ des fantomes

            # Si le compteur de frame est un multiple de 300 et que le nombre de fantomes partis est inférieur à 5
            if pyxel.frame_count % 300 == 0 and self.depart_fantomes < 5:
                self.depart_fantomes += 1

            # Si le nombre de fantomes partis est supérieur à 0, on arrête l'animation d'attente de Clyde pour le laisser partir de la cage des fantomes
            if self.depart_fantomes >= 0:
                self.clyde.arreter_animation_attente()
            # Si le nombre de fantomes partis est supérieur à 1, on arrête l'animation d'attente de Pinky pour le laisser partir de la cage des fantomes
            if self.depart_fantomes >= 1:
                self.pinky.arreter_animation_attente()
            # Si le nombre de fantomes partis est supérieur à 2, on arrête l'animation d'attente de Blinky pour le laisser partir de la cage des fantomes
            if self.depart_fantomes >= 2:
                self.blinky.arreter_animation_attente()
            # Si le nombre de fantomes partis est supérieur à 3, on arrête l'animation d'attente de Inky pour le laisser partir de la cage des fantomes
            if self.depart_fantomes >= 3:
                self.inky.arreter_animation_attente()

            # Liste pour vérifier si un fantome a mangé Pacman
            liste_mort = []

            # Déplacement des fantomes et vérification si un fantome a mangé Pacman
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

            # Si un fantome a mangé Pacman, on enlève une vie et on réinitialise les fantomes et Pacman
            if True in liste_mort:
                self.vie -= 1 # Enlève une vie

                # Retéléportation des fantomes
                self.clyde : Clyde = Clyde(self.L, self.G, speed=14) # Recréation de Clyde
                self.blinky : Blinky = Blinky(self.L, self.G, speed=13) # Recréation de Blinky
                self.pinky : Pinky = Pinky(self.L, self.G, speed=15) # Recréation de Pinky
                self.inky : Inky = Inky(self.L, self.G, speed=14) # Recréation de Inky
                self.pac_man = Pac_man(self.L) # Recréation de Pacman
                self.depart_fantomes = 0 # Réinitialisation du compteur de départ des fantomes

            # Gestions des déplacements de Pacman
            self.pac_man.deplacer()

            # Gestion des collisions avec les murs
            self.score += self.L.detection_gomme(
                self.pac_man.get_x(), self.pac_man.get_y())
            
            # Gestion des collisions avec les powergums
            tmp_pg = self.L.detection_powergum(
                self.pac_man.get_x(), self.pac_man.get_y())
            
            self.score += tmp_pg # Ajout du score des powergums, permet d'aoir un effet cumulatif des fantomes mangés

            # Si une powergum est mangée, les fantomes peuvent être mangés
            if tmp_pg > 0:
                # Les fantomes peuvent être mangés
                self.clyde.can_be_eaten()
                self.blinky.can_be_eaten()
                self.pinky.can_be_eaten()
                self.inky.can_be_eaten()

        else:
            # Bouton de démarrage du jeu
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.game_started = True

            # Animation de la bouche de Pacman sur l'écran
            self.pac_man_bouche_compteur += 1

            # Animation de Pacman sur l'écran titre
            if self.pac_man_ecrant_titre_x >= 30:
                self.pac_man_ecrant_titre_x = 0

            # Vérifier si le compteur a atteint l'intervalle défini pour l'animation de la bouche de Pacman sur l'écran titre
            if self.pac_man_bouche_compteur >= 20:
                self.pac_man_bouche_compteur = 0  # Réinitialiser le compteur
                self.pac_man_ecrant_titre_x += 1  # Déplacer le sprite de la bouche

    def draw(self):
        """ Fonction de dessin du jeu """

        pyxel.cls(0) # Nettoie l'écran avec la couleur noire 

        # Si le jeu a commencé
        if self.game_started:

            # Si le mode développeur est activé
            if self.dev_mode:
                if self.path_finding == 1:
                    self.pinky.affiche_chemin(self.pac_man.get_x(), self.pac_man.get_y()) # Affiche le chemin de Pinky pour atteindre Pacman, le chemin de fuite ou le retour à la cage
                elif self.path_finding == 2:
                    self.blinky.affiche_chemin(self.pac_man.get_x(), self.pac_man.get_y()) # Affiche le chemin de Blinky pour atteindre Pacman, le chemin de fuite ou le retour à la cage
                elif self.path_finding == 3:
                    self.inky.affiche_chemin(self.pac_man.get_x(), self.pac_man.get_y()) # Affiche le chemin de Inky pour atteindre Pacman, le chemin de fuite ou le retour à la cage
                elif self.path_finding == 4:
                    self.clyde.affiche_chemin(self.pac_man.get_x(), self.pac_man.get_y()) # Affiche le chemin de Clyde pour atteindre Pacman, le chemin de fuite ou le retour à la cage
                elif self.path_finding == 5:
                    pass # n'affiche rien


            # Affichage du labyrinthe
            self.L.affiche()

            # Affichage des fantomes
            self.clyde.affiche()
            self.blinky.affiche()
            self.inky.affiche()
            self.pinky.affiche()

            # Affichage de Pacman
            self.pac_man.afficher()

            # Affichage du score, du highscore et du nombre de vies
            pyxel.text(4, 252, "SCORE: " + str(self.score), 7) # Affichage du score
            pyxel.text(4, 262, "HI-SCORE: " + str(self.highscore), 7) # Affichage du highscore
            pyxel.text(130, 252, "1UP", 7) # Affichage du texte "1UP"

            # Pour chaque vie restante, on affiche un sprite de Pacman représentant une vie
            for i in range(self.vie):
                pyxel.blt(98+i*10, 260, 0, 8, 0, 8, 8, 0)

        else:

            # Logo du jeu

            pyxel.blt(60, 48, 0, 0, 24, 116, 17, 0)
            pyxel.rect(61, 40, 105, 2, 7)
            pyxel.rect(61, 70, 105, 2, 7)
            pyxel.text(61, 80, "VERSION PYXEL", 7)

            # Crédits
            pyxel.text(8, 238, "COHET SIMONT", 7)
            pyxel.text(8, 248, "BAUDELET KAELIAN", 7)
            pyxel.text(8, 258, "2023-2024", 7)

            # Bouton de démarrage du jeu
            pyxel.text(99, 165, "> JOUER", 10)
            pyxel.text(72, 180, "Appuyez sur [ESPACE]", 7)

            #Informations générales du jeu sur l'écran titre

            pyxel.blt(64, 116, 0, 8, 16, 8, 8, 0)  # Gomme normale
            pyxel.text(76, 118, "10", 7) # Score pour la gomme normale
            pyxel.blt(64, 128, 0, 0, 16, 8, 8, 0)  # Powergum (super gomme)
            pyxel.text(76, 130, "100", 7) # Score pour la powergum

            pyxel.blt(110, 98, 0, 0, 8, 8, 8) # Inky
            pyxel.text(123, 100, "Inky", 7) # Nom de Inky
            pyxel.blt(110, 108, 0, 8 * 1, 8, 8, 8) # Blinky
            pyxel.text(123, 110, "Blinky", 7) # Nom de Blinky
            pyxel.blt(110, 118, 0, 8 * 2, 8, 8, 8) # Pinky
            pyxel.text(123, 120, "Pinky", 7) # Nom de Pinky
            pyxel.blt(110, 128, 0, 8 * 3, 8, 8, 8) # Clyde
            pyxel.text(123, 130, "Clyde", 7) # Nom de Clyde

            pyxel.blt(40, 195, 0, 0, 50, 116, 80, 0) # Personnage de Pacman

            # Informations sur les touches du jeu
            pyxel.text(165, 257, "H - MODE DEV", 7)


            # Animation de Pacman sur l'écran titre
            if self.pac_man_ecrant_titre_x > 28:
                self.pac_man_ecrant_titre_x = -8

            # Animation de la bouche de Pacman sur l'écran titre
            if self.pac_man_bouche_compteur < 20 // 2:
                pyxel.blt(8 * self.pac_man_ecrant_titre_x + 40, 8,
                          0, 0, 0, 8, 8, 0)  # Bouche fermée
            else:
                pyxel.blt(8 * self.pac_man_ecrant_titre_x + 40,
                          8, 0, 8, 0, 8, 8, 0)

            # Affichage de Pacman sur l'écran titre
            pyxel.blt(8 * self.pac_man_ecrant_titre_x, 8, 0, 0, 8, 32, 8, 0)

        # Si le mode développeur est activé
        if self.dev_mode:

            # Affichage des informations de la touche pour quitter le mode développeur
            pyxel.text(4, 4, "DEV MODE (H pour quitter)", 11)

            # Affichage des informations de débogage du jeu
            pyxel.text(4, 12, "Ordre des fantomes: {}".format(self.depart_fantomes), 2)
            pyxel.text(4, 20, "Position de Pacman : ({}, {}) ".format(self.pac_man.get_x(), self.pac_man.get_y()), 2)
            pyxel.text(4, 28, "Position de Blinky : ({}, {}) ".format(self.blinky.ghost.get_x(), self.blinky.ghost.get_y()), 2)
            pyxel.text(4, 36, "Position de Pinky : ({}, {}) ".format(self.pinky.ghost.get_x(), self.pinky.ghost.get_y()), 2)
            pyxel.text(4, 44, "Position de Inky : ({}, {}) ".format(self.inky.ghost.get_x(), self.inky.ghost.get_y()), 2)
            pyxel.text(4, 52, "Position de Clyde : ({}, {}) ".format(self.clyde.ghost.get_x(), self.clyde.ghost.get_y()), 2)
            pyxel.text(4, 60, "Vitesse de Blinky : {} ".format(self.blinky.speed), 2)
            pyxel.text(4, 68, "Vitesse de Pinky : {} ".format(self.pinky.speed), 2)
            pyxel.text(4, 76, "Vitesse de Inky : {} ".format(self.inky.speed), 2)
            pyxel.text(4, 84, "Vitesse de Clyde : {} ".format(self.clyde.speed), 2)
            pyxel.text(4, 92, "Nombre de gommes : {} ".format(self.L.total_pagomme), 2)
            pyxel.text(178, 4, "FPS : {}/60".format(pyxel.frame_count%60), 2)

            # Affichage des touches pour les fonctionnalités du mode développeur (mode de triche pour les tests)
            pyxel.text(122, 52, "Touches : ", 3)
            pyxel.text(122, 60, "J : Arreter les fantomes", 3)
            pyxel.text(122, 68, "K : Ajouter une vie", 3)
            pyxel.text(122, 76, "L : Changer le chemin", 3)


# Labyrinthe du jeu
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

# Lancement du jeu
Jeu(list(laby))
