from simulation.cars.human_car import HumanCar
from simulation.cars.autonomous_car import AutonomousCar

# Lane 0 (human): two cars, no time headway (base Car behaviour)
human_lead = HumanCar(80, 0, speed=25, acceleration=0, max_speed=30)
human_follower = HumanCar(0, 0, speed=50, acceleration=8, max_speed=60)
# Lane 1 (autonomous): lead + follower with time headway (stops early)
autonomous_lead = AutonomousCar(
    90, 1, speed=25, acceleration=0, max_speed=30, time_headway=0
)
autonomous_follower = AutonomousCar(
    20, 1, speed=50, acceleration=6, max_speed=60, time_headway=0.2
)


def setup(sim, t):
    sim.road(length=200, lanes=2)
    if t < 0.05:
        sim.add_car(human_lead)
        sim.add_car(human_follower)
        sim.add_car(autonomous_lead)
        sim.add_car(autonomous_follower)


def reset():
    human_lead.position = 80
    human_lead.speed = 25
    human_follower.position = 0
    human_follower.speed = 50
    autonomous_lead.position = 90
    autonomous_lead.speed = 25
    autonomous_follower.position = 20
    autonomous_follower.speed = 50
