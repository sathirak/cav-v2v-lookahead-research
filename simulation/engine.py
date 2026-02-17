"""Simulation engine: road, vehicles, stepping, and collision detection/resolution."""

from collections import defaultdict
from typing import Optional, List, Union

from simulation.objects import (
    Road,
    Vehicle,
    HumanVehicle,
    AutonomousVehicle,
    HumanDriverConfig,
    DEFAULT_HUMAN_CONFIG,
)


# Vehicle type identifiers for add_car()
TYPE_HUMAN = "human"
TYPE_AUTONOMOUS = "autonomous"


class CarsOnRoad:
    """
    Simulation state: one road and a list of vehicles.

    - Step: human vehicles update_following (delayed reaction) then all vehicles step.
    - Collision resolution: overlapping vehicles on the same lane are pushed apart and
      velocity/acceleration are coupled so they move as a stack.
    """

    def __init__(
        self,
        road_length: float,
        human_config: Optional[HumanDriverConfig] = None,
    ) -> None:
        self.road = Road(road_length)
        self.cars: List[Union[HumanVehicle, AutonomousVehicle]] = []
        self.human_config = human_config if human_config is not None else DEFAULT_HUMAN_CONFIG

    def add_car(
        self,
        position: float = 0.0,
        velocity: float = 0.0,
        acceleration: float = 0.0,
        id: Optional[int] = None,
        length: float = Vehicle.DEFAULT_LENGTH,
        lane: int = 0,
        vehicle_type: str = TYPE_HUMAN,
    ) -> Union[HumanVehicle, AutonomousVehicle]:
        """Add a vehicle. vehicle_type is 'human' or 'autonomous'. Returns the new vehicle."""
        if id is None:
            id = len(self.cars) + 1
        position = self.road.clamp(position)
        id = int(id)

        if vehicle_type == TYPE_AUTONOMOUS:
            car: Union[HumanVehicle, AutonomousVehicle] = AutonomousVehicle(
                position=position,
                velocity=velocity,
                acceleration=acceleration,
                id=id,
                length=length,
                lane=lane,
            )
        else:
            car = HumanVehicle(
                position=position,
                velocity=velocity,
                acceleration=acceleration,
                id=id,
                length=length,
                lane=lane,
                config=self.human_config,
            )
        self.cars.append(car)
        return car

    def get_car(self, id: int) -> Optional[Vehicle]:
        """Return the vehicle with the given id, or None."""
        for car in self.cars:
            if car.id == id:
                return car
        return None

    def step(self, dt: float, t: float = 0.0) -> bool:
        """
        Advance simulation by dt. Humans update_following (delayed reaction), then
        all vehicles step, remove any that reach the end of the road, then detect and resolve collisions.
        t: current simulation time (required for human reaction delay).
        Returns True if any overlap was detected (before resolution).
        """
        for car in self.cars:
            if hasattr(car, "update_following"):
                car.update_following(self.cars, t, dt)
        for car in self.cars:
            car.step(dt)
        # Remove cars when their rear (position - length) reaches the end of the road
        self.cars = [c for c in self.cars if c.position - c.length < self.road.length]
        for car in self.cars:
            # Allow position up to road.length + car.length so the car can drive off and be removed
            car.position = max(0.0, min(car.position, self.road.length + car.length))
        had_collision = self._detect_collision()
        self._resolve_collisions()
        return had_collision

    def _detect_collision(self) -> bool:
        """Return True if any two vehicles on the same lane overlap."""
        for i, a in enumerate(self.cars):
            for b in self.cars[i + 1 :]:
                if a.overlaps(b):
                    return True
        return False

    def _resolve_collisions(self) -> None:
        """Group cars by lane and run vehicle collision resolution for each lane."""
        by_lane = defaultdict(list)
        for car in self.cars:
            by_lane[car.lane].append(car)
        for lane_cars in by_lane.values():
            lane_cars.sort(key=lambda c: c.position)
            Vehicle.resolve_collisions_in_lane(lane_cars, self.road)
