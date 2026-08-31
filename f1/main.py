from copy import deepcopy

from f1.calendar_2026 import F1_2026_CALENDAR
from f1.driver import AggressiveDriver, BalancedDriver, ConservativeDriver
from f1.season import Season
from f1.team import Team


mercedes = Team("Mercedes", strength=97, pit_speed=3)
ferrari = Team("Ferrari", strength=94, pit_speed=3)
mclaren = Team("McLaren", strength=92, pit_speed=3)
red_bull = Team("Red Bull Racing", strength=89, pit_speed=3)
racing_bulls = Team("Racing Bulls", strength=82, pit_speed=2)
alpine = Team("Alpine", strength=81, pit_speed=2)
haas = Team("Haas", strength=77, pit_speed=2)
audi = Team("Audi", strength=75, pit_speed=2)
williams = Team("Williams", strength=74, pit_speed=2)
aston_martin = Team("Aston Martin", strength=73, pit_speed=2)
cadillac = Team("Cadillac", strength=70, pit_speed=1)


def assign_to_team(driver, team):
    driver.team = team
    return driver


driver_templates = [
    # Mercedes
    assign_to_team(BalancedDriver("Russell", 95, 96, 0, True), mercedes),
    assign_to_team(AggressiveDriver("Antonelli", 97, 94, 0, True), mercedes),

    # Ferrari
    assign_to_team(AggressiveDriver("Leclerc", 96, 96, 0, True), ferrari),
    assign_to_team(BalancedDriver("Hamilton", 94, 98, 0, True), ferrari),

    # McLaren
    assign_to_team(BalancedDriver("Norris", 96, 95, 0, True), mclaren),
    assign_to_team(BalancedDriver("Piastri", 94, 94, 0, True), mclaren),

    # Red Bull Racing
    assign_to_team(AggressiveDriver("Verstappen", 98, 99, 0, True), red_bull),
    assign_to_team(AggressiveDriver("Hadjar", 91, 88, 0, True), red_bull),

    # Racing Bulls
    assign_to_team(AggressiveDriver("Lawson", 87, 86, 0, True), racing_bulls),
    assign_to_team(AggressiveDriver("Lindblad", 85, 82, 0, True), racing_bulls),

    # Alpine
    assign_to_team(BalancedDriver("Gasly", 89, 91, 0, True), alpine),
    assign_to_team(AggressiveDriver("Colapinto", 86, 84, 0, True), alpine),

    # Haas
    assign_to_team(BalancedDriver("Ocon", 86, 89, 0, True), haas),
    assign_to_team(AggressiveDriver("Bearman", 87, 86, 0, True), haas),

    # Audi
    assign_to_team(ConservativeDriver("Hulkenberg", 86, 92, 0, True), audi),
    assign_to_team(BalancedDriver("Bortoleto", 86, 85, 0, True), audi),

    # Williams
    assign_to_team(BalancedDriver("Sainz", 91, 94, 0, True), williams),
    assign_to_team(BalancedDriver("Albon", 89, 91, 0, True), williams),

    # Aston Martin
    assign_to_team(ConservativeDriver("Alonso", 90, 99, 0, True), aston_martin),
    assign_to_team(ConservativeDriver("Stroll", 83, 84, 0, True), aston_martin),

    # Cadillac
    assign_to_team(ConservativeDriver("Perez", 85, 92, 0, True), cadillac),
    assign_to_team(ConservativeDriver("Bottas", 87, 94, 0, True), cadillac),
]


def create_drivers():
    return deepcopy(driver_templates)


def main():
    season = Season(create_drivers(), F1_2026_CALENDAR, seed=2026)
    season.run()

    print("\n=== RACE SUMMARIES ===")
    sprint_results = iter(season.sprints)
    for race in season.races:
        pole_sitter = race.starting_grid[0].name
        podium = ", ".join(driver.name for driver in race.finishers[:3])
        dnf_count = sum(driver.dnf for driver in race.results)

        if not podium:
            podium = "No classified finishers"

        print(
            f"{race.circuit.name} | Pole: {pole_sitter} | "
            f"Podium: {podium} | DNF: {dnf_count}"
        )

        if race.circuit.has_sprint:
            sprint = next(sprint_results)
            sprint_winner = (
                sprint.finishers[0].name
                if sprint.finishers
                else "No classified finishers"
            )
            print(f"  Sprint winner: {sprint_winner}")

    print("\n=== DRIVERS' CHAMPIONSHIP ===")
    for position, driver in enumerate(season.driver_standings(), start=1):
        print(f"P{position} - {driver.name}: {driver.points} pts")

    print("\n=== CONSTRUCTORS' CHAMPIONSHIP ===")
    for position, team in enumerate(season.team_standings(), start=1):
        print(f"P{position} - {team.name}: {team.points} pts")


if __name__ == "__main__":
    main()
