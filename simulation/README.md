# Cav V2V Lookahead Research

Simple simulation: cars on a straight road (position, velocity, acceleration).

## Setup

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

With the venv activated, from the project root:

```bash
python run_simulation.py
```

Or run the module:

```bash
python -m simulation.main
```

## Visualizer

To see the cars moving on the road in a window:

```bash
python run_visualizer.py
```

Or:

```bash
python -m simulation.visualizer
```

Requires `matplotlib` (see requirements.txt).
