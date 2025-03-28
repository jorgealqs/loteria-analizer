import logging


def get_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger instance.

    Args:
        name: Logger name

    Returns:
        logging.Logger: Configured logger instance
    """
    logging.basicConfig(
        filename="logs/app.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        encoding='utf-8'
    )
    return logging.getLogger(name)
