
def get(dict, **args):
    """Get a value from a dict, or return a default value."""
    item = None
    tdict = dict
    for key, default in args.items():
        if key in dict:
            tdict = tdict[key]
    return default