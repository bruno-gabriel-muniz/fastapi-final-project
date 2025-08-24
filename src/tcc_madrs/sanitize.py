from re import sub


def sanitize(name: str):
    return sub(' {2,}', ' ', name.lower()).strip(' ')
