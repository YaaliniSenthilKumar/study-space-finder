"""Study Space Finder: shows which Purdue study spaces are Quiet, Filling up, or Full."""
from data import load_spaces, load_readings, spaces_with_status


def main():
    spaces = load_spaces()
    readings = load_readings()
    items = spaces_with_status(spaces, readings)

    print("Study spaces right now:")
    for item in items:
        print(
            f"- {item['name']} ({item['building']}): "
            f"{item['status']} ({item['count']}/{item['capacity']})"
        )


if __name__ == "__main__":
    main()
