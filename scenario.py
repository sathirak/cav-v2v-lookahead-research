from simulation.cars.human_car import HumanCar

ROAD_LENGTH = 1000
NUM_CARS = 5
SPACING = 35
START = 50

# Lead car slows to trigger shockwave; followers react and slow in sequence
human_platoon = [
    HumanCar(
        START + i * SPACING,
        0,
        speed=45,
        acceleration=-2.2 if i == NUM_CARS - 1 else 0,
        max_speed=60,
        time_headway=0.2,
    )
    for i in range(NUM_CARS)
]


def setup(sim, t):
    sim.road(length=ROAD_LENGTH, lanes=1)
    if t < 0.05:
        for car in human_platoon:
            sim.add_car(car)


def reset():
    for i, car in enumerate(human_platoon):
        car.position = START + i * SPACING
        car.speed = 35
        car.acceleration = -1.2 if i == NUM_CARS - 1 else 0
