"""
Cav V2V Lookahead Research — 1D road simulation with human and autonomous vehicles.

Public API:
  - Vehicle, HumanVehicle, AutonomousVehicle
  - Road, CarsOnRoad
  - get_scenario, list_scenarios, DEFAULT_SCENARIO
"""

from simulation.objects import (
    Vehicle,
    HumanVehicle,
    AutonomousVehicle,
    Road,
    HumanDriverConfig,
    DEFAULT_HUMAN_CONFIG,
)
from simulation.engine import CarsOnRoad
from simulation.scenario import (
    get_scenario,
    list_scenarios,
    DEFAULT_SCENARIO,
)

__all__ = [
    "Vehicle",
    "HumanVehicle",
    "AutonomousVehicle",
    "Road",
    "CarsOnRoad",
    "HumanDriverConfig",
    "DEFAULT_HUMAN_CONFIG",
    "get_scenario",
    "list_scenarios",
    "DEFAULT_SCENARIO",
]
