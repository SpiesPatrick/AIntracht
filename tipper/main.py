import logging

from components import tipp_generator, tipp_sender
from services import setup_logging as sl

logger = logging.getLogger(__name__)

def main():
    '''
    Setup logging configuration
    '''
    sl.setup_logging()

    logger.info('-------------------------------')
    logger.info('----- STARTING AI-NTRACHT -----')

    '''
    Check if tipps already safed in DB. If not:
      -> generate prompt and send it to bot
      -> receive tipps and safe them into DB
    '''
    tipp_generator.generate()

    '''
    Check if tipps already safed AND tipped in DB (bool "getippt"). If not:
      -> get tipps from current matchday
      -> navigate through Kicktipp and tipp the shit out of hell
    '''
    tipp_sender.send()

    logger.info('----- THE END -----------------')
    logger.info('-------------------------------')

if __name__ == '__main__':
    main()
