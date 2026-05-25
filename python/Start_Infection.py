#createur : Sabri Hicham
#Modification : Ikdoumi Ilian
import socket
import struct
import time
import threading
import math
import random

from Agent import Agent, LIEUX
from a_star_2d import GrilleAStar
from personnes import personnes

HOST = "127.0.0.1"
PORT = 5061

SPEED_FACTOR = 1.0

def get_delay(base):
    return base / SPEED_FACTOR

grille = GrilleAStar(30, 20)

COLLISION_RADIUS = 0.4
REPEL_STRENGTH   = 0.2

RAYON_INFECTION      = 0.5
PROBA_INFECTION      = 0.05
SEUIL_GUERISON_LIEUX = 6    

def envoyer_lieux(conn):
    conn.sendall(struct.pack("!I", len(LIEUX)))
    for nom, (x, y) in LIEUX.items():
        nom_b = nom.encode("utf-8")
        conn.sendall(struct.pack("!I", len(nom_b)))
        conn.sendall(nom_b)
        conn.sendall(struct.pack("!dd", x, y))

def get_etat_code(agent):
    if agent.etat == "infecte": return 1
    if agent.etat == "immunise": return 2
    return 0

def envoyer_position(conn, agent):
    nom_b = agent.nom.encode("utf-8")
    x, y = agent.position
    etat_code = get_etat_code(agent)

    data = (
        struct.pack("!I", len(nom_b))
        + nom_b
        + struct.pack("!dd", x, y)
        + struct.pack("!B", etat_code)
    )
    conn.sendall(data)

def ecouter_commandes(conn):
    global SPEED_FACTOR
    while True:
        try:
            msg = conn.recv(1024).decode().strip()
            if msg.startswith("SPEED"):
                _, val = msg.split()
                SPEED_FACTOR = float(val)
                print(f"⚡ Nouvelle SPEED_FACTOR = {SPEED_FACTOR}")
        except:
            break

class AgentThread(threading.Thread):

    def __init__(self, agent, conn, grille, all_agents):
        super().__init__()
        self.agent = agent
        self.conn = conn
        self.grille = grille
        self.all_agents = all_agents

        self.index = 0
        self.trajet_termine = False
        self.fini_parcours = False

    def gerer_collisions(self):
        for other in self.all_agents:
            if other is self.agent:
                continue
            dx = self.agent.position[0] - other.position[0]
            dy = self.agent.position[1] - other.position[1]
            dist = math.hypot(dx, dy)

            if dist < 1e-6:
                continue
            if dist < COLLISION_RADIUS:
                push = (COLLISION_RADIUS - dist) * REPEL_STRENGTH
                self.agent.position = (
                    self.agent.position[0] + (dx/dist)*push,
                    self.agent.position[1] + (dy/dist)*push
                )

    def gerer_infection(self):
        if self.agent.etat != "sain":
            return

        for other in self.all_agents:
            if other is self.agent or other.etat != "infecte":
                continue

            dx = self.agent.position[0] - other.position[0]
            dy = self.agent.position[1] - other.position[1]
            if math.hypot(dx, dy) < RAYON_INFECTION:
                if random.random() < PROBA_INFECTION:
                    self.agent.etat = "infecte"
                    self.agent.lieux_parcourus_infecte = 0
                    print(f"🦠 {self.agent.nom} INFECTÉ par {other.nom}")
                    return

    def maj_etat_sanitaire(self):
        if self.agent.etat == "infecte":
            if self.agent.lieux_parcourus_infecte >= SEUIL_GUERISON_LIEUX:
                self.agent.etat = "immunise"
                print(f"✅ {self.agent.nom} est GUÉRI")
                self.agent.lieux_parcourus_infecte = 0

    def run(self):
        global SPEED_FACTOR

        while True:   
            self.index = 0
            self.fini_parcours = False

            depart = self.agent.parcours[0]
            self.agent.position = LIEUX[depart]
            self.agent.memoire = [[0 for _ in range(30)] for _ in range(20)]
            dx, dy = LIEUX[depart]
            self.agent.memoire[int(dy)][int(dx)] = 1

            while self.index < len(self.agent.parcours) - 1:

                depart = self.agent.parcours[self.index]
                arrivee = self.agent.parcours[self.index + 1]
                but_nom = arrivee
                but = self.agent.lieux_connus.get(but_nom, None)

                print(f"\n➡️ {self.agent.nom} commence trajet {depart} → {arrivee}")

                tick = 0

                while True:

                    if but is not None:
                        dist = math.hypot(self.agent.position[0] - but[0],
                                          self.agent.position[1] - but[1])
                        if dist < 0.2:

                            if self.agent.etat == "infecte":
                                self.agent.lieux_parcourus_infecte += 1

                            print(f"🏁 {self.agent.nom} ARRIVÉ à {arrivee}")
                            break

                    if but is None:
                        angle = self.agent.choisir_angle_exploration()
                    else:
                        champ_vision = (
                            self.agent.rayon_vision,
                            self.agent.angle_vision,
                            self.agent.position
                        )
                        angle = self.grille.a_star_next_step(
                            self.agent.position, but,
                            self.agent.vitesse, champ_vision, self.agent.memoire
                        )
                        if angle is None:
                            angle = self.agent.choisir_angle_exploration()

                    rad = math.radians(angle)
                    nx = self.agent.position[0] + math.cos(rad) * self.agent.vitesse
                    ny = self.agent.position[1] + math.sin(rad) * self.agent.vitesse

                    nx = max(0, min(nx, 29))
                    ny = max(0, min(ny, 19))
                    self.agent.position = (nx, ny)

                    self.gerer_collisions()

                    self.agent.update_vision()

                    if but is None and but_nom in self.agent.lieux_connus:
                        but = self.agent.lieux_connus[but_nom]
                        tick = 0

                    self.gerer_infection()
                    self.maj_etat_sanitaire()

                    envoyer_position(self.conn, self.agent)

                    tick += 1
                    if but is not None and tick > 300:
                        print(f"⛔ {self.agent.nom} dépasse 300 ticks → STOP")
                        break

                    time.sleep(get_delay(1/60))

                self.index += 1
                self.trajet_termine = True

                while self.trajet_termine:
                    time.sleep(get_delay(0.01))

            self.fini_parcours = True
            print(f"🔁 {self.agent.nom} a terminé son parcours → redémarrage…")

def main():
    print("Serveur en attente du client Java…")
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)

    conn, addr = s.accept()
    print("Client connecté :", addr)

    envoyer_lieux(conn)

    threading.Thread(target=ecouter_commandes, args=(conn,), daemon=True).start()

    agents = []
    for nom, parcours in personnes.items():
        a = Agent(nom, parcours)
        agents.append(a)

    if agents:
        agents[0].etat = "infecte"

    threads = []
    for a in agents:
        t = AgentThread(a, conn, grille, agents)
        threads.append(t)
        t.start()
        time.sleep(0.05)

    print("\n🚀 SIMULATION INFINIE LANCÉE\n")

    while True:
        while not all(t.trajet_termine or t.fini_parcours for t in threads):
            time.sleep(get_delay(0.01))

        print("\n=== 🔁 TOUS LES AGENTS ONT FINI UN TOUR ===\n")

        for t in threads:
            t.trajet_termine = False

if __name__ == "__main__":
    main()
