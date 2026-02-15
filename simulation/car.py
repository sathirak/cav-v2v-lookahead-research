"""A car: position, velocity, and acceleration on a 1D road."""


class Car:
    def __init__(
        self, position=0.0, velocity=0.0, acceleration=0.0, id=None, length=50.0, lane=0
    ):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.id = id
        self.length = length  # metres, for collision
        self.lane = lane  # which lane (0, 1, ...); other lanes reserved for other stuff

    def step(self, dt):
        """Move the car forward by dt seconds."""
        self.position += self.velocity * dt + 0.5 * self.acceleration * dt * dt
        self.velocity = max(0, self.velocity + self.acceleration * dt)
