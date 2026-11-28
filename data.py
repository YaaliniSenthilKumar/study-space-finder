"""Loads the data files and works out the status of every study space."""
import csv
import json
from datetime import datetime
from statistics import mean

from status import get_status

DAY_NAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]


def hour_label(hour):
    """Turn an hour from 0 to 23 into text, like 13 into '1:00 PM'."""
    suffix = "AM" if hour < 12 else "PM"
    shown = hour % 12 or 12      # 0 and 12 both show as 12
    return f"{shown}:00 {suffix}"


def floor_number(floor):
    """Turn floor text into a number, like '2nd floor' into 2.

    The basement and the ground floor count as 0.
    """
    if floor[0].isdigit():
        return int(floor[0])
    return 0


def load_spaces(path="spaces.json"):
    """Read the list of study spaces from a JSON file."""
    with open(path) as f:
        return json.load(f)


def load_readings(path="readings.csv"):
    """Read the occupancy readings from a CSV file.

    Each reading is a dictionary with: space, count, timestamp, weekday
    (0 is Monday), and hour (0 to 23).
    """
    readings = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            stamp = datetime.fromisoformat(row["timestamp"])
            readings.append(
                {
                    "space": row["space"],
                    "count": int(row["count"]),
                    "timestamp": row["timestamp"],
                    "weekday": stamp.weekday(),
                    "hour": stamp.hour,
                }
            )
    return readings


def typical_counts(readings, weekday, hour):
    """Average count for each space at a given weekday and hour.

    Returns {space name: average count}. For example, the average number of
    people in each room on Fridays at 1 PM.
    """
    found = {}
    for reading in readings:
        if reading["weekday"] == weekday and reading["hour"] == hour:
            found.setdefault(reading["space"], []).append(reading["count"])
    return {name: round(mean(counts)) for name, counts in found.items()}


def filter_by_building(items, building):
    """Keep only the spaces in one building. 'All buildings' keeps everything."""
    if building == "All buildings":
        return list(items)
    return [item for item in items if item["building"] == building]


def rank_by_quietness(items):
    """Sort spaces from emptiest to fullest, compared to their size."""
    return sorted(items, key=lambda item: item["count"] / item["capacity"])


def quietest_space(items):
    """Return the space that is the emptiest compared to its size, or None."""
    ranked = rank_by_quietness(items)
    return ranked[0] if ranked else None


def best_summary_lines(items, when="right now"):
    """Write a short summary of the best space as a list of text lines.

    The first line is the heading. Returns an empty list if there are no spaces.
    'when' is text like 'on Friday at 1:00 PM'.
    """
    ranked = rank_by_quietness(items)
    if not ranked:
        return []
    best = ranked[0]

    # Overview of all the rooms being looked at.
    total = len(items)
    with_room = sum(1 for item in items if item["status"] != "Full")
    free_seats = sum(item["capacity"] - item["count"] for item in items)
    quiet = sum(1 for item in items if item["status"] == "Quiet")
    filling = sum(1 for item in items if item["status"] == "Filling up")
    full = sum(1 for item in items if item["status"] == "Full")

    # Details about the best space.
    percent_full = round(100 * best["count"] / best["capacity"])
    seats_free = best["capacity"] - best["count"]
    if best["computers"] > 0:
        computers = f"Computers: {best['computers']} in this room"
    else:
        computers = "Computers: none"
    features = ", ".join(best["features"]) if best["features"] else "none listed"

    lines = [
        f"Best {when}: {best['name']}",
        f"{best['building']}, {best['floor']}  |  Noise: {best['noise_level']}",
        f"Usually {best['count']} of {best['capacity']} people there "
        f"({percent_full}% full), {seats_free} seats free",
        computers,
        f"Features: {features}",
        f"Overall: {with_room} of {total} study rooms usually have space "
        f"({free_seats} free seats). {quiet} Quiet, {filling} Filling up, {full} Full.",
    ]
    if len(ranked) > 1:
        second = ranked[1]
        lines.append(
            f"Next best: {second['name']} ({second['count']}/{second['capacity']} people)"
        )
    return lines


def spaces_with_status(spaces, counts):
    """Combine the spaces and their counts into one list.

    counts is {space name: number of people}, such as from typical_counts().
    Each item has: name, building, floor, capacity, noise_level, computers,
    features, count, and status.
    """
    result = []
    for space in spaces:
        count = counts.get(space["name"], 0)
        item = dict(space)
        item["count"] = count
        item["status"] = get_status(count, space["capacity"])
        result.append(item)
    return result
