# a_star_2d.py — createur : Ikdoumi Ilian
import math

class GrilleAStar:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur

    def heuristique(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def a_star_next_step(self, depart, but, vitesse, champ_vision, memoire):
        ax, ay = depart
        bx, by = but

        if math.hypot(bx - ax, by - ay) < vitesse:
            return None

        best_angle = None
        best_score = 1e9

        rayon_vision, angle_vision, (vx, vy) = champ_vision
        start_x, start_y = round(ax), round(ay)
        dest_x, dest_y = round(bx), round(by)

        for ang in range(0, 360, 5):
            rad = math.radians(ang)
            nx = ax + math.cos(rad) * vitesse
            ny = ay + math.sin(rad) * vitesse
            fx, fy = round(nx), round(ny)

            score = self.heuristique((nx, ny), but)

            # ---- Penalité selon la mémoire ----
            cell = memoire[fy][fx]
            if cell == 2:          # obstacle connu
                score += 2000
            elif cell == 0:        # safe
                score += 0
            elif cell == 1:        # inconnu : un peu risqué
                score += 15

           
            dxv = fx - vx
            dyv = fy - vy
            dist_v = math.hypot(dxv, dyv)
            if dist_v <= rayon_vision and dist_v > 0:
                if memoire[fy][fx] == 2:     
                    ang_to_point = math.degrees(math.atan2(dyv, dxv))
                    diff = abs((ang_to_point - ang + 180) % 360 - 180)
                    if diff <= angle_vision / 2:
                        score += 2000       

            
            for oy in range(len(memoire)):
                for ox in range(len(memoire[0])):
                    if memoire[oy][ox] == 2:

                        
                        if (ox, oy) == (start_x, start_y):
                            continue
                        if (ox, oy) == (dest_x, dest_y):
                            continue

                        dist = math.hypot(nx - ox, ny - oy)
                        if dist < 2.5:
                            score += 999999  
                        elif dist < 3.0:
                            score += 40      

            if score < best_score:
                best_score = score
                best_angle = ang

        return best_angle
