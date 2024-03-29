from collections import deque

class Graph:
    def __init__(self, grid):
        # On crée un graphe à partir de la grille
        self.graph = {}

        # On parcourt la grille pour créer les sommets et les arêtes
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                # On ne crée pas de sommet pour les murs
                if grid[i][j] != 1:
                    self.graph[(i,j)] = []

                    # On ajoute les arêtes pour chaque case adjacente non mur
                    if i-1 > -1 and grid[i-1][j] != 1:
                        self.graph[(i,j)].append((i-1, j))
                    if i+1 < len(grid) and grid[i+1][j] != 1:
                        self.graph[(i,j)].append((i+1, j))
                    if j-1 > -1 and grid[i][j-1] != 1:
                        self.graph[(i,j)].append((i, j-1))
                    if j+1 < len(grid[0]) and grid[i][j+1] != 1:
                        self.graph[(i,j)].append((i, j+1))

    # Algo parcours Largeur
    def parcours_largeur(self, som1, som2):
        """ renvoie le chemin par le parcours en largeur du sommet
        som1 jusqu'au sommet som2 """

        # on inverse les coordonnées pour éviter des bugs
        som1 = (som1[1], som1[0])
        som2 = (som2[1], som2[0])
        
        # file pour le parcours en largeur
        file = deque()
        # False s'il n'y a pas de marque sinon le sommet d'ou elle vient
        marques = {v : False for v in self.graph.keys()}
        parcours = []
        
        marques[som1] = som1 # le sommet vient de lui même
        file.append(som1) # on ajoute le sommet de départ
        
        u = som1 # sommet courant pour éviter les crachs
        # on explore tout le graphe jusqu'a tomber sur le bon sommet
        # pas besoin de faire tout le parcours
        while u != som2 and len(file)>0:
            # on prend le sommet en tête de file
            u = file.popleft()
            # on ajoute les sommets adjacents non marqués
            for v in self.graph[u]:
                if marques[v] == False:
                     marques[v] = u # on marque le sommet avec le sommet d'ou on vient
                     file.append(v)    
            # on ajoute le sommet courant au parcours
            parcours.append(u)

        # on remonte le chemin parcouru en utilisant les marques
        chemin = []
        while u != som1:
            chemin.append(u)
            u = marques[u]
        chemin.append(u)
            
        # on retourne la liste et la renvoie
        chemin.reverse()
        return chemin
    
    # Algo parcours Profondeur
    def parcours_profondeur(self, som1, som2):
        """ renvoie le chemin par le parcours en profondeur du sommet
        som1 jusqu'au sommet som2 """
        som1 = (som1[1], som1[0])
        som2 = (som2[1], som2[0])
        
        file = deque()
        # False s'il n'y a pas de marque sinon le sommet d'ou elle vient
        marques = {v : False for v in self.graph.keys()}
        parcours = []
        
        marques[som1] = som1 # le sommet vient de lui même
        file.append(som1)
        
        u = som1
        # on explore tout le graphe jusqu'a tomber sur le bon sommet
        while u != som2 and len(file)>0:
            u = file.pop()
            for v in self.graph[u]:
                if marques[v] == False:
                     marques[v] = u
                     file.append(v)    
            parcours.append(u)

        # on remonte le chemin parcouru en utilisant les marques
        chemin = []
        while u != som1:
            chemin.append(u)
            u = marques[u]
        chemin.append(u)
            
        # on retourne la liste et la renvoie
        chemin.reverse()
        return chemin
                

# Algo Dijkstra
def dijkstra(grille, source, cible):
    n, m = len(grille), len(grille[0])
    distances = [[float('inf')] * m for _ in range(n)]
    distances[source[0]][source[1]] = 0
    file = deque([(source, 0)])

    while file:
        (x, y), dist = file.popleft()
        if (x, y) == cible:
            return distances

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and grille[nx][ny] != 1:
                new_dist = dist + 1
                if new_dist < distances[nx][ny]:
                    distances[nx][ny] = new_dist
                    file.append(((nx, ny), new_dist))

    return distances


def get_chemin(grille, source, cible):
    distances = dijkstra(grille, source, cible)
    x, y = cible
    chemin = []
    
    while (x, y) != source:
        chemin.append((x, y))
        dists = [distances[x+1][y], distances[x-1]
                 [y], distances[x][y+1], distances[x][y-1]]
        min_dist = min(dists)
        if dists[0] == min_dist:
            x += 1
        elif dists[1] == min_dist:
            x -= 1
        elif dists[2] == min_dist:
            y += 1
        else:
            y -= 1
            
    chemin.append(source)
    chemin.reverse()
    return chemin