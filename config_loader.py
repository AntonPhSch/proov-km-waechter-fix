# config_loader.py
# Reads settings.cfg.
# Hand-rolled in 2013; modernized 2025.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict:
    """Parse settings.cfg and return a dict of known key/value pairs.

    Unknown keys are silently ignored (a typo in the file will not surface as an error,
    but all valid keys will be present).
    """
    if path is None:
        path = SETTINGS_FILE
    settings: dict = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict, key: str, fallback: int) -> int:
    """Return an integer value from the settings dict, or fallback if absent/invalid."""
    try:
        return int(settings[key])
    except (KeyError, ValueError):
        return fallback


def get_setting(settings: dict, key: str, fallback: str = "") -> str:
    """Return a string value from the settings dict, or fallback if absent."""
    return settings.get(key, fallback)
