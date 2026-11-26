"""Seed script: makes fake (mock) occupancy counts and saves them to readings.csv.

Only anonymous counts are stored, never anything about individual students.
Run it once before main.py:  python seed.py
"""
import csv
import json
import random
from datetime import datetime, timedelta

DAYS = 14          # how many days of fake history to make
START_HOUR = 8     # first reading of the day (8 AM)
END_HOUR = 23      # last reading of the day (11 PM)


def busy_fraction(hour, weekday):
    """Return how full a space usually is (0.0 to 1.0) at this hour."""
    if hour < 10:
        base = 0.15
    elif hour < 12:
        base = 0.45
    elif hour < 17:
        base = 0.75    # afternoons are busiest
    elif hour < 20:
        base = 0.55
    else:
        base = 0.35
    if weekday >= 5:   # Saturday and Sunday are quieter
        base *= 0.6
    return base


def make_readings(spaces, days=DAYS):
    """Build a list of readings: [space name, count, timestamp]."""
    readings = []
    today = datetime.now().replace(minute=0, second=0, microsecond=0)
    for day_back in range(days, 0, -1):
        day = today - timedelta(days=day_back)
        for hour in range(START_HOUR, END_HOUR + 1):
            stamp = day.replace(hour=hour)
            for space in spaces:
                fraction = busy_fraction(hour, stamp.weekday())
                fraction += random.uniform(-0.15, 0.15)   # a little randomness
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
