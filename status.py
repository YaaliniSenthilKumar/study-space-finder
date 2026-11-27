"""Status logic: turns a headcount into Quiet, Filling up, or Full."""

QUIET_LIMIT = 0.50   # below 50% full is Quiet
FULL_LIMIT = 0.85    # above 85% full is Full


def get_status(count, capacity):
    """Return 'Quiet', 'Filling up', or 'Full' for a space.

    count    -- how many people are in the space right now
    capacity -- how many people the space can hold
    """
    if capacity <= 0:
        raise ValueError("capacity must be greater than 0")

    fraction = count / capacity

    if fraction < QUIET_LIMIT:
        return "Quiet"
    if fraction <= FULL_LIMIT:
        return "Filling up"
    return "Full"
