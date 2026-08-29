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

        # 1. nowy tick
        self.current_lap += 1

        # 2. każdy driver aktualizuje stan (paliwo, opony, performance)
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

        leader_time = ranking[0].total_time

        for driver in ranking:
            driver.gap = driver.total_time - leader_time

        # 4. wyprzedzanie (od tyłu, stabilnie)
        i = len(ranking) - 1
        while i > 0:
            attacker = ranking[i]
            defender = ranking[i - 1]

            # interakcja (czy wyprzedzenie się uda)
            if attacker.interact(defender):
                ranking[i], ranking[i - 1] = ranking[i - 1], ranking[i]
                i -= 1  # cofamy się po swapie
            else:
                i -= 1

        # 5. aktualizacja pozycji
        for p, driver in enumerate(ranking, start=1):
            driver.position = p

        # 6. zapis nowej kolejności jako “stan świata”


        # 7. zakończenie wyścigu
        if self.current_lap >= self.total_laps:
            self.finished = True

        self.logger.save_lap(self.current_lap, self.drivers)

    def run(self):

        while not self.finished:
            self.step()

            print("================================")
            print(f"Lap {self.current_lap}/{self.total_laps}")

            for driver in self.drivers:
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


