"""Seed script: makes fake (mock) occupancy counts and saves them to readings.csv.

Only anonymous counts are stored, never anything about individual students.
Run it once before main.py:  python seed.py
"""
import csv
import json
import random
from datetime import datetime, timedelta

DAYS = 14          # how many days of fake history to make
FIRST_HOUR = 0     # readings cover the whole day, 12 AM
LAST_HOUR = 23     # up to 11 PM


def busy_fraction(hour, weekday):
    """Return how full a space usually is (0.0 to 1.0) at this hour.

    weekday is 0 for Monday up to 6 for Sunday.
    """
    if hour < 6:
        base = 0.03    # overnight: almost empty
    elif hour < 8:
        base = 0.10
    elif hour < 10:
        base = 0.25
    elif hour < 12:
        base = 0.50
    elif hour < 17:
        base = 1.00    # 12 PM to 5 PM is the busiest time
    elif hour < 20:
        base = 0.65
    elif hour < 23:
        base = 0.40
    else:
        base = 0.12
    if weekday >= 5:   # Saturday and Sunday are quieter
        base *= 0.6
    return base


def make_readings(spaces, days=DAYS):
    """Build a list of readings: [space name, count, timestamp]."""
    # Each space gets its own popularity, so some rooms are always busier.
    # Seeding with the name means a room keeps the same popularity every run.
    popularity = {
        space["name"]: random.Random(space["name"]).uniform(0.6, 1.1)
        for space in spaces
    }

    readings = []
    today = datetime.now().replace(minute=0, second=0, microsecond=0)
    for day_back in range(days, 0, -1):
        day = today - timedelta(days=day_back)
        for hour in range(FIRST_HOUR, LAST_HOUR + 1):
            stamp = day.replace(hour=hour)
            for space in spaces:
                fraction = busy_fraction(hour, stamp.weekday())
                fraction *= popularity[space["name"]]
                fraction *= random.uniform(0.8, 1.2)   # a little randomness
                fraction = max(0.0, min(1.0, fraction))
                count = round(space["capacity"] * fraction)
                readings.append([space["name"], count, stamp.isoformat()])
    return readings


def main():
    with open("spaces.json") as f:
        spaces = json.load(f)

    readings = make_readings(spaces)

    with open("readings.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["space", "count", "timestamp"])
        writer.writerows(readings)

    print(f"Wrote {len(readings)} readings for {len(spaces)} spaces to readings.csv")


if __name__ == "__main__":
    main()
