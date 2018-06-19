# error formatting for extended-abc


class AbstractClassError(Exception):
    """Custom Exception raised to list errors encountered.

    Raised with list of NotImplementedErrors and TypeErrors
    """
    pass


def formaterror(dct):
    """Format dict: name: [list of errors]

    Raises AbstractClassError
    """
    rv = '\n'

    for name, errors in dct.items():
        if errors:
            rv += '\n{}:\n'.format(name)
            for item in errors:
                rv += ' ' * len(name) + '{e}\n'.format('', e=item)
    raise AbstractClassError(rv)
