from collections import deque  # Importation de la classe deque pour la file/la pile


class Graph:
    """ Classe du Graphe"""

    def __init__(self, grid):
        """ Constructeur de la classe Graphe """
        # On crée un graphe à partir de la grille
        self.graph = {}  # Dictionnaire des sommets et des arêtes du graphe vide

        # On parcourt la grille pour créer les sommets et les arêtes du graphe
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                # On ne crée pas de sommet pour les murs
                if grid[i][j] != 1:
                    # On crée un sommet pour chaque case non mur
                    self.graph[(i, j)] = []

                    # On ajoute les arêtes pour chaque case adjacente non mur
                    if i - 1 > - \
                            1 and grid[i - 1][j] != 1:  # Si la case adjacente en haut n'est pas un mur
                        # On ajoute l'arête entre la case courante et la case
                        # adjacente en haut
                        self.graph[(i, j)].append((i - 1, j))
                    # Si la case adjacente en bas n'est pas un mur
                    if i + 1 < len(grid) and grid[i + 1][j] != 1:
                        # On ajoute l'arête entre la case courante et la case
                        # adjacente en bas
                        self.graph[(i, j)].append((i + 1, j))
                    if j - 1 > - \
                            1 and grid[i][j - 1] != 1:  # Si la case adjacente à gauche n'est pas un mur
                        # On ajoute l'arête entre la case courante et la case
                        # adjacente à gauche
                        self.graph[(i, j)].append((i, j - 1))
                    # Si la case adjacente à droite n'est pas un mur
                    if j + 1 < len(grid[0]) and grid[i][j + 1] != 1:
                        # On ajoute l'arête entre la case courante et la case
                        # adjacente à droite
                        self.graph[(i, j)].append((i, j + 1))

    # Algo parcours Largeur
    def parcours_largeur(self, som1, som2):
        """ Renvoie le chemin par le parcours en largeur du sommet
        som1 jusqu'au sommet som2 """

        # On inverse les coordonnées pour éviter des bugs (x, y) -> (y, x)
        som1 = (som1[1], som1[0])
        som2 = (som2[1], som2[0])

        # File pour le parcours en largeur
        file = deque()  # File vide

        # False s'il n'y a pas de marque sinon le sommet d'ou elle vient
        # Dictionnaire des marques
        marques = {v: False for v in self.graph.keys()}
        parcours = []  # Liste des sommets parcourus

        marques[som1] = som1  # Le sommet vient de lui même
        file.append(som1)  # On ajoute le sommet de départ

        u = som1  # Sommet courant pour éviter les crachs

        # On explore tout le graphe jusqu'a tomber sur le bon sommet, pas
        # besoin de faire tout le parcours
        while u != som2 and len(file) > 0:
            # On prend le sommet en tête de file
            u = file.popleft()
            # On ajoute les sommets adjacents non marqués
            for v in self.graph[u]:
                if not marques[v]:
                    # On marque le sommet avec le sommet d'ou on vient
                    marques[v] = u  # On marque le sommet
                    file.append(v)  # On ajoute le sommet à la file
            # On ajoute le sommet courant au parcours
            parcours.append(u)  # On ajoute le sommet courant au parcours

        # On remonte le chemin parcouru en utilisant les marques
        chemin = []  # Liste des sommets du chemin

        # Tant qu'on a pas atteint le sommet de départ
        while u != som1:
            chemin.append(u)  # on ajoute le sommet courant
            u = marques[u]  # on prend le sommet d'ou on vient
        chemin.append(u)  # on ajoute le sommet de départ

        # On retourne la liste et la renvoie
        chemin.reverse()
        return chemin

    # Algo parcours Profondeur
    def parcours_profondeur(self, som1, som2):
        """ Renvoie le chemin par le parcours en profondeur du sommet
        som1 jusqu'au sommet som2 """

        # On inverse les coordonnées pour éviter des bugs, (x, y) -> (y, x)
        som1 = (som1[1], som1[0])
        som2 = (som2[1], som2[0])

        pile = deque()  # Pile vide
        # False s'il n'y a pas de marque sinon le sommet d'ou elle vient
        # Dictionnaire des marques
        marques = {v: False for v in self.graph.keys()}
        parcours = []  # Liste des sommets parcourus

        marques[som1] = som1  # le sommet vient de lui même
        pile.append(som1)  # On ajoute le sommet de départ

        u = som1  # Sommet courant pour éviter les crachs
        # On explore tout le graphe jusqu'a tomber sur le bon sommet, pas
        # besoin de faire tout le parcours

        # Tant qu'on a pas atteint le sommet de destination et qu'il reste des
        # sommets à explorer
        while u != som2 and len(pile) > 0:
            # On prend le sommet en haut de la pile
            u = pile.pop()
            # On ajoute les sommets adjacents non marqués
            for v in self.graph[u]:
                # Si le sommet n'est pas marqué
                if not marques[v]:
                    # On marque le sommet avec le sommet d'ou on vient
                    marques[v] = u  # On marque le sommet
                    pile.append(v)  # On ajoute le sommet à la pile
            parcours.append(u)  # On ajoute le sommet courant au parcours

        # On remonte le chemin parcouru en utilisant les marques
        chemin = []  # Liste des sommets du chemin
        # Tant qu'on a pas atteint le sommet de départ
        while u != som1:
            chemin.append(u)  # On ajoute le sommet courant
            u = marques[u]  # On prend le sommet d'ou on vient
        chemin.append(u)  # On ajoute le sommet de départ

        # On retourne la liste et la renvoie
        chemin.reverse()  # On inverse le chemin pour avoir le bon ordre
        return chemin  # On retourne le chemin


