"""Study Space Finder: shows which Purdue study spaces are Quiet, Filling up, or Full."""
import json


def load_spaces(path="spaces.json"):
    """Read the list of study spaces from a JSON file."""
    with open(path) as f:
        return json.load(f)


def main():
    spaces = load_spaces()
    print("Study spaces:")
    for space in spaces:
        print(f"- {space['name']} ({space['building']})")


if __name__ == "__main__":
    main()
