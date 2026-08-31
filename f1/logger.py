import csv
import os


class RaceLogger:

    def __init__(self, filename="race_log_2026.csv"):
        self.filename = filename
        self.file_exists = os.path.isfile(self.filename)

    def save_lap(self, circuit, lap, drivers):

        with open(self.filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)


            if not self.file_exists:
                writer.writerow([
                    "circuit",
                    "lap",
                    "name",
                    "position",
                    "total_time",
                    "gap",
                    "tyre",
                    "fuel",
                    "dnf",
                    "dnf_reason",
                    "completed_laps",
                    "pit_stops"
                ])
                self.file_exists = True

            for d in drivers:
                writer.writerow([
                    circuit.name,
                    lap,
                    d.name,
                    d.position,
                    round(d.total_time, 3),
                    round(d.gap, 3),
                    d.tyre_fresh,
                    d.fuel,
                    d.dnf,
                    d.dnf_reason,
                    d.completed_laps,
                    d.pit_stops
                ])
