"""Human-driven vehicle (same physics as base Vehicle)."""

from .vehicle import Vehicle


class HumanVehicle(Vehicle):
    """Human-driven vehicle. Same physics as base Vehicle; used for scenario labelling and visualizer filtering."""

    VEHICLE_KIND = "human"
