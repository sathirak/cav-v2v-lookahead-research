from simulation.car import Car

# Same lane: fast car behind will catch and collide with slow car ahead
lead_car = Car(60, 0, speed=25, color=0)
chase_car = Car(0, 0, speed=80, color=2)


def setup(sim, t):
    sim.road(length=200, lanes=2)
    if t < 0.05:
        sim.add_car(lead_car)
        sim.add_car(chase_car)


def reset():
    lead_car.position = 60
    chase_car.position = 0
