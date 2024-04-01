from math import inf # Importation de l'infini
import pyxel # Importation de la bibliothèque Pyxel
from collections import deque # Importation de la classe deque


class Lab:
    """Classe Labyrinthe"""

    def __init__(self, l: list):
        """Constructeur de la classe Labyrinthe"""
        self.grille = [] # Grille du labyrinthe
        # On copie la grille pour pouvoir la modifier sans modifier l'originale lorsqu'il faudra la réinitialiser
        for ligne in l:
            self.grille.append(ligne[:]) # On copie la grille
        self.total_pagomme = self.comptage_gomme(l) # Nombre total de gommes
        self.adjacence = {} # Dictionnaire des sommets et des arêtes du graphe vide

        # On parcourt la grille pour créer les sommets et les arêtes du graphe
        for i in range(len(l)):
            for j in range(len(l[0])):
                # On crée un sommet pour chaque case non mur
                if l[i][j] != 1:
                    self.adjacence[l[i][j]] = []

    def comptage_gomme(self, l: list) -> int:
        """Compte le nombre de gommes dans la grille"""
        compteur = 0 # Compteur de gommes
        # On parcourt la grille pour compter le nombre de gommes
        for i in range(len(l)):
            for j in range(len(l[0])):
                # On compte le nombre de gommes dans la grille
                if l[i][j] == 2:
                    compteur += 1 # On incrémente le compteur de gommes
        return compteur # Renvoie le nombre de gommes

    def get_grille(self):
        """Renvoie la grille"""
        return self.grille # Renvoie la grille

    def affiche(self):
        """Affiche le labyrinthe"""
        for i in range(len(self.grille)):
            for j in range(len(self.grille[0])):
                # On affiche les éléments du labyrinthe en fonction de leur valeur dans la grille
                if self.grille[i][j] == 1:
                    pyxel.rect(j * 8 + 1, i * 8 + 1, 6, 6, 5)  # Mur
                elif self.grille[i][j] == 2:
                    pyxel.blt(j * 8, i * 8, 0, 8, 16, 8, 8, 0)  # Gomme normale
                elif self.grille[i][j] == 3:
                    pyxel.blt(j * 8, i * 8, 0, 0, 16, 8, 8, 0)  # Powergum (super gomme)
                elif self.grille[i][j] == 4:
                    pyxel.rect(j * 8 + 3, i * 8 + 1, 2, 6, 7)  # Porte de sortie de la cage des fantômes

    def collision(self, x, y):
        """Vérifie s'il y a collision"""
        # Si la case est un mur, il y a collision (retourne True)
        if self.grille[y][x] == 1 or self.grille[y][x] == 4:
            return True # Il y a collision (retourne True)

    def detection_gomme(self, x, y):
        """Détecte une gomme"""

        # Si une gomme est détectée, on la mange
        if self.grille[y][x] == 2: # Si la case est une gomme
            self.total_pagomme -= 1 # On décrémente le nombre de gommes
            self.grille[y][x] = 0 # On mange la gomme
            return 10 # On gagne 10 points
        return 0 # Sinon on ne gagne pas de points

    def detection_powergum(self, x, y):
        """Détecte une powergum"""
        # Si une powergum est détectée, on la mange
        if self.grille[y][x] == 3: # Si la case est une powergum
            self.grille[y][x] = 0 # On mange la powergum
            return 100 # On gagne 100 points
        return 0 # Sinon on ne gagne pas de points
