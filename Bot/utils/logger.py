import logging 


def setup_logger(logger_name: str, filename: str) -> logging.Logger:
    """Sets up and returns the logger object with the specified parameters"""
    
    formatter = logging.Formatter(fmt='%(asctime)s: %(message)s')
    handler = logging.FileHandler(filename=filename, mode='w+', encoding='UTF-8') 
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO) # info, debug, error ...
    logger.addHandler(handler)

    return logger
