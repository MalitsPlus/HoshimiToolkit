from pathlib import Path

def get_path(file: str) -> Path:
    return Path(file).resolve().parent
