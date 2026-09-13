import random


class Qualifying:
    def __init__(self, drivers, circuit):
        self.drivers = drivers
        self.circuit = circuit
        self.results = []

    def run(self):
        scored_drivers = [
            (
                driver.calculate_base_performance(self.circuit)
                + random.uniform(-2, 2),
                driver,
            )
            for driver in self.drivers
        ]
        scored_drivers.sort(key=lambda entry: entry[0], reverse=True)

        self.results = [driver for _, driver in scored_drivers]
        for position, driver in enumerate(self.results, start=1):
            driver.grid_position = position
            driver.position = position
            driver.total_time = (position - 1) * 0.12

        return self.results
