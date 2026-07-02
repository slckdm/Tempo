import logging

from toolkit.logging import DATEFMT, FMT, LoggingLevel

logger = logging.getLogger(__name__)


def setup_logging(*, level: LoggingLevel = LoggingLevel.INFO) -> None:
    logging.basicConfig(level=level, datefmt=DATEFMT, format=FMT, force=True)
    logger.info("Logging is set up")
