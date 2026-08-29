from dataclasses import dataclass


@dataclass(frozen=True)
class Circuit:
    name: str
    total_laps: int
    base_lap_time: float
