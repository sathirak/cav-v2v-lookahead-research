"""Cars on a road: add cars, step the simulation."""

import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from simulation.car import Car
from simulation.road import Road


class CarsOnRoad:
    def __init__(self, road_length):
        self.road = Road(road_length)
        self.cars = []

    def add_car(self, position=0, velocity=0, acceleration=0, id=None):
        car = Car(
            position=self.road.clamp(position),
            velocity=velocity,
            acceleration=acceleration,
            id=id or "car_%d" % len(self.cars),
        )
        self.cars.append(car)
        return car

    def step(self, dt):
        for car in self.cars:
            car.step(dt)
            car.position = self.road.clamp(car.position)


def main():
    sim = CarsOnRoad(road_length=1000)

    sim.add_car(position=0, velocity=10, acceleration=1, id="car_1")
    sim.add_car(position=100, velocity=5, acceleration=0.5, id="car_2")
    sim.add_car(position=500, velocity=20, acceleration=-0.2, id="car_3")

    print("Initial:", [(c.id, c.position, c.velocity) for c in sim.cars])

    for i in range(1, 4):
        sim.step(dt=1)
        print("After %ds:" % i, [(c.id, c.position, c.velocity) for c in sim.cars])


if __name__ == "__main__":
    main()
