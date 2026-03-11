import logging
from pathlib import Path


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure application logging once.
    All child loggers under 'alc' inherit this configuration.
    """

    # get project root (src/alc_breach_tool)
    project_root = Path(__file__).resolve().parents[2]
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "app.log"

    root_logger = logging.getLogger("alc")
    root_logger.setLevel(level)
    root_logger.propagate = False

    if root_logger.handlers:
        return  # prevent duplicate handlers

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)