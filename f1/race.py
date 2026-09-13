from f1.logger import RaceLogger
from f1.qualifying import Qualifying


F1_POINTS = (25, 18, 15, 12, 10, 8, 6, 4, 2, 1)


class Race:
    def __init__(self, drivers, circuit, logger=None, points=F1_POINTS):
        self.drivers = drivers
        self.circuit = circuit
        self.total_laps = circuit.total_laps
        self.current_lap = 0
        self.finished = False
        self.finishers = []
        self.results = []
        self.fastest_lap_driver = None
        self.fastest_lap_time = None
        self.points_system = points
        self.logger = logger or RaceLogger()
        self.qualifying = Qualifying(self.drivers, self.circuit)
        self.starting_grid = self.qualifying.run()

    def step(self):
        if self.finished:
            return

        self.current_lap += 1

        for driver in self.drivers:
            if driver.in_race:
                if driver.suffers_technical_failure(self.circuit):
                    continue

                driver.act(self.circuit)
                if driver.in_race:
                    driver.total_time += driver.lap_time
                    driver.completed_laps = self.current_lap
                    if (
                        self.fastest_lap_time is None
                        or driver.lap_time < self.fastest_lap_time
                    ):
                        self.fastest_lap_driver = driver
                        self.fastest_lap_time = driver.lap_time

        active = [d for d in self.drivers if d.in_race]

        if not active:
            self.finished = True
            self.record_results([])
            self.logger.save_lap(self.circuit, self.current_lap, self.drivers)
            return

        ranking = sorted(active, key=lambda d: d.total_time)

        i = len(ranking) - 1
        while i > 0:
            attacker = ranking[i]
            defender = ranking[i - 1]

            if attacker.interact(defender, self.circuit):
                attacker.total_time = defender.total_time - 0.001
                ranking[i], ranking[i - 1] = ranking[i - 1], ranking[i]
                i -= 1
            else:
                i -= 1

        ranking = sorted(
            (driver for driver in ranking if driver.in_race),
            key=lambda driver: driver.total_time,
        )

        if not ranking:
            self.finished = True
            self.record_results([])
            self.logger.save_lap(self.circuit, self.current_lap, self.drivers)
            return

        leader_time = ranking[0].total_time

        for p, driver in enumerate(ranking, start=1):
            driver.position = p
            driver.gap = driver.total_time - leader_time



        if self.current_lap >= self.total_laps:
            self.finished = True

            self.record_results(ranking)
            self.award_points()

        self.logger.save_lap(self.circuit, self.current_lap, self.drivers)

    def record_results(self, finishers):
        self.finishers = list(finishers)
        retired = sorted(
            (driver for driver in self.drivers if driver.dnf),
            key=lambda driver: (driver.completed_laps, -driver.total_time),
            reverse=True,
        )

        for position, driver in enumerate(retired, start=len(self.finishers) + 1):
            driver.position = position

        self.results = self.finishers + retired

    def award_points(self):
        for driver, points in zip(self.finishers, self.points_system):
            driver.points += points
            if driver.team:
                driver.team.points += points

    def run(self):

        while not self.finished:
            self.step()

            print("================================")
            print(
                f"{self.circuit.name} | "
                f"Lap {self.current_lap}/{self.total_laps}"
            )

            active_drivers = sorted(
                (driver for driver in self.drivers if driver.in_race),
                key=lambda driver: driver.position,
            )

            for driver in active_drivers:
                if driver.position == 1:
                    print(f"P1 - {driver.name} | Leader")
                else:
                    print(
                        f"P{driver.position} - "
                        f"{driver.name} | +{driver.gap:.2f}s"
                        f" | Pits: {driver.pit_stops}"
                    )

            print("\n=== DNF ===")
            for d in self.drivers:
                if not d.in_race:
                    print(f"DNF - {d.name} | {d.dnf_reason}")


