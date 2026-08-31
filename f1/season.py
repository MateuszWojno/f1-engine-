import random
from dataclasses import replace

from f1.race import F1_POINTS, Race


SPRINT_POINTS = (8, 7, 6, 5, 4, 3, 2, 1)


class Season:
    def __init__(self, drivers, calendar, seed=None):
        self.drivers = drivers
        self.calendar = tuple(calendar)
        self.seed = seed
        self.races = []
        self.sprints = []

    def run(self):
        if self.seed is not None:
            random.seed(self.seed)

        for circuit in self.calendar:
            if circuit.has_sprint:
                sprint_circuit = replace(
                    circuit,
                    name=f"{circuit.name} Sprint",
                    total_laps=max(1, round(circuit.total_laps / 3)),
                    has_sprint=False,
                )
                self.sprints.append(self.run_event(sprint_circuit, SPRINT_POINTS))

            self.races.append(self.run_event(circuit))

        return self.driver_standings()

    def run_event(self, circuit, points=None):
        for driver in self.drivers:
            driver.reset_race_state()

        race = Race(self.drivers, circuit, points=points or F1_POINTS)
        while not race.finished:
            race.step()

        return race

    def driver_standings(self):
        return sorted(self.drivers, key=lambda driver: driver.points, reverse=True)

    def team_standings(self):
        teams = {
            driver.team.name: driver.team
            for driver in self.drivers
            if driver.team
        }
        return sorted(teams.values(), key=lambda team: team.points, reverse=True)
