class Team:
    def __init__(self, name, strength, pit_speed, power, aerodynamics):
        self.name = name
        self.strength = strength
        self.pit_speed = pit_speed
        self.power = power
        self.aerodynamics = aerodynamics
        self.reliability = min(0.97, 0.84 + strength * 0.0013)
        self.points = 0




