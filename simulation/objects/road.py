"""Road model: a 1D segment from 0 to length (meters)."""


class Road:
    """A straight road segment. Positions are clamped to [0, length]."""

    def __init__(self, length: float) -> None:
        self.length = length

    def clamp(self, position: float) -> float:
        """Clamp position to the valid road interval [0, length]."""
        return max(0.0, min(self.length, position))
