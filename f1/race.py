from f1.logger import RaceLogger


class Race:
    def __init__(self, drivers, total_laps, logger=None):
        self.drivers = drivers
        self.total_laps = total_laps
        self.current_lap = 0
        self.finished = False
        self.logger = logger or RaceLogger()

    def step(self):
        if self.finished:
            return

        self.current_lap += 1

        for driver in self.drivers:
            if driver.in_race:
                driver.act()
                driver.total_time += driver.lap_time

        active = [d for d in self.drivers if d.in_race]

        if not active:
            self.finished = True
            self.logger.save_lap(self.current_lap, self.drivers)
            return

        ranking = sorted(active, key=lambda d: d.total_time)

        i = len(ranking) - 1
        while i > 0:
            attacker = ranking[i]
            defender = ranking[i - 1]

            if attacker.interact(defender):
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
            self.logger.save_lap(self.current_lap, self.drivers)
            return

        leader_time = ranking[0].total_time

        for p, driver in enumerate(ranking, start=1):
            driver.position = p
            driver.gap = driver.total_time - leader_time



        if self.current_lap >= self.total_laps:
            self.finished = True

        self.logger.save_lap(self.current_lap, self.drivers)

    def run(self):

        while not self.finished:
            self.step()

            print("================================")
            print(f"Lap {self.current_lap}/{self.total_laps}")

            for driver in self.drivers:
                if not driver.in_race:
                    continue

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
                    print(f"DNF - {d.name}")


