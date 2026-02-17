import config


class Car:
    def __init__(self, initial_position, lane, speed=80.0, color=0, length=None):
        self.position = initial_position
        self.lane = lane
        self.speed = speed
        self.color = color
        self.length = length if length is not None else config.CAR_LENGTH_UNITS

    @property
    def back(self):
        return self.position - self.length / 2

    @property
    def front(self):
        return self.position + self.length / 2

    def update(self, dt, road_length, others=None):
        others = others or []
        new_pos = self.position + self.speed * dt
        max_pos = road_length - self.length / 2
        for other in others:
            if other is self or other.lane != self.lane:
                continue
            if other.position > self.position:
                max_pos = min(max_pos, other.back - self.length / 2)
        self.position = min(max_pos, new_pos)


def collides(car1, car2):
    if car1.lane != car2.lane:
        return False
    return not (car1.front <= car2.back or car2.front <= car1.back)
