
import logging

logger = logging.getLogger(__name__)

class Logger:

    def __inti__(self):
        FORMAT = '%(asctime)s | %(user)s | %(levelname)s : %(message)s'
        logging.basicConfig(
            filename='INSERT_FILENAME_HERE',
            format=FORMAT,
            level=logging.INFO
        )

    def info(self, log):
        logger.info(log)

    def error(self, log):
        logger.error(log)

    def debug(self, log):
        logger.debug(log)

    def warning(self, log):
        logger.warning(log)
