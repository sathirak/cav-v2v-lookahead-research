"""
Configuration for the human driver model (control experiment).

Defines reaction delay, look-ahead, panic factor, and perception error
so scenarios can set all variables beforehand.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class HumanDriverConfig:
    """
    All parameters for realistic human driver behaviour.

    Rule 1 - Reaction Delay: human reacts to leader state from t - reaction_time.
    Rule 2 - Tunnel Vision: look_ahead must be 1 (only the car directly in front).
    Rule 3 - Panic: if perceived gap < panic_gap, braking is multiplied by panic_brake_multiplier.
    """

    # Rule 1: Brain lag (seconds). Human reacts to leader state from this long ago.
    reaction_time: float = 1.2
    # Rule 2: Look-ahead range (vehicles). Must be 1 for human (tunnel vision).
    look_ahead: int = 1
    # Rule 3: Gap below this (m) triggers panic braking.
    panic_gap: float = 10.0
    # Rule 3: Multiplier on braking force when in panic mode (e.g. 1.2 = 20% harder).
    panic_brake_multiplier: float = 1.2
    # Rule 3: Perception error on gap (e.g. 0.05 = ±5%).
    perception_error: float = 0.05

    # Following model: safe gap = min_gap + headway_time * velocity
    min_gap: float = 5.0
    headway_time: float = 1.5
    # Standard braking and following accelerations (m/s²)
    brake_accel: float = -4.0
    follow_accel: float = 1.0

    def __post_init__(self) -> None:
        if self.look_ahead != 1:
            raise ValueError("Human driver look_ahead must be 1 (tunnel vision)")


# Default config used when none is provided
DEFAULT_HUMAN_CONFIG = HumanDriverConfig()
