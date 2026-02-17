from simulation.cars.car import Car


class HumanCar(Car):
    def __init__(self, *args, color=1, **kwargs):
        super().__init__(*args, color=color, **kwargs)
