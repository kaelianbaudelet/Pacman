from math import inf
import pyxel
from collections import deque

class Lab:
    
    def __init__(self, l: list):
        self.grille = l
        
        self.adjacence = {}
        
        for i in range(len(l)):
            for j in range(len(l[0])):
                if l[i][j] != 1:
                    self.adjacence[l[i][j]] = []
                    
    def get_grille(self):
        return self.grille
        
    def affiche(self):
        for i in range(len(self.grille)):
            for j in range(len(self.grille[0])):
                if self.grille[i][j] == 1:
                    pyxel.rect(j*8+1, i*8+1, 6, 6, 5) # mur
                elif self.grille[i][j] == 2:
                    pyxel.blt(j*8, i*8, 0, 8, 16, 8, 8, 0) # gomme normale
                elif self.grille[i][j] == 3:
                    pyxel.blt(j*8, i*8, 0, 0, 16, 8, 8, 0) # powergum
                
    def collision(self, x, y):
        # Si la case est un mur, il y a collision (retourne True)
        if self.grille[y][x] == 1:
            return True

    def detection_gomme(self, x, y):
        # Si une gomme est détectée, on la mange
        if self.grille[y][x] == 2:
            self.grille[y][x] = 0
            return 10
        return 0

    def detection_powergum(self, x, y):
        # Si une powergum est détectée, on la mange
        if self.grille[y][x] == 3:
            self.grille[y][x] = 0
            return 100
        return 0
