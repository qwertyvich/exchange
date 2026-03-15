import json
from pathlib import Path
from typing import Any, Dict

_SETTINGS: Dict[str, Any] | None = None

def load_settings(force: bool = False) -> Dict[str, Any]:
    global _SETTINGS
    if _SETTINGS is not None and not force:
        return _SETTINGS

    path = Path(__file__).resolve().parent / "settings.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    _SETTINGS = data
    return data
    
    
def reset_settings_cache() -> None:
    global _SETTINGS
    _SETTINGS = None