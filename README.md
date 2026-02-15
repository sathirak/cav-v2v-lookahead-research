# Cav V2V Lookahead Research

A minimal 1D road simulation for researching connected and autonomous vehicles (CAVs). Cars move along a straight road with position, velocity, and acceleration; the engine resolves same-lane collisions by stacking vehicles and coupling their motion.

## Features

- **Physics**: 1D kinematics (constant acceleration per step), velocity clamped to non-negative.
- **Collision handling**: Overlapping vehicles on the same lane are resolved by pushing them apart and coupling velocity/acceleration so they move as a stack.
- **Vehicle types**: Human and autonomous vehicles (same physics; types used for scenario layout and visualizer options).
- **Scenarios**: Named setups (e.g. pileup, simple, two_lanes) with optional control updates over time.
- **Visualizer**: Pygame window with two lanes, car IDs, time, pause/restart, and optional hiding of human vehicles.

## Project structure

```
.
├── README.md
├── requirements.txt
├── run_simulation.py    # Headless simulation CLI
├── run_visualizer.py    # Pygame visualizer CLI
└── simulation/
    ├── __init__.py      # Package and public API
    ├── main.py          # Headless entry point
    ├── objects/         # Road and vehicles
    │   ├── __init__.py
    │   ├── road.py      # Road (1D segment)
    │   ├── vehicle.py   # Base Vehicle (kinematics)
    │   ├── human_vehicle.py
    │   └── autonomous_vehicle.py
    ├── engine.py        # CarsOnRoad (simulation state and step)
    ├── scenario.py      # Named scenarios (make + update)
    └── visualizer.py    # Pygame visualization
```

## Setup

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

**Headless simulation** (from project root):

```bash
python run_simulation.py [scenario] [--steps N] [--dt T]
```

- `scenario`: `pileup` (default), `simple`, or `two_lanes`
- `--steps`: number of steps (default: 10)
- `--dt`: time step in seconds (default: 1.0)

Examples:

```bash
python run_simulation.py
python run_simulation.py pileup --steps 20
python run_simulation.py simple --dt 0.5
```

**Pygame visualizer**:

```bash
python run_visualizer.py [scenario] [--hide-humans]
```

- `scenario`: same as above
- `--hide-humans`: do not draw human vehicles (simulation still runs with them)

Examples:

```bash
python run_visualizer.py
python run_visualizer.py pileup --hide-humans
```

**As modules** (from project root):

```bash
python -m simulation.main pileup
python -m simulation.visualizer
```

## Scenarios

| Name       | Description |
|-----------|-------------|
| `pileup`  | Five cars per lane (lane 0: autonomous, lane 1: human). Head car brakes at t≥8 s, stops 3 s, then accelerates again. |
| `simple`  | Lane 0: two autonomous; lane 1: one human; constant speed. |
| `two_lanes` | Lane 0: two autonomous; lane 1: two human. |

Convention: **lane 0** = autonomous, **lane 1** = human.

## Requirements

- Python 3.9+
- Pygame ≥ 2.0 (for the visualizer only; headless run has no GUI dependency)

## License

See repository.
