"""
Headless simulation entry point.

Run from project root: python run_simulation.py [scenario] [--steps N] [--dt T]
"""

from typing import Optional

from simulation.scenario import get_scenario, list_scenarios, DEFAULT_SCENARIO


def main(
    scenario_name: Optional[str] = None,
    steps: int = 10,
    dt: float = 1.0,
) -> Optional[int]:
    """
    Run the simulation for a given scenario.
    Returns None on success, or 1 if scenario is unknown (and prints to stderr).
    """
    if scenario_name is None:
        scenario_name = DEFAULT_SCENARIO
    scenario = get_scenario(scenario_name)
    if scenario is None:
        print("Unknown scenario: %r" % scenario_name)
        print("Available:", ", ".join(list_scenarios()))
        return 1
    make_simulation, update_controls = scenario

    sim = make_simulation()
    t = 0.0

    print("Scenario: %s" % scenario_name)
    print("Initial:", [(c.id, c.position, c.velocity) for c in sim.cars])

    for _ in range(steps):
        update_controls(sim, t)
        had_collision = sim.step(dt)
        t += dt
        if had_collision:
            print("Collision!")
        print("t = %.1fs:" % t, [(c.id, c.position, c.velocity) for c in sim.cars])

    return None


if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else None
    exit_code = main(scenario_name=name)
    sys.exit(exit_code if exit_code is not None else 0)
