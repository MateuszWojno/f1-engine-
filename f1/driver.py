from abc import ABC, abstractmethod
import random

class Driver (ABC):

    def __init__(self, name, speed, skill, position, in_race):
        self.name = name
        self.speed = speed
        self.skill = skill
        self.points = 0
        self.team = None
        self.reset_race_state(position, in_race)

    def reset_race_state(self, position=0, in_race=True):
        self.tyre_fresh = 100
        self.fuel = 100
        self.position = position
        self.grid_position = position
        self.in_race = in_race
        self.performance = 0
        self.lap_time = 0
        self.total_time = 0
        self.completed_laps = 0
        self.gap = 0
        self.pit_stops = 0
        self.in_pit = False
        self.dnf = False
        self.dnf_reason = None

    @abstractmethod
    def act(self, circuit):
        pass

    def interact(self, other, circuit):

        defense = other.speed + other.skill + random.randint(1,10)
        attack = self.speed + self.skill + random.randint(1,10)
        attack -= (circuit.overtaking_difficulty - 0.5) * 12

        if random.random() < circuit.collision_risk:

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
        pit_speed = self.team.pit_speed if self.team else 0
        self.total_time += max(20, 25 - pit_speed)

        # nowe opony
        self.tyre_fresh = 100

    def retire(self, reason):
        self.in_race = False
        self.dnf = True
        self.dnf_reason = reason

    def crash(self):
        self.retire("Collision")

    def suffers_technical_failure(self, circuit):
        if not self.team:
            return False

        failure_risk = (1 - self.team.reliability) / circuit.total_laps
        if random.random() < failure_risk:
            self.retire("Technical failure")
            return True

        return False

    def calculate_base_performance(self):
        team_strength = self.team.strength if self.team else 80
        return self.speed * 0.4 + self.skill * 0.4 + team_strength * 0.2



class AggressiveDriver(Driver):

    def act(self, circuit):

        if not self.in_race:
            return

        self.fuel -= circuit.fuel_consumption * random.uniform(1.05, 1.15)
        self.tyre_fresh -= circuit.tyre_wear * random.randint(3, 7)

        # zabezpieczenia
        self.fuel = max(self.fuel, 0)
        self.tyre_fresh = max(self.tyre_fresh, 0)

        if self.tyre_fresh <= 30:
            self.pit_stop()

        # 🔥 straty
        fuel_penalty = self.fuel * 0.02
        tyre_loss = 100 - self.tyre_fresh

        self.performance = (
            self.calculate_base_performance() -
            fuel_penalty -
            tyre_loss * 0.4 +
            random.uniform(-1, 1)
        )

        self.lap_time = circuit.base_lap_time - self.performance * 0.03

        # DNF
        if self.fuel <= 0 or self.tyre_fresh <= 0:
            reason = "Out of fuel" if self.fuel <= 0 else "Tyre failure"
            self.retire(reason)
            self.performance -= 1000

class ConservativeDriver(Driver):

    def act(self, circuit):

        if not self.in_race:
            return

        self.fuel -= circuit.fuel_consumption * random.uniform(0.90, 0.98)
        self.tyre_fresh -= circuit.tyre_wear * random.randint(2, 5)

        self.fuel = max(self.fuel, 0)
        self.tyre_fresh = max(self.tyre_fresh, 0)

        if self.tyre_fresh <= 20:
            self.pit_stop()

        fuel_penalty = self.fuel * 0.02
        tyre_loss = 100 - self.tyre_fresh

        self.performance = (
                self.calculate_base_performance() -
                fuel_penalty -
                tyre_loss * 0.4 +
                random.uniform(-1, 1)
        )

        self.lap_time = circuit.base_lap_time - self.performance * 0.03

        if self.fuel <= 0 or self.tyre_fresh <= 0:
            reason = "Out of fuel" if self.fuel <= 0 else "Tyre failure"
            self.retire(reason)
            self.performance -= 1000

class BalancedDriver(Driver):

    def act(self, circuit):

        if not self.in_race:
            return

        self.fuel -= circuit.fuel_consumption * random.uniform(0.98, 1.05)
        self.tyre_fresh -= circuit.tyre_wear * random.randint(2, 6)

        self.fuel = max(self.fuel, 0)
        self.tyre_fresh = max(self.tyre_fresh, 0)

        if self.tyre_fresh <= 25:
            self.pit_stop()

        fuel_penalty = self.fuel * 0.02
        tyre_loss = 100 - self.tyre_fresh

        self.performance = (
                self.calculate_base_performance() -
                 fuel_penalty -
                tyre_loss * 0.4 +
                random.uniform(-1, 1)
        )

        self.lap_time = circuit.base_lap_time - self.performance * 0.03

        if self.fuel <= 0 or self.tyre_fresh <= 0:
            reason = "Out of fuel" if self.fuel <= 0 else "Tyre failure"
            self.retire(reason)
            self.performance -= 1000
