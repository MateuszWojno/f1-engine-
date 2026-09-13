# F1 2026 Season Simulation Engine

Object-oriented Python simulation of a complete Formula 1 season. The engine models qualifying, sprint weekends, race events and championship standings while accounting for driver ability, team performance and circuit characteristics.

The project is designed as a portfolio application for exploring simulation logic, data modelling and season-level performance analysis.

## Highlights

- Simulates a 23-round F1 2026-inspired calendar with six sprint weekends.
- Includes 22 drivers across 11 teams, each with individual driver and car-performance attributes.
- Models driver speed and skill, team power and aerodynamics, pit-stop speed and reliability.
- Uses circuit-specific lap counts, base lap times, fuel consumption, tyre wear, overtaking difficulty, collision risk and power demand.
- Runs qualifying before each event and uses the result to build the starting grid.
- Simulates overtakes, collisions, technical failures, tyre degradation, pit stops, DNFs and dynamic track positions.
- Awards Grand Prix and sprint points, then produces drivers' and constructors' championships.
- Reports poles, podiums, fastest laps, DNFs, sprint winners, wins and podium totals.
- Writes lap-by-lap data to a CSV file for further analysis.

## Tech stack

- Python 3
- Object-oriented programming
- Python standard library: `dataclasses`, `random`, `csv`, `copy`
- Git and GitHub

No third-party packages are required.

## Run locally

```bash
git clone https://github.com/MateuszWojno/f1-engine-.git
cd f1-engine-
python -m f1
```

On Windows, use the interpreter from the active virtual environment if you have one:

```powershell
.venv\Scripts\python.exe -m f1
```

Each execution produces a different season because the default simulation is random.

## Example output

```text
=== RACE SUMMARIES ===
Chinese Grand Prix | Pole: Russell | Podium: Verstappen, Leclerc, Norris | Fastest: Verstappen (78.42s) | DNF: 2
  Sprint winner: Piastri

=== DRIVERS' CHAMPIONSHIP ===
P1 - Verstappen: 312 pts | Wins: 6 | Podiums: 14

=== CONSTRUCTORS' CHAMPIONSHIP ===
P1 - Mercedes: 489 pts
```

The values above are illustrative; simulation output varies from run to run.

## Simulation model

### Drivers and teams

Each driver has `speed`, `skill` and a driving style:

- `AggressiveDriver` pushes harder, which can increase tyre wear and fuel use.
- `BalancedDriver` provides a middle ground between pace and conservation.
- `ConservativeDriver` preserves tyres and fuel more effectively.

Teams contribute `power`, `aerodynamics`, `pit_speed` and reliability. A car's effective performance changes by circuit: power has a larger impact on high-speed tracks, while aerodynamics matters more on technical circuits.

### Race weekends

For each round, the engine:

1. Runs qualifying and assigns a starting grid.
2. Runs a sprint event when the circuit is marked as a sprint weekend.
3. Simulates the Grand Prix lap by lap.
4. Awards points and updates both championships.
5. Stores race summaries and detailed lap data.

Sprint races use the top-eight scoring system: `8, 7, 6, 5, 4, 3, 2, 1`. Grand Prix races use the top-ten scoring system: `25, 18, 15, 12, 10, 8, 6, 4, 2, 1`.

### Reliability and incidents

Technical failures are based on team reliability and race distance. On-track interactions can lead to time losses, collisions or retirements. Retired drivers are classified by completed race distance.

## CSV race log

Running the application creates or appends to `race_log_2026.csv` in the working directory. It records each driver's state after every lap:

```text
circuit, lap, name, position, total_time, gap, tyre, fuel, dnf, dnf_reason, completed_laps, pit_stops
```

This file can be imported into Excel, Power BI or pandas for analysis and visualisation.

## Project structure

```text
f1-engine-
├── f1/
│   ├── __main__.py          # Application entry point
│   ├── main.py              # Teams, drivers and console output
│   ├── season.py            # Season orchestration and standings
│   ├── race.py              # Race loop, results and points
│   ├── qualifying.py        # Qualifying and grid generation
│   ├── driver.py            # Driver behaviours and race actions
│   ├── team.py              # Team performance attributes
│   ├── circuit.py           # Circuit data model
│   ├── calendar_2026.py     # Season calendar
│   └── logger.py            # CSV lap logger
└── README.md
```

## Reproducible simulations

`Season` accepts an optional seed when you need to reproduce a specific run:

```python
season = Season(create_drivers(), F1_2026_CALENDAR, seed=2026)
season.run()
```

## Future improvements

- Weather conditions and tyre-compound strategy
- Safety cars, virtual safety cars and red flags
- Automated tests for race, points and standings logic
- Charts and a dashboard built from the CSV race log
- Command-line options for seed selection and output paths

## Disclaimer

This is an educational simulation. Driver ratings, team ratings and circuit parameters are modelling assumptions, not official Formula 1 performance data.
