"""Simulation engine: CarsOnRoad class."""

from simulation.car import Car
from simulation.road import Road


class CarsOnRoad:
    def __init__(self, road_length):
        self.road = Road(road_length)
        self.cars = []

    def add_car(
        self, position=0, velocity=0, acceleration=0.0, id=None, length=50, lane=0
    ):
        car = Car(
            position=self.road.clamp(position),
            velocity=velocity,
            acceleration=acceleration,
            id=id or "car_%d" % len(self.cars),
            length=length,
            lane=lane,
        )
        self.cars.append(car)
        return car

    def get_car(self, id):
        """Return the car with the given id, or None."""
        for car in self.cars:
            if car.id == id:
                return car
        return None

    def step(self, dt):
        for car in self.cars:
            car.step(dt)
            car.position = self.road.clamp(car.position)

    def check_collision(self):
        """True if any two cars in the same lane overlap (1D)."""
        for i, a in enumerate(self.cars):
            for b in self.cars[i + 1 :]:
                if a.lane != b.lane:
                    continue
                if (
                    a.position - a.length < b.position
                    and b.position - b.length < a.position
                ):
                    return True
        return False
