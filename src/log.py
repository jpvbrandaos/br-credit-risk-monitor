import logging


def get_logger(nome):
    logger = logging.getLogger(nome)
    if not logger.handlers:  # evita duplicar handler se importado mais de uma vez
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
