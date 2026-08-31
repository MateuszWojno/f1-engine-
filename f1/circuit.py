from dataclasses import dataclass


@dataclass(frozen=True)
class Circuit:
    name: str
    total_laps: int
    base_lap_time: float
    fuel_consumption: float
    tyre_wear: float
    overtaking_difficulty: float
    collision_risk: float
    has_sprint: bool = False
