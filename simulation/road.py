"""A straight road from 0 to length."""


class Road:
    def __init__(self, length):
        self.length = length

    def clamp(self, position):
        """Keep position between 0 and road length."""
        return max(0, min(self.length, position))
