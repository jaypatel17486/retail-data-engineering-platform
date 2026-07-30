from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = BASE_DIR / "data" / "raw"

LOG_DIR = BASE_DIR / "logs"

BATCH_SIZE = 1000