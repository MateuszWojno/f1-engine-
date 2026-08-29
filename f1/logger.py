import csv
import os


class RaceLogger:

    def __init__(self, filename="race_log.csv"):
        self.filename = filename
        self.file_exists = os.path.isfile(self.filename)

    def save_lap(self, lap, drivers):

        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)


            if not self.file_exists:
                writer.writerow([
                    "lap",
                    "name",
                    "position",
                    "total_time",
                    "gap",
                    "tyre",
                    "fuel",
                    "dnf",
                    "pit_stops"
                ])
                self.file_exists = True

            for d in drivers:
                writer.writerow([
                    lap,
                    d.name,
                    d.position,
                    round(d.total_time, 3),
                    round(d.gap, 3),
                    d.tyre_fresh,
                    d.fuel,
                    d.dnf,
                    d.pit_stops
                ])