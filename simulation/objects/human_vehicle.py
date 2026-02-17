"""
Human-driven vehicle: realistic control experiment with reaction delay,
tunnel vision (look-ahead=1), and panic/perception error.
"""

import random
from typing import Optional, List, Any

from .vehicle import Vehicle
from .human_driver_config import HumanDriverConfig, DEFAULT_HUMAN_CONFIG


# History entry: (t, leader_position, leader_velocity, leader_length)
_HistoryEntry = tuple


class HumanVehicle(Vehicle):
    """
    Human-driven vehicle. Behaves differently from CAVs:

    - Rule 1: Reacts to leader state from t - reaction_time (history buffer).
    - Rule 2: Look-ahead = 1 only (car directly in front).
    - Rule 3: Panic braking when gap < panic_gap; perception error on gap.
    """

    VEHICLE_KIND = "human"

    def __init__(
        self,
        position: float = 0.0,
        velocity: float = 0.0,
        acceleration: float = 0.0,
        id: Optional[int] = None,
        length: float = Vehicle.DEFAULT_LENGTH,
        lane: int = 0,
        config: Optional[HumanDriverConfig] = None,
    ) -> None:
        super().__init__(
            position=position,
            velocity=velocity,
            acceleration=acceleration,
            id=id,
            length=length,
            lane=lane,
        )
        self._config = config if config is not None else DEFAULT_HUMAN_CONFIG
        # History buffer: (t, leader_position, leader_velocity, leader_length); keep ~3s
        self._leader_history: List[_HistoryEntry] = []
        self._max_history_time = 3.0
        # If set by scenario (e.g. scripted brake), use this instead of following logic
        self._scripted_accel: Optional[float] = None

    def _get_leader(self, all_cars: List[Any]) -> Optional[Vehicle]:
        """Return the car directly in front (look-ahead = 1). Same lane, smallest position > self.position."""
        candidates = [
            c for c in all_cars
            if c is not self and c.lane == self.lane and c.position > self.position
        ]
        if not candidates:
            return None
        return min(candidates, key=lambda c: c.position)

    def _record_leader_state(self, leader: Vehicle, t: float) -> None:
        """Append current leader state to history; prune old entries."""
        self._leader_history.append((t, leader.position, leader.velocity, leader.length))
        # Keep only last max_history_time seconds (roughly)
        cutoff = t - self._max_history_time
        self._leader_history = [e for e in self._leader_history if e[0] >= cutoff]

    def _get_delayed_leader_state(self, t: float) -> Optional[_HistoryEntry]:
        """Return (t, pos, vel, length) for time t - reaction_time (closest entry)."""
        target_t = t - self._config.reaction_time
        if not self._leader_history:
            return None
        best = min(
            self._leader_history,
            key=lambda e: abs(e[0] - target_t),
        )
        if abs(best[0] - target_t) > self._config.reaction_time + 0.5:
            return None
        return best

    def _perceived_gap(self, actual_gap: float) -> float:
        """Apply ±perception_error to gap (noisy estimation)."""
        noise = 1.0 + self._config.perception_error * random.uniform(-1.0, 1.0)
        return max(0.0, actual_gap * noise)

    def update_following(self, all_cars: List[Any], t: float, dt: float) -> None:
        """
        Update acceleration using delayed leader state (Rule 1), look-ahead=1 (Rule 2),
        and panic/perception (Rule 3). Call once per step before physics step.
        If _scripted_accel is set (e.g. by scenario), use that and skip following logic.
        """
        if self._scripted_accel is not None:
            self.acceleration = self._scripted_accel
            return
        leader = self._get_leader(all_cars)
        if leader is None:
            return

        self._record_leader_state(leader, t)
        delayed = self._get_delayed_leader_state(t)
        if delayed is None:
            return

        _d_t, d_pos, d_vel, d_len = delayed
        # Gap we "think" we have: leader was at d_pos (rear at d_pos - d_len), we are at self.position
        delayed_gap = d_pos - d_len - self.position
        perceived_gap = self._perceived_gap(delayed_gap)

        cfg = self._config
        safe_gap = cfg.min_gap + cfg.headway_time * self.velocity

        # Panic: gap below threshold → harder braking
        if perceived_gap < cfg.panic_gap:
            self.acceleration = cfg.brake_accel * cfg.panic_brake_multiplier
            return
        # Too close (below safe gap) → standard brake
        if perceived_gap < safe_gap:
            self.acceleration = cfg.brake_accel
            return
        # React to delayed leader speed
        if self.velocity > d_vel:
            self.acceleration = cfg.brake_accel
        elif self.velocity < d_vel:
            self.acceleration = cfg.follow_accel
        else:
            self.acceleration = cfg.brake_accel if perceived_gap < safe_gap else 0.0
