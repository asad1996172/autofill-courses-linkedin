import logging

import colorlog


def setup_logger():
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    colorlog_format = "%(log_color)s" + log_format

    # Set up colorlog
    logger = colorlog.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            colorlog_format,
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            secondary_log_colors={},
            style="%",
        )
    )
    logger.addHandler(handler)

    return logger
