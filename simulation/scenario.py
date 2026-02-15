"""Scenario setup: create specific simulation configurations."""

from simulation.engine import CarsOnRoad


def make_simulation(road_length=1000):
    """Five cars in traffic; all start at same speed. Head car brakes later via update_controls."""
    sim = CarsOnRoad(road_length)

    # 5 cars, 20 m/s, 60m apart (10m gap). All same behaviour at start.
    sim.add_car(position=0, velocity=20, acceleration=0, id="car_1", lane=0)
    sim.add_car(position=60, velocity=20, acceleration=0, id="car_2", lane=0)
    sim.add_car(position=120, velocity=20, acceleration=0, id="car_3", lane=0)
    sim.add_car(position=180, velocity=20, acceleration=0, id="car_4", lane=0)
    sim.add_car(position=240, velocity=20, acceleration=0, id="car_5", lane=0)

    return sim


def update_controls(sim, t):
    """Called every step. Make head car brake hard after t >= 2 s."""
    if t >= 8.0:
        head = sim.get_car("car_5")
        if head is not None:
            head.acceleration = -8
