from simulation.cars.human_car import HumanCar
from simulation.cars.autonomous_car import AutonomousCar

human_1 = HumanCar(0, 0, speed=40, acceleration=5, max_speed=60)
autonomous_1 = AutonomousCar(50, 1, speed=30, acceleration=0, max_speed=50)


def setup(sim, t):
    sim.road(length=200, lanes=2)
    if t < 0.05:
        sim.add_car(human_1)
        sim.add_car(autonomous_1)


def reset():
    human_1.position = 0
    human_1.speed = 40
    autonomous_1.position = 50
    autonomous_1.speed = 30