# Algo Dijkstra
def dijkstra(grille, source, cible):
    """Renvoie les distances minimales de la source à chaque sommet de la grille"""
    n, m = len(grille), len(grille[0])  # Taille de la grille
    # Initialisation des distances par un nombre infini pour chaque sommet de
    # la grille
    distances = [[float('inf')] * m for _ in range(n)]
    # La distance de la source à elle-même est nulle
    distances[source[0]][source[1]] = 0
    file = deque([(source, 0)])  # File pour le parcours en largeur

    # Tant que la file n'est pas vide
    while file:
        (x, y), dist = file.popleft()  # On defile le sommet et sa distance
        if (x, y) == cible:  # Si on atteint le sommet cible, on retourne les distances
            return distances  # On retourne les distances

        for dx, dy in [(1, 0), (-1, 0), (0, 1),
                       (0, -1)]:  # On parcourt les sommets adjacents
            nx, ny = x + dx, y + dy  # Coordonnées du sommet adjacent
            # Si le sommet est dans la grille et n'est pas un mur
            if 0 <= nx < n and 0 <= ny < m and grille[nx][ny] != 1:
                new_dist = dist + 1  # On calcule la nouvelle distance
                # Si la nouvelle distance est plus petite que l'ancienne
                if new_dist < distances[nx][ny]:
                    distances[nx][ny] = new_dist  # On met à jour la distance
                    # On ajoute le sommet à la file avec sa nouvelle distance
                    file.append(((nx, ny), new_dist))

    return distances  # On retourne les distances sous forme de matrice qu'on va utiliser pour retrouver le chemin


def get_chemin(grille, source, cible):
    """Renvoie le chemin le plus court de la source à la cible"""
    distances = dijkstra(
        grille,
        source,
        cible)  # On calcule les distances minimales a l'aide de l'algorithme de Dijkstra
    x, y = cible  # Coordonnées de la cible
    chemin = []  # Chemin le plus court vers la cible

    # Tant qu'on n'a pas atteint la source
    while (x, y) != source:
        chemin.append((x, y))  # On ajoute le sommet courant au chemin
        dists = [distances[x + 1][y], distances[x - 1][y], distances[x][y + 1],
                 distances[x][y - 1]]  # On recupere les distances des sommets adjacents
        min_dist = min(dists)  # On recupere la distance minimale

        # On se deplace vers le sommet adjacent ayant la distance minimale
        if dists[0] == min_dist:  # Si la distance minimale est celle du sommet adjacent en bas
            x += 1  # On se deplace vers le bas
        elif dists[1] == min_dist:  # Si la distance minimale est celle du sommet adjacent en haut
            x -= 1  # On se deplace vers le haut
        elif dists[2] == min_dist:  # Si la distance minimale est celle du sommet adjacent à droite
            y += 1  # On se deplace vers la droite
        else:  # Si la distance minimale est celle du sommet adjacent à gauche
            y -= 1  # On se deplace vers la gauche

    chemin.append(source)  # On ajoute la source au chemin
    # On inverse le chemin pour avoir le bon ordre des sommets du chemin a
    # parcourir
    chemin.reverse()
    return chemin  # On retourne le chemin le plus court sous forme de liste de sommets et leurs coordonnées
