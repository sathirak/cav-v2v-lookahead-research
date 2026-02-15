#!/usr/bin/env python3
"""
Run the Pygame visualizer from the project root.

Examples:
  python run_visualizer.py
  python run_visualizer.py pileup
  python run_visualizer.py pileup --hide-humans
"""

import argparse
import sys

from simulation.visualizer import run_visualizer
from simulation.scenario import list_scenarios, DEFAULT_SCENARIO


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the road simulation visualizer (Pygame).",
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
        "--hide-humans",
        action="store_true",
        help="Do not draw human vehicles (simulation still runs with them)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    run_visualizer(
        scenario_name=args.scenario,
        show_human_cars=not args.hide_humans,
    )
    sys.exit(0)
