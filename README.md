# Epidemic Spread Simulation
Real-time virus spread simulation with autonomous agents (A* pathfinding, Python ↔ Java sockets, multithreading)

Group project done during my 2nd year of MIASHS at Université Paul Valéry Montpellier 3, with Adem Ejebli and Hicham Sabri.

The goal was to simulate the spread of a virus in a population of autonomous agents moving around a virtual city. Each agent follows a route between places (school, park, work, supermarket...), moves continuously using an adapted A* algorithm, and can get infected depending on its proximity to other infected agents.

I was mainly in charge of the Python side: the agents, the A* pathfinding, the memory system and the multithreading.

## How it works

The project is split into two programs running in real time:

- a Python engine handles the simulation logic (agents, movement, infection, threads)
- a Java application handles the real-time graphical display

Both communicate through network sockets, sending each agent's position and health state tick by tick.

## Main features

- Continuous movement with an A* algorithm adapted to work by angles instead of cell by cell
- A vision system: each agent only discovers the map progressively through its field of view
- A memory grid per agent (unknown / safe / place) used by A* to plan routes and avoid obstacles
- Map exploration split into four quadrants the agent searches one after another
- Health states: healthy, infected, immune, with infection based on distance between agents
- Collision avoidance: agents that get too close automatically move apart
- Multithreading: one thread per agent, synchronized between cycles
- Live statistics (healthy / infected / immune counts) displayed on the Java side

## Tech stack

- Python — simulation engine (agents, A*, infection, threads)
- Java (Swing) — graphical interface
- TCP sockets — Python ↔ Java communication

## Repository content

- `python/` — simulation engine (Agent.py, a_star_2d.py, Start_Infection.py, personnes.py)
- `java/` — Swing application (MainApp, PanelSimulation, Agent, NetworkThread)
- `report/` — full project report (in French), week by week

## Team — Group 13

Adem Ejebli, Ilian Ikdoumi, Hicham Sabri.
