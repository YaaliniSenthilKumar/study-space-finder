"""Loads the data files and works out the current status of every study space."""
import csv
import json

from status import get_status


def load_spaces(path="spaces.json"):
    """Read the list of study spaces from a JSON file."""
    with open(path) as f:
        return json.load(f)


def load_readings(path="readings.csv"):
    """Read the occupancy readings from a CSV file.

    Returns a list of dictionaries with the keys: space, count, timestamp.
    """
    readings = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            readings.append(
                {
                    "space": row["space"],
                    "count": int(row["count"]),
                    "timestamp": row["timestamp"],
                }
            )
    return readings


def latest_counts(readings):
    """Return the most recent count for each space, as {space name: count}."""
    latest = {}   # space name -> (timestamp, count)
    for reading in readings:
        name = reading["space"]
        if name not in latest or reading["timestamp"] > latest[name][0]:
            latest[name] = (reading["timestamp"], reading["count"])
    return {name: count for name, (stamp, count) in latest.items()}


def spaces_with_status(spaces, readings):
    """Combine the spaces and their latest counts into one list.

    Each item has: name, building, capacity, noise_level, count, status.
    """
    counts = latest_counts(readings)
    result = []
    for space in spaces:
        count = counts.get(space["name"], 0)
        item = dict(space)
        item["count"] = count
        item["status"] = get_status(count, space["capacity"])
        result.append(item)
    return result
