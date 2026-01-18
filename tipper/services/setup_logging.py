import logging

from models import config


def setup_logging():
    conf = config.load_config()
    FILENAME = conf.logging.filename
    FILEPATH = conf.logging.filepath
    LEVEL = level(conf.logging.level)
    FORMAT = conf.logging.format if conf.logging.format else '%(asctime)s | %(levelname)s : %(message)s'
    logging.basicConfig(
        filename=FILEPATH + FILENAME,
        format=FORMAT,
        level=LEVEL
        )

def level(loglevel):
    match loglevel:
        case 'debug': return logging.DEBUG
        case 'info': return logging.INFO
        case 'warn': return logging.WARNING
        case 'error': return logging.ERROR

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info('Check Info')
    logger.error('Check Error')
    logger.debug('Check Debug')
    logger.warning('Check Warning')

if __name__ == '__main__':
    main()
