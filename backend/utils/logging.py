import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
)

def logging_info(message, level):
    logging.info(message)
    
def logging_error(message, level):
    logging.error(message)

def logging_critical(message, level):
    logging.critical(message)

def logging_warning(message, level):
    logging.warning(message)
