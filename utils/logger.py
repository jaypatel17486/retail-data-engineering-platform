import logging
import os
from pathlib import Path

# ============================================
# Create logs directory
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)


# ============================================
# Logger Factory
# ============================================

def get_logger(name: str, logfile: str):

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    )

    file_handler = logging.FileHandler(
        LOG_DIR / logfile
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)

    return logger


# ============================================
# Individual Loggers
# ============================================

warehouse_logger = get_logger(
    "Warehouse",
    "warehouse.log"
)

streaming_logger = get_logger(
    "Streaming",
    "streaming.log"
)

spark_logger = get_logger(
    "Spark",
    "spark.log"
)

airflow_logger = get_logger(
    "Airflow",
    "airflow.log"
)

app_logger = get_logger(
    "Application",
    "application.log"
)