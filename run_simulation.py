#!/usr/bin/env python3
"""
Run the headless simulation from the project root.

Examples:
  python run_simulation.py
  python run_simulation.py pileup
  python run_simulation.py simple --steps 20
"""

import argparse
import sys

from simulation.main import main
from simulation.scenario import list_scenarios, DEFAULT_SCENARIO


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the road simulation (headless).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Scenarios: {', '.join(list_scenarios())}",
    )
    parser.add_argument(
        "scenario",
        nargs="?",
        default=DEFAULT_SCENARIO,
        help=f"Scenario name (default: {DEFAULT_SCENARIO})",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=10,
        help="Number of simulation steps (default: 10)",
    )
    parser.add_argument(
        "--dt",
        type=float,
        default=1.0,
        help="Time step in seconds (default: 1.0)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(scenario_name=args.scenario, steps=args.steps, dt=args.dt) or 0)
