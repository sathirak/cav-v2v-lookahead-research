"""Cars on a road: add cars, step the simulation."""

import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from simulation.scenario import make_simulation, update_controls


def main():
    sim = make_simulation()
    dt = 1.0
    t = 0.0

    print("Initial:", [(c.id, c.position, c.velocity) for c in sim.cars])

    for _ in range(10):
        update_controls(sim, t)
        sim.step(dt)
        t += dt
        if sim.check_collision():
            print("Collision!")
            break
        print("t = %.1fs:" % t, [(c.id, c.position, c.velocity) for c in sim.cars])


if __name__ == "__main__":
    main()
