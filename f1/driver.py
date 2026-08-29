from abc import ABC, abstractmethod
import random

class Driver (ABC):

    def __init__(self, name, speed, skill, position, in_race):
        self.name = name
        self.speed = speed
        self.skill = skill
        self.tyre_fresh = 100
        self.fuel = 100
        self.position = position
        self.in_race = in_race
        self.performance = 0
        self.lap_time = 0
        self.total_time = 0
        self.gap = 0
        self.pit_stops = 0
        self.in_pit = False
        self.dnf = False
        self.team = None

    @abstractmethod
    def act(self):
        pass

    def interact(self, other):

        defense = other.speed + other.skill + random.randint(1,10)
        attack = self.speed + self.skill + random.randint(1,10)

        if random.random() < 0.01:

            collision_type = random.random()

            # mały kontakt
            if collision_type < 0.7:
                self.total_time += 3
                other.total_time += 3

            # większy kontakt
            elif collision_type < 0.95:
                self.total_time += 10
                other.total_time += 5

            # duży dzwon
            else:
                self.crash()
                other.crash()

            return False

        if attack > defense:
            return True

        return False


    def pit_stop(self):
        self.pit_stops += 1

        # strata czasu na alei serwisowej
        self.total_time += 25

        # nowe opony
        self.tyre_fresh = 100

    def crash(self):
        self.in_race = False
        self.dnf = True



class AggressiveDriver(Driver):

    def act(self):

        if not self.in_race:
            return

        self.fuel -= random.randint(2, 4)
        self.tyre_fresh -= random.randint(3, 7)

        # zabezpieczenia
        self.fuel = max(self.fuel, 0)
        self.tyre_fresh = max(self.tyre_fresh, 0)

        if self.tyre_fresh <= 30:
            self.pit_stop()

        # 🔥 straty
        fuel_loss = 100 - self.fuel
        tyre_loss = 100 - self.tyre_fresh

        self.performance = (
            self.speed * 0.5 +
            self.skill * 0.5 -
            fuel_loss * 0.2 -
            tyre_loss * 0.4 +
            random.uniform(-1, 1)
        )

        self.lap_time = 120 - self.performance * 0.1

        # DNF
        if self.fuel <= 0 or self.tyre_fresh <= 0:
            self.in_race = False
            self.dnf = True
            self.performance -= 1000

class ConservativeDriver(Driver):

    def act(self):

        if not self.in_race:
            return

        self.fuel -= random.randint(1, 2)
        self.tyre_fresh -= random.randint(2, 5)

        self.fuel = max(self.fuel, 0)
        self.tyre_fresh = max(self.tyre_fresh, 0)

        if self.tyre_fresh <= 20:
            self.pit_stop()

        fuel_loss = 100 - self.fuel
        tyre_loss = 100 - self.tyre_fresh

        self.performance = (
                self.speed * 0.5 +
                self.skill * 0.5 -
                fuel_loss * 0.2 -
                tyre_loss * 0.4 +
                random.uniform(-1, 1)
        )

        self.lap_time = 120 - self.performance * 0.1

        if self.fuel <= 0 or self.tyre_fresh <= 0:
            self.in_race = False
            self.dnf = True
            self.performance -= 1000

class BalancedDriver(Driver):

    def act(self):

        if not self.in_race:
            return

        self.fuel -= random.randint(2, 3)
        self.tyre_fresh -= random.randint(2, 6)

        self.fuel = max(self.fuel, 0)
        self.tyre_fresh = max(self.tyre_fresh, 0)

        if self.tyre_fresh <= 25:
            self.pit_stop()

        fuel_loss = 100 - self.fuel
        tyre_loss = 100 - self.tyre_fresh

        self.performance = (
                self.speed * 0.5 +
                self.skill * 0.5 -
                 fuel_loss * 0.2 -
                tyre_loss * 0.4 +
                random.uniform(-1, 1)
        )

        self.lap_time = 120 - self.performance * 0.1

        if self.fuel <= 0 or self.tyre_fresh <= 0:
            self.in_race = False
            self.dnf = True
            self.performance -= 1000
