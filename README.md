<p align="center">
  <img src="https://github.com/alizealebaron/alizealebaron/blob/main/assets/fly-in.png" width="120"/>
</p>
<h3 align="center">
  <em>Drones are interesting.</em>
</h3>

---

<div align="center">
  <p>
      <img src="https://img.shields.io/badge/score-125%20%2F%20100-success?style=for-the-badge" />
      <img src="https://img.shields.io/github/languages/count/alizealebaron/fly-in?style=for-the-badge&logo=" />
      <img src="https://img.shields.io/github/languages/top/alizealebaron/fly-in?style=for-the-badge" />
      <img src="https://img.shields.io/github/last-commit/alizealebaron/fly-in?style=for-the-badge" />
  </p>
</div>

## ⚠️ Avant propos

- **Portfolio :** Ce repertoire se concentre sur un seul sujet. Vous pouvez retrouver tous mes projets sur mon [profil](https://github.com/alizealebaron).
- **Sujet :** Conformément aux règles de 42, vous ne trouverez pas le sujet de l'exercice dans ce répertoire.
- **État du projet:** Le code est exactement le même que lorsqu'il est validé. Il ne sera pas mis à jour même s'il contient des erreurs.
- **Aide & Licence :** Ce repertoire est principalement là pour vous aider à faire votre propre code. Évitez de copier / coller sans comprendre le code.

## 🦆 Status

**Commencé le :** 26/02/2026

**Rendu le :** 02/04/2026.

## Description

**Fly-In** is an advanced drone simulation and pathfinding optimization system. The project simulates autonomous drones navigating through a network of interconnected zones while respecting capacity limitations on both nodes and connections.

### Project Goal

The primary objective of Fly-In is to efficiently coordinate multiple drones from a start hub to an end hub through an arbitrary graph network, minimizing the total number of turns required while respecting several constraints:

- **Zone Capacity Limits**: Each zone can only accommodate a limited number of drones simultaneously
- **Connection Capacity Limits**: Connections between zones have maximum capacity constraints
- **Zone Type Variations**: Different zone types impose different movement mechanics (normal, restricted, priority, blocked)
- **Dynamic Path Recalculation**: Paths must be recalculated at each turn to accommodate real-time changes in network availability

### Key Features

- **Intelligent Pathfinding**: Uses Dijkstra's algorithm with dynamic recalculation to find optimal paths for each drone
- **Constraint Management**: Handles complex capacity constraints and zone type restrictions
- **Multi-Agent Coordination**: Manages simultaneous movement of multiple drones with collision avoidance
- **Visual Representation**: Generates graph visualizations using NetworkX and Matplotlib to display network topology
- **Comprehensive Testing**: Includes test maps ranging from simple linear paths to impossible challenges with 25 drones
- **Robust Error Handling**: Extensive validation of input files with detailed error reporting for 20+ error types

## Instructions

### Requirements

- Python >= 3.10
- Poetry (package manager)
- Linux/Unix environment (tested on Linux)

### Installation

1. **Clone the repository** (if not already done):
```bash
cd /path/to/fly-in
```

2. **Set up the Python virtual environment and install dependencies**:
```bash
make all
```

This command will:
- Create a Python virtual environment (.venv)
- Install all dependencies via Poetry
- Verify the setup with linting and type checking

3. **Activate the new python env (commande for linux)**:
```bash
source .venv/bin/activate
```

### Running the Program

To run Fly-In with a specific map file:

```bash
python3 main.py path_to_the_map
```

Replace `maps/easy/01_linear_path.txt` with any valid map file from the `maps/` directory.

**Supported map directories:**
- `maps/easy/` - Simple introductory challenges
- `maps/medium/` - Intermediate optimization puzzles
- `maps/hard/` - Advanced complex scenarios
- `maps/challenger/` - Research and stress testing (extreme difficulty)
- `maps/debug/` - Debugging and edge case testing

### Development Commands

```bash
# Install all dependencies and setup environment
make all

# Run the program
make run

# Run type checking with mypy
make lint-strict

# Run linting analysis
make lint

# Clean up generated files
make clean

# Remove virtual environment
make fclean

# Reinstall everything from scratch
make re
```

### Input File Format

Map files define the network topology in plain text format:

```
<number_of_drones>

<zone_definition>
...
<connection_definition>
...
```

**Zone Definition**: `<name> <x> <y> <type> [<max_drones>, <color>, <zone>]`
- `max_drones`: optional, default is 1
- `color`: color of the node
- `zone`: normal, restricted, priority, blocked

**Connection Definition**: `<zone1> <zone2> [<max_link_capacity>]`
- `max_link_capacity`: optional, maximum drones on connection simultaneously

### Output

The program outputs:
1. **Console output**: Turn-by-turn drone movements showing which drones moved where
2. **Graph visualization**: NetworkX graph displayed with matplotlib showing:
   - Zones as colored nodes
   - Connections as edges
   - Zone positions based on x,y coordinates from the file

## Algorithm Choices and Implementation Strategy

### Core Algorithm: Dijkstra with Dynamic Recalculation

**Why Dijkstra?**
- Guarantees shortest path in weighted graphs
- Efficient time complexity: O((V + E) log V) with binary heap
- Suitable for real-time recalculation at each turn

### Implementation Strategy

#### 1. **Graph Representation**

The project uses multiple interconnected models:
- **Node**: Represents a zone with name, coordinates, type, and capacity
- **Connexion**: Represents edges with capacity constraints
- **Drone**: Represents moving agents with position tracking and state
- **FlyinManager**: Centralized manager orchestrating all entities

#### 2. **Path Calculation** (dijkstra.py)

At each turn, for each drone needing movement:
1. Calculate shortest path from current position to end hub
2. Check constraints:
   - Destination zone must not be full (capacity < max_drones)
   - Destination must not be blocked
   - Connection must have available capacity
3. Update path weights dynamically based on:
   - Zone type (restricted zones have weight 2, others weight 1)
   - Current occupancy of zones
   - Active connections

#### 3. **Movement Coordination** (moove_drone.py)

**Two-phase movement system:**

**Phase 1: Connection Processing**
- Drones on connections try to enter their destination zone
- Respects zone capacities and connection limitations
- Updates drone state upon successful entry

**Phase 2: Node Processing**
- Uses priority queue starting from end hub
- Processes nodes in order to minimize cascading movements
- Each drone on a node attempts to move to next calculated waypoint
- Ensures efficient coordination without deadlocks

#### 4. **Constraint Handling**

**Zone Capacity Limits:**
```python
if new_dist < dict_distances[neighbor.name] and
   neighbor.is_completed() is False and
   neighbor.zone != "blocked":
    # Path is valid, add to queue
```

**Connection Management:**
- Each connection tracks active drones
- Respects per-connection capacity limits
- Handles 2-turn restricted zone transitions

## Visual Representation Features

### Graph Visualization System

The project includes a sophisticated visualization module using NetworkX and Matplotlib:

#### 1. **Network Topology Display**

```python
show_graph(flyinManager, filename)
```

**Features:**
- **Node Positioning**: Uses coordinates from input file to position zones in 2D space
- **Color-Coded Nodes**: Visual distinction between zone types:
  - Green: Start hub
  - Red: End hub
  - Blue: Normal zones
  - Yellow: Priority zones
  - Orange: Restricted zones
  - Gray: Blocked zones
- **Edge Representation**: Connections shown as gray lines between zones

#### 2. **Spatial Layout**

The visualization preserves spatial relationships from the input file:
- X, Y coordinates from zone definitions used for node positioning
- Enables intuitive understanding of physical network layout
- Helps identify bottlenecks and inefficient paths visually

## Resources

### Documentation and References

#### Graph Theory

- [Graph Theory in Python](https://sites.google.com/view/aide-python/graphiques/graphs-et-th%C3%A9orie-des-r%C3%A9seaux-en-langage-python)
- [Graph Theory Fundamentals](https://en.wikipedia.org/wiki/Graph_theory)

#### Dijkstra Algorithms

- [Dijkstra's Algorithm - Maths-cours](https://www.maths-cours.fr/methode/algorithme-de-dijkstra-etape-par-etape)
- [Dijkstra's Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

#### Python Graph Libraries

- [Arcade Documentation](https://api.arcade.academy/en/stable/index.html) - Graphic View
- [Pydantic Data Validation](https://docs.pydantic.dev/) - Type-safe data handling

#### Other Fly-in project

- [Overtek's fly-in](https://github.com/Overtekk/Fly-in)

### AI Usage Documentation

**Use of AI in this project:**

1. **Dijkstra Algorithms**
   - Clarification and explanation of the Dijkstra algorithm
   - Debugging some of the algorithm error

2. **Checking Norm**
   - Helped to fix numerous mypy errors
   - Verify that all code comments are in English

3. **Documentation and Comments**
   - AI assisted in generating docstrings for some functions and classes
   - Correction of spelling mistakes and rewording of incorrect sentences

## Project Structure

```
fly-in/
├── main.py                 # Entry point for the application
├── pyproject.toml          # Poetry project configuration
├── Makefile                # Build automation
├── README42.md             # Original 42 project requirements
├── maps/                   
│   ├── easy/               # Simple test cases (linear, fork, basic capacity)
│   ├── medium/             # Intermediate cases (dead ends, loops, priorities)
│   ├── hard/               # Advanced cases (mazes, extreme capacity)
│   ├── challenger/         # Extreme challenges (25 drones)
│   └── invalid/            # Error case testing (20+ error types)
└── src/
    ├── algorithm/          
    │   ├── dijkstra.py     # Shortest path calculation
    │   └── moove_drone.py  # Movement coordination
    ├── models/             # Data models
    │   ├── flyinManager.py 
    │   ├── node.py         # Zone representation
    │   ├── connexion.py    # Connection representation
    │   └── drone.py        # Drone representation
    ├── parsing/            
    │   └── parsing.py      # File parser with validation
    ├── utils/              
    │   ├── error.py        # Error handling
    │   └── color.py        # Color utilities
    └── view/               
        └── graph_view.py   # Network visualization
```

## Testing

The project includes extensive test maps covering:

- **Easy Maps** (3): Linear paths, simple forks, basic capacity
- **Medium Maps** (3): Dead ends, circular loops, priority puzzles
- **Hard Maps** (3): Maze nightmares, capacity hell, ultimate challenges
- **Challenger Maps** (1): The impossible dream (25 drones)
- **Debug Maps** (3): Metadata and parsing edge cases
- **Invalid Maps** (21): Comprehensive error case coverage

Run any map with:
```bash
python3 main.py maps/hard/01_maze_nightmare.txt
```

## License

This project is licensed under CC0 1.0 Universal (Public Domain).

---

**Last Updated**: March 26, 2026\
**Contact :** alebaron@student.42lehavre.fr
