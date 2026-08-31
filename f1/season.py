from f1.race import Race


class Season:
    def __init__(self, drivers, calendar):
        self.drivers = drivers
        self.calendar = tuple(calendar)
        self.races = []

    def run(self):
        for circuit in self.calendar:
            for driver in self.drivers:
                driver.reset_race_state()

            race = Race(self.drivers, circuit)
            while not race.finished:
                race.step()

            self.races.append(race)

        return self.driver_standings()

    def driver_standings(self):
        return sorted(self.drivers, key=lambda driver: driver.points, reverse=True)

    def team_standings(self):
        teams = {
            driver.team.name: driver.team
            for driver in self.drivers
            if driver.team
        }
        return sorted(teams.values(), key=lambda team: team.points, reverse=True)
