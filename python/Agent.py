#createur : Ikdoumi Ilian 
import random
import math
from math import cos, sin, radians
from a_star_2d import GrilleAStar

LIEUX = {
    "Ecole": (5, 18),
    "Bibliotheque": (10, 5),
    "Parc": (20, 16),
    "Travail": (23, 10),
    "Supermarche": (28, 14),
    "Cafe": (16, 9),
    "Cinema": (4, 9),
    "Restaurant": (11, 15),
}

class Agent:
    def __init__(self, nom, parcours, largeur_grille=30, hauteur_grille=20):
        self.nom = nom
        self.parcours = parcours
        self.position = LIEUX[parcours[0]]
        self.vitesse = 0.1

        self.memoire = [[0 for _ in range(largeur_grille)] for _ in range(hauteur_grille)]
        x, y = round(self.position[0]), round(self.position[1])
        self.memoire[y][x] = 1

        self.rayon_vision = 4.0
        self.angle_vision = 120

        self.index_parcours = 0
        self.lieux_connus = {parcours[0]: self.position}

        self.angle_exploration = random.randint(0, 359)
        self.explo_ticks = 0
        self.max_persist = 50

        self.quadrant_order = [1, 2, 3, 4]
        self.quadrants_done = {1: False, 2: False, 3: False, 4: False}

        self.etat = "sain"
        self.ticks_infecte = 0
        self.lieux_parcourus_infecte = 0  

    def quadrant_rect(self, q):
        if q == 1:
            return 0, 15, 10, 20
        if q == 2:
            return 15, 30, 10, 20
        if q == 3:
            return 15, 30, 0, 10
        if q == 4:
            return 0, 15, 0, 10

    def get_quadrant(self, x, y):
        if y >= 10:
            return 1 if x < 15 else 2
        else:
            return 4 if x < 15 else 3

    def check_quadrant_done(self, q):
        x0, x1, y0, y1 = self.quadrant_rect(q)
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                if self.memoire[yy][xx] == 0:
                    return False
        return True

    def update_quadrants_done(self):
        for q in self.quadrant_order:
            if not self.quadrants_done[q] and self.check_quadrant_done(q):
                self.quadrants_done[q] = True

    def get_current_quadrant(self):
        for q in self.quadrant_order:
            if not self.quadrants_done[q]:
                return q
        return None

    def detecter_lieux_reels(self):
        px, py = self.position
        for nom, (lx, ly) in LIEUX.items():
            dist = math.hypot(px - lx, py - ly)
            if dist < 4.0:
                self.lieux_connus[nom] = (lx, ly)
                ry, rx = round(ly), round(lx)
                if 0 <= ry < len(self.memoire) and 0 <= rx < len(self.memoire[0]):
                    self.memoire[ry][rx] = 1

    def update_vision(self):
        px, py = self.position
        R = int(self.rayon_vision)
        current = (round(px), round(py))

        self.detecter_lieux_reels()

        next_target = None
        if self.index_parcours + 1 < len(self.parcours):
            next_target = LIEUX[self.parcours[self.index_parcours + 1]]

        for dy in range(-R, R + 1):
            for dx in range(-R, R + 1):
                x = round(px + dx)
                y = round(py + dy)

                if not (0 <= x < len(self.memoire[0]) and 0 <= y < len(self.memoire)):
                    continue

                if (x, y) in LIEUX.values():
                    if (x, y) == current:
                        self.memoire[y][x] = 1
                        continue

                    if next_target is not None and (x, y) == next_target:
                        self.memoire[y][x] = 1
                        continue

                    self.memoire[y][x] = 2

                    for nom, coord in LIEUX.items():
                        if coord == (x, y):
                            self.lieux_connus[nom] = coord
                    continue

                self.memoire[y][x] = 1

        self.update_quadrants_done()

    def choisir_angle_exploration(self):
        if self.explo_ticks < self.max_persist:
            self.explo_ticks += 1
            return self.angle_exploration

        current_quad = self.get_current_quadrant()
        meilleur_angle = None
        meilleur_score = -1e9

        for _ in range(400):
            ang = random.randint(0, 359)
            rad = radians(ang)
            nx = self.position[0] + cos(rad) * self.vitesse
            ny = self.position[1] + sin(rad) * self.vitesse
            fx, fy = round(nx), round(ny)

            if not (0 <= fx < len(self.memoire[0]) and 0 <= fy < len(self.memoire)):
                continue

            if self.memoire[fy][fx] == 2:
                continue

            score = 0
            if self.memoire[fy][fx] == 0:
                score += 100
            else:
                score -= 10

            # 🔥 Ajout : ÉVITEMENT DES LIEUX IDENTIQUE À A*
            for nom, (lx, ly) in LIEUX.items():
                dist_lieu = math.hypot(nx - lx, ny - ly)

                if dist_lieu < 2.5:
                    score -= 999999
                    continue

                elif dist_lieu < 3.0:
                    score -= 40

            if current_quad is not None:
                if self.get_quadrant(fx, fy) == current_quad:
                    score += 40
                else:
                    score -= 40

            if score > meilleur_score:
                meilleur_score = score
                meilleur_angle = ang

        if meilleur_angle is None:
            meilleur_angle = random.randint(0, 359)

        self.angle_exploration = meilleur_angle
        self.explo_ticks = 0
        return meilleur_angle
