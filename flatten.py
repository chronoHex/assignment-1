def flatten(obj):
    if isinstance(obj, int):
        s.extend(obj)
    else:
        s = []
        for sublist in obj:
            s.extend(flatten(sublist))
        return s
