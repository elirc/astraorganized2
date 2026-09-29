"""Use Windows extended paths while retaining pathlib containment checks."""
from pathlib import Path
import os


def extended_path(path):
    path = Path(path).resolve()
    value = str(path)
    if os.name != 'nt' or value.startswith('\\\\?\\'):
        return path
    if value.startswith('\\\\'):
        return Path('\\\\?\\UNC\\' + value[2:])
    return Path('\\\\?\\' + value)
