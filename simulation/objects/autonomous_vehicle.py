"""Autonomous vehicle (same physics as base Vehicle)."""

from .vehicle import Vehicle


class AutonomousVehicle(Vehicle):
    """Autonomous vehicle. Same physics as base Vehicle; used for scenario labelling and visualizer filtering."""

    VEHICLE_KIND = "autonomous"
