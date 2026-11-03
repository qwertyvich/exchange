from copy import deepcopy
from .documents import read_document, write_document


def load_settings(force=False):
    return deepcopy(read_document("settings", {}))


def save_settings(data):
    write_document("settings", data)


def reset_settings_cache():
    # Database reads work across all API workers.
    pass
