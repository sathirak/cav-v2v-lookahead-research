"""
Named scenarios: factory and control-update functions.

Each scenario is (make_fn, update_fn):
  - make_fn(road_length) -> CarsOnRoad
  - update_fn(sim, t) -> None  (optional; adjusts accelerations etc. by time t)

Convention: lane 0 = autonomous, lane 1 = human.
"""

from typing import Callable, Dict, Tuple, Optional

from simulation.engine import CarsOnRoad, TYPE_AUTONOMOUS, TYPE_HUMAN


# Type alias: (make_sim, update_controls)
Scenario = Tuple[
    Callable[..., CarsOnRoad],
    Callable[[CarsOnRoad, float], None],
]


def _make_pileup(road_length: float = 1000) -> CarsOnRoad:
    """Five cars per lane (ids 1–5 autonomous, 6–10 human); same layout and speeds."""
    sim = CarsOnRoad(road_length)
    positions = [0, 60, 120, 180, 300]
    for i, pos in enumerate(positions):
        sim.add_car(
            position=pos,
            velocity=20,
            acceleration=0.1,
            id=i + 1,
            lane=0,
            vehicle_type=TYPE_AUTONOMOUS,
        )
    for i, pos in enumerate(positions):
        sim.add_car(
            position=pos,
            velocity=20,
            acceleration=0.2,
            id=i + 6,
            lane=1,
            vehicle_type=TYPE_HUMAN,
        )
    return sim


def _update_pileup(sim: CarsOnRoad, t: float) -> None:
    """Head car (id 5 and 10) brakes at t>=8, stops 3 s, then accelerates again."""
    head_auto = sim.get_car(5)
    head_human = sim.get_car(10)
    if t < 8.0:
        return
    if t < 11.0:
        for car in (head_auto, head_human):
            if car is not None:
                car.acceleration = -8
    elif t < 14.0:
        for car in (head_auto, head_human):
            if car is not None:
                car.acceleration = 0
    else:
        for car in (head_auto, head_human):
            if car is not None:
                car.acceleration = 2


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

SCENARIOS: Dict[str, Scenario] = {
    "pileup": (_make_pileup, _update_pileup),
}

DEFAULT_SCENARIO = "pileup"


def get_scenario(name: str) -> Optional[Scenario]:
    """Return (make_fn, update_fn) for the named scenario, or None."""
    return SCENARIOS.get(name)


def list_scenarios() -> list:
    """Return sorted list of scenario names."""
    return sorted(SCENARIOS.keys())
