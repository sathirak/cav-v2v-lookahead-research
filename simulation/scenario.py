"""
Named scenarios: factory and control-update functions.

To add or edit a scenario:
  1. make_fn(road_length, ...) creates CarsOnRoad and adds vehicles.
  2. update_fn(sim, t) sets scripted accelerations each step (e.g. from a phase table).
  Register in SCENARIOS at the bottom.

Convention: lane 0 = autonomous, lane 1 = human.
"""

from typing import Callable, Dict, Tuple, Optional

from simulation.engine import CarsOnRoad, TYPE_AUTONOMOUS, TYPE_HUMAN
from simulation.objects import HumanDriverConfig


# Type alias: (make_sim, update_controls)
Scenario = Tuple[
    Callable[..., CarsOnRoad],
    Callable[[CarsOnRoad, float], None],
]


# ---------------------------------------------------------------------------
# Pileup: human config tuned for maximum realism (control experiment)
# ---------------------------------------------------------------------------

PILEUP_HUMAN_CONFIG = HumanDriverConfig(
    # Rule 1 – Brain lag: slow reaction (see brake lights → process → move foot)
    reaction_time=1.4,
    # Rule 2 – Tunnel vision: only the car directly in front
    look_ahead=1,
    # Rule 3 – Panic: when gap suddenly drops below this, over-brake
    panic_gap=8.0,
    panic_brake_multiplier=1.35,
    # Noisy gap estimation (humans are bad at judging distance)
    perception_error=0.08,
    # Following: safe gap = min_gap + headway_time * velocity
    min_gap=6.0,
    headway_time=1.8,
    # Slightly under-brake when “comfortable”, panic then over-brakes
    brake_accel=-3.8,
    follow_accel=0.8,
)


# Human lane: column in traffic – tight spacing so one sudden brake causes a shockwave.
# Column order (front to back): 13, 12, 11, 10, 9, 8, 7.  Gap ~15 m between cars.
HUMAN_LANE_POSITIONS = [0, 65, 130, 195, 260, 325, 390]
HEAD_HUMAN_ID = 13
SECOND_HUMAN_ID = 12

AUTO_LANE_POSITIONS = [0, 65, 130, 195, 260, 325]
HEAD_AUTO_ID = 6


# ---------------------------------------------------------------------------
# Pileup timeline: edit this table to change what happens and when.
# Each row: (phase_name, t_start, t_end, head_car_accel, second_car_scripted_accel)
#   - t_end=None means "until end of sim"
#   - second_car_scripted_accel: None = normal following; number = force that accel (e.g. -7 brake)
# Second shockwave is at 35–38 s so the column has time to speed back up first.
# ---------------------------------------------------------------------------

PILEUP_PHASES = [
    ("first_shockwave", 0, 3, -7.0, None),
    ("first_hold", 3, 5, 0.0, None),
    ("speed_up", 5, 35, 2.0, None),
    ("second_shockwave", 35, 38, 2.0, -7.0),
    ("second_hold", 38, 40, 2.0, 0.0),
    ("resume", 40, None, 2.0, None),
]


def _pileup_phase_at(t: float):
    """Return (head_accel, second_scripted_accel) for time t from PILEUP_PHASES."""
    for name, t_start, t_end, head_accel, second_accel in PILEUP_PHASES:
        if t < t_start:
            continue
        if t_end is not None and t >= t_end:
            continue
        return head_accel, second_accel
    # past last phase: use last phase's resume behaviour
    last = PILEUP_PHASES[-1]
    return last[3], last[4]


def _make_pileup(
    road_length: float = 1500,
    human_config: Optional[HumanDriverConfig] = None,
) -> CarsOnRoad:
    """
    Column of cars in traffic; sudden head-car brake triggers a shockwave in the human lane.
    Lane 0: 6 autonomous. Lane 1: 7 human drivers in tight formation (~15 m gaps).
    Uses PILEUP_HUMAN_CONFIG by default.
    """
    sim = CarsOnRoad(road_length, human_config=human_config or PILEUP_HUMAN_CONFIG)
    for i, pos in enumerate(AUTO_LANE_POSITIONS):
        sim.add_car(
            position=pos,
            velocity=20,
            acceleration=0,
            id=i + 1,
            lane=0,
            vehicle_type=TYPE_AUTONOMOUS,
        )
    for i, pos in enumerate(HUMAN_LANE_POSITIONS):
        sim.add_car(
            position=pos,
            velocity=20,
            acceleration=0,
            id=len(AUTO_LANE_POSITIONS) + 1 + i,
            lane=1,
            vehicle_type=TYPE_HUMAN,
        )
    return sim


def _update_pileup(sim: CarsOnRoad, t: float) -> None:
    """Apply pileup timeline: phases are defined in PILEUP_PHASES (read/write there)."""
    head_auto = sim.get_car(HEAD_AUTO_ID)
    head_human = sim.get_car(HEAD_HUMAN_ID)
    second_human = sim.get_car(SECOND_HUMAN_ID)

    head_accel, second_scripted = _pileup_phase_at(t)

    for car in (head_auto, head_human):
        if car is not None:
            car.acceleration = head_accel
    if second_human is not None:
        second_human._scripted_accel = second_scripted


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
