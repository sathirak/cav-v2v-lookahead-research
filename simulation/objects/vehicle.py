"""Base vehicle model: 1D kinematics (position, velocity, acceleration) and lane."""

from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.objects.road import Road


class Vehicle:
    """
    A vehicle on the road with 1D kinematics.

    Position is the front bumper; length is the car length. Velocity is
    non-negative. Physics: constant acceleration over each step, then
    position and velocity updated via kinematic equations.
    """

    DEFAULT_LENGTH = 50.0

    def __init__(
        self,
        position: float = 0.0,
        velocity: float = 0.0,
        acceleration: float = 0.0,
        id: Optional[int] = None,
        length: float = DEFAULT_LENGTH,
        lane: int = 0,
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.id = id
        self.length = length
        self.lane = lane

    def step(self, dt: float) -> None:
        """Advance state by dt seconds using constant-acceleration kinematics."""
        self.position += self.velocity * dt + 0.5 * self.acceleration * dt * dt
        self.velocity = max(0.0, self.velocity + self.acceleration * dt)

    def overlaps(self, other: "Vehicle") -> bool:
        """Return True if this vehicle and other are on the same lane and overlap (1D)."""
        if self.lane != other.lane:
            return False
        return (
            self.position - self.length < other.position
            and other.position - other.length < self.position
        )

    def resolve_with_ahead(self, front: "Vehicle", road: "Road") -> None:
        """
        Resolve overlap with the vehicle ahead (front). Call on the rear vehicle.
        Pushes self back to touch front's rear and couples velocity/acceleration (stack).
        """
        self.position = front.position - front.length
        self.velocity = front.velocity
        self.acceleration = front.acceleration
        self.position = road.clamp(self.position)

    @staticmethod
    def resolve_collisions_in_lane(cars: List["Vehicle"], road: "Road") -> None:
        """
        Resolve all overlaps in a list of cars on the same lane (sorted by position).
        Repeatedly push overlapping rear vehicles back until no overlaps remain.
        """
        if len(cars) < 2:
            return
        for _ in range(len(cars) * 2):
            changed = False
            for i in range(len(cars) - 1):
                rear, front = cars[i], cars[i + 1]
                if rear.overlaps(front):
                    rear.resolve_with_ahead(front, road)
                    changed = True
            if not changed:
                break
