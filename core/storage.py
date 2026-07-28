import json
import os
import config

DATA_DIR = config.DATA_DIR

def _path(filename):
    return os.path.join(DATA_DIR, filename)

def load_json(filename, default):
    path = _path(filename)

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(path):
        save_json(filename, default)
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        save_json(filename, default)
        return default

def save_json(filename, data):
    path = _path(filename)

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
