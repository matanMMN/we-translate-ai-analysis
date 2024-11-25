from meditranslate.app.loggers import logger

def empty_dependency(dependency : str):
    """An empty dependency that logs a message."""
    def wrapper():
        logger.debug(f"Empty dependency called Instead Of {dependency}.")
        return None
    return wrapper
