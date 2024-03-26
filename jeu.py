import pyxel

from ghost import *
from pac_man import *
from labyrinthe import *
from graph import *

class Jeu:
    
    def __init__(self, laby):
        
        pyxel.init(224, 264, title="Pac-man", fps = 60)
        pyxel.load("res.pyxres")
        
        # création du labyrinthe
        self.L = Lab(laby)
        # et du graphe
        self.G = Graph(laby)
        
        # creation de Pac Man
        self.pac_man = Pac_man(self.L)
        
        # création des fantomes
        self.clyde = Clyde(self.L, speed=10)
        self.blinky = Blinky(self.L, speed=10)
        self.pinky = Pinky(self.L, self.G, speed=10)
        self.inky = Inky(self.L, self.G, speed=10)

        self.powertime = False
        self.game_started = False
        self.score = 0
        
        # Lancement du jeu
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if self.game_started:
            # deplacement de pac-man
            self.pac_man.deplacer()
            
            self.score += self.L.detection_gomme(self.pac_man.get_x(), self.pac_man.get_y())
            self.L.detection_powergum(self.pac_man.get_x(), self.pac_man.get_y())
            
            # deplacement des fantomes
            self.clyde.deplacer()
            self.blinky.deplacer(self.pac_man.get_x(), self.pac_man.get_y())
            self.pinky.deplacer(self.pac_man.get_x(), self.pac_man.get_y())
            self.inky.deplacer(self.pac_man.get_x(), self.pac_man.get_y())

        # Bouton de démarrage du jeu
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.game_started = True
                
    def draw(self):
        pyxel.cls(0)
        if self.game_started:
            # affichage du labyrinthe
            self.L.affiche()

            # affichage de pacman
            self.pac_man.afficher()
            
            # affihage des fantomes
            self.clyde.affiche()
            self.blinky.affiche()
            self.inky.affiche()
            self.pinky.affiche()

            # affichage du score
            pyxel.text(8, 250, "SCORE: " + str(self.score), 7)
        else:
            # Bouton de démarrage du jeu
            pyxel.rect(80, 120, 64, 16, 7)
            pyxel.text(90, 125, "START", 0)
              
laby = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
[1,3,1,0,0,1,2,1,0,0,0,1,2,1,1,2,1,0,0,0,1,2,1,0,0,1,3,1],
[1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
[1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
[1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
[1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
[1,0,0,0,0,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,0,0,0,0,1],
[1,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,1],
[1,0,0,0,0,1,2,1,1,0,1,1,0,0,0,0,1,1,0,1,1,2,1,0,0,0,0,1],
[1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
[0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
[1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
[1,0,0,0,0,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,0,0,0,0,1],
[1,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,1],
[1,0,0,0,0,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,0,0,0,0,1],
[1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
[1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
[1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
[1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
[1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
[1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
[1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
[1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    
Jeu(laby)