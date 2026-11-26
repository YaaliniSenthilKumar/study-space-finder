# Study Space Finder

A small Python command-line tool that helps Purdue students see which library
and study spaces are Quiet, Filling up, or Full, using anonymized (mock)
occupancy counts.

CS final project. Work in progress.

## How to run

```
python3 -m venv .venv
source .venv/bin/activate
python seed.py     # makes fake data in readings.csv
python main.py
```

## Privacy

Only anonymous occupancy counts are stored, never information about individual students.
