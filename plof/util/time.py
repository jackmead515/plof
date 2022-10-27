

def parse_elapsed_time(elapsed: str) -> int:
    """
    Parse a string representing an elapsed time into a number of seconds.
    Return the number of seconds represented by the string.

    - elapsed: The string to parse.
    """
    elapsed = elapsed.lower()
    if elapsed.endswith("ms"):
        return int(elapsed[:-2]) / 1000
    elif elapsed.endswith('s'):
        return int(elapsed[:-1])
    elif elapsed.endswith('m'):
        return int(elapsed[:-1]) * 60
    elif elapsed.endswith('h'):
        return int(elapsed[:-1]) * 60 * 60
    elif elapsed.endswith('d'):
        return int(elapsed[:-1]) * 60 * 60 * 24
    else:
        return int(elapsed)