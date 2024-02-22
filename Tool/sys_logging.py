from includes import *

class CustomFormatter(logging.Formatter):

    green =  "\x1b[32;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s][%(name)s][%(levelname)-5.5s] %(message)s (%(filename)s:%(lineno)d)"
    # format = "[%(asctime)s][%(name)s][%(levelname)-5.5s] %(message)s"
    dateFmt = "%y-%m-%d_%H:%M:%S"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.dateFmt)
        return formatter.format(record)


def setup_custom_logger(logger_name:str, save_dir:str="log", is_save_file:bool=True):
    # Create date folder
    log_folder = os.path.join("log", datetime.now().strftime('%Y-%m-%d'))
    os.makedirs(log_folder, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Create terimal verbose hander
    console_formatter = CustomFormatter()
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file hander - every 12 minute split to 1 file (5 file in 1 hour)
    if is_save_file:
        log_filename = datetime.now().strftime(f'%y%m%d_{logger_name}_log_%H%M%S.log')
        log_file = os.path.join(log_folder, log_filename)
        file_formatter = CustomFormatter()
        # file_formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)-5s] %(message)s', '%Y-%m-%d_%H:%M:%S')
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when='M',
            interval=12,
            backupCount=0,
            encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger

if __name__ == '__main__':

    # Setup custom logger 
    logger = setup_custom_logger()

    # Record different message 
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')