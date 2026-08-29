from f1.team import Team
from f1.driver import AggressiveDriver
from f1.driver import ConservativeDriver
from f1.driver import BalancedDriver
from f1.race import Race

red_bull = Team("Red Bull", strength=95, pit_speed=2)
ferrari = Team("Ferrari", strength=92, pit_speed=1)
mercedes = Team("Mercedes", strength=90, pit_speed=1)
mclaren = Team("McLaren", strength=93, pit_speed=2)

# Red Bull
verstappen = AggressiveDriver("Verstappen", speed=97, skill=98, position=0, in_race=True)
verstappen.team = red_bull
tsunoda = AggressiveDriver("Tsunoda", speed=85, skill=84, position=0, in_race=True)

# Ferrari
leclerc = AggressiveDriver("Leclerc", speed=94, skill=93, position=0, in_race=True)
hamilton = BalancedDriver("Hamilton", speed=91, skill=96, position=0, in_race=True)

# McLaren
norris = BalancedDriver("Norris", speed=95, skill=93, position=0, in_race=True)
piastri = BalancedDriver("Piastri", speed=94, skill=91, position=0, in_race=True)

# Mercedes
russell = BalancedDriver("Russell", speed=92, skill=90, position=0, in_race=True)
antonelli = AggressiveDriver("Antonelli", speed=88, skill=85, position=0, in_race=True)

# Aston Martin
alonso = ConservativeDriver("Alonso", speed=89, skill=95, position=0, in_race=True)
stroll = ConservativeDriver("Stroll", speed=82, skill=80, position=0, in_race=True)

# Alpine
gasly = BalancedDriver("Gasly", speed=86, skill=86, position=0, in_race=True)
colapinto = AggressiveDriver("Colapinto", speed=84, skill=82, position=0, in_race=True)

# Haas
ocon = BalancedDriver("Ocon", speed=85, skill=85, position=0, in_race=True)
bearman = AggressiveDriver("Bearman", speed=86, skill=83, position=0, in_race=True)

# Racing Bulls
hadjar = AggressiveDriver("Hadjar", speed=87, skill=84, position=0, in_race=True)
lawson = AggressiveDriver("Lawson", speed=86, skill=84, position=0, in_race=True)

# Williams
albon = BalancedDriver("Albon", speed=89, skill=88, position=0, in_race=True)
sainz = AggressiveDriver("Sainz", speed=91, skill=90, position=0, in_race=True)

# Sauber
hulkenberg = ConservativeDriver("Hulkenberg", speed=84, skill=88, position=0, in_race=True)
bortoleto = AggressiveDriver("Bortoleto", speed=84, skill=81, position=0, in_race=True)

drivers = [
    verstappen, tsunoda,
    leclerc, hamilton,
    norris, piastri,
    russell, antonelli,
    alonso, stroll,
    gasly, colapinto,
    ocon, bearman,
    hadjar, lawson,
    albon, sainz,
    hulkenberg, bortoleto
]

def main():
    race = Race(drivers, total_laps=30)
    race.run()


if __name__ == "__main__":
    main()
